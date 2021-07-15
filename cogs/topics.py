from discord.ext import commands
from utils import topicslist
import random

class Topics(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command()
	async def topic(self, ctx):
		await ctx.message.delete()
		topics = random.choice(topicslist.topicsList)
		await ctx.send(topics)



def setup(bot):
	bot.add_cog(Topics(bot))