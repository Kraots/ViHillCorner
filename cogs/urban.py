import discord
from discord.ext import commands
import aiohttp
import utils.colors as color

class UrbanDictionary(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command()
	async def define(self, ctx, term: str):
		async with ctx.typing():
			async with aiohttp.ClientSession() as session:
				async with session.get(f"https://api.dictionaryapi.dev/api/v1/entries/en/{term}") as r:
					result = await r.json()
			try:
				data = result[0]['meaning']
				key = list(data.keys())[0]
			except KeyError:
				em = discord.Embed(color=color.red, title="Error", description="```Unable to find that word```", timestamp = ctx.message.created_at)
				em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=em)
				return

			embed = discord.Embed(color=color.lightpink, timestamp = ctx.message.created_at)
			embed.title = f"Definition of {term}"
			embed.add_field(name="Definition", value=data[key][0]['definition'], inline=False)
			try:
				embed.add_field(name="Example", value=data[key][0]['example'], inline=False)
			except KeyError:
				pass
			try:
				synonyms = " | ".join(data[key][0]['synonyms'])
				embed.add_field(name="Synonyms", value=synonyms, inline=False)
			except KeyError:
				pass
			embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)






def setup(client):
	client.add_cog(UrbanDictionary(client))