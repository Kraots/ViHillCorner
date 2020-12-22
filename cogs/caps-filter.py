import discord
from discord.ext import commands


class CapsFilter(commands.Cog):

	def __init__(self, client):
		self.client = client

#	@commands.Cog.listener()
#	async def on_message(self, message : discord.Message):
#		await message.channel.send(message.content)
#		print (message.content)


def setup(client):
	client.add_cog(CapsFilter(client))