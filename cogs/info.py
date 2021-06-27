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
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def sfw(self, ctx, members : Greedy[Member] = None):
		sfw = discord.Embed(title="NSFW Warning", description="Please keep the chat appropiate and sfw.", color=discord.Color.red())
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=sfw, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=sfw, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')

	@commands.command(aliases=['lvlinfo', 'levelinfo', 'lvl-info', 'level-info', 'howtolvl', 'howtolevel'])
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def level_info(self, ctx, members : Greedy[Member] = None):
		lvl = discord.Embed(title="How to lvl up", description="You can level up in this server by chatting in any channel. Spamming or `XP farming` would result in level reset. \n\nTo check your rank, send `!rank` in <#750160851822182486>.", color=discord.Color.red())
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=lvl, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=lvl, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')

	@commands.command(aliases=['rankinfo', 'rank-info', 'rankcheck'])
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def rank_info(self, ctx, members : Greedy[Member] = None):
		rank = discord.Embed(title="How to check your rank", description="Send `!rank` in <#750160851822182486> to check your rank.", color=discord.Color.red())
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=rank, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=rank, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')

	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def spam(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="Spam warning", description="Please do not spam the chat <:heartato:789581738124640256> <:cry_why:789581737873244160>")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')


	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def english(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="Warning", description="This is an English only server! Speaking any other languages will lead to a mute. <:satania_love:789809969049632768>")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')


	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def cam(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="How to Stream or Enable Webcam in VCs:", description="You need to be level 5 in order to stream or enable your webcam in voice channels. <:bloblove:758378159015723049>")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')


	@commands.command()
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def vc(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="How to gain acces to VC:", description="To speak in a voice channel on VHC, you must be level 3.  Send `!rank` in <#750160851822182486> to check your rank.")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em, reference=ctx.replied_reference)
		await msg.add_reaction('🗑️')

	@commands.command(aliases=['attachments', 'videos', 'links', 'files'])
	@commands.has_any_role('Mod', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def images(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=discord.Color.red(), title="Why i can't send images?", description="To send images/videos in all channels, you must be level 40, until then please use the images/videos channels.  Send `!rank` in <#750160851822182486> to check your rank.")
		mention_list = []

		if members == None:
			msg = await ctx.send(embed=em, reference=ctx.replied_reference)

		else:
			for member in members:
				a = member.mention
		
				mention_list.append(a)
				mentions = " ".join(mention_list)
			
			msg = await ctx.send(mentions, embed=em, reference=ctx.replied_reference)
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


	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You must be at least `level 20+` in order to use this command! %s" % (ctx.author.mention))



























def setup (client):
	client.add_cog(info(client))