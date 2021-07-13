from trivia import trivia
import asyncio
import utils.colors as color
from discord.ext import commands
import motor.motor_asyncio
import os
import discord
import random
import games
bot_channels = [752164200222163016, 750160851822182486, 750160851822182487]



DBKEY = os.getenv('MONGODBLVLKEY')

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']['Trivia']

class TriviaCommands(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix and ctx.channel.id in bot_channels


	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra=False, aliases=['trivia'])
	async def _trivia(self, ctx):
		trivia = games.Trivia(ctx)
		await trivia.start()

	@_trivia.group(invoke_without_command=True, case_insensitive=True)
	async def points(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		user = await db.find_one({'_id': member.id})
		if user is None:
			if member == ctx.author:
				await ctx.send("You never played trivia before! %s" % (ctx.author.mention))
				return
			await ctx.send("That user never played trivia before! %s" % (ctx.author.mention))
			return
		
		rank = 0
		rankings = db.find().sort('points', -1)
		for data in await rankings.to_list(99999999999):
			rank += 1
			if user['_id'] == data['_id']:
				break
		
		if member == ctx.author:
			title = "Here are your points:"
		else:
			title = "Here are %s's points:" % (member.display_name)

		em = discord.Embed(color=color.lightpink, title=title)
		em.set_thumbnail(url=member.avatar_url)
		em.add_field(name="Points:", value="**%s**" % (user['points']), inline=False)
		em.add_field(name="Rank:", value="`#%s`" % (rank), inline=False)
		await ctx.send(embed=em)
	
	@_trivia.command(aliases=['lb', 'leaderboard', 'top'])
	async def __lb(self, ctx):
		rank = 0
		em = discord.Embed(color=color.lightpink, title="Here's top `5` trivia users with most points:")
		
		rankings = db.find().sort('points', -1)
		for data in await rankings.to_list(5):
			rank += 1
			user = ctx.guild.get_member(data['_id'])
			em.add_field(name="`#%s` %s" % (rank, user.display_name), value="**%s** points" % (data['points']), inline=False)
		
		await ctx.send(embed=em)
	
	@points.command(aliases=['set'])
	@commands.is_owner()
	async def __set(self, ctx, amount: int, user: discord.Member = None):
		if user is None: 
			user = ctx.author
		
		userDb = await db.find_one({'_id': user.id})
		if userDb is None:
			await ctx.send("The user has never played trivia before. His points cannot be changed since he is not registered in the database.")
			return

		await db.update_one({'_id': user.id}, {'$set':{'points': amount}})
		await ctx.send("Succesfully set the points for user `%s` to **%s**." % (user.display_name, amount))

	@points.command(aliases=['add'])
	@commands.is_owner()
	async def __add(self, ctx, amount: int, user: discord.Member = None):
		if user is None: 
			user = ctx.author
		
		userDb = await db.find_one({'_id': user.id})
		if userDb is None:
			await ctx.send("The user has never played trivia before. His points cannot be changed since he is not registered in the database.")
			return

		await db.update_one({'_id': user.id}, {'$inc':{'points': amount}})
		await ctx.send("Succesfully added **%s** points for user `%s`." % (amount, user.display_name))

	@points.command(aliases=['reset'])
	@commands.is_owner()
	async def __reset(self, ctx, user: discord.Member = None):
		if user is None: 
			user = ctx.author
		
		userDb = await db.find_one({'_id': user.id})
		if userDb is None:
			await ctx.send("The user has never played trivia before. His points cannot be changed since he is not registered in the database.")
			return

		await db.update_one({'_id': user.id}, {'$set':{'points': 0}})
		await ctx.send("Succesfully reset points for user `%s`." % (user.display_name))
	
	@points.command(aliases=['give'])
	async def gift(self, ctx, amount: str, member: discord.Member = None):
		if member is None:
			await ctx.send("You must specify the member you wish to give points to %s." % (ctx.author.mention))
			return
		elif member == ctx.author:
			await ctx.send("You cannot gift yourself... It doesn't really make any sense does it? %s" % (ctx.author.mention))
			return
		
		user = await db.find_one({'_id': ctx.author.id})
		memberDb = await db.find_one({'_id': member.id})
		if user is None:
			await ctx.send("You have never played trivia before. You cannot use this command. %s" % (ctx.author.mention))
			return
		try:
			amount = int(amount)
		except ValueError:
			if amount == 'all':
				amount = user['points']
			else:
				await ctx.send("The amount must be a number. %s" % (ctx.author.mention))
				return
		if user['points'] < amount:
			await ctx.send("You don't have that many points. %s" % (ctx.author.mention))
			return
		elif amount < 5:
			await ctx.send("You cannot give less than **5** points. %s" % (ctx.author.mention))
			return
		elif str(amount)[-1] not in ['5', '0']:
			await ctx.send("The number must always end in **5** or **0**. %s" % (ctx.author.mention))
			return
		elif memberDb is None:
			await ctx.send("That user has never played trivia before. You give points to them. %s" % (ctx.author.mention))
			return
		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == member.id
		msg = await ctx.send("%s wants to give you **%s** points. Do you accept? %s" % (ctx.author.mention, amount, member.mention))
		await msg.add_reaction('<:agree:797537027469082627>')
		await msg.add_reaction('<:disagree:797537030980239411>')

		try:
				reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)

		except asyncio.TimeoutError:
			new_msg = f"{ctx.author.mention} Did not react in time."
			await msg.edit(content=new_msg)
			await msg.clear_reactions()
			return
		
		else:
			if str(reaction.emoji) == '<:agree:797537027469082627>':		
				await db.update_one({'_id': ctx.author.id}, {'$inc':{'points': -amount}})
				await db.update_one({'_id': member.id}, {'$inc':{'points': amount}})
				e = "%s has accepted. Succesfully gifted the points %s" % (member.mention, ctx.author.mention)
				await msg.clear_reactions()
				await msg.edit(content=e)
			
			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = "%s has rejected your gift. %s" % (member.mention, ctx.author.mention)
				await msg.edit(content=e)
				await msg.clear_reactions()

	@_trivia.error
	async def trivia_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send(error.original)
		
		elif isinstance(error, commands.TooManyArguments):
			return
	
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await db.delete_one({'_id': member.id})

def setup(client):
	client.add_cog(TriviaCommands(client))