import discord
from discord.ext import commands
import aiohttp
import utils.colors as color

class Cat(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command()
	async def cat(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("http://aws.random.cat/meow") as r:
				data = await r.json()

			imgUrl = data['file']

			embed = discord.Embed(title="Cat", url=imgUrl, color=color.orange, timestamp=ctx.message.created_at)
			embed.set_image(url=imgUrl)
			embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
			msg = await ctx.send(embed=embed)
			await msg.add_reaction("❤️")
			await msg.add_reaction("😸")


def setup(bot):
	bot.add_cog(Cat(bot))