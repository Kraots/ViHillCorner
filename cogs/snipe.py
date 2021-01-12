import discord
from discord.ext import commands

snipes = {}

class Snipe(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix



	@commands.Cog.listener()
	async def on_message_delete(self, message: discord.Message):
		if message.author.id == 374622847672254466:
			return
		elif message.author.bot:
			return
		else:
			snipes[message.channel.id] = message

	
	@commands.command()
	async def snipe(self, ctx, *, channel: discord.TextChannel = None):
		channel = channel or ctx.channel
		try:
			msg = snipes[channel.id]
		except KeyError:
			return await ctx.reply('Nothing to snipe!')

		embed = discord.Embed(description= msg.content, color=msg.author.color, timestamp=msg.created_at)
		embed.set_author(name=msg.author, icon_url=msg.author.avatar_url)
		embed.set_footer(text="Deleted in `{}`".format(msg.channel))
		await ctx.reply(embed=embed)


			

def setup (client):
	client.add_cog(Snipe(client))