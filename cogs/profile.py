import discord
from discord.ext import commands
from typing import Optional
from utils.helpers import profile

class Userinfo(commands.Cog):
	""" Get info for user"""
	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.group(invoke_without_command=True)
	async def profile(self, ctx, *, user: Optional[discord.Member]):
		if ctx.invoked_subcommand is None:
			if not user:
				user = ctx.message.author
			em = profile(ctx,user)
			await ctx.send(embed=em)
			await ctx.message.delete()

def setup(bot):
	bot.add_cog(Userinfo(bot))
