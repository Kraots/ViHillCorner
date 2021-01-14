import discord
from discord.ext import commands
import wolframalpha
import utils.colors as color
import os

wolf_key = os.getenv("WOLFRAM_KEY")

wolf = wolframalpha.Client(wolf_key)

class Calculator(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(aliases=['calculator', 'calculate'])
	async def calc(self, ctx, *args):
		async with ctx.typing():
			query = " ".join(args)
			res = wolf.query(query)
			try:
				result = next(res.results).text
			except Exception:
				await ctx.send("Failed.")
				return

			em = discord.Embed(color=color.lightpink, title="Calculator")
			em.add_field(name="Operation:", value=query, inline=False)
			em.add_field(name="Result:", value=result, inline=False)
			em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
			
			await ctx.send(embed=em)
			return






def setup(client):
	client.add_cog(Calculator(client))	