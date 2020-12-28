import discord
from discord.ext import commands
import utils.colors as color
from utils.helpers import BotChannels

class Suggest(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command()
	@commands.check(BotChannels)
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def suggest(self, ctx, *, args):
		await ctx.message.delete()
		suggest = discord.Embed(color=color.inviscolor, title="", description=f"{args}", timestamp=ctx.message.created_at)
		suggest.set_author(name=f'{ctx.author.name} suggested:', icon_url=ctx.author.avatar_url)
		suggestions = self.client.get_channel(750160850593251454)
		msg = await suggestions.send(embed=suggest)
		await msg.add_reaction('✅')
		await msg.add_reaction('❌')
		em = discord.Embed(color=color.inviscolor, description=f"[Suggestion]({msg.jump_url}) successfully added!")
		await ctx.channel.send(embed=em)

	@suggest.error
	async def suggest_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.message.delete()
			msg = f"To use this command go to <#750160851822182486> or <#750160851822182487>.\n{ctx.author.mention}"
			ctx.command.reset_cooldown(ctx)
			await ctx.channel.send(msg, delete_after=6)

		elif isinstance(error, commands.CommandOnCooldown):
				await ctx.message.delete()
				msg = 'Your on cooldown, please try again in **{:.2f}**s.'.format(error.retry_after)
				await ctx.channel.send(msg, delete_after=3)

		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.message.delete()
			msg = "You have to add your suggestion."
			ctx.command.reset_cooldown(ctx)
			await ctx.channel.send(msg, delete_after=3)

		else:
				raise error

def setup (client):
	client.add_cog(Suggest(client))
