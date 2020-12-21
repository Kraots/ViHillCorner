import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import Greedy

class info(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = ";"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

		
		# SFW

	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def sfw(self, ctx, members : Greedy[Member] = None):
		sfw = discord.Embed(title="NSFW Warning", description="Please keep the chat appropiate and sfw.", color=discord.Color.red())
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=sfw)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=sfw)
		await msg.add_reaction('🗑️')

	@commands.command(aliases=['lvl'])
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def level(self, ctx, members : Greedy[Member] = None):
		lvl = discord.Embed(title="How to lvl up", description="You can level up in this server by chatting in any channel. Spamming or `XP farming` would result in level reset. \n\nTo check your rank, send `^rank` in <#750160851822182486>.", color=discord.Color.red())
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=lvl)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=lvl)
		await msg.add_reaction('🗑️')

	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def rank(self, ctx, members : Greedy[Member] = None):
		rank = discord.Embed(title="How to check your rank", description="Send `^rank` in <#750160851822182486> to check your rank.", color=discord.Color.red())
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=rank)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=rank)
		await msg.add_reaction('🗑️')

	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def spam(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="Spam warning", description="Please do not spam the chat <:heartato:789581738124640256> <:cry_why:789581737873244160>")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em)
		await msg.add_reaction('🗑️')


	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def english(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="Warning", description="This is an English only server! Speaking any other languages will lead to a mute. <:satania_love:789809969049632768>")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em)
		await msg.add_reaction('🗑️')


	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def cam(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="How to Stream or Enable Webcam in VCs:", description="You need to be level 5 in order to stream or enable your webcam in voice channels. <:bloblove:758378159015723049>")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em)
		await msg.add_reaction('🗑️')


	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def vc(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="How to gain acces to VC:", description="To speak in a voice channel on VHC, you must be level 3.  Send `^rank` in <#750160851822182486> to check your rank.")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em)
		await msg.add_reaction('🗑️')

	@commands.command(aliases=['attachments', 'videos', 'links', 'files'])
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def images(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="Why i can't send images?", description="To send images/videos in all channels, you must be level 69, until then please use the images/videos channels.  Send `^rank` in <#750160851822182486> to check your rank.")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = f" ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em)
		await msg.add_reaction('🗑️')


#	@commands.command()
#	async def age(self, ctx, members : Greedy[Member] = None):
#		em = discord.Embed(color=discord.Color.red(), title="Warning:", description="Please do not joke about being under the minimum age for Discord as per its ToS.")
#		mention_list = []
#
#		if members == None:
#			msg = await ctx.send(embed=em)
#
#		else:
#			for member in members:
#				a = member.mention
#		
#				mention_list.append(a)
#				mentions = f" ".join(mention_list)
#			
#			msg = await ctx.send(mentions, embed=em)
#		await msg.add_reaction('🗑️')






























def setup (client):
	client.add_cog(info(client))