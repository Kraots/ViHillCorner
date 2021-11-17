import os
import aiohttp
import datetime
from typing import Optional

import disnake
from disnake.ext import commands
from disnake.ext.commands.slash_core import (
    SubCommandGroup,
    SubCommand
)

from utils import context
from utils.ButtonRoles import ButtonRoles
from utils.HelpCommand import PaginatedHelpCommand
from utils.helpers import reraise, slash_reraise, ConfirmView

import motor.motor_asyncio
from deta import Deta

import asyncdagpi as dagpi

token = os.environ.get('DISCORD_BOT_SECRET')

key1 = os.getenv('MONGODBKEY')
cluster1 = motor.motor_asyncio.AsyncIOMotorClient(key1)
database1 = cluster1['ViHillCornerDB']

key2 = os.getenv('MONGODBLVLKEY')
cluster2 = motor.motor_asyncio.AsyncIOMotorClient(key2)
database2 = cluster2['ViHillCornerDB']

key3 = os.getenv('EXTRA_DB_KEY')
cluster3 = motor.motor_asyncio.AsyncIOMotorClient(key3)
database3 = cluster3['ViHillCornerDB']

key4 = os.getenv('MONGODBKEY2')
cluster4 = motor.motor_asyncio.AsyncIOMotorClient(key4)
database4 = cluster4['ViHillCornerDB']

deta_key = os.getenv('DETA_KEY')
deta = Deta(deta_key)


class ViHillCorner(commands.Bot):
    def __init__(self):
        allowed_mentions = disnake.AllowedMentions(roles=False, everyone=False, users=True)
        intents = disnake.Intents.all()
        super().__init__(
            help_command=PaginatedHelpCommand(),
            command_prefix=('!', ';'),
            allowed_mentions=allowed_mentions,
            intents=intents,
            case_insensitive=True,
            test_guilds=[
                750160850077089853,
                787357561116426258
            ]
        )
        self.add_check(self.check_dms)
        self.db1 = database1
        self.db2 = database2
        self.db3 = database3
        self.db4 = database4
        self.base = deta.Base
        self.url = 'https://vihillcorner.deta.dev'
        self.reraise = reraise
        self.slash_reraise = slash_reraise
        self.confirm_view = ConfirmView
        self.snipes = {}
        self.poll_views = {}
        self.tags = []
        self.tag_aliases = []
        self.added_views = False
        self.dagpi_client = dagpi.Client(os.getenv('DAGPI_TOKEN'))

        self.load_extension('docs')
        self.load_extension('jishaku')
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = '1'
        os.environ['JISHAKU_FORCE_PAGINATOR'] = '1'
        os.environ['JISHAKU_EMBEDDED_JSK'] = '1'
        os.environ['JISHAKU_EMBEDDED_JSK_COLOR'] = 'blurple'

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

        for filename in os.listdir('./reload_cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'reload_cogs.{filename[:-3]}')

    @property
    def _owner(self) -> disnake.User:
        if self._owner_id:
            return self.get_user(self._owner_id)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        if not hasattr(self, '_session'):
            self._session = aiohttp.ClientSession(loop=self.loop)

        if not hasattr(self, '_presence_changed'):
            activity = disnake.Activity(type=disnake.ActivityType.watching, name='you | !help')
            await self.change_presence(status=disnake.Status.dnd, activity=activity)
            self._presence_changed = True

        if not hasattr(self, '_owner_id'):
            app = await self.application_info()
            self._owner_id = app.owner.id

        if self.added_views is False:
            self.add_view(view=ButtonRoles(), message_id=886686657842135100)
            self.add_view(view=ButtonRoles(), message_id=886686816634277928)
            self.add_view(view=ButtonRoles(), message_id=886686899371139143)
            self.add_view(view=ButtonRoles(), message_id=886687040400420915)
            self.added_views = True

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)
        await self.invoke(ctx)

    async def check_dms(self, ctx):
        if ctx.author.id == self.owner_id:
            return True
        if isinstance(ctx.channel, disnake.DMChannel):
            await ctx.send('Commands do not work in dm channels. Please use commands in <#750160851822182486>')
            return False
        return True

    def get_slash_sub_command_group(
        self,
        name: str,
        parent: str
    ) -> Optional[SubCommandGroup]:
        """Get a :class:`.SubCommandGroup` from the given parent.

        Parameters
        ----------
            name: :class:`str`
                The name of the sub command group.
            parent: :class:`str`
                The top-level slash command of this group.

        Returns
        -------
            Optional[:class:`SubCommandGroup`]
                The slash sub command group that was requested. If not found, returns ``None``.
        """

        slash = self.get_slash_command(parent)
        if slash:
            group = slash.children.get(name)
            if isinstance(group, SubCommandGroup):
                return group

        return None

    def get_slash_sub_command(
        self,
        name: str,
        parent: str,
        parent_group: str = None
    ) -> Optional[SubCommand]:
        """Get a :class:`.SubCommand` from the given parent.

        Parameters
        ----------
            name: :class:`str`
                The name of the sub command.
            parent: :class:`str`
                The top-level slash command of this sub command.
            parent_group: :class:`str`
                The ``.SubCommandGroup`` this sub command is part of.

        Returns
        -------
            Optional[:class:`SubCommand`]
                The slash sub command that was requested. If not found, returns ``None``.
        """

        slash = self.get_slash_command(parent)
        if slash:
            if parent_group:
                group = slash.children.get(parent_group)
                if isinstance(group, SubCommandGroup):
                    sub_command = group.children.get(name)
                    return sub_command
                return None

            sub_command = slash.children.get(name)
            if isinstance(sub_command, SubCommand):
                return sub_command

        return None


ViHillCorner().run(token)
