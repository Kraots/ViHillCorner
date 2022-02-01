import os
import aiohttp
import datetime
from typing import Optional, Union

import disnake
from disnake.ext import commands
from disnake.ext.commands.slash_core import (
    InvokableSlashCommand,
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
        self.owner_id = 938083216865243206
        self.db1 = database1
        self.db2 = database2
        self.db3 = database3
        self.base = deta.Base
        self.url = 'https://vihillcorner.deta.dev'

        self.added_views = False
        self.add_check(self.check_dms)
        self.confirm_view = ConfirmView
        self.reraise = reraise
        self.slash_reraise = slash_reraise

        self.execs = {}
        self.snipes = {}
        self.poll_views = {}
        self.tags = []
        self.tag_aliases = []

        self.ignored_channels = (
            750160851822182486,
            750160851822182487,
            752164200222163016,
            855126816271106061,
            787359417674498088
        )

        self.dagpi_client = dagpi.Client(os.getenv('DAGPI_TOKEN'))

        self.load_extension('docs')
        self.load_extension('jishaku')
        os.environ['JISHAKU_NO_DM_TRACEBACK'] = '1'
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

    def get_slash_command(
        self, name: str
    ) -> Optional[Union[InvokableSlashCommand, SubCommandGroup, SubCommand]]:
        """Works like ``Bot.get_command``, but for slash commands.

        If the name contains spaces, then it will assume that you are looking for a :class:`.SubCommand` or
        a :class:`.SubCommandGroup`.
        e.g: ``'foo bar'`` will get the sub command group, or the sub command ``bar`` of the top-level slash command
        ``foo`` if found, otherwise ``None``.

        Parameters
        -----------
        name: :class:`str`
            The name of the slash command to get.

        Returns
        --------
        Optional[Union[:class:`InvokableSlashCommand`, :class:`SubCommandGroup`, :class:`SubCommand`]]
            The slash command that was requested. If not found, returns ``None``.
        """

        if not isinstance(name, str):
            raise TypeError(f"Expected name to be str, not {name.__class__}")

        chain = name.split()
        slash = self.all_slash_commands.get(chain[0])
        if slash is None:
            return None

        if len(chain) == 1:
            return slash
        elif len(chain) == 2:
            return slash.children.get(chain[1])
        elif len(chain) == 3:
            group = slash.children.get(chain[1])
            if isinstance(group, SubCommandGroup):
                return group.children.get(chain[2])

    async def get_webhook(
        self,
        channel: disnake.TextChannel,
        *,
        name: str = "ViHill Corner",
        avatar: disnake.Asset = None,
    ) -> disnake.Webhook:
        """Returns the general bot hook or creates one."""

        webhooks = await channel.webhooks()
        webhook = disnake.utils.find(lambda w: w.name and w.name.lower() == name.lower(), webhooks)

        if webhook is None:
            webhook = await channel.create_webhook(
                name=name,
                avatar=await avatar.read() if avatar else None,
                reason="Used ``get_webhook`` but webhook didn't exist",
            )

        return webhook

    async def reference_to_message(self, reference: disnake.MessageReference) -> Optional[disnake.Message]:
        if reference._state is None or reference.message_id is None:
            return None

        channel = reference._state.get_channel(reference.channel_id)
        if channel is None:
            return None

        if not isinstance(channel, (disnake.TextChannel, disnake.Thread)):
            return None

        try:
            return await channel.fetch_message(reference.message_id)
        except disnake.NotFound:
            return None


ViHillCorner().run(token)
