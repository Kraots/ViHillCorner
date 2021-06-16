from trivia import trivia
import asyncio
import utils.colors as color
from discord.ext import commands
import motor.motor_asyncio
import os
import discord
import random
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
		points2 = 0
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		m1 = await ctx.send("%s Please pick a mode:\n\u2800• **Solo**\n\u2800• **Competitive**\n\n*To cancel type `!cancel`*" % (ctx.author.mention))
		try:
			while True:
				modee = await self.client.wait_for('message', check=check, timeout=180)
				mode = modee.content.lower()
				if mode in ['solo', 'competitive', 'comp', '!cancel']:
					break
				else:
					await modee.reply("That is not a valid mode.Please pick a mode:\n\u2800• **Solo**\n\u2800• **Competitive**\n\n*To cancel type `!cancel`*")
		
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
							question = await trivia.question(amount=1, difficulty=difficulty)

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
							
							rand = random.randint(1, 4)
							
							if question[0]['type'] == 'boolean':							
								em = discord.Embed(color=color.lightpink, title="[TRUE/FALSE]\nHere is your `%s` question %s" % (question_nr, ctx.author.display_name), description='*%s*' % (question[0]['question']))
							elif question[0]['type'] == 'multiple':	
								if rand == 1:
									correct = "`A.`"
									desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['correct_answer'], question[0]['incorrect_answers'][0], question[0]['incorrect_answers'][1], question[0]['incorrect_answers'][2])
								elif rand == 2:
									correct = "`B.`"
									desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['incorrect_answers'][0], question[0]['correct_answer'], question[0]['incorrect_answers'][1], question[0]['incorrect_answers'][2])
								elif rand == 3:
									correct = "`C.`"
									desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['incorrect_answers'][0], question[0]['incorrect_answers'][1], question[0]['correct_answer'], question[0]['incorrect_answers'][2])
								elif rand == 4:
									correct = "`D.`"
									desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['incorrect_answers'][0], question[0]['incorrect_answers'][1], question[0]['incorrect_answers'][2], question[0]['correct_answer'])						
								em = discord.Embed(color=color.lightpink, title="[CHOOSE THE CORRECT ANSWER]\nHere is your `%s` question %s" % (question_nr, ctx.author.display_name), description=desc)
							question_msg = await ctx.send(embed=em)

							try:
								while True:
									answerr = await self.client.wait_for('message', check=check, timeout=180)
									answer = answerr.content.lower()
									if answer in ['a', 'b', 'c', 'd']:
										if rand == 1:
											if answer == 'a':
												answer = question[0]['correct_answer'].lower()
											else:
												answer = "."
										elif rand == 2:
											if answer == 'b':
												answer = question[0]['correct_answer'].lower()
											else:
												answer = "."
										elif rand == 3:
											if answer == 'c':
												answer = question[0]['correct_answer'].lower()
											else:
												answer = "."
										elif rand == 4:
											if answer == 'd':
												answer = question[0]['correct_answer'].lower()
											else:
												answer = "."
										break
									else:
										em = discord.Embed(title="That is not a valid form of reply. To get to your question please click me (the blue text).", url=question_msg.jump_url)
										await answerr.reply(embed=em)
							
							except asyncio.TimeoutError:
								await ctx.send("Ran out of time. %s" % (ctx.author.mention))
								return
							
							else:
								if answer == question[0]['correct_answer'].lower():
									if difficulty == 'easy':
										await answerr.reply("Correct! You get **5** points.")
										points += 5
									elif difficulty == 'medium':
										await answerr.reply("Correct! You get **10** points.")
										points += 10
									elif difficulty == 'hard':
										await answerr.reply("Correct! You get **15** points.")
										points += 15
								else:
									if difficulty == 'easy':
										await answerr.reply("Wrong. You lose **5** points.\nThe correct answer was %s **%s**" % (correct, question[0]['correct_answer']))
										points -= 5
									elif difficulty == 'medium':
										await answerr.reply("Wrong. You lose **10** points.\nThe correct answer was %s **%s**" % (correct, question[0]['correct_answer']))
										points -= 10
									elif difficulty == 'hard':
										await answerr.reply("Wrong. You lose **15** points.\nThe correct answer was %s **%s**" % (correct, question[0]['correct_answer']))
										points -= 15

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
						
						result = discord.Embed(color=final_color, title="Trivia has ended.", description=final_result)
						result.add_field(name='Your total points before:', value="**%s**" % (before_points), inline=False)
						result.add_field(name='Your total points now:', value="**%s**" % (after_points), inline=False)

						await ctx.reply(embed=result)
			
			elif mode in ['competitive', 'comp']:
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
						await ctx.send("How many points do you want to bet.")
						try:
							user = await db.find_one({'_id': ctx.author.id})
							while True:
								wager_amountt = await self.client.wait_for('message', check=check, timeout=180)
								
								try:
									if wager_amountt.content.lower() == '!cancel':
										await ctx.send("Canceled. %s" % ctx.author.mention)
										return
									elif wager_amountt.content.lower() == 'all':
										if user is None:
											await ctx.send("You never played trivia before, you cannot challenge someone else since you don't have any points. %s" % (ctx.author.mention))
											return
										wager_amount = user['points']
									else:
										wager_amount = int(wager_amountt.content)
								except ValueError:
									await ctx.send("Not a number. %s" % (ctx.author.mention))
								else:
									if wager_amount < 15:
										await ctx.send("You must place a minimum of `15` points bet. %s" % (ctx.author.mention))
									elif str(wager_amount)[-1] not in ['5', '0']:
										await ctx.send("The number must always end in **5** or **0**. %s" % (ctx.author.mention))
									elif user['points'] < wager_amount:
										print("here 2")
										await ctx.send("You do not have enough points to place this bet. %s" % (ctx.author.mention))
										return
									else:
										break

						except asyncio.TimeoutError:
							await ctx.send("Ran out of time. %s" % (ctx.author.mention))
							return
									
						else:		
							await ctx.send("Choose your opponent by pinging them. %s" % (ctx.author.mention))
							try:
								while True:
									opponentt = await self.client.wait_for('message', check=check, timeout=180)
									opponent = opponentt.mentions
									try:
										if opponent[1]:
											await opponentt.reply("You can only choose **1** opponent at a time.")
									except IndexError:
										if not opponent:
											if opponentt.content.lower() == '!cancel':
												await ctx.send("Canceled. %s" % (ctx.author.mention))
												return
											await opponentt.reply("You must ping them!")
										else:
											opponent = opponent[0]
											if opponent == ctx.author:
												await opponentt.reply("You cannot choose yourself!")
											else:
												break
								
							except asyncio.TimeoutError:
								await ctx.send("Ran out of time. %s" % (ctx.author.mention))
								return

							else:
								opponent_db = await db.find_one({'_id': opponent.id})
								if opponent_db is None:
									await ctx.send("The opponent you chose has never played trivia before. You cannot challange this person. %s" % (ctx.author.mention))
									return
								elif opponent_db['points'] < wager_amount:
									await ctx.send("The opponent you chose does not have enough points according to the bet you placed. %s" % (ctx.author.mention))
									return
								
								else:
									def checkk(reaction, user):
										return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == opponent.id
									msg = await ctx.send("%s You got challenged by %s to a 1v1 trivia. Here are the conditions that your opponent chose:\n\u2800• **Mode**: `%s`\n\u2800• **Difficulty**: `%s`\n\u2800• **Rounds**: `%s`\n\u2800• **Bet**: `%s` points\n\nDo you accept?" % (opponent.mention, ctx.author.mention, mode, difficulty, amount, wager_amount))
									await msg.add_reaction('<:agree:797537027469082627>')
									await msg.add_reaction('<:disagree:797537030980239411>')

									try:
										reaction, user = await self.client.wait_for('reaction_add', check=checkk, timeout=180)

									except asyncio.TimeoutError:
										new_msg = f"{opponent.mention} Did not react in time."
										await msg.edit(content=new_msg)
										await msg.clear_reactions()
										return
									
									else:
										if str(reaction.emoji) == '<:agree:797537027469082627>':
											e = "%s Has accepted. Starting Trivia." % (opponent.mention)
											await msg.clear_reactions()
											await msg.edit(content=e)
											def opponent_check(m):
												return m.author == opponent and m.channel == ctx.channel

										
										elif str(reaction.emoji) == '<:disagree:797537030980239411>':
											e = "%s Has not accepted." % (opponent.mention)
											await msg.clear_reactions()
											await msg.edit(content=e)
											return

										for i in range(amount):
											question = await trivia.question(amount=2, difficulty=difficulty, quizType='boolean')

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
											
											if question[0]['type'] == 'boolean':
												em = discord.Embed(color=color.lightpink, title="[TRUE/FALSE]\nHere is your `%s` question %s" % (question_nr, ctx.author.display_name), description='*%s*' % (question[0]['question']))
											elif question[0]['type'] == 'multiple':	
												rand = random.randint(1, 4)
												if rand == 1:
													correct = "`A.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['correct_answer'], question[0]['incorrect_answers'][0], question[0]['incorrect_answers'][1], question[0]['incorrect_answers'][2])
												elif rand == 2:
													correct = "`B.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['incorrect_answers'][0], question[0]['correct_answer'], question[0]['incorrect_answers'][1], question[0]['incorrect_answers'][2])
												elif rand == 3:
													correct = "`C.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['incorrect_answers'][0], question[0]['incorrect_answers'][1], question[0]['correct_answer'], question[0]['incorrect_answers'][2])
												elif rand == 4:
													correct = "`D.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[0]['question'], question[0]['incorrect_answers'][0], question[0]['incorrect_answers'][1], question[0]['incorrect_answers'][2], question[0]['correct_answer'])
												em = discord.Embed(color=color.lightpink, title="[CHOOSE THE CORRECT ANSWER]\nHere is your `%s` question %s" % (question_nr, ctx.author.display_name), description=desc)
											question_msg = await ctx.send(embed=em)
											try:
												while True:
													answerr = await self.client.wait_for('message', check=check, timeout=180)
													answer = answerr.content.lower()
													if answer in ['a', 'b', 'c', 'd']:
														if rand == 1:
															if answer == 'a':
																answer = question[0]['correct_answer'].lower()
															else:
																answer = "."
														elif rand == 2:
															if answer == 'b':
																answer = question[0]['correct_answer'].lower()
															else:
																answer = "."
														elif rand == 3:
															if answer == 'c':
																answer = question[0]['correct_answer'].lower()
															else:
																answer = "."
														elif rand == 4:
															if answer == 'd':
																answer = question[0]['correct_answer'].lower()
															else:
																answer = "."
														break
													else:
														em = discord.Embed(title="That is not a valid form of reply. To get to your question please click me (the blue text).", url=question_msg.jump_url)
														await answerr.reply(embed=em)
											
											except asyncio.TimeoutError:
												await ctx.send("Ran out of time. %s" % (ctx.author.mention))
											
											else:
												if answer == question[0]['correct_answer'].lower():
													if difficulty == 'easy':
														await answerr.reply("Correct! You get **5** points. %s" % (ctx.author.mention))
														points += 5
													elif difficulty == 'medium':
														await answerr.reply("Correct! You get **10** points. %s" % (ctx.author.mention))
														points += 10
													elif difficulty == 'hard':
														await answerr.reply("Correct! You get **15** points. %s" % (ctx.author.mention))
														points += 15
												else:
													if difficulty == 'easy':
														await answerr.reply("Wrong. You lose **5** points. %s\nThe correct answer was %s **%s**" % (ctx.author.mention, correct, question[0]['correct_answer']))
														points -= 5
													elif difficulty == 'medium':
														await answerr.reply("Wrong. You lose **10** points. %s\nThe correct answer was %s **%s**" % (ctx.author.mention, correct, question[0]['correct_answer']))
														points -= 10
													elif difficulty == 'hard':
														await answerr.reply("Wrong. You lose **15** points. %s\nThe correct answer was %s **%s**" % (ctx.author.mention, correct, question[0]['correct_answer']))
														points -= 15
												
											if question[0]['type'] == 'boolean':
												em = discord.Embed(color=color.lightpink, title="[TRUE/FALSE]\nHere is your `%s` question %s" % (question_nr, opponent.display_name), description='*%s*' % (question[1]['question']))
											elif question[0]['type'] == 'multiple':	
												rand = random.randint(1, 4)
												if rand == 1:
													correct = "`A.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[1]['question'], question[1]['correct_answer'], question[1]['incorrect_answers'][0], question[1]['incorrect_answers'][1], question[1]['incorrect_answers'][2])
												elif rand == 2:
													correct = "`B.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[1]['question'], question[1]['incorrect_answers'][0], question[1]['correct_answer'], question[1]['incorrect_answers'][1], question[1]['incorrect_answers'][2])
												elif rand == 3:
													correct = "`C.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[1]['question'], question[1]['incorrect_answers'][0], question[1]['incorrect_answers'][1], question[1]['correct_answer'], question[1]['incorrect_answers'][2])
												elif rand == 4:
													correct = "`D.`"
													desc = '*%s*\n\u2800`A.` **%s**\n\u2800`B.` **%s**\n\u2800`C.` **%s**\n\u2800`D.` **%s**' % (question[1]['question'], question[1]['incorrect_answers'][0], question[1]['incorrect_answers'][1], question[1]['incorrect_answers'][2], question[1]['correct_answer'])
												em = discord.Embed(color=color.lightpink, title="[CHOOSE THE CORRECT ANSWER]\nHere is your `%s` question %s" % (question_nr, ctx.author.display_name), description=desc)
											question_msg = await ctx.send(embed=em)
											try:
												while True:
													answerr = await self.client.wait_for('message', check=opponent_check, timeout=180)
													answer = answerr.content.lower()
													if answer in ['a', 'b', 'c', 'd']:
														if rand == 1:
															if answer == 'a':
																answer = question[1]['correct_answer'].lower()
															else:
																answer = "."
														elif rand == 2:
															if answer == 'b':
																answer = question[1]['correct_answer'].lower()
															else:
																answer = "."
														elif rand == 3:
															if answer == 'c':
																answer = question[1]['correct_answer'].lower()
															else:
																answer = "."
														elif rand == 4:
															if answer == 'd':
																answer = question[1]['correct_answer'].lower()
															else:
																answer = "."
														break
													else:
														em = discord.Embed(title="That is not a valid form of reply. To get to your question please click me (the blue text).", url=question_msg.jump_url)
														await answerr.reply(embed=em)
											
											except asyncio.TimeoutError:
												await ctx.send("Ran out of time. %s" % (opponent.mention))
											
											else:
												if answer == question[1]['correct_answer'].lower():
													if difficulty == 'easy':
														await answerr.reply("Correct! You get **5** points. %s" % (opponent.mention))
														points2 += 5
													elif difficulty == 'medium':
														await answerr.reply("Correct! You get **10** points. %s" % (opponent.mention))
														points2 += 10
													elif difficulty == 'hard':
														await answerr.reply("Correct! You get **15** points. %s" % (opponent.mention))
														points2 += 15
												else:
													if difficulty == 'easy':
														await answerr.reply("Wrong. You lose **5** points. %s\nThe correct answer was %s **%s**" % (opponent.mention, correct, question[1]['correct_answer']))
														points2 -= 5
													elif difficulty == 'medium':
														await answerr.reply("Wrong. You lose **10** points. %s\nThe correct answer was %s **%s**" % (opponent.mention, correct, question[1]['correct_answer']))
														points2 -= 10
													elif difficulty == 'hard':
														await answerr.reply("Wrong. You lose **15** points. %s\nThe correct answer was %s **%s**" % (opponent.mention, correct, question[1]['correct_answer']))
														points2 -= 15

					user = await db.find_one({'_id': ctx.author.id})
					draw = False

					if points > points2:		# USER/AUTHOR WIN
						final_result = "***%s Has won the wager (`%s` points).***" % (ctx.author.mention, wager_amount)					
						before_points_user = user['points']
						after_points_user = before_points_user + wager_amount
						before_points_opponent = opponent_db['points']
						after_points_opponent = before_points_opponent - wager_amount
						await db.update_one({'_id': ctx.author.id}, {'$inc':{'points': wager_amount}})
						await db.update_one({'_id': opponent.id}, {'$inc':{'points': -wager_amount}})
					
					elif points < points2:		# OPPONENT WIN
						final_result = "***%s Has won (`%s` points).***" % (opponent.mention, wager_amount)
						before_points_user = user['points']
						after_points_user = before_points_user - wager_amount
						before_points_opponent = opponent_db['points']
						after_points_opponent = before_points_opponent + wager_amount
						await db.update_one({'_id': ctx.author.id}, {'$inc':{'points': -wager_amount}})
						await db.update_one({'_id': opponent.id}, {'$inc':{'points': wager_amount}})
					
					elif points == points2:
						final_result = "***Draw. No one lost and no one won anything.***"
						draw = True

					result = discord.Embed(color=color.blue, title="Trivia has ended.", description=final_result)
					if draw == False:
						result.add_field(name="**-->** `%s's` total points before:" % (ctx.author.display_name), value="**%s**" % (before_points_user), inline=True)
						result.add_field(name="`%s's` total points after:" % (ctx.author.display_name), value="**%s**" % (after_points_user), inline=False)
						result.add_field(name="**-->** `%s's` total points before:" % (opponent.display_name), value="**%s**" % (before_points_opponent), inline=True)
						result.add_field(name="`%s's` total points after:" % (opponent.display_name), value="**%s**" % (after_points_opponent), inline=False)
					

					await ctx.reply(embed=result)



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
		if isinstance(error, commands.TooManyArguments):
			return

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await db.delete_one({'_id': member.id})

def setup(client):
	client.add_cog(TriviaCommands(client))