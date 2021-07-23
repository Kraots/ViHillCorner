import discord
from discord.ext import commands
import asyncio
from traceback import format_exception
import utils.colors as color

class GlobalErrorHandler(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if ctx.command.has_error_handler():
			return
	
		if isinstance(error, commands.NotOwner):
			error = discord.Embed(title="ERROR", description="Command Error: You do not own this bot!")
			
			await ctx.send(embed=error, delete_after=8)
			await asyncio.sleep(7.5)
			await ctx.message.delete()
		
		elif isinstance(error, commands.errors.CommandNotFound):
			return
		
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			return await ctx.send(f"You are missing an argument! See `!help {ctx.command}` if you do not know how to use this.")

		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send("Could not find member.")
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.errors.UserNotFound):
			await ctx.send("Could not find user.")
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.errors.CheckFailure):
			return

		else:
			kraots = self.bot.get_user(self.bot.owner_id)
			get_error = "".join(format_exception(error, error, error.__traceback__))
			em = discord.Embed(description=f'```py\n{get_error}\n```')
			if ctx.guild.id == 750160850077089853:
				await kraots.send(content=f"**An error occured with the command `{ctx.command}`, here is the error:**", embed=em)
				em = discord.Embed(title='Oops... An error has occured.', description='An error has occured while invoking this command and has been sent to my master to fix it.', color=color.red)
				await ctx.send(embed=em)
			else:
				await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(GlobalErrorHandler(bot))