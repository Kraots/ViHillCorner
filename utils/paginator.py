from typing import Any, Dict, Optional, List, Union
import asyncio

import disnake
from disnake import ApplicationCommandInteraction, MessageInteraction

from . import menus

from utils.context import Context


class RoboPages(disnake.ui.View):
    def __init__(
        self,
        source: menus.PageSource,
        *,
        ctx: Union[Context, ApplicationCommandInteraction],
        check_embeds: bool = True,
        compact: bool = False,
        quit_delete: bool = False,
    ):
        super().__init__()
        self.source: menus.PageSource = source
        self.check_embeds: bool = check_embeds
        self.ctx: Union[Context, ApplicationCommandInteraction] = ctx
        self.message: Optional[disnake.Message] = None
        self.current_page: int = 0
        self.compact: bool = compact
        self.quit_delete: bool = quit_delete
        self.input_lock = asyncio.Lock()
        self.clear_items()
        self.fill_items()

    def fill_items(self) -> None:
        if not self.compact:
            self.numbered_page.row = 1
            self.stop_pages.row = 1

        if self.source.is_paginating():
            max_pages = self.source.get_max_pages()
            use_last_and_first = max_pages is not None and max_pages >= 2
            if use_last_and_first:
                self.add_item(self.go_to_first_page)
            self.add_item(self.go_to_previous_page)
            if not self.compact:
                self.add_item(self.go_to_current_page)
            self.add_item(self.go_to_next_page)
            if use_last_and_first:
                self.add_item(self.go_to_last_page)
            if not self.compact:
                self.add_item(self.numbered_page)
            self.add_item(self.stop_pages)

    async def _get_kwargs_from_page(self, page: int) -> Dict[str, Any]:
        value = await disnake.utils.maybe_coroutine(self.source.format_page, self, page)
        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            return {'content': value, 'embed': None}
        elif isinstance(value, disnake.Embed):
            return {'embed': value, 'content': None}
        else:
            return {}

    async def show_page(self, interaction: MessageInteraction, page_number: int) -> None:
        page = await self.source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(page_number)
        if kwargs:
            if interaction.response.is_done():
                if self.message:
                    await self.message.edit(**kwargs, view=self)
            else:
                await interaction.response.edit_message(**kwargs, view=self)

    def _update_labels(self, page_number: int) -> None:
        self.go_to_first_page.disabled = page_number == 0
        if self.compact:
            max_pages = self.source.get_max_pages()
            self.go_to_last_page.disabled = max_pages is None or (page_number + 1) >= max_pages
            self.go_to_next_page.disabled = max_pages is not None and (page_number + 1) >= max_pages
            self.go_to_previous_page.disabled = page_number == 0
            return

        self.go_to_current_page.label = str(page_number + 1)
        self.go_to_previous_page.label = str(page_number)
        self.go_to_next_page.label = str(page_number + 2)
        self.go_to_next_page.disabled = False
        self.go_to_previous_page.disabled = False
        self.go_to_first_page.disabled = False

        max_pages = self.source.get_max_pages()
        if max_pages is not None:
            self.go_to_last_page.disabled = (page_number + 1) >= max_pages
            if (page_number + 1) >= max_pages:
                self.go_to_next_page.disabled = True
                self.go_to_next_page.label = '???'
            if page_number == 0:
                self.go_to_previous_page.disabled = True
                self.go_to_previous_page.label = '???'

    async def show_checked_page(self, interaction: MessageInteraction, page_number: int) -> None:
        max_pages = self.source.get_max_pages()
        try:
            if max_pages is None:
                # If it doesn't give maximum pages, it cannot be checked
                await self.show_page(interaction, page_number)
            elif max_pages > page_number >= 0:
                await self.show_page(interaction, page_number)
        except IndexError:
            # An error happened that can be handled, so ignore it.
            pass

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        if interaction.user and interaction.user.id in (self.ctx.bot._owner_id, self.ctx.author.id):
            return True
        await interaction.response.send_message('This pagination menu cannot be controlled by you, sorry!', ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        if self.message:
            await self.message.edit(view=None)
        else:
            if self.ctx.response.is_done():
                await self.ctx.edit_original_message(view=None)
            else:
                await self.ctx.response.edit_message(view=None)

    async def on_error(self, error: Exception, item: disnake.ui.Item, interaction: MessageInteraction) -> None:
        if interaction.response.is_done():
            await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
        else:
            await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

    async def start(self) -> None:
        if self.check_embeds and not self.ctx.channel.permissions_for(self.ctx.me).embed_links:
            await self.ctx.send('Bot does not have embed links permission in this channel.')
            return

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        self._update_labels(0)
        if isinstance(self.ctx, ApplicationCommandInteraction):
            self.message = await self.ctx.response.send_message(**kwargs, view=self)
        else:
            self.message = await self.ctx.send(**kwargs, view=self)

    @disnake.ui.button(label='???', style=disnake.ButtonStyle.grey)
    async def go_to_first_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """go to the first page"""
        await self.show_page(interaction, 0)

    @disnake.ui.button(label='Back', style=disnake.ButtonStyle.blurple)
    async def go_to_previous_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """go to the previous page"""
        await self.show_checked_page(interaction, self.current_page - 1)

    @disnake.ui.button(label='Current', style=disnake.ButtonStyle.grey, disabled=True)
    async def go_to_current_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        pass

    @disnake.ui.button(label='Next', style=disnake.ButtonStyle.blurple)
    async def go_to_next_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """go to the next page"""
        await self.show_checked_page(interaction, self.current_page + 1)

    @disnake.ui.button(label='???', style=disnake.ButtonStyle.grey)
    async def go_to_last_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """go to the last page"""
        # The call here is safe because it's guarded by skip_if
        await self.show_page(interaction, self.source.get_max_pages() - 1)

    @disnake.ui.button(label='Skip to page...', style=disnake.ButtonStyle.grey)
    async def numbered_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """lets you type a page number to go to"""
        if self.input_lock.locked():
            await interaction.response.send_message('Already waiting for your response...', ephemeral=True)
            return

        if self.message is None:
            return

        async with self.input_lock:
            channel = self.message.channel
            author_id = interaction.user and interaction.user.id
            await interaction.response.send_message('What page do you want to go to?', ephemeral=True)

            def message_check(m):
                return m.author.id == author_id and channel == m.channel and m.content.isdigit()

            try:
                msg = await self.ctx.bot.wait_for('message', check=message_check, timeout=30.0)
            except asyncio.TimeoutError:
                await interaction.followup.send('Took too long.', ephemeral=True)
                await asyncio.sleep(5)
            else:
                page = int(msg.content)
                await msg.delete()
                await self.show_checked_page(interaction, page - 1)

    @disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red)
    async def stop_pages(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """stops the pagination session."""
        await interaction.response.defer()
        await interaction.delete_original_message()
        if not isinstance(self.ctx, ApplicationCommandInteraction):
            if self.quit_delete:
                await self.ctx.message.delete()
        self.stop()


class FieldPageSource(menus.ListPageSource):
    """A page source that requires (field_name, field_value) tuple items."""

    def __init__(self, entries, *, per_page=12):
        super().__init__(entries, per_page=per_page)
        self.embed = disnake.Embed(colour=disnake.Colour.blurple())

    async def format_page(self, menu, entries):
        self.embed.clear_fields()

        for key, value in entries:
            self.embed.add_field(name=key, value=value, inline=False)

        maximum = self.get_max_pages()
        if maximum > 1:
            text = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
            self.embed.set_footer(text=text)

        return self.embed


class TextPageSource(menus.ListPageSource):
    def __init__(self, entries):
        super().__init__(entries, per_page=1)
        self.initial_page = True

    async def format_page(self, menu, entries):
        maximum = self.get_max_pages()
        if maximum > 1:
            title = f'Page {menu.current_page + 1}/{maximum}'
            menu.embed.title = title

        menu.embed.description = f'```py\n{entries}\n```'
        return menu.embed


class TextPage(RoboPages):
    def __init__(self, ctx, entries, *, footer: str = None, quit_delete: bool = False):
        super().__init__(TextPageSource(entries), ctx=ctx, compact=True, quit_delete=quit_delete)
        self.embed = disnake.Embed()
        if footer is not None:
            self.embed.set_footer(text=footer)


class SimplePageSource(menus.ListPageSource):
    def __init__(self, entries, *, per_page=12):
        super().__init__(entries, per_page=per_page)
        self.initial_page = True

    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'{index + 1}. {entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
            menu.embed.set_footer(text=footer)

        menu.embed.description = '\n'.join(pages)
        return menu.embed


class SimplePages(RoboPages):
    """A simple pagination session reminiscent of the old Pages interface.

    Basically an embed with some normal formatting.
    """

    def __init__(self, ctx, entries, *, per_page=12, color=None, compact=False):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx, compact=compact)
        if color is None:
            color = disnake.Color.blurple()
        self.embed = disnake.Embed(colour=color)


class NewToDoMenus(menus.ListPageSource):
    def __init__(self, entries, *, per_page=12, todo_footer):
        super().__init__(entries, per_page=per_page)
        self.todo_footer = todo_footer

    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'{entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            if self.todo_footer:
                footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} todos)'
            else:
                footer = f'Page {menu.current_page + 1}/{maximum}'
            menu.embed.set_footer(text=footer)

        menu.embed.description = "\n".join(pages)
        return menu.embed


class NewCustomMenus(menus.ListPageSource):
    def __init__(self, entries, *, per_page=12):
        super().__init__(entries, per_page=per_page)

    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'`{index + 1}.` {entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
            menu.embed.set_footer(text=footer)

        menu.embed.description = "\n".join(pages)
        return menu.embed


class CustomMenu(RoboPages):
    def __init__(self, ctx, entries, *, per_page=12, title="", color=None, compact=False):
        super().__init__(NewCustomMenus(entries, per_page=per_page), ctx=ctx, compact=compact)
        if color is None:
            color = disnake.Color.blurple()
        self.embed = disnake.Embed(colour=color, title=title)


class ToDoMenu(RoboPages):
    def __init__(
        self,
        ctx,
        entries: List[str],
        *,
        per_page: int = 12,
        title: str = "",
        color=None,
        author_name: str = None,
        author_icon_url: str = None,
        todo_footer: bool = True,
        compact: bool = True
    ):
        super().__init__(
            NewToDoMenus(
                entries,
                per_page=per_page,
                todo_footer=todo_footer),
            ctx=ctx,
            compact=compact
        )
        if color is None:
            color = disnake.Color.blurple()
        self.embed = disnake.Embed(colour=color, title=title)
        if author_name is not None:
            self.embed.set_author(name=author_name, icon_url=author_icon_url)


class EmbedPaginator(disnake.ui.View):
    def __init__(
        self,
        ctx,
        embeds: List[disnake.Embed],
        *,
        timeout: float = 180.0
    ):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.embeds = embeds
        self.current_page = 0

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        if interaction.user and interaction.user.id in (self.ctx.bot._owner_id, self.ctx.author.id):
            return True
        await interaction.response.send_message('This pagination menu cannot be controlled by you, sorry!', ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        if self.message:
            await self.message.edit(view=None)

    async def show_page(self, inter: MessageInteraction, page_number: int):
        if (
            (page_number < 0) or
            (page_number > len(self.embeds) - 1)
        ):
            if not inter.response.is_done():
                await inter.response.defer()
            return
        self.current_page = page_number
        embed = self.embeds[page_number]
        embed.set_footer(text=f'Page {self.current_page + 1}/{len(self.embeds)}')
        if inter.response.is_done():
            await self.message.edit(embed=embed)
        else:
            await inter.response.edit_message(embed=embed)

    @disnake.ui.button(label='???', style=disnake.ButtonStyle.grey)
    async def go_to_first_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """Go to the first page."""

        await self.show_page(interaction, 0)

    @disnake.ui.button(label='Back', style=disnake.ButtonStyle.blurple)
    async def go_to_previous_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """Go to the previous page."""

        await self.show_page(interaction, self.current_page - 1)

    @disnake.ui.button(label='Next', style=disnake.ButtonStyle.blurple)
    async def go_to_next_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """Go to the next page."""

        await self.show_page(interaction, self.current_page + 1)

    @disnake.ui.button(label='???', style=disnake.ButtonStyle.grey)
    async def go_to_last_page(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """Go to the last page."""

        await self.show_page(interaction, len(self.embeds) - 1)

    @disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red)
    async def stop_pages(self, button: disnake.ui.Button, interaction: MessageInteraction):
        """Stops the pagination session."""

        await interaction.response.defer()
        await interaction.delete_original_message()
        self.stop()

    async def start(self):
        """Start paginating over the embeds."""
        embed = self.embeds[0]
        embed.set_footer(text=f'Page 1/{len(self.embeds)}')
        if isinstance(self.ctx, ApplicationCommandInteraction):
            if not self.ctx.response.is_done():
                self.message = await self.ctx.response.send_message(embed=embed, view=self)
            else:
                self.message = await self.ctx.followup.send(embed=embed, view=self)
            return
        self.message = await self.ctx.send(embed=embed, view=self)
