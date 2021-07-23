import discord
from discord.ext import commands
import utils.colors as color
from utils.helpers import NSFW
from discord.ext.commands import Greedy
from discord import Member 
from utils.paginator import SimplePages
import pymongo
import hmtai

nsfw_url = 'https://nekobot.xyz/api/image?type='
nsfw_categs = ['hentai', 'ass', 'thigh', 'hass', 'hboobs', 'pgif', 'paizuri', 'boobs', 'pussy', 'hyuri', 'hthigh', 'lewdneko', 'anal', 'hmidriff', 'feet', 'gonewild', 'hkitsune', '4k', 'blowjob', 'tentacle', 'hentai_anal']
real_categs = ['ass', 'thigh', 'pgif', 'boobs', 'pussy', 'anal', 'feet', 'gonewild', '4k', 'blowjob']
hentai_categs = ['hentai', 'hass', 'hboobs', 'paizuri', 'hyuri', 'hthigh', 'lewdneko', 'hmidriff', 'hkitsune', 'tentacle', 'hentai_anal']

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
	async def nsfw(self, ctx):
		"""See the types of nsfw 😏"""

		return await ctx.send("There are only 3 types: `real`, `hentai` and `old`\nType `!nsfw <type>` to see all the categories of a type.\n***Keep in mind that these only work in the nsfw channel.***")

	@nsfw.command(name='old')
	@commands.check(NSFW)
	async def nsfw_old(self, ctx, category: str = None):
		"""Get nsfw image 😏"""

		if category is None:
			categs = "ass **•** bdsm **•** cum **•** manga/doujin **•** femdom **•** hentai **•** masturbation **•** ero **•** orgy **•** yuri **•** pantsu/panties **•** glasses **•** cuckold **•** blowjob/bj **•** foot **•** thighs **•** vagina **•** ahegao **•** uniform **•** tentacles"
			em = discord.Embed(title="Here are all the categories for the old nsfw:", description=categs, color=color.blue)
			return await ctx.send(embed=em)

		nsfwType = category.lower()
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
			return	await ctx.send("This category is not supported.")

		result = hmtai.useHM(version='v2', category=nsfwType)
		
		em = discord.Embed(color=color.pastel)
		em.set_image(url=result)
		em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)

	@nsfw.command(name='real')
	@commands.check(NSFW)
	async def nsfw_real(self, ctx, category: str = None):
		"""Get a real porn random image based on the chosen category 😏"""
		
		if category is None:
			categs = "ass **•** thigh **•** gif **•** boobs **•** pussy **•** anal **•** feet **•** wild **•** 4k **•** bj/blowjob"
			em = discord.Embed(color=color.blue, title="Here are all the categories for real porn:", description=categs)
			em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=em)

		categ = category.lower()
		if not categ in real_categs:
			if categ == 'thighs':
				categ = 'thigh'
			elif categ == 'bj':
				categ = 'blowjob'
			elif categ == 'gif':
				categ = 'pgif'
			elif categ == 'wild':
				categ = 'gonewild'
			elif categ == 'boob':
				categ = 'boobs'
			else:
				return await ctx.reply("Not in the existing real nsfw categories.")
		
		async with self.bot.session.get(nsfw_url + categ) as resp:
			if resp.status != 200:
				kraots = self.bot.get_user(self.bot.owner_id)
				await kraots.send(f"`{ctx.command} {categ}` returned **{resp.status}**")
				return await ctx.send("There has been an error from the **API**, please try again later.")
			content = await resp.json()
			url = content['message']
		em = discord.Embed(color=color.pastel)
		em.set_image(url=url)
		em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)

	@nsfw.command(name='hentai')
	@commands.check(NSFW)
	async def nsfw_hentai(self, ctx, category: str = None):
		"""Get a hentai random image based on the chosen category 😏"""

		if category is None:
			categs = f"hentai **•** paizuri **•** yuri **•** thighs **•** neko **•** anal **•** hmidriff **•** kitsune **•** tentacle **•** anal"
			em = discord.Embed(color=color.blue, title="Here are all the categories for hentai:", description=categs)
			em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=em)

		categ = category.lower()
		if not categ in hentai_categs:
			if categ == 'ass':
				categ = 'hass'
			elif categ in ['boob', 'boobs']:
				categ = 'hboobs'
			elif categ == 'yuri':
				categ = 'hyuri'
			elif categ in ['thigh', 'thighs']:
				categ = 'hthigh'
			elif categ == 'neko':
				categ = 'lewdneko'
			elif categ == 'anal':
				categ = 'hentai_anal'
			elif categ == 'kitsune':
				categ = 'hkitsune'
			elif categ == 'tentacles':
				categ = 'tentacle'
			else:
				return await ctx.reply("Not in the existing hentai categories.")

		async with self.bot.session.get(nsfw_url + categ) as resp:
			if resp.status != 200:
				kraots = self.bot.get_user(self.bot.owner_id)
				await kraots.send(f"`{ctx.command} {categ}` returned **{await resp.json()}**")
				return await ctx.send("There has been an error from the **API**, please try again later.")
			content = await resp.json()
			url = content['message']
		em = discord.Embed(color=color.pastel)
		em.set_image(url=url)
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
	
	@nsfw_old.error
	async def nsfw_old_error(self, ctx, error):
		if isinstance(error, commands.errors.CheckFailure):
			await ctx.reply('This command is only usable in a nsfw marked channel.')
	
	@nsfw_real.error
	async def nsfw_real_error(self, ctx, error):
		if isinstance(error, commands.errors.CheckFailure):
			await ctx.reply('This command is only usable in a nsfw marked channel.')
	
	@nsfw_hentai.error
	async def nsfw_hentai_error(self, ctx, error):
		if isinstance(error, commands.errors.CheckFailure):
			await ctx.reply('This command is only usable in a nsfw marked channel.')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
			
		await self.db.delete_one({'_id': member.id})

def setup(bot):
	bot.add_cog(NSFW(bot))