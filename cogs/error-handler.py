from discord.ext import commands

class GlobalErrorHandler(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if ctx.command.has_error_handler():
			return
	
		await self.bot.reraise(ctx, error)

def setup(bot):
	bot.add_cog(GlobalErrorHandler(bot))