import discord
from discord.ext import commands
import asyncio
import utils.colors as color

class GlobalErrorHandler(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
	
		if hasattr(ctx.command, 'on_error'):
				return

		cog = ctx.cog
		if cog:
			if cog._get_overridden_method(cog.cog_command_error) is not None:
				return
		
	
		if isinstance(error, commands.NotOwner):
			error = discord.Embed(title="ERROR", description="Command Error: You do not own this bot!", color=color.pink)
			
			await ctx.channel.send(embed=error, delete_after=5)
			await asyncio.sleep(4.5)
			await ctx.message.delete()

		elif isinstance(error, commands.errors.CommandInvokeError):
			error = discord.Embed(title="___ERROR___", description=f'**OUTPUT:**\n\n```{str(error)}```', color=color.pink)
			await ctx.channel.send(embed=error, delete_after=50)
			await asyncio.sleep(49.5)
			await ctx.message.delete()

		elif isinstance(error, UnboundLocalError):
			pass
			

						# print(type(error))

def setup (client):
	client.add_cog(GlobalErrorHandler(client))