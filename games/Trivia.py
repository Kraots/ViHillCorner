from trivia import trivia
import asyncio
import utils.colors as color
import disnake
import random

class Trivia:
	def __init__(self, ctx):
		self.db = ctx.bot.db2['Trivia']
		self.bot = ctx.bot
		self.player = ctx.author
		self.ctx = ctx
		self.points = 0
		self.points2 = 0
	
	async def update_db(self, user, points):
		await self.db.update_one({'_id': user.id}, {'$inc':{'points': points}})

	async def get_mode(self) -> str:
		await self.ctx.send(f"{self.player.mention} Please pick a mode:\n\u2800• **Solo**\n\u2800• **Competitive**\n\n*To cancel type `!cancel`*")
		def check(m):
			return m.channel.id == self.ctx.channel.id and m.author.id == self.player.id
		try:
			while True:
				mode = await self.bot.wait_for('message', check=check, timeout=180)
				if mode.content.lower() == '!cancel':
					raise Exception('Cancelled.')
				elif mode.content.lower() in ['solo', 'competitive', 'comp']:
					break
				else:
					await mode.reply("Invalid mode.")
		except asyncio.TimeoutError:
			raise Exception(f'Took too much to respond {self.player.mention}')
		
		return mode.content.lower()

	async def get_questions_amount(self) -> int:
		await self.ctx.send(f'{self.player.mention} How many questions should there be? `3-10`')
		def check(m):
			return m.channel.id == self.ctx.channel.id and m.author.id == self.player.id
		try:
			while True:
				_amount = await self.bot.wait_for('message', check=check, timeout=180)
				try:
					if _amount.content.lower() == '!cancel':
						raise Exception('Cancelled')
					amount = int(_amount.content)
					if amount < 3 or amount > 10:
						await _amount.reply("The number must be between **3** or **10**, no higher or less.")
					else:
						break

				except ValueError:
					await _amount.reply("That is not a number.")
		
		except asyncio.TimeoutError:
			raise Exception(f'Took too much to respond {self.player.mention}')
		
		return amount
	
	async def get_difficulty(self) -> str:
		await self.ctx.send(f"{self.player.mention} Please choose a difficulty:\n\u2800• **Easy**\n\u2800• **Medium**\n\u2800• **Hard**")
		def check(m):
			return m.channel.id == self.ctx.channel.id and m.author.id == self.player.id
		try:
			while True:
				_difficulty = await self.bot.wait_for('message', check=check, timeout=180)
				difficulty = _difficulty.content.lower()
				if difficulty == '!cancel':
					raise Exception('Cancelled')
				elif difficulty in ['easy', 'medium', 'hard']:
					break
				else:
					await _difficulty.reply("That is not a valid form of difficulty. Please choose from:\n\u2800• **Easy**\n\u2800• **Medium**\n\u2800• **Hard**")
		
		except asyncio.TimeoutError:
			raise Exception(f'Took too much to respond {self.player.mention}')
		
		return difficulty
	
	async def get_wager_amount(self) -> int:
		def check(m):
			return m.channel.id == self.ctx.channel.id and m.author.id == self.player.id
		await self.ctx.send(f"How many points do you want to bet? {self.player.mention}")
		user = await self.db.find_one({'_id': self.player.id})
		if user is None:
			raise Exception("You have never played this game before, therefore cannot play this gamemode.")
		try:
			while True:
				_wager_amount = await self.bot.wait_for('message', check=check, timeout=180)
				wager_amount = _wager_amount.content
				if wager_amount.lower() == '!cancel':
					raise Exception('Cancelled.')
				elif wager_amount.lower() == 'all':
					wager_amount = user['points']
				else:
					try:
						wager_amount = int(_wager_amount.content)
					except ValueError:
						await _wager_amount.reply("Not a number!")
				if wager_amount < 15:
					await _wager_amount.reply(f"You must place a minimum of `15` points bet. {self.player.mention}")
				elif str(wager_amount)[-1] not in ['5', '0']:
					await _wager_amount.reply(f"The number must always end in **5** or **0**. {self.player.mention}")
				elif user['points'] < wager_amount:
					raise Exception(f"You do not have enough points to place this bet. {self.player.mention}")
				else:
					break
		
		except asyncio.TimeoutError:
			raise Exception(f'Took too much to respond {self.player.mention}')
		
		return wager_amount

	async def get_opponent(self, wager_amount) -> disnake.Member:
		def check(m):
			return m.channel.id == self.ctx.channel.id and m.author.id == self.player.id
		await self.ctx.send(f"Choose your opponent by pinging them. {self.player.mention}")
		try:
			while True:
				_opponent = await self.bot.wait_for('message', check=check, timeout=180)
				opponent = _opponent.mentions
				try:
					if opponent[1]:
						await _opponent.reply("You can only choose **1** opponent at a time.")
				except IndexError:
					if not opponent:
						if _opponent.content.lower() == '!cancel':
							raise Exception("Cancelled.")
						await _opponent.reply("You must ping them!")
					else:
						opponent = opponent[0]
						if opponent.id == self.player.id:
							await _opponent.reply("You cannot choose yourself!")
						else:
							break
			
		except asyncio.TimeoutError:
			raise Exception(f'Took too much to respond {self.player.mention}')
		
		else:
			opponent_db = await self.db.find_one({'_id': opponent.id})
			if opponent_db is None:
				raise Exception(f"The opponent you chose has never played trivia before. You cannot challenge this person. {self.player.mention}")
			elif opponent_db['points'] < wager_amount:
				raise Exception(f"The opponent you chose does not have enough points according to the bet you placed. {self.player.mention}")
		
		return opponent

	def ord_numbers(self, n, amount) -> str:
		if n == 0:
			nr = '1st'
		elif n == 1:
			nr = '2nd'
		elif n == 2:
			nr = '3rd'
		elif n == 3:
			nr = '4th'
		elif n == 4:
			nr = '5th'
		elif n == 5:
			nr = '6th'
		elif n == 6:
			nr = '7th'
		elif n == 7:
			nr = '8th'
		elif n == 8:
			nr = '9th'
		if n == (amount - 1):
			nr = 'last'
		
		return nr

	async def send_question(self, user, question_index, question_nr, question_type, question, rand):
		if question_type == 'boolean':							
			em = disnake.Embed(color=color.lightpink, title=f"[TRUE/FALSE]\nHere is your `{question_nr}` question {user.display_name}", description=f"*{question[question_index]['question']}*")
		
		elif question[question_index]['type'] == 'multiple':
			if rand == 1:
				correct_choice = "`A.`"
				desc = f"*{question[question_index]['question']}*\n\u2800`A.` **{question[question_index]['correct_answer']}**\n\u2800`B.` **{question[question_index]['incorrect_answers'][0]}**\n\u2800`C.` **{question[question_index]['incorrect_answers'][1]}**\n\u2800`D.` **{question[question_index]['incorrect_answers'][2]}**"
			elif rand == 2:
				correct_choice = "`B.`"
				desc = f"*{question[question_index]['question']}*\n\u2800`A.` **{question[question_index]['incorrect_answers'][0]}**\n\u2800`B.` **{question[question_index]['correct_answer']}**\n\u2800`C.` **{question[question_index]['incorrect_answers'][1]}**\n\u2800`D.` **{question[question_index]['incorrect_answers'][2]}**"
			elif rand == 3:
				correct_choice = "`C.`"
				desc = f"*{question[question_index]['question']}*\n\u2800`A.` **{question[question_index]['incorrect_answers'][0]}**\n\u2800`B.` **{question[question_index]['incorrect_answers'][1]}**\n\u2800`C.` **{question[question_index]['correct_answer']}**\n\u2800`D.` **{question[question_index]['incorrect_answers'][2]}**"
			elif rand == 4:
				correct_choice = "`D.`"
				desc = f"*{question[question_index]['question']}*\n\u2800`A.` **{question[question_index]['incorrect_answers'][0]}**\n\u2800`B.` **{question[question_index]['incorrect_answers'][1]}**\n\u2800`C.` **{question[question_index]['incorrect_answers'][2]}**\n\u2800`D.` **{question[question_index]['correct_answer']}**"
			em = disnake.Embed(color=color.lightpink, title=f"[CHOOSE THE CORRECT ANSWER]\nHere is your `{question_nr}` question {user.display_name}", description=desc)
		
		question_msg = await self.ctx.send(embed=em)
		try:
			correct_choice = correct_choice
		except UnboundLocalError:
			correct_choice = None

		return {'jump_url': question_msg.jump_url, 'correct_choice': correct_choice}

	async def get_answer(self, user, question_index, rand, question, JumpUrl):
		def check(m):
			return m.channel.id == self.ctx.channel.id and m.author.id == user.id
		try:
			while True:
				_answer = await self.bot.wait_for('message', check=check, timeout=180)
				answer = _answer.content.lower()
				if answer in ['a', 'b', 'c', 'd', 'true', 'false']:
					if rand == 1:
						if answer == 'a':
							answer = question[question_index]['correct_answer'].lower()
						elif answer not in ['true', 'false']:
							answer = "."
					elif rand == 2:
						if answer == 'b':
							answer = question[question_index]['correct_answer'].lower()
						elif answer not in ['true', 'false']:
							answer = "."
					elif rand == 3:
						if answer == 'c':
							answer = question[question_index]['correct_answer'].lower()
						elif answer not in ['true', 'false']:
							answer = "."
					elif rand == 4:
						if answer == 'd':
							answer = question[question_index]['correct_answer'].lower()
						elif answer not in ['true', 'false']:
							answer = "."
					break
				else:
					em = disnake.Embed(title="That is not a valid form of reply. To get to your question please click me (the blue text).", url=JumpUrl)
					await _answer.reply(embed=em)
		
		except asyncio.TimeoutError:
			raise Exception(f'Took too much to respond {user.mention}')

		return [answer, _answer]

	async def check_answer(self, user, answer, difficulty, question_index, question, question_type, correct_choice):
		_answer = answer[1]
		answer = answer[0]

		if answer == question[question_index]['correct_answer'].lower():
			
			if difficulty == 'easy':
				await _answer.reply(f"Correct! You get **5** points. {user.mention}")
				if user == self.player:
					self.points += 5
				else:
					self.points2 += 5
			
			elif difficulty == 'medium':
				await _answer.reply(f"Correct! You get **10** points. {user.mention}")
				if user == self.player:
					self.points += 10
				else:
					self.points2 += 10
			
			elif difficulty == 'hard':
				await _answer.reply(f"Correct! You get **15** points. {user.mention}")
				if user == self.player:
					self.points += 15
				else:
					self.points2 += 15
		else:
			
			if difficulty == 'easy':
				if question_type == 'multiple':
					await _answer.reply(f"Wrong. You lose **5** points. {user.mention}\nThe correct answer was {correct_choice} **{question[question_index]['correct_answer']}**")
				else:
					await _answer.reply(f"Wrong. You lose **5** points. {user.mention}\nThe correct answer was **{question[question_index]['correct_answer']}**")
				if user == self.player:
					self.points += -5
				else:
					self.points2 += -5
			
			elif difficulty == 'medium':
				if question_type == 'multiple':
					await _answer.reply(f"Wrong. You lose **10** points. {user.mention}\nThe correct answer was {correct_choice} **{question[question_index]['correct_answer']}**")
				else:
					await _answer.reply(f"Wrong. You lose **10** points. {user.mention}\nThe correct answer was **{question[question_index]['correct_answer']}**")
				if user == self.player:
					self.points += -10
				else:
					self.points2 += -10
			
			elif difficulty == 'hard':
				if question_type == 'multiple':
					await _answer.reply(f"Wrong. You lose **15** points. {user.mention}\nThe correct answer was {correct_choice} **{question[question_index]['correct_answer']}**")
				else:
					await _answer.reply(f"Wrong. You lose **15** points. {user.mention}\nThe correct answer was **{question[question_index]['correct_answer']}**")
				if user == self.player:
					self.points += -15
				else:
					self.points2 += -15

	async def solo(self) -> disnake.Embed:
		difficulty = await self.get_difficulty()
		rounds = await self.get_questions_amount()
		for i in range(rounds):
			question = await trivia.question(amount=1, difficulty=difficulty)
			question_nr = self.ord_numbers(i, rounds)
			question_type = question[0]['type']
			rand = random.randint(1,4)
			
			result = await self.send_question(self.player, 0, question_nr, question_type, question, rand)
			answer = await self.get_answer(self.player, 0, rand, question, result['jump_url'])
			await self.check_answer(self.player, answer, difficulty, 0, question, question_type, result['correct_choice'])

		if self.points < 0:
			final_result = f"You lost **{self.points}** points. OOF"
			final_color = color.red
		elif self.points == 0:
			final_result = "You didn't get any points but you didn't lose any either."
			final_color = disnake.Color.light_grey()
		elif self.points >= 5:
			final_result = f"You got **{self.points}** points. Congratulations"
			final_color = disnake.Color.green()

		user = await self.db.find_one({'_id': self.player.id})
		if user is None:
			before_points = 0
			after_points = self.points
			post = {
				'_id': self.player.id,
				'points': self.points
					}
			await self.db.insert_one(post)
		else:
			before_points = user['points']
			after_points = before_points + self.points
			await self.update_db(self.player, self.points)
		
		em = disnake.Embed(color=final_color, title="Trivia has ended.", description=final_result)
		em.add_field(name='Your total points before:', value="**%s**" % (before_points), inline=False)
		em.add_field(name='Your total points now:', value="**%s**" % (after_points), inline=False)

		return em
	
	async def competitive(self) -> disnake.Embed:
		difficulty = await self.get_difficulty()
		rounds = await self.get_questions_amount()
		wager_amount = await self.get_wager_amount()
		opponent = await self.get_opponent(wager_amount)

		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == opponent.id
		msg = await self.ctx.send(f"{opponent.mention} You got challenged by **{self.player}** to a 1v1 trivia. Here are the conditions that your opponent chose:\n\u2800• **Difficulty**: {difficulty}\n\u2800• **Rounds**: {rounds}\n\u2800• **Bet**: `{wager_amount}` points\n\nDo you accept?")
		await msg.add_reaction('<:agree:797537027469082627>')
		await msg.add_reaction('<:disagree:797537030980239411>')

		try:
			reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)

		except asyncio.TimeoutError:
			new_msg = f"{opponent.mention} Did not react in time."
			await msg.edit(content=new_msg)
			await msg.clear_reactions()
			return
		
		else:
			if str(reaction.emoji) == '<:agree:797537027469082627>':
				e = f"{opponent.mention} Has accepted. Starting Trivia."
				await msg.clear_reactions()
				await msg.edit(content=e)

			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = f"{opponent.mention} Has not accepted."
				await msg.clear_reactions()
				await msg.edit(content=e)
				return

		for i in range(rounds):
			question = await trivia.question(amount=2, difficulty=difficulty)
			question_nr = self.ord_numbers(i, rounds)
			question_type1 = question[0]['type']
			question_type2 = question[1]['type']
			rand = random.randint(1,4)
			
			result = await self.send_question(self.player, 0, question_nr, question_type1, question, rand)
			answer = await self.get_answer(self.player, 0, rand, question, result['jump_url'])
			await self.check_answer(self.player, answer, difficulty, 0, question, question_type1, result['correct_choice'])

			result = await self.send_question(opponent, 1, question_nr, question_type2, question, rand)
			answer = await self.get_answer(opponent, 1, rand, question, result['jump_url'])
			await self.check_answer(opponent, answer, difficulty, 1, question, question_type2, result['correct_choice'])

		user = await self.db.find_one({'_id': self.player.id})
		opponentDb = await self.db.find_one({'_id': opponent.id})

		draw = False
		if self.points > self.points2:		# USER/AUTHOR WIN
			final_result = f"***{self.player.mention} Has won the wager (`{wager_amount}` points).***"
			before_points_user = user['points']
			after_points_user = before_points_user + wager_amount
			before_points_opponent = opponentDb['points']
			after_points_opponent = before_points_opponent - wager_amount
			await self.update_db(self.player, wager_amount)
			await self.update_db(opponent, -wager_amount)
		
		elif self.points < self.points2:		# OPPONENT WIN
			final_result = f"***{opponent.mention} Has won (`{wager_amount}` points).***"
			before_points_user = user['points']
			after_points_user = before_points_user - wager_amount
			before_points_opponent = opponentDb['points']
			after_points_opponent = before_points_opponent + wager_amount
			await self.update_db(opponent, wager_amount)
			await self.update_db(self.player, -wager_amount)
		
		elif self.points == self.points2:
			final_result = "***Draw. No one lost and no one won anything.***"
			draw = True

		em = disnake.Embed(color=color.blue, title="Trivia has ended.", description=final_result)
		if draw == False:
			em.add_field(name=f"**-->** `{self.player.display_name}'s` total points before:", value=f"**{before_points_user}**", inline=True)
			em.add_field(name=f"`{self.player.display_name}'s` total points after:", value=f"**{after_points_user}**" , inline=False)
			em.add_field(name=f"**-->** `{opponent.display_name}'s` total points before:", value=f"**{before_points_opponent}**", inline=True)
			em.add_field(name=f"`{opponent.display_name}'s` total points after:", value=f"**{after_points_opponent}**", inline=False)

		return em

	async def start(self):
		mode = await self.get_mode()
		
		if mode == 'solo':
			em = await self.solo()
			await self.ctx.send(embed=em)
			return
		
		elif mode in ['comp', 'competitive']:
			try:
				em = await self.competitive()
				await self.ctx.send(embed=em)
			except:
				pass
			return