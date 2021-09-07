import disnake
from disnake.ext import commands
import os
from utils import context
import datetime
import aiohttp
import motor.motor_asyncio
from utils.HelpCommand import PaginatedHelpCommand
from utils.helpers import reraise

token = os.environ.get('DISCORD_BOT_SECRET')

key1 = os.getenv('MONGODBKEY')
cluster1 = motor.motor_asyncio.AsyncIOMotorClient(key1)
database1 = cluster1['ViHillCornerDB']

key2 = os.getenv('MONGODBLVLKEY')
cluster2 = motor.motor_asyncio.AsyncIOMotorClient(key2)
database2 = cluster2['ViHillCornerDB']

class ViHillCorner(commands.Bot):
	def __init__(self):
		allowed_mentions = disnake.AllowedMentions(roles=False, everyone=False, users=True)
		intents = disnake.Intents.all()
		super().__init__(help_command=PaginatedHelpCommand(), command_prefix=('!', ';'), allowed_mentions=allowed_mentions, intents=intents, case_insensitive=True, test_guilds=None)
		self.session = aiohttp.ClientSession(loop=self.loop)
		self.db1 = database1
		self.db2 = database2
		self.reraise = reraise
		self.snipes = {}

		self.load_extension('jishaku')
		os.environ['JISHAKU_FORCE_PAGINATOR'] = '1'
		os.environ['JISHAKU_EMBEDDED_JSK'] = '1'
		os.environ['JISHAKU_EMBEDDED_JSK_COLOR'] = 'blurple'

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.load_extension(f'cogs.{filename[:-3]}')

		for filename in os.listdir('./reload_cogs'):
			if filename.endswith('.py'):
				self.load_extension(f'reload_cogs.{filename[:-3]}')
		
	async def on_ready(self):
		if not hasattr(self, 'uptime'):
			self.uptime = datetime.datetime.utcnow()
			self._owner = await self.fetch_user(374622847672254466)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=context.Context)
		await self.invoke(ctx)

ViHillCorner().run(token)