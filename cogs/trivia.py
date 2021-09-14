import utils.colors as color
from disnake.ext import commands
import disnake
import games

class Trivia(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db2['Trivia']
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra=False)
	async def trivia(self, ctx):
		"""Start your trivia game."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		trivia = games.Trivia(ctx)
		await trivia.start()

	@trivia.group(name='points', invoke_without_command=True, case_insensitive=True)
	async def trivia_points(self, ctx, member: disnake.Member = None):
		"""See how many points the member has."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		member = member or ctx.author
		
		user = await self.db.find_one({'_id': member.id})
		if user is None:
			if member == ctx.author:
				await ctx.send("You never played trivia before! %s" % (ctx.author.mention))
				return
			await ctx.send("That user never played trivia before! %s" % (ctx.author.mention))
			return
		
		rank = 0
		rankings = await self.db.find().sort('points', -1).to_list(100000)
		for data in rankings:
			rank += 1
			if user['_id'] == data['_id']:
				break
		
		if member == ctx.author:
			title = "Here are your points:"
		else:
			title = "Here are %s's points:" % (member.display_name)

		em = disnake.Embed(color=color.lightpink, title=title)
		em.set_thumbnail(url=member.display_avatar)
		em.add_field(name="Points:", value="**%s**" % (user['points']), inline=False)
		em.add_field(name="Rank:", value="`#%s`" % (rank), inline=False)
		await ctx.send(embed=em)
	
	@trivia.command(name='leaderboard', aliases=['lb', 'top'])
	async def trivia_leaderboard(self, ctx):
		"""See the top 5 members with the most amount of trivia points."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		rank = 0
		em = disnake.Embed(color=color.lightpink, title="Here's top `5` trivia users with most points:")
		
		rankings = await self.db.find().sort('points', -1).to_list(5)
		for data in rankings:
			rank += 1
			user = ctx.guild.get_member(data['_id'])
			em.add_field(name="`#%s` %s" % (rank, user.display_name), value="**%s** points" % (data['points']), inline=False)
		
		await ctx.send(embed=em)
	
	@trivia_points.command(name='set')
	@commands.is_owner()
	async def tiriva_points_set(self, ctx, amount: int, member: disnake.Member = None):
		"""Set the trivia points for the member."""

		member = member or ctx.author
		
		userDb = await self.db.find_one({'_id': member.id})
		if userDb is None:
			await ctx.send("The user has never played trivia before. His points cannot be changed since he is not registered in the database.")
			return

		await self.db.update_one({'_id': member.id}, {'$set':{'points': amount}})
		await ctx.send("Succesfully set the points for user `%s` to **%s**." % (member.display_name, amount))

	@trivia_points.command(name='add')
	@commands.is_owner()
	async def trivia_points_add(self, ctx, amount: int, member: disnake.Member = None):
		"""Add trivia points to the member."""

		member = member or ctx.author
		
		userDb = await self.db.find_one({'_id': member.id})
		if userDb is None:
			await ctx.send("The member has never played trivia before. His points cannot be changed since he is not registered in the database.")
			return

		await self.db.update_one({'_id': member.id}, {'$inc':{'points': amount}})
		await ctx.send("Succesfully added **%s** points for member `%s`." % (amount, member.display_name))

	@trivia_points.command(name='reset')
	@commands.is_owner()
	async def trivia_points_reset(self, ctx, member: disnake.Member = None):
		"""Reset the points for the member."""

		member = member or ctx.author
		
		userDb = await self.db.find_one({'_id': member.id})
		if userDb is None:
			await ctx.send("The user has never played trivia before. His points cannot be changed since he is not registered in the database.")
			return

		await self.db.update_one({'_id': member.id}, {'$set':{'points': 0}})
		await ctx.send("Succesfully reset points for user `%s`." % (member.display_name))
	
	@trivia_points.command(name='gift', aliases=['give'])
	async def trivia_points_gift(self, ctx, amount: str, member: disnake.Member = None):
		"""Gift some of your points to the other member."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		if member is None:
			await ctx.send("You must specify the member you wish to give points to %s." % (ctx.author.mention))
			return
		elif member == ctx.author:
			await ctx.send("You cannot gift yourself... It doesn't really make any sense does it? %s" % (ctx.author.mention))
			return
		
		user = await self.db.find_one({'_id': ctx.author.id})
		memberDb = await self.db.find_one({'_id': member.id})
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
		view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.", member)
		view.message = msg = await ctx.send("%s wants to give you **%s** points. Do you accept? %s" % (ctx.author.mention, amount, member.mention), view=view)
		await view.wait()
		if view.response is True:		
			await self.db.update_one({'_id': ctx.author.id}, {'$inc':{'points': -amount}})
			await self.db.update_one({'_id': member.id}, {'$inc':{'points': amount}})
			e = "%s has accepted. Succesfully gifted the points %s" % (member.mention, ctx.author.mention)
			return await msg.edit(content=e, view=view)
		
		elif view.response is False:
			e = "%s has rejected your gift. %s" % (member.mention, ctx.author.mention)
			return await msg.edit(content=e, view=view)

	@trivia.error
	async def trivia_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send(error.original)
		
		elif isinstance(error, commands.TooManyArguments):
			return
		
		else:
			await self.bot.reraise(ctx, error)

		 
	
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({'_id': member.id})

def setup(bot):
	bot.add_cog(Trivia(bot))