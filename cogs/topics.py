from discord.ext import commands
from utils import topicslist
import random

class Topics(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command()
	async def topic(self, ctx):
		await ctx.message.delete()
		topics = random.choice(topicslist.topicsList)
		await ctx.send(topics)



def setup (client):
	client.add_cog(Topics(client))