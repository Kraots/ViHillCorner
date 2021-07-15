import discord
from discord.ext import commands
import asyncio
from utils.helpers import Pag
from traceback import format_exception

class GlobalErrorHandler(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
	
		if hasattr(ctx.command, 'on_error'):
				return

		cog = ctx.cog
		if cog:
			if cog._get_overridden_method(cog.cog_command_error) is not None:
				return
		
	
		if isinstance(error, commands.NotOwner):
			error = discord.Embed(title="ERROR", description="Command Error: You do not own this bot!")
			
			await ctx.send(embed=error, delete_after=8)
			await asyncio.sleep(7.5)
			await ctx.message.delete()
		
		elif isinstance(error, commands.errors.CommandNotFound):
			return
		
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("You are missing an argument!")
			return

		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send("Member does not exist!")
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.errors.CheckFailure):
			return

		else:
			get_error = "".join(format_exception(error, error, error.__traceback__))
			pager = Pag(
			timeout=100,
			entries=[get_error[i: i + 2000] for i in range(0, len(get_error), 2000)],
			length=1,
			title="___ERROR___",
			prefix="```py\n",
			suffix="```"
			)
			await pager.start(ctx)
			
			

						# print(type(error))

def setup (bot):
	bot.add_cog(GlobalErrorHandler(bot))