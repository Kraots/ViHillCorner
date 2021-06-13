from trivia import trivia
import asyncio
import utils.colors as color
from discord.ext import commands
import motor.motor_asyncio
import os
import discord
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
		points = 0
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		m1 = await ctx.send("%s Please pick a mode:\n\u2800• **Solo**\n\u2800• **Competitive** (COMING SOON)\n\n*To cancel type `!cancel`*" % (ctx.author.mention))
		try:
			while True:
				modee = await self.client.wait_for('message', check=check, timeout=180)
				mode = modee.content.lower()
				if mode in ['solo', 'competitive', '!cancel']:
					break
				else:
					await modee.reply("That is not a valid mode.Please pick a mode:\n\u2800• **Solo**\n\u2800• **Competitive** (COMING SOON)\n\n*To cancel type `!cancel`*")
		
		except asyncio.TimeoutError:
			e = "Ran out of time to answer. %s" % (ctx.author.mention)
			await m1.edit(content=e)
			return
		
		else:
			if mode == '!cancel':
				await modee.reply("Canceled.")
				return
			
			elif mode == 'solo':
				await ctx.send("How many questions should there be? `3-10`")
				try:
					while True:
						amountt = await self.client.wait_for('message', check=check, timeout=180)
						try:
							if amountt.content.lower() == '!cancel':
								await amountt.reply("Canceled.")
								return
							amount = int(amountt.content)
							if amount < 3 or amount > 10:
								await amountt.reply("The number must be between **3** or **10**, no higher or less.")
							else:
								break

						except ValueError:
							await amountt.reply("That is not a number.")
				
				except asyncio.TimeoutError:
							await ctx.send("Took too much to respond. %s" % (ctx.author.mention))
							return
				
				else:
					
					await ctx.send("Please choose a difficulty:\n\u2800• **Easy**\n\u2800• **Medium**\n\u2800• **Hard**")
					try:
						while True:
							difficultyy = await self.client.wait_for('message', check=check, timeout=180)
							difficulty = difficultyy.content.lower()
							if difficulty == '!cancel':
								await difficultyy.reply("Canceled.")
								return
							elif difficulty in ['easy', 'medium', 'hard']:
								break
							else:
								await difficultyy.reply("That is not a valid form of difficulty. Please choose from:\n\u2800• **Easy**\n\u2800• **Medium**\n\u2800• **Hard**")
					
					except asyncio.TimeoutError:
						await ctx.send("Took too much to respond. %s" % (ctx.author.mention))
						return
					
					else:
						for i in range(amount):
							question = await trivia.question(amount=1, difficulty=difficulty, quizType='boolean')

							if i == 0:
								question_nr = '1st'
							elif i == 1:
								question_nr = '2nd'
							elif i == 2:
								question_nr = '3rd'
							elif i == 3:
								question_nr = '4th'
							elif i == 4:
								question_nr = '5th'
							elif i == 5:
								question_nr = '6th'
							elif i == 6:
								question_nr = '7th'
							elif i == 7:
								question_nr = '8th'
							elif i == 8:
								question_nr = '9th'
							if i == (amount - 1):
								question_nr = 'last'
							
							em = discord.Embed(color=color.lightpink, title="[TRUE/FALSE]\nHere is your `%s` question %s" % (question_nr, ctx.author.display_name), description='*%s*' % (question[0]['question']))
							await ctx.send(embed=em)
							try:
								while True:
									answerr = await self.client.wait_for('message', check=check, timeout=180)
									answer = answerr.content.lower()
									if answer == '!cancel':
										await answerr.reply('Canceled.')
										return
									elif answer in ['true', 'false']:
										break
									else:
										await answerr.reply('That is not a valid form of reply.')
							
							except asyncio.TimeoutError:
								await ctx.send("Ran out of time. %s" % (ctx.author.mention))
								return
							
							else:
								if answer == question[0]['correct_answer'].lower():
									await answerr.reply("Correct! You get **5** points.")
									points += 5
								else:
									await answerr.reply("Wrong. You lose **5** points.\nThe correct answer was **%s**" % (question[0]['correct_answer'].lower()))
									points -= 5

						if points < 0:
							final_result = "You lost **%s** points. OOF" % (points)
							final_color = color.red
						elif points == 0:
							final_result = "You didn't get any points but you didn't lose any either."
							final_color = discord.Color.light_grey()
						elif points >= 5:
							final_result = "You got **%s** points. Congratulations" % (points)
							final_color = discord.Color.green()
						
						user = await db.find_one({'_id': ctx.author.id})
						if user is None:
							before_points = 0
							after_points = points
							post = {'_id': ctx.author.id,
									'points': points}
							await db.insert_one(post)
						else:
							before_points = user['points']
							after_points = before_points + points
							await db.update_one({'_id': ctx.author.id}, {'$inc':{'points': points}})
						
						print(points)
						print(final_color)
						result = discord.Embed(color=final_color, title="Trivia has ended.", description=final_result)
						result.add_field(name='Your total points before:', value="**%s**" % (before_points), inline=False)
						result.add_field(name='Your total points now:', value="**%s**" % (after_points), inline=False)

						await ctx.reply(embed=result)



	@_trivia.command()
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

	@_trivia.error
	async def trivia_error(self, ctx, error):
		if isinstance(error, commands.TooManyArguments):
			return

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await db.delete_one({'_id': member.id})

def setup(client):
	client.add_cog(TriviaCommands(client))