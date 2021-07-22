import discord
from discord.ext import commands
import utils.colors as color
from utils.helpers import NSFW
from discord.ext.commands import Greedy
from discord import Member 
from utils.paginator import SimplePages
import pymongo
import hmtai

class TagPageEntry:
	def __init__(self, entry):

		self.id = entry['_id']

	def __str__(self):
		return f'<@!{self.id}>\u2800•\u2800(`UserID:` {self.id})'

class TagPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [TagPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)

class NSFW(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['NSFW blocks']
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.check(NSFW)
	async def nsfw(self, ctx, nsfwType: str = None):
		"""Get nsfw image 😏"""

		if nsfwType is None:
			em = discord.Embed(title="Here are all the available nsfw categories:", description="**ass** • **bdsm** • **cum** • **manga/doujin** • **femdom** • **hentai** • **masturbation** • **ero** • **orgy** • **yuri** • **pantsu/panties** • **glasses** • **cuckold** • **blowjob/bj** • **foot** • **thighs** • **vagina** • **ahegao** • **uniform** • **tentacles**", color=color.lightpink)
			await ctx.send(embed=em)
			return

		nsfwType = nsfwType.lower()
		if nsfwType == 'tentacle':
			nsfwType = 'tentacles'
		elif nsfwType in ['doujin', 'doujins']:
			nsfwType = 'manga'
		elif nsfwType in ['vagina', 'vag']:
			nsfwType = 'pussy'
		elif nsfwType == 'pantsu':
			nsfwType = 'panties'
		elif nsfwType == 'bj':
			nsfwType = 'blowjob'
		elif nsfwType == 'feet':
			nsfwType = 'foot'
		
		elif nsfwType == 'gangbang':
			await ctx.send("This category is not supported.")
			return
		result = hmtai.useHM(version='v2', category=nsfwType)
		
		em = discord.Embed(timestamp=ctx.message.created_at, color=color.pastel)
		em.set_image(url=result)
		em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)


	@nsfw.command()
	async def me(self, ctx, choice : str):
		"""
		The choice must be either `add` or `remove`.
		If you're blocked you won't be able to use any.
		"""

		user = ctx.author
		guild = self.bot.get_guild(750160850077089853)
		nsfwchannel = guild.get_channel(780374324598145055)

		result = await self.db.find_one({'_id': user.id})

		if choice == "remove":
			try:
				await nsfwchannel.set_permissions(user, overwrite = None)
				await user.send("You cannot see the nsfw channel anymore. <:weird:773538796087803934>")
				await ctx.message.delete()
			except:
				return

		elif choice == "add":
			if result != None:
				await ctx.send("You are restricted from using that command, therefore your permissions have not been changed! {}".format(user.mention))
				return

			else:
				await nsfwchannel.set_permissions(user, read_messages = True, reason = "The user requested by himself the permission using `!nsfw me`")
				await user.send('You can now see the nsfw channel! <#780374324598145055> <:peepo_yay:773535977624698890>')
				await ctx.message.delete()


	@nsfw.group(name='block')
	@commands.has_role(754676705741766757)
	async def nsfw_block(self, ctx, members : Greedy[Member]):
		"""Blocks the members from accessing the nsfw channel."""

		guild = self.bot.get_guild(750160850077089853)
		nsfwchannel = guild.get_channel(780374324598145055)

		blocked_list = []
		for member in members:
			try:
				await nsfwchannel.set_permissions(member, overwrite = None)
			except:
				pass
			
			a = f"{member.name}#{member.discriminator}"
			blocked_list.append(a)
			blocked_members = " | ".join(blocked_list)

			post = {'_id': member.id}
			try:
				await self.db.insert_one(post)
			except pymongo.errors.DuplicateKeyError:
				pass

		await ctx.send(f"`{blocked_members}` have been blocked from seeing the nsfw channel.")

	@nsfw.command(name='blocks')
	@commands.has_role(754676705741766757)
	async def nsfw_blocks(self, ctx):
		"""Sends a list with the blocked users for the nsfw channel."""

		try:
			entries = await self.db.find().to_list(100000)
			p = TagPages(entries = entries, per_page = 7)
			await p.start(ctx)
		except:
			await ctx.send("There are no members whose acces has been restricted.")

	@nsfw.command(name='unblock')
	@commands.has_role(754676705741766757)
	async def nsfw_unblock(self, ctx, members : Greedy[Member]):
		"""Unblock the members from accessing the nsfw channel."""

		blocked_list = []
		for member in members:
			
			a = f"{member.name}#{member.discriminator}"
			blocked_list.append(a)
			blocked_members = " | ".join(blocked_list)

			await self.db.delete_one({'_id': member.id})
			await member.send("Your acces for using the `!nsfw me` command has ben re-approved.")
			

		await ctx.send(f"`{blocked_members}` have been unblocked from seeing the nsfw channel.")



	@nsfw.error
	async def nsfw_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			if 754676705741766757 in [role.id for role in ctx.message.author.roles]:
				await ctx.send('Invalid format!\nUse: `!nsfw block <users>` or `!nsfw unblock <users>`!')
			else:

				msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
				await ctx.send(msg)
		else:
			raise error

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
			
		await self.db.delete_one({'_id': member.id})

def setup(bot):
	bot.add_cog(NSFW(bot))