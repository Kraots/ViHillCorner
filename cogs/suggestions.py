import discord
from discord.ext import commands
import utils.colors as color
from utils.helpers import BotChannels
from utils.paginator import SimplePages
import pymongo
from discord.ext.commands import Greedy
from discord import Member
import asyncio

class TagPageEntry:
	def __init__(self, entry):

		self.id = entry['_id']

	def __str__(self):
		return f'<@!{self.id}>\u2800•\u2800(`UserID:` {self.id})'

class TagPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [TagPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)

class Suggest(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db2['Suggestion blocks']
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.check(BotChannels)
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def suggest(self, ctx, *, args):
		"""Make a suggestion in <#858997857968193596>."""

		result = await self.db.find_one({'_id': ctx.author.id})
		if result != None:
			await ctx.send("You are blocked from using this command. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

		await ctx.message.delete()
		em1 = discord.Embed(color=color.lightpink, title="Are you ready to post your suggestion?", description="**`%s`**" %(args))
		em1.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
		msg1 = await ctx.send(embed=em1)
		await msg1.add_reaction('<:agree:797537027469082627>')
		await msg1.add_reaction('<:disagree:797537030980239411>')

		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
		
		try:
			reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)
		
		except asyncio.TimeoutError:
			new_msg = f"{ctx.author.mention} Did not react in time."
			await msg1.edit(content=new_msg, embed=None)
			await msg1.clear_reactions()
			return
		
		else:
			if str(reaction.emoji) == '<:agree:797537027469082627>':
				suggest = discord.Embed(color=color.inviscolor, title="", description=f"{args}", timestamp=ctx.message.created_at)
				suggest.set_author(name=f'{ctx.author.name} suggested:', icon_url=ctx.author.avatar_url)
				suggestions = self.bot.get_channel(750160850593251454)
				msg = await suggestions.send(embed=suggest)
				await msg.add_reaction('<:agree:797537027469082627>')
				await msg.add_reaction('<:disagree:797537030980239411>')
				em = discord.Embed(color=color.inviscolor, title="Suggestion successfully added!", url=msg.jump_url)
				await msg1.edit(embed=em)
				await msg1.clear_reactions()
				return

			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = "Suggestion aborted. %s" % (ctx.author.mention)
				await msg1.edit(content=e, embed=None)
				await msg1.clear_reactions()
				return
	
	@suggest.command(name='block')
	@commands.is_owner()
	async def suggest_block(self, ctx, members: Greedy[Member]):
		"""Block the members from using the suggest command."""

		blocked_list = []
		if len(members) < 1:
			await ctx.send("You have not given any member to block.")
			return
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			blocked_list.append(a)
			post = {'_id': member.id}
			try:
				await self.db.insert_one(post)
			except pymongo.errors.DuplicateKeyError:
				pass
			await member.send("You are not able to use the command `!suggest` anymore, you have been blocked from using it due to abuse or innapropriate use.")
		blocked_users = " | ".join(blocked_list)
		await ctx.send("`%s` have been blocked from using the command **!suggest**." % (blocked_users))

	@suggest.command(name='unblock')
	@commands.is_owner()
	async def suggest_unblock(self, ctx, members: Greedy[Member]):
		"""Unblock the members from using the suggest command."""

		unblocked_list = []
		if len(members) < 1:
			await ctx.send("You have not given any member to block.")
			return
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			unblocked_list.append(a)
			post = {'_id': member.id}
			await self.db.delete_one(post)
			await member.send("You are able to use the command `!suggest` again. Do **not** abuse it and do **not** use it for innapropriate things that will result in your access being taken away again.")
		unblocked_users = " | ".join(unblocked_list)
		await ctx.send("`%s` have been allowed to use the command **!suggest** again." % (unblocked_users))

	@suggest.command(name='blocks')
	@commands.is_owner()
	async def suggest_blocks(self, ctx):
		"""Get a list with all the members who have been blocked from using the command suggest."""

		try:
			entries = await self.db.find().to_list(100000)
			p = TagPages(entries = entries, per_page = 7)
			await p.start(ctx)
		except:
			await ctx.send("There are no members whose access has been restricted.")

	@suggest.error
	async def suggest_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.message.delete()
			msg = f"To use this command go to <#750160851822182486> or <#750160851822182487>.\n{ctx.author.mention}"
			ctx.command.reset_cooldown(ctx)
			await ctx.send(msg, delete_after=6)

		elif isinstance(error, commands.CommandOnCooldown):
				await ctx.message.delete()
				msg = 'Your on cooldown, please try again in **{:.2f}**s.'.format(error.retry_after)
				await ctx.send(msg, delete_after=3)

		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.message.delete()
			msg = "You have to add your suggestion."
			ctx.command.reset_cooldown(ctx)
			await ctx.send(msg, delete_after=3)

		 

def setup(bot):
	bot.add_cog(Suggest(bot))
