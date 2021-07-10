import asyncio
import random
from discord import player
import motor.motor_asyncio
import os
import discord

DBKEY = os.getenv('MONGODBKEY')

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
ecoDb = cluster['ViHillCornerDB']['Economy']

class TicTacToe:
	def __init__(self, pl1, pl2, ctx, bot):
		self.player1 = pl1
		self.player2 = pl2
		self.ctx = ctx
		self.bot = bot
		self.turns = 0
		self.board = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']
	
	def choose_starter(self):
		choosePlayer = random.choice([1, 2])
		if choosePlayer == 1:
			self.starter = self.player1
		elif choosePlayer == 2:
			self.starter = self.player2
		return self.starter
	
	def check_win(self):
		if self.board[0] == self.board[1] == self.board[2]: # Check 1-3
			return True
		elif self.board[3] == self.board[4] == self.board[5]: # Check 4-6
			return True
		elif self.board[6] == self.board[7] == self.board[8]: # Check 7-9
			return True
		elif self.board[0] == self.board[3] == self.board[6]: # Check 1-7
			return True
		elif self.board[1] == self.board[4] == self.board[7]: # Check 2-8
			return True
		elif self.board[2] == self.board[5] == self.board[8]: # Check 3-9
			return True
		elif self.board[0] == self.board[4] == self.board[8]: # Check 1-9
			return True
		elif self.board[2] == self.board[4] == self.board[6]: # Check 3-7
			return True
		else:
			return False
	
	async def get_move(self, pl):
		if pl == self.player1:
			sign = ':x:'
			Player = self.player1
			Opponent = self.player2
		elif pl == self.player2:
			sign = ':o:'
			Player = self.player2
			Opponent = self.player1
		self.turns += 1
		em = discord.Embed(description=f"{self.board[0]} {self.board[1]} {self.board[2]}\n{self.board[3]} {self.board[4]} {self.board[5]}\n{self.board[6]} {self.board[7]} {self.board[8]}")
		await self.ctx.send(f'{pl.mention} make your move, {sign}\n', embed=em)
		def check(m):
			return m.channel == self.ctx.channel and m.author == pl
		try:
			while True:
				answer = await self.bot.wait_for('message', check=check, timeout=180)
				try:
					self.answer = int(answer.content)
				except:
					if str(answer.content).lower() in ['forfeit', 'cancel']:
						await ecoDb.update_one({'_id': Opponent.id}, {'$inc':{'wallet': 10000}})
						await ecoDb.update_one({'_id': Player.id}, {'$inc':{'wallet': -10000}})
						raise Exception(f"**{Player.display_name}** Has forfeit.\n\n{Opponent.mention} Won **10,000** <:carrots:822122757654577183>!\n{Player.mention} Lost **10,000** <:carrots:822122757654577183>!")
					await answer.reply(content='Must be a number between **1-9**')
				else:
					if 0 >= self.answer or self.answer >= 10:
						await answer.reply(content='Must be a number between **1-9**')
					else:
						if self.board[self.answer - 1] not in [':o:', ':x:']:
							self.board[self.answer -1] = sign
							break
						else:
							await self.ctx.send("That place is already taken.")

		except asyncio.TimeoutError:
			raise Exception(f"The game has been canceled since {Player.mention} took too much to give an answer. {Opponent.mention}")

				

	async def start(self):
		self.choose_starter()
		
		if self.starter == self.player1:
			player = self.player1
			opponent = self.player2
		elif self.starter == self.player2:
			player = self.player2
			opponent = self.player1
		
		while True:
			await self.get_move(player)
			em = discord.Embed(description=f"{self.board[0]} {self.board[1]} {self.board[2]}\n{self.board[3]} {self.board[4]} {self.board[5]}\n{self.board[6]} {self.board[7]} {self.board[8]}")
			if self.check_win() == True:
				await ecoDb.update_one({'_id': player.id}, {'$inc':{'wallet': 10000}})
				await ecoDb.update_one({'_id': opponent.id}, {'$inc':{'wallet': -10000}})
				await self.ctx.send(f"{player.mention} Won **10,000** <:carrots:822122757654577183>!\n{opponent.mention} Lost **10,000** <:carrots:822122757654577183>!\n\n", embed=em)
				return
			elif self.turns == 9:
				await self.ctx.send(f"It's a draw. {player.mention} {opponent.mention}\n", embed=em)
				return
			
			await self.get_move(opponent)
			em = discord.Embed(description=f"{self.board[0]} {self.board[1]} {self.board[2]}\n{self.board[3]} {self.board[4]} {self.board[5]}\n{self.board[6]} {self.board[7]} {self.board[8]}")
			if self.check_win() == True:
				await ecoDb.update_one({'_id': opponent.id}, {'$inc':{'wallet': 10000}})
				await ecoDb.update_one({'_id': player.id}, {'$inc':{'wallet': -10000}})
				await self.ctx.send(f"{opponent.mention} Won **10,000** <:carrots:822122757654577183>!\n{player.mention} Lost **10,000** <:carrots:822122757654577183>!\n\n", embed=em)
				return
			elif self.turns == 9:
				await self.ctx.send(f"It's a draw. {player.mention} {opponent.mention}\n", embed=em)
				return