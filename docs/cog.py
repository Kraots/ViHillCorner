from __future__ import annotations

import asyncio
import sys
import string as st
from types import SimpleNamespace
from typing import Dict, NamedTuple, Optional, List, Tuple

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Param

from .converters import Inventory, PackageName
from .lock import SharedEvent
from .messages import send_denial
from cogs.dev import QuitButton
from utils.paginator import ToDoMenu
from utils import fuzzy
from .utils import create_task, Scheduler
from . import PRIORITY_PACKAGES, batch_parser, doc_cache
from .inventory_parser import InventoryDict, fetch_inventory

from main import ViHillCorner

# symbols with a group contained here will get the group prefixed on duplicates
FORCE_PREFIX_GROUPS = (
    "term",
    "label",
    "token",
    "doc",
    "pdbcommand",
    "2to3fixer",
)
NOT_FOUND_DELETE_DELAY = 30.0
# Delay to wait before trying to reach a rescheduled inventory again, in minutes
FETCH_RESCHEDULE_DELAY = SimpleNamespace(first=2, repeated=5)

DOC_SYMBOLS = {}
ALL_PACKAGES = []


async def autocomplete_doc(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    abc = st.ascii_lowercase
    doc_symbols = []
    for symbol in DOC_SYMBOLS:
        if symbol[0] in abc:
            doc_symbols.append(symbol)
    matches = fuzzy.finder(string, doc_symbols, lazy=False)[:25]
    return matches


async def autocomplete_package_name(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    matches = fuzzy.finder(string, ALL_PACKAGES, lazy=False)[:25]
    return matches


class DocItem(NamedTuple):
    """Holds inventory symbol information."""

    package: str  # Name of the package name the symbol is from
    group: str  # Interpshinx "role" of the symbol, for example `label` or `method`
    base_url: str  # Absolute path to to which the relative path resolves, same for all items with the same package
    relative_url_path: str  # Relative path to the page where the symbol is located
    symbol_id: str  # Fragment id used to locate the symbol on the page

    @property
    def url(self) -> str:
        """Return the absolute url to the symbol."""
        return self.base_url + self.relative_url_path


class Docs(commands.Cog):
    """A set of commands for querying & displaying documentation."""

    def __init__(self, bot: ViHillCorner):
        # Contains URLs to documentation home pages.
        # Used to calculate inventory diffs on refreshes and to display all currently stored inventories.
        self.base_urls = {}
        self.bot = bot
        self.prefix = '!'
        self.db = self.bot.db3['Docs']
        self.doc_symbols: Dict[str, DocItem] = {}  # Maps symbol names to objects containing their metadata.
        self.item_fetcher = batch_parser.BatchParser()

        self.inventory_scheduler = Scheduler(self.__class__.__name__)

        self.refresh_event = asyncio.Event()
        self.refresh_event.set()
        self.symbol_get_event = SharedEvent()
        self.init_refresh_task = create_task(
            self.init_refresh_inventory(),
            name="Doc inventory init",
            event_loop=self.bot.loop
        )

    async def cog_check(self, ctx: commands.Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '📚'

    async def init_refresh_inventory(self) -> None:
        """Refresh documentation inventory on cog initialization."""
        await self.refresh_inventories()

    def update_single(self, package_name: str, base_url: str, inventory: InventoryDict) -> None:
        """
        Build the inventory for a single package and adds its items to the cache.
        Where:
            * `package_name` is the package name to use in logs and when qualifying symbols
            * `base_url` is the root documentation URL for the specified package, used to build
                absolute paths that link to specific symbols
            * `package` is the content of a intersphinx inventory.
        """
        self.base_urls[package_name] = base_url
        if package_name not in ALL_PACKAGES:
            ALL_PACKAGES.append(package_name)

        for group, items in inventory.items():
            for symbol_name, relative_doc_url in items:

                # e.g. get 'class' from 'py:class'
                group_name = group.split(":")[1]
                symbol_name = self.ensure_unique_symbol_name(
                    package_name,
                    group_name,
                    symbol_name,
                )

                relative_url_path, _, symbol_id = relative_doc_url.partition("#")
                # Intern fields that have shared content so we're not storing unique strings for every object
                doc_item = DocItem(
                    package_name,
                    sys.intern(group_name),
                    base_url,
                    sys.intern(relative_url_path),
                    symbol_id,
                )
                self.doc_symbols[symbol_name] = doc_item
                DOC_SYMBOLS[symbol_name] = doc_item
                self.item_fetcher.add_item(doc_item)

    async def update_or_reschedule_inventory(
        self,
        api_package_name: str,
        base_url: str,
        inventory_url: str,
    ) -> None:
        """
        Update the cog's inventories, or reschedule this method to execute again if the remote inventory is unreachable.
        The first attempt is rescheduled to execute in `FETCH_RESCHEDULE_DELAY.first` minutes, the subsequent attempts
        in `FETCH_RESCHEDULE_DELAY.repeated` minutes.
        """
        package = await fetch_inventory(inventory_url)

        if not package:
            if api_package_name in self.inventory_scheduler:
                self.inventory_scheduler.cancel(api_package_name)
                delay = FETCH_RESCHEDULE_DELAY.repeated
            else:
                delay = FETCH_RESCHEDULE_DELAY.first
            self.inventory_scheduler.schedule_later(
                delay * 60,
                api_package_name,
                self.update_or_reschedule_inventory(api_package_name, base_url, inventory_url),
            )
        else:
            if not base_url:
                base_url = self.base_url_from_inventory_url(inventory_url)
            self.update_single(api_package_name, base_url, package)

    def ensure_unique_symbol_name(self, package_name: str, group_name: str, symbol_name: str) -> str:
        """
        Ensure `symbol_name` doesn't overwrite an another symbol in `doc_symbols`.
        For conflicts, rename either the current symbol or the existing symbol with which it conflicts.
        Store the new name in `renamed_symbols` and return the name to use for the symbol.
        If the existing symbol was renamed or there was no conflict, the returned name is equivalent to `symbol_name`.
        """
        if (item := self.doc_symbols.get(symbol_name)) is None:
            return symbol_name  # There's no conflict so it's fine to simply use the given symbol name.

        def rename(prefix: str, *, rename_extant: bool = False) -> str:
            new_name = f"{prefix}.{symbol_name}"
            if new_name in self.doc_symbols:
                # If there's still a conflict, qualify the name further.
                if rename_extant:
                    new_name = f"{item.package}.{item.group}.{symbol_name}"
                else:
                    new_name = f"{package_name}.{group_name}.{symbol_name}"

            if rename_extant:
                # Instead of renaming the current symbol, rename the symbol with which it conflicts.
                self.doc_symbols[new_name] = self.doc_symbols[symbol_name]
                DOC_SYMBOLS[new_name] = DOC_SYMBOLS[symbol_name]
                return symbol_name
            else:
                return new_name

        # When there's a conflict, and the package names of the items differ, use the package name as a prefix.
        if package_name != item.package:
            if package_name in PRIORITY_PACKAGES:
                return rename(item.package, rename_extant=True)
            else:
                return rename(package_name)

        # If the symbol's group is a non-priority group from FORCE_PREFIX_GROUPS,
        # add it as a prefix to disambiguate the symbols.
        elif group_name in FORCE_PREFIX_GROUPS:
            if item.group in FORCE_PREFIX_GROUPS:
                needs_moving = FORCE_PREFIX_GROUPS.index(group_name) < FORCE_PREFIX_GROUPS.index(item.group)
            else:
                needs_moving = False
            return rename(item.group if needs_moving else group_name, rename_extant=needs_moving)

        # If the above conditions didn't pass, either the existing symbol has its group in FORCE_PREFIX_GROUPS,
        # or deciding which item to rename would be arbitrary, so we rename the existing symbol.
        else:
            return rename(item.group, rename_extant=True)

    async def refresh_inventories(self) -> None:
        """Refresh internal documentation inventories."""
        self.refresh_event.clear()
        await self.symbol_get_event.wait()
        self.inventory_scheduler.cancel_all()

        self.base_urls.clear()
        self.doc_symbols.clear()
        await self.item_fetcher.clear()

        coros = [
            self.update_or_reschedule_inventory(
                item['package'], item['base_url'], item['inventory_url']
            ) for item in await self.db.find().to_list(100000)
        ]
        asyncio.gather(*coros)

        self.refresh_event.set()

    def get_symbol_item(self, symbol_name: str) -> Tuple[str, Optional[DocItem]]:
        """
        Get the `DocItem` and the symbol name used to fetch it from the `doc_symbols` dict.

        If the doc item is not found directly from the passed in name and the name contains a space,
        the first word of the name will be attempted to be used to get the item.
        """

        doc_item = self.doc_symbols.get(symbol_name)
        if doc_item is None and " " in symbol_name:
            symbol_name = symbol_name.split(" ", maxsplit=1)[0]
            doc_item = self.doc_symbols.get(symbol_name)

        return symbol_name, doc_item

    async def get_symbol_markdown(self, doc_item: DocItem) -> str:
        """
        Get the Markdown from the symbol `doc_item` refers to.
        `item_fetcher` is used to fetch the page and parse the
        HTML from it into Markdown.
        """
        markdown = await doc_cache.get(doc_item)
        if markdown is None:
            try:
                markdown = await self.item_fetcher.get_markdown(doc_item)

            except aiohttp.ClientError:
                return "Unable to parse the requested symbol due to a network error."

            except Exception:
                return "Unable to parse the requested symbol due to an error."

            if markdown is None:
                return "Unable to parse the requested symbol."

        return markdown

    async def create_symbol_embed(self, symbol_name: str) -> Optional[disnake.Embed]:
        """
        Attempt to scrape and fetch the data for the given `symbol_name`, and build an embed from its contents.
        If the symbol is known, an Embed with documentation about it is returned.
        """
        if not self.refresh_event.is_set():
            await self.refresh_event.wait()
        # Ensure a refresh can't run in case of a context switch until the with block is exited
        with self.symbol_get_event:
            data = self.get_symbol_item(symbol_name)
            symbol_name, doc_item = data
            if doc_item is None:
                return None

            embed = disnake.Embed(
                title=disnake.utils.escape_markdown(symbol_name),
                url=f"{doc_item.url}#{doc_item.symbol_id}",
                description=await self.get_symbol_markdown(doc_item)
            )
            return embed

    @commands.slash_command(name="docs")
    async def docs_group(self, inter) -> None:
        """Base slash for all docs subcommands."""
        pass

    @docs_group.sub_command(name='inventories')
    async def doc_inventories(self, inter: ApplicationCommandInteraction):
        """Shows all the documentation available inventories."""

        lines = sorted(f"• [`{name}`]({url})" for name, url in self.base_urls.items())
        if self.base_urls:
            paginator = ToDoMenu(
                inter,
                lines,
                per_page=5,
                todo_footer=False,
                title=f'All inventories (`{len(self.base_urls)}` total)'
            )
            await paginator.start()

        else:
            inventory_embed = disnake.Embed(title=f'All inventories (`{len(self.base_urls)}` total)', color=disnake.Color.blurple())
            inventory_embed.description = "Hmmm, seems like there's nothing here yet."
            await inter.response.send_message(embed=inventory_embed)

    @docs_group.sub_command(name="get")
    async def get_command(
        self,
        inter: ApplicationCommandInteraction,
        symbol_name: str = Param(
            description='The doc to look for',
            autocomplete=autocomplete_doc
        )
    ) -> None:
        """Return a documentation embed for a given symbol."""

        await inter.response.defer()
        symbol = symbol_name.strip("`")
        doc_embed = await self.create_symbol_embed(symbol)

        if doc_embed is None:
            view = QuitButton(inter, timeout=NOT_FOUND_DELETE_DELAY, delete_after=True)
            view.message = await send_denial(inter, "No documentation found for the requested symbol.", view=view)

        else:
            view = QuitButton(inter)
            await inter.followup.send(embed=doc_embed, view=view)

    @staticmethod
    def base_url_from_inventory_url(inventory_url: str) -> str:
        """Get a base url from the url to an objects inventory by removing the last path segment."""
        return inventory_url.removesuffix("/").rsplit("/", maxsplit=1)[0] + "/"

    @docs_group.sub_command(name="set_doc")
    @commands.is_owner()
    async def set_command(
        self,
        inter: ApplicationCommandInteraction,
        package_name: str,
        inventory: str
    ) -> None:
        """Adds a new documentation metadata object to the inventory."""

        await inter.response.defer(ephemeral=True)
        package_name = await PackageName.convert(inter, package_name)
        inventory = await Inventory.convert(inter, inventory)

        inventory_url, inventory_dict = inventory

        base_url = self.base_url_from_inventory_url(inventory_url)

        doc = await self.db.find_one({'package': package_name})
        if doc is not None:
            return await inter.followup.send(f'A doc with the name `{package_name}` already exists in the database.', ephemeral=True)
        body = {
            'package': package_name,
            'base_url': base_url,
            'inventory_url': inventory_url
        }

        await self.db.insert_one(body)
        self.update_single(package_name, base_url, inventory_dict)
        await inter.followup.send(f"Added the package `{package_name}` to the database and updated the inventories.", ephemeral=True)

    @docs_group.sub_command(name="delete_doc")
    @commands.is_owner()
    async def delete_command(
        self,
        inter: ApplicationCommandInteraction,
        package_name: str = Param(
            description='The doc to remove',
            autocomplete=autocomplete_package_name
        )
    ) -> None:
        """
        Removes the specified package from the database.
        """

        await inter.response.defer(ephemeral=True)
        package_name = await PackageName.convert(inter, package_name)

        doc = await self.db.find_one({'package': package_name})
        if doc is None:
            return await inter.followup.send(f'Doc `{package_name}` doesn\'t exist in the database.', ephemeral=True)

        await self.db.delete_one({'package': package_name})
        await doc_cache.delete(package_name)
        ALL_PACKAGES.pop(ALL_PACKAGES.index(package_name))
        await self.refresh_inventories()

        await inter.followup.send(f"Successfully deleted `{package_name}` and refreshed the inventories.", ephemeral=True)

    @docs_group.sub_command(name="refresh_doc")
    @commands.is_owner()
    async def refresh_command(
        self,
        inter: ApplicationCommandInteraction
    ) -> None:
        """Refresh inventories and show the difference."""

        await inter.response.defer(ephemeral=True)
        old_inventories = set(self.base_urls)
        await self.refresh_inventories()
        new_inventories = set(self.base_urls)

        if added := ", ".join(new_inventories - old_inventories):
            added = "+ " + added

        if removed := ", ".join(old_inventories - new_inventories):
            removed = "- " + removed

        embed = disnake.Embed(
            title="Inventories refreshed",
            description=f"```diff\n{added}\n{removed}```" if added or removed else ""
        )
        await inter.followup.send(embed=embed, ephemeral=True)

    @docs_group.sub_command(name="clear_doc_cache")
    @commands.is_owner()
    async def clear_cache_command(
        self,
        inter: ApplicationCommandInteraction,
        package_name: str = Param(
            description='The doc to clear the cache for',
            autocomplete=autocomplete_package_name
        )
    ) -> None:
        """Clear the persistent deta cache for `package`."""

        await inter.response.defer(ephemeral=True)
        package_name = await PackageName.convert(inter, package_name)
        if await doc_cache.delete(package_name):
            await inter.followup.send(f"Successfully cleared the cache for `{package_name}`.", ephemeral=True)
        else:
            await inter.followup.send("No keys matching the package found.", ephemeral=True)

    def cog_unload(self) -> None:
        """Clear scheduled inventories, queued symbols and cleanup task on cog unload."""
        self.inventory_scheduler.cancel_all()
        self.init_refresh_task.cancel()
        create_task(self.item_fetcher.clear(), name="DocCog.item_fetcher unload clear")
