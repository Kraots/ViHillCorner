import discord
from discord.errors import HTTPException
from discord.ext import commands
import utils.colors as color
import async_tio

class Calculator(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
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
		exit_status_ = result.exit_status
		if int(exit_status_) == 1:
			return await ctx.reply("Are you sure you're using this command for a valid operation?")

		try:
			em = discord.Embed()
			em.set_author(name=f"Here's your result `{ctx.author.display_name}`:", icon_url=ctx.author.avatar_url)
			em.add_field(name="Operation:", value=f"`{args}`", inline=False)
			em.add_field(name="Result:", value=f"`{result.stdout}`")
			em.color = color.lightpink
			await ctx.send(embed=em, reference=ctx.replied_reference)
		except HTTPException:
			em = discord.Embed()
			em.set_author(name=f"Here's your result `{ctx.author.display_name}`:", icon_url=ctx.author.avatar_url)
			em.add_field(name="Operation:", value="`Operation too long`", inline=False)
			em.add_field(name="Result:", value=f"`{result.stdout}`")
			em.color = color.lightpink
			await ctx.send(embed=em, reference=ctx.replied_reference)



def setup(bot):
	bot.add_cog(Calculator(bot))	