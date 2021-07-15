import discord
from discord.ext import commands
import aiohttp
import utils.colors as color

class Dog(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command()
	async def dog(self, ctx): 
		async with aiohttp.ClientSession() as cs:
			async with cs.get("http://random.dog/woof.json") as r:
				data = await r.json()

			embed = discord.Embed(title="Dog", url=data['url'], color=color.orange, timestamp=ctx.message.created_at)
			embed.set_image(url=data['url'])
			embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
			msg = await ctx.send(embed=embed)
			await msg.add_reaction("❤️")
			await msg.add_reaction("🐶")

def setup(client):
	client.add_cog(Dog(client))