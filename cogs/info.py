import discord
from discord.ext import commands
import utils.colors as color
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
	async def sfw(self, ctx, members : Greedy[Member] = None):
		sfw = discord.Embed(title="NSFW Warning", description="Please keep the chat appropiate and sfw.", color=color.red)
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
	async def level(self, ctx, members : Greedy[Member] = None):
		lvl = discord.Embed(title="How to lvl up", description="You can level up in this server by chatting in any channel. Spamming or `XP farming` would result in level reset. \n\nTo check your rank, send `^rank` in <#750160851822182486>.", color=color.red)
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
	async def rank(self, ctx, members : Greedy[Member] = None):
		rank = discord.Embed(title="How to check your rank", description="Send `^rank` in <#750160851822182486> to check your rank.", color=color.red)
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
	async def spam(self, ctx, members : Greedy[Member] = None):
		em = discord.Embed(color=color.red, title="Spam warning", description="Please do not spam the chat <:heartato:789581738124640256> <:cry_why:789581737873244160>")
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































def setup (client):
	client.add_cog(info(client))