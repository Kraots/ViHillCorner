import discord
from discord.ext import commands
import os
import asyncio
from utils import context
import datetime
import aiohttp

token = os.environ.get('DISCORD_BOT_SECRET')

class ViHillCorner(commands.Bot):
	def __init__(self):
		allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
		intents = discord.Intents.all()
		super().__init__(command_prefix=('!', ';'), allowed_mentions=allowed_mentions, intents=intents)
		self.session = aiohttp.ClientSession(loop=self.loop)

		self.remove_command('help')

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.load_extension(f'cogs.{filename[:-3]}')

		for filename in os.listdir('./outsidereloadcogs'):
			if filename.endswith('.py'):
				self.load_extension(f'outsidereloadcogs.{filename[:-3]}')

		self.load_extension('jishaku')
		
	async def on_ready(self):
		if not hasattr(self, 'uptime'):
			self.uptime = datetime.datetime.utcnow()

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=context.Context)
		await self.invoke(ctx)

ViHillCorner().run(token)