import discord
from discord.ext import commands
import os
import utils.colors as color

class All(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.prefix = '!'
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.is_owner()
	async def load(self, ctx, extension):
			self.bot.load_extension(extension)
			await ctx.reply(f":inbox_tray: `{extension}`")

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.is_owner()
	async def _reload(self, ctx, extension):
			self.bot.unload_extension(extension)
			self.bot.load_extension(extension)
			await ctx.reply(f":repeat: `{extension}`")

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.is_owner()
	async def unload(self, ctx, extension):
			self.bot.unload_extension(extension)
			await ctx.reply(f":outbox_tray: `{extension}`")



	@_reload.command(aliases=["all"])
	@commands.is_owner()
	async def reload_all(self, ctx):
		cogs_list = []
		em = discord.Embed(color=color.inviscolor, title="Reloaded the next cogs:")

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				try:
					self.bot.unload_extension(f'cogs.{filename[:-3]}')
					self.bot.load_extension(f'cogs.{filename[:-3]}')
					a = f":repeat: `cogs.{filename[:-3]}`\n"
					cogs_list.append(a)

					final_Cogs = "".join(cogs_list)
				except:
					b = f"❌ `cogs.{filename[:-3]}`\n"
					cogs_list.append(b)

					final_Cogs = "".join(cogs_list)

		em.description = final_Cogs
		em.set_footer(text="If the cog has an ❌, then it means it failed to load, or was never loaded.")
		await ctx.reply(embed=em)


	@load.command(aliases=["all"])
	@commands.is_owner()
	async def load_all(self, ctx):
		cogs_list = []
		em = discord.Embed(color=color.inviscolor, title="Loaded the next cogs:")

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				try:
					self.bot.load_extension(f'cogs.{filename[:-3]}')
					a = f":inbox_tray: `cogs.{filename[:-3]}`\n"
					cogs_list.append(a)

					final_Cogs = "".join(cogs_list)
				except:
					b = f"❌ `cogs.{filename[:-3]}`\n"
					cogs_list.append(b)

					final_Cogs = "".join(cogs_list)

		em.description = final_Cogs
		em.set_footer(text="If the cog has an ❌, then it means it failed to load, or was already loaded.")
		await ctx.reply(embed=em)

	@unload.command(aliases=["all"])
	@commands.is_owner()
	async def unload_all(self, ctx):
		cogs_list = []
		em = discord.Embed(color=color.inviscolor, title="Unloaded the next cogs:")

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				try:
					self.bot.unload_extension(f'cogs.{filename[:-3]}')
					a = f":outbox_tray: `cogs.{filename[:-3]}`\n"
					cogs_list.append(a)

					final_Cogs = "".join(cogs_list)
				except:
					b = f"❌ `cogs.{filename[:-3]}`\n"
					cogs_list.append(b)

					final_Cogs = "".join(cogs_list)

		em.description = final_Cogs
		em.set_footer(text="If the cog has an ❌, then it means it failed to unload, or was never loaded.")
		await ctx.reply(embed=em)



def setup(bot):
	bot.add_cog(All(bot))