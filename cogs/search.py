import discord
from discord.ext import commands
import wolframalpha
import utils.colors as color
import os

wolf_key = os.getenv("WOLFRAM_KEY")

wolf = wolframalpha.Client(wolf_key)

class UrbanDictionary(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command()
	async def search(self, ctx, *args):
		async with ctx.typing():
			query = " ".join(args)
			try:
				res = wolf.query(query)
			except:
				await ctx.send("Invalid query, what are you searching for!?!?!??!")
				return

			try:
				result = next(res.results).text
			except Exception:
				await ctx.reply("Failed.")
				return

			em = discord.Embed(color=color.lightpink)
			em.add_field(name="Query:", value=query, inline=False)
			em.add_field(name="Result:", value=result, inline=False)
			em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
			
			await ctx.reply(embed=em)
			return






def setup(client):
	client.add_cog(UrbanDictionary(client))