import random
import asyncio

class Fight:
	def __init__(self, pl1, pl2, ctx):
		self.p1 = pl1
		self.p2 = pl2
		self.ctx = ctx
		self.bot = ctx.bot
		self.p1_hp = 100
		self.p2_hp = 100
		self.started = False

	def fight(self, hp) -> list[int, int]:
		dmg = random.randint(1,50)
		return [dmg, hp-dmg]

	def health(self, hp) -> list[int, int]:
		healt = random.randint(1,35)
		return [healt, hp+healt]
	
	def update_health(self, affected_player, option, hp) -> int:
		if option == 'fight':
			new_hp = self.fight(hp)
			if affected_player == self.p1:
				self.p1_hp = new_hp[1]
			elif affected_player == self.p2:
				self.p2_hp = new_hp[1]
		elif option == 'health':
			new_hp = self.health(hp)
			if affected_player == self.p1:
				self.p1_hp = new_hp[1]
			elif affected_player == self.p2:
				self.p2_hp = new_hp[1]
		return new_hp

	def check_health(self) -> bool:
		if self.p2_hp <= 0:
			return True
		elif self.p1_hp <= 0:
			return True
		else:
			return False

	async def action(self, p):
		if p == self.p1:
			Player = self.p1
			PlayerHP =  self.p1_hp
			Opponent = self.p2
			OpponentHP = self.p2_hp
		elif p == self.p2:
			Player = self.p2
			PlayerHP = self.p2_hp
			Opponent = self.p1
			OpponentHP = self.p1_hp
		def check(m):
			return m.channel == self.ctx.channel and m.author == p
		if self.started == False:
			await self.ctx.send(f"{Player.mention} Please choose what you wish to do next from the following options:\n`fight`, `health`, `forfeit`")
		try:
			while True:
				response = await self.bot.wait_for('message', check=check, timeout=120)
				option = response.content.lower()
				if option == 'forfeit':
					raise Exception(f"**{Player.display_name}** has forfeited. {Opponent.mention} won!")
				elif option == 'fight':
					new_hp = self.update_health(Opponent, 'fight', OpponentHP)
					if self.check_health() == True:
						return
					return await self.ctx.send(f"**{Player.display_name}** chose `fight` and has dealt **{new_hp[0]}** damage.\n`{Opponent.display_name}`'s hp is now at **{new_hp[1]}**\n\n{Opponent.mention} Please choose what you wish to do next from the following options:\n`fight`, `health`, `forfeit`")
				elif option in ['health', 'hp']:
					new_hp = self.update_health(Player, 'health', PlayerHP)
					if self.check_health() == True:
						return
					return await self.ctx.send(f"**{Player.display_name}** chose `health` and has gotten an increase of **{new_hp[0]}** hp\n`{Player.display_name}`'s hp is now at **{new_hp[1]}**\n\n{Opponent.mention} Please choose what you wish to do next from the following options:\n`fight`, `health`, `forfeit`")
				else:
					await response.reply("Invalid option.")

		except asyncio.TimeoutError:
			raise Exception(f"The game has been canceled since {Player.mention} took too much to give an answer. {Opponent.mention}")

	async def start(self):
		while True:
			await self.action(self.p1)
			self.started = True
			if self.p2_hp <= 0:
				return await self.ctx.send(f"**{self.p1.display_name}** won the fight. {self.p2.mention} you lost!\n\nTotal HP left:\n\u2800• `{self.p1.display_name}` => **{self.p1_hp}**\n\u2800• `{self.p2.display_name}` => **{self.p2_hp}**")
			await self.action(self.p2)
			if self.p1_hp <= 0:
				return await self.ctx.send(f"**{self.p2.display_name}** won the fight. {self.p1.mention} you lost!\n\nTotal HP left:\n\u2800• `{self.p2.display_name}` => **{self.p2_hp}**\n\u2800• `{self.p1.display_name}` => **{self.p1_hp}**")