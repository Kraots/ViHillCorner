import discord
from discord.ext import commands
import utils.colors as color
import async_tio

class Calculator(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(aliases=['calculator', 'calculate'])
	async def calc(self, ctx, *, args:str):
		if '^' in args:
			args = args.replace('^', '**')
	
		tio = await async_tio.Tio()
		result = await tio.execute(f"print({args})", language="python3")
		await tio.close()

		em = discord.Embed()
		em.set_author(name=f"Here's your result `{ctx.author.display_name}`:", icon_url=ctx.author.avatar_url)
		em.add_field(name="Operation:", value=args, inline=False)
		em.add_field(name="Result:", value=result.stdout)
		em.color = color.lightpink
		await ctx.send(embed=em)



def setup(client):
	client.add_cog(Calculator(client))	