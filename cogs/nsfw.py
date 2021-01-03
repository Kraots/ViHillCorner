import discord
from discord.ext import commands
import aiohttp
import utils.colors as color
from utils.helpers import NSFW
from discord.ext.commands import Greedy
from discord import Member
import json

class NSFW(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.check(NSFW)
	async def nsfw(self, ctx):
		await ctx.send('`!nsfw hentai` | `!nsfw yuri` | `!nsfw tentacle` | `!nsfw real` | `!nsfw yiff`')

	@nsfw.command()
	@commands.check(NSFW)
	async def hentai(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://www.reddit.com/r/hentai/random/.json") as r:
				res = await r.json()
				EntryPoint = res[0]['data']['children'] [0]['data']           
				imgUrl = EntryPoint['url']
				Title = EntryPoint['title']

				embed = discord.Embed(title=Title, url=imgUrl, timestamp=ctx.message.created_at, color=color.pastel)
				embed.set_image(url=imgUrl)
				embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)

	@nsfw.command()
	@commands.check(NSFW)
	async def yuri(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://www.reddit.com/r/yuri/random/.json") as r:
				res = await r.json()
				imgUrl = res[0]['data']['children'] [0]['data']
				linkUrl = imgUrl['url']
				titleUrl = imgUrl['title']

				embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
				embed.set_image(url=linkUrl)
				embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)

	@nsfw.command(aliases=['tentacles'])
	@commands.check(NSFW)
	async def tentacle(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://www.reddit.com/r/Tentai/random/.json") as r:
				res = await r.json()
				imgUrl = res[0]['data']['children'] [0]['data']
				linkUrl = imgUrl['url']
				titleUrl = imgUrl['title']

				embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
				embed.set_image(url=linkUrl)
				embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)

	@nsfw.command()
	@commands.check(NSFW)
	async def real(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://www.reddit.com/r/pornpics/random/.json") as r:
				res = await r.json()
				imgUrl = res[0]['data']['children'] [0]['data']
				linkUrl = imgUrl['url']
				titleUrl = imgUrl['title']

				embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
				embed.set_image(url=linkUrl)
				embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)

	@nsfw.command()
	@commands.check(NSFW)
	async def yiff(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://www.reddit.com/r/yiff/random.json") as r:
				res = await r.json()
				imgUrl = res[0]['data']['children'] [0]['data']
				linkUrl = imgUrl['url']
				titleUrl = imgUrl['title']

				embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
				embed.set_image(url=linkUrl)
				embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)

	@nsfw.command()
	async def me(self, ctx, choice : str):
		user = ctx.author
		guild = self.client.get_guild(750160850077089853)
		nsfwchannel = guild.get_channel(780374324598145055)

		users = await get_nsfw_data()

		if choice == "remove":
			try:
				await nsfwchannel.set_permissions(user, overwrite = None)
				await user.send("You cannot see the nsfw channel anymore. <:weird:773538796087803934>")
				await ctx.message.delete()
			except:
				return

		elif choice == "add":
			if str(user.id) in users:
				await ctx.send("You are blocked from the nsfw channel, therefore your permissions have not been changed! {}".format(user.mention))
				return

			else:
				await nsfwchannel.set_permissions(user, read_messages = True, reason = "The user requested by himself the permission using `!nsfw me`")
				await user.send('You can now see the nsfw channel! <#780374324598145055> <:peepo_yay:773535977624698890>')
				await ctx.message.delete()


	@nsfw.command()
	@commands.has_role("Staff")
	async def block(self, ctx, members : Greedy[Member]):
		users = await get_nsfw_data()
		guild = self.client.get_guild(750160850077089853)
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

			users[str(member.id)] = {}
			users[str(member.id)]["is_blocked"] = "yes"
			with open("nsfw-blocks.json", "w", encoding = 'utf-8') as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
		
		await ctx.send(f"`{blocked_members}` have been blocked from seeing the nsfw channel.")



	@nsfw.command()
	@commands.has_role("Staff")
	async def unblock(self, ctx, members : Greedy[Member]):
		users = await get_nsfw_data()

		blocked_list = []
		for member in members:
			
			a = f"{member.name}#{member.discriminator}"
			blocked_list.append(a)
			blocked_members = " | ".join(blocked_list)

			try:
				del users[str(member.id)]
				with open("nsfw-blocks.json", "w", encoding = 'utf-8') as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
			except KeyError:
				await ctx.send("User(s) are not blocked.")
		
		await ctx.send(f"`{blocked_members}` have been unblocked from seeing the nsfw channel.")




	@nsfw.error
	async def nsfw_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			if "Staff" in [role.name for role in ctx.message.author.roles]:
				await ctx.send('Invalid format!\nUse: `!nsfw block <users>` or `!nsfw unblock <users>`!')
			else:

				msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
				await ctx.channel.send(msg)

	@hentai.error
	async def hentai_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
			await ctx.channel.send(msg)

	@yuri.error
	async def yuri_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
			await ctx.channel.send(msg)

	@tentacle.error
	async def tentacle_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
			await ctx.channel.send(msg)












async def get_nsfw_data():
	with open("nsfw-blocks.json", "r") as f:
		users = json.load(f)
	
	return users





# https://www.reddit.com/r/hentai/random/.json
def setup (client):
	client.add_cog(NSFW(client))