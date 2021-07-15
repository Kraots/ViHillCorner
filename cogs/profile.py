import discord
from discord.ext import commands
from utils.helpers import profile

class Userinfo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command()
	async def profile(self, ctx, user: discord.Member = None):
		if user is None:
			user = ctx.author
		
		em = profile(ctx, user)
		await ctx.send(embed=em)
		await ctx.message.delete()

def setup(bot):
	bot.add_cog(Userinfo(bot))
