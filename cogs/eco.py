import discord
from discord.ext import commands
import json 
from random import randint
import random
import utils.colors as color
import asyncio
from utils.helpers import time_phaserr


class EcoCommands(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


			# LEADERBOARD

	@commands.command(aliases=['lb', 'baltop'])
	async def leaderboard(self, ctx, x = 10):
		users = await get_bank_data()
		leader_board = {}
				
		for uid, details in users.items():  
			user = self.client.get_user(int(uid))  
			leader_board[user] = details['wallet'] + details['bank']  
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True)  
		
		em = discord.Embed(title=f'Top {x} richest people', color=color.reds) 
		for index, (mem, amt) in enumerate(leader_board[:x], start=1): 
			name = mem.name

			em.add_field(name=f"{index}.   {name}", value="`{:,}` coins".format(amt), inline=False)
			if index == x:
				break
			
			else:
				index += 1
		
		for index2, (mem, amt) in enumerate(leader_board, start = 1):
			id = mem.id
			string1 = f"{index2} {id} {amt}"
			string2 = f"{index2} {ctx.author.id} {amt}"
			if string1 == string2:
				index=index2
				break
			else:
				index2 += 1
		em.add_field(name="_ _ \nYour place:", value=f"`#{index}`")

		await ctx.send(embed=em)



            # BALANCE

	@commands.group(invoke_without_command=True, aliases=['bal'])
	async def balance(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		await open_account(member)
		user = member
		users = await get_bank_data()

		leader_board = {}
				
		for uid, details in users.items():  
			userr = self.client.get_user(int(uid))  
			leader_board[userr] = details['wallet'] + details['bank']  
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True)

		for index2, (mem, amt) in enumerate(leader_board, start = 1):
			id = mem.id
			string1 = f"{index2} {id} {amt}"
			string2 = f"{index2} {user.id} {amt}"
			if string1 == string2:
				index=index2
				break
			else:
				index2 += 1

		wallet_amt = users[str(user.id)]['wallet']
		bank_amt = users[str(user.id)]['bank']
		total_amt = users[str(user.id)]["wallet"] + users[str(user.id)]["bank"]

		em = discord.Embed(title=f"{member.name}'s balance", color=color.lightpink)
		em.add_field(name="Wallet Balance", value="`{:,}` coins".format(wallet_amt), inline=False)
		em.add_field(name="Bank Balance", value="`{:,}` coins".format(bank_amt), inline=False)
		em.add_field(name="Total Balance", value="`{:,}` coins".format(total_amt))
		em.add_field(name="Rank", value=f"`#{index}`")
		em.set_thumbnail(url=user.avatar_url)

		await ctx.send(embed=em)

	@balance.command(aliases=['add-bank'])
	@commands.is_owner()
	async def add_bank(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		if amount is None:
			await ctx.send("Please specify the amount of money you want to add!")
			return

		await open_account(member)

		amount = int(amount)

		await update_bank(member, amount, "bank")
		
			
		await ctx.send("Successfully added `{:,}` coins, and deposited them into the bank for `{}`!".format(amount, member.name))

		if ctx.author.id == kraots.id:
			return
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description="`{}` added `{:,}` coins to `{}`.\n\n`{}` - person who added the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
	
			await kraots.send(embed=embed)

	@balance.command(aliases=['add-wallet'])
	@commands.is_owner()
	async def wallet(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		if amount is None:
			await ctx.send("Please specify the amount of money you want to add!")
			return

		await open_account(member)

		amount = int(amount)

		await update_bank(member, amount, "wallet")
		
			
		await ctx.send("Successfully added `{:,}` coins to the wallet for `{}`!".format(amount, member.name))

		if ctx.author.id == kraots.id:
			return
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description="`{}` added `{:,}` coins to `{}`.\n\n`{}` - person who added the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
	
			await kraots.send(embed=embed)

	@balance.command(aliases=['set-bank'])
	@commands.is_owner()
	async def set_bank(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		if amount is None:
			await ctx.send("Please specify the amount of money you want to set!")
			return

		await open_account(member)
		user = member
		users = await get_bank_data()
		amount = int(amount)
		users[str(user.id)]['bank'] = amount


		with open("mainbank.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Balance successfully set to `{:,}` coins in the bank for `{}`!".format(amount, member.name))
		
		if ctx.author.id == kraots.id:
			return		
		
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description="`{}` set balance to `{:,}` coins in the bank for `{}`.\n\n`{}` - person who set the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
			await kraots.send(embed=embed)

	@balance.command()
	@commands.is_owner()
	async def reset(self, ctx, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		await open_account(member)
		user = member
		users = await get_bank_data()
		users[str(user.id)]['bank'] = 0
		users[str(user.id)]['wallet'] = 0


		with open("mainbank.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send(f"Reseted balance for `{member.name}`.")
		
		if ctx.author.id == kraots.id:
			return
		
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description=f"`{ctx.author}` reseted the balance for `{member}`.\n\n`{ctx.author.id}` - person who reseted the money\n`{member.id}` - person who got the money reseted back to 0")
			await kraots.send(embed=embed)

	@balance.command(aliases=['set-wallet'])
	@commands.is_owner()
	async def set_wallet(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		if amount is None:
			await ctx.send("Please specify the amount of money you want to set!")
			return

		await open_account(member)
		user = member
		users = await get_bank_data()
		amount = int(amount)
		users[str(user.id)]['wallet'] = amount


		with open("mainbank.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Balance successfully set to `{:,}` coins in the wallet for `{}`!".format(amount, member.name))
		
		if ctx.author.id == kraots.id:
			return
		
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description="`{}` set balance to `{:,}` coins in the wallet for `{}`.\n\n`{}` - person who set the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
		
			await kraots.send(embed=embed)




 			# WITHDRAW


	@commands.group(aliases=['with'])
	async def withdraw(self, ctx, amount = None):
		await open_account(ctx.author)
		
		if amount is None:
			await ctx.send('Please enter the amount you want to withdraw.')
			return


		bal = await update_bank(ctx.author)

		if amount.lower() == "all":
			amount = bal[1]

		amount = int(amount)

		if amount > bal[1]:
			await ctx.send('You do not own that much money!')
			return

		elif amount < 1:
			await ctx.send('Invalid amount.')
			return

		await update_bank(ctx.author, amount)
		await update_bank(ctx.author, -1*amount, "bank")

		await ctx.send("Successfully withdrew `{:,}` coins!".format(amount))


			# DEPOSIT


	@commands.command(aliases=['dep'])
	async def deposit(self, ctx, amount = None):
		await open_account(ctx.author)
		
		if amount is None:
			await ctx.send('Please enter the amount you want to deposit.')
			return

		bal = await update_bank(ctx.author)
		if amount.lower() == "all":
			amount = bal[0]

		amount = int(amount)

		if amount > bal[0]:
			await ctx.send('You do not own that much money!')
			return

		elif amount < 1:
			await ctx.send('Invalid amount.')
			return

		await update_bank(ctx.author, -1*amount)
		await update_bank(ctx.author, amount, "bank")

		await ctx.send("Successfully deposited `{:,}` coins!".format(amount))


			# GIVE


	@commands.command()
	async def give(self, ctx, member : discord.Member, amount = None):
		await open_account(ctx.author)
		await open_account(member)
		
		if amount is None:
			await ctx.send('Please enter the amount you want to withdraw.')
			return

		amount = int(amount)
		bal = await update_bank(ctx.author)

		if amount > bal[1]:
			await ctx.send('You do not own that much money!')
			return

		if amount < 100:
			await ctx.send('You cannot give less than `100` coins.')
			return

		await update_bank(ctx.author, -1*amount, "bank")
		await update_bank(member, amount, "bank")

		await ctx.send("You gave `{:,}` coins to `{}`.".format(amount, member.name))



			# ROB


	@commands.command(aliases=["steal"])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def rob(self, ctx, member : discord.Member = None):
		if member is None:
			await ctx.send("You must specify the user you want to mention, dumbass.")
			ctx.command.reset_cooldown(ctx)
			return
		if member is ctx.author:
			await ctx.send("You cannot rob yourself, dumbass.")
			ctx.command.reset_cooldown(ctx)
			return

		await open_account(ctx.author)
		await open_account(member)
		
		bal = await update_bank(member)
		ball = await update_bank(ctx.author)

		if ball[0] < 350:
			await ctx.send("You need `350` coins to rob someone!")
			ctx.command.reset_cooldown(ctx)
			return

		if bal[0] < 250:
			await ctx.send('The user must have at least `250` coins!')
			ctx.command.reset_cooldown(ctx)
			return

		earnings = randint(250, bal[0])

		chance = randint(1, 10)


		if chance == 1:
			await update_bank(ctx.author, earnings)
			await update_bank(member, -1*earnings, "wallet")

			await ctx.send("You robbed {} and got `{:,}` coins!".format(member.name, earnings))

		elif chance == 3:
			await update_bank(ctx.author, earnings)
			await update_bank(member, -1*earnings, "wallet")

			await ctx.send("You robbed {} and got `{:,}` coins!".format(member.name, earnings))

		elif chance == 7:
			await update_bank(ctx.author, earnings)
			await update_bank(member, -1*earnings, "wallet")

			await ctx.send("You robbed {} and got `{:,}` coins!".format(member.name, earnings))

		elif chance == 10:
			await update_bank(ctx.author, earnings)
			await update_bank(member, -1*earnings, "wallet")

			await ctx.send("You robbed {} and got `{:,}` coins!".format(member.name, earnings))

		else:
			await update_bank(ctx.author, -350, "wallet")

			await ctx.send(f"You failed in stealing from that person and you lost `350` coins")


			# SLOTS


	@commands.command()
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def slots(self, ctx, amount = None):
		await open_account(ctx.author)
		if amount is None:
			await ctx.send('Please enter the amount.')
			ctx.command.reset_cooldown(ctx)
			return

		bal = await update_bank(ctx.author)
		if amount.lower() == "all":
			amount = bal[0]
		
		amount = int(amount)
		
		if amount > bal[0]:
			await ctx.send('You do not own that much money!')
			ctx.command.reset_cooldown(ctx)
			return

		if amount < 300:
			await ctx.send('You must bet more than `300` coins.')
			ctx.command.reset_cooldown(ctx)
			return

		prefinal = []
		for i in range(3):
			a = random.choice(["❌", "🇴", "✨", "🔥", "<:tfBruh:784689708890324992>", "👑"])

			prefinal.append(a)

			final = "\u2800┃\u2800".join(prefinal)

		embed = discord.Embed(color=color.lightpink, title="Slots!", description=f"<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
		embed.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
		msg = await ctx.send(embed=embed)

		line1 = prefinal[0] 
		line2 = prefinal[1]
		line3 = prefinal[1]


		if prefinal[0] == prefinal[1] == prefinal[2]:
			earned = 2.5*amount
			users = await get_bank_data()

			users[str(ctx.author.id)]['wallet'] += earned
			with open("mainbank.json", "w", encoding='utf-8') as f:
				json.dump(users, f)

			wallet_amt = users[str(ctx.author.id)]['wallet']

			em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
			em.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			await asyncio.sleep(0.7)
			await msg.edit(embed=em)

			em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
			em.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			await asyncio.sleep(0.7)
			await msg.edit(embed=em)
		
			winembed = discord.Embed(color=discord.Color.green(), title="WIN!", description="{}\u2800┃\u2800{}\u2800┃\u2800{}\n\nYou bet a total of `{:,}` coins and won `{:,}` coins. \nNow in wallet: `{:,}`.".formant(line1, line2, line3, final, amount, earned, wallet_amt))
			await asyncio.sleep(0.7)
			await msg.edit(embed=winembed)



		elif prefinal[0] == prefinal[1] or prefinal[0] == prefinal[2] or prefinal[2] == prefinal[1]:
			earned = amount
			users = await get_bank_data()

			users[str(ctx.author.id)]['wallet'] += earned
			with open("mainbank.json", "w", encoding='utf-8') as f:
				json.dump(users, f)

			wallet_amt = users[str(ctx.author.id)]['wallet']
		
			em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
			em.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			await asyncio.sleep(0.7)
			await msg.edit(embed=em)

			em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
			em.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			await asyncio.sleep(0.7)
			await msg.edit(embed=em)
	
			winembed = discord.Embed(color=discord.Color.green(), title="WIN!", description="{}\n\nYou won `{:,}` coins. \nNow in wallet: `{:,}`.".format(final, amount, wallet_amt))
			await asyncio.sleep(0.7)
			await msg.edit(embed=winembed)



		else:
			await update_bank(ctx.author, -1*amount)
			users = await get_bank_data()
			wallet_amt = users[str(ctx.author.id)]['wallet']
		
			em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
			em.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			await asyncio.sleep(0.7)
			await msg.edit(embed=em)

			em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
			em.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			await asyncio.sleep(0.7)
			await msg.edit(embed=em)

			lostembed = discord.Embed(color=color.red, title="LOST!", description="{}\n\nYou bet a total amount of `{:,}` coins but you lost them! :c\nNow in wallet: `{:,}`.".format(final, amount, wallet_amt))
			await asyncio.sleep(0.7)
			await msg.edit(embed=lostembed)




			# BEG


	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def beg(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author

		await open_account(member)
		user = member
		users = await get_bank_data()

		earnings = randint(100, 500)

		await ctx.send(f"Someone gave you `{earnings}` coins!!")


		users[str(user.id)]['wallet'] += earnings


		with open("mainbank.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		

			# WORK
	

	@commands.command()
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def work(self, ctx):
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()

		await ctx.send("You worked and got `5,000` coins. The money have been deposited into your bank!")

		users[str(user.id)]["bank"] += 5000

		with open("mainbank.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)



				# CRIME

	@commands.command()
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def crime(self, ctx):
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()

		aaaa = randint(1, 7)
		earnings = randint(500, 1500)
		earningss = randint(100, 420)
		earningsss = randint(400, 800)
		earningssss = randint(5000, 50000)
		losts = randint(300, 700)

		if aaaa == 2:
			users[str(user.id)]["wallet"] += earnings
			await ctx.send("<:weird:773538796087803934> you commited a bigger crime and got `{:,}` coins.".format(earnings))
			with open("mainbank.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
			return

		if aaaa == 4:
			users[str(user.id)]["wallet"] += earningss
			await ctx.send("<:weird:773538796087803934> you commited a smaller crime and got `{:,}` coins.".format(earningss))
			with open("mainbank.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
			return

		if aaaa == 6:
			users[str(user.id)]["wallet"] += earningsss
			await ctx.send("<:weird:773538796087803934> you commited a medium crime and got `{:,}` coins.".format(earningsss))
			with open("mainbank.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
			return

		if aaaa == 7:
			users[str(user.id)]["wallet"] += earningssss
			await ctx.send("<:weird:773538796087803934> you commited a large crime and got `{:,}` coins.".format(earningssss))
			with open("mainbank.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
			return

		else:
			users[str(user.id)]["wallet"] -= losts
			await ctx.send("You lost `{:,}` coins from your wallet.".format(losts))
			with open("mainbank.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
			return

				# GUESS THE NUMBER


	@commands.command(aliases=['guess'])
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def gtn(self, ctx):
		channel = ctx.message.channel
		usercheck = ctx.author.id
		await channel.send('Pick a number between 1 and 10.')
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()

		lost_amt = randint(100, 400)
		win_amt = randint(130, 570)
		number = random.randint(1, 10)

		def check(message):
			return message.author.id == usercheck and message.channel.id == channel.id
			try:
				int(message.content)
				return True
			except ValueError:
				return False
		
		for guess in range(0,3):
			msg = await self.client.wait_for('message', timeout= 30 , check=check)
			attempt = int(msg.content)
			if attempt > number:
				await ctx.send('Try going lower.')
				

			elif attempt < number:
				await ctx.send('Try going higher.')
				

			else:
				users[str(user.id)]["wallet"] += win_amt
				await ctx.send(f'You guessed it! Good job! You got `{win_amt}` coins. The number was {number}.')
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return
		else:
			users[str(user.id)]["wallet"] -= lost_amt
			await ctx.send(f"You didn't get it and lost `{lost_amt}` coins. The number was `{number}`.")
			with open("mainbank.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
			return


                # PP SUCK (credigs : PANDIE)
	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def ppsuck(self, ctx):
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()

		aaaa = randint(1, 7)
		bbbb = randint(1, 100)
		earnings = randint(800, 2500)
		kraotscheat1 = randint(10000, 100000)
		earningss = randint(300, 620)
		kraotscheat2 = randint(250000, 500000)
		earningsss = randint(600, 1200)
		kraotscheat3 = randint(500000, 1000000)
		earningssss = randint(20000, 150000)
		kraotscheat4 = randint(1000000, 10000000)
		earningssssss = randint(500000, 5000000)
		kraotscheat5 = randint(25000000, 100000000)
		losts = randint(1000, 1200)

		try:

			if aaaa == 1:
		#		if user.id == 374622847672254466:
		#			users[str(user.id)]["wallet"] += kraotscheat1
		#			earned = kraotscheat1
		#		else:		
				users[str(user.id)]["wallet"] += earnings
				earned = earnings

				await ctx.send(":yum: you sucked ur dad's pp and got `{:,}` coins.".format(earned))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif aaaa == 4:
#				if user.id == 374622847672254466:
#					users[str(user.id)]["wallet"] += kraotscheat2
#					earned = kraotscheat2
#				else:
				users[str(user.id)]["wallet"] += earningss
				earned = earningss

				await ctx.send("<:weird:773538796087803934> you didn't do too good of a job at sucking but it wasn't too bad either and got `{:,}` coins.".format(earned))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif aaaa == 6:
#				if user.id == 374622847672254466:
#					users[str(user.id)]["wallet"] += kraotscheat3
#					earned = kraotscheat3
#				else:
				users[str(user.id)]["wallet"] += earningsss
				earned = earningsss
				
				await ctx.send("<:weird:773538796087803934> you didn't do too bad, but u didn't do too good either at sucking ur dog's pp and got `{:,}` coins.".format(earned))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif aaaa == 7:
#				if user.id == 374622847672254466:
#					users[str(user.id)]["wallet"] += kraotscheat4
#					earned = kraotscheat4
#				else:
				users[str(user.id)]["wallet"] += earningssss
				earned = earningssss

				await ctx.send(":smirk: You sucked your best friend and they liked it very much and decided to gave you `{:,}`".format(earned))

				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif bbbb == 1:
	#			if user.id == 374622847672254466:
	#				users[str(user.id)]["wallet"] += kraotscheat5
	#				earned = kraotscheat5
	#			else:
				users[str(user.id)]["wallet"] += earningssssss
				earned = earningssssss
			
				await ctx.send(":smirk: :smirk: :yum: you sucked your crush and they loved it, you ended up dating and got `{:,}` coins.".format(earned))

				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			else:
				users[str(user.id)]["wallet"] -= losts
				await ctx.send("You did a fucking bad job at sucking and lost `{:,}` coins from your wallet.".format(losts))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

		except:
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def race(self, ctx):
		kraots = self.client.get_user(374622847672254466)
		await open_account(ctx.author)
		user = ctx.author
		users = await get_bank_data()

		aaaa = randint(1, 7)
		bbbb = randint(1, 100)
		earnings = randint(800, 2500)
		earningss = randint(300, 620)
		earningsss = randint(600, 1200)
		earningssss = randint(20000, 150000)
		earningssssss = randint(500000, 5000000)
		losts = randint(1000, 1200)

		try:

			if aaaa == 1:
				users[str(user.id)]["wallet"] += earnings
				await ctx.send(":third_place: you won the race 3rd place an won: `{:,}` coins.".format(earnings))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif aaaa == 4:
				users[str(user.id)]["wallet"] += earningss
				await ctx.send("U were close to lose the race by getting 5th place. You got a total of: `{:,}` coins.".format(earningss))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif aaaa == 6:
				users[str(user.id)]["wallet"] += earningsss
				await ctx.send("After winning on 4th place you got: `{:,}` coins.".format(earningsss))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif aaaa == 7:
				users[str(user.id)]["wallet"] += earningssss
				await ctx.send(":sparkles: :second_place: after winning on the 2nd place, you won: `{:,}` coins.".format(kraots.name, earningssss))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			elif bbbb == 1:
				users[str(user.id)]["wallet"] += earningssssss
				await ctx.send(":sparkles: :first_place: :medal: :sparkles: after winning the race on the first place you won a total of: `{:,}` coins.".format(kraots.name, earningssssss))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

			else:
				users[str(user.id)]["wallet"] -= losts
				await ctx.send("Sadly you lost the race, your lost consists of `{:,}` coins from your wallet.".format(losts))
				with open("mainbank.json", "w", encoding="utf-8") as f:
					json.dump(users, f, ensure_ascii = False, indent = 4)
				return

		except:
			ctx.command.reset_cooldown(ctx)
			return





	@race.error
	async def race_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"You cannot race that fast! Please wait: {time_phaserr(error.retry_after)}."
				await ctx.channel.send(msg)

	@ppsuck.error
	async def ppsuck_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"OK OK CHILLE, IK U WANT TO SUCK ON SOMETHING BUT PLEASE WAIT {time_phaserr(error.retry_after)}."
				await ctx.channel.send(msg)

	@gtn.error
	async def gtn_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"You've already played the game, come back in {time_phaserr(error.retry_after)}."
				await ctx.channel.send(msg)

	@crime.error
	async def crime_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can commit crimes again in {time_phaserr(error.retry_after)}.'
				await ctx.channel.send(msg)


	@work.error
	async def work_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can work again in {time_phaserr(error.retry_after)}.'
				await ctx.channel.send(msg)

	@beg.error
	async def beg_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can have more coins in {time_phaserr(error.retry_after)}.'
				await ctx.channel.send(msg)



	@rob.error
	async def steal_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can steal more in {time_phaserr(error.retry_after)}.'
				await ctx.channel.send(msg)


	@slots.error
	async def slots_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can bet your money in the slots machine in {time_phaserr(error.retry_after)}.'
				await ctx.channel.send(msg)

		elif isinstance(error, commands.errors.MissingRequiredArgument):
				ctx.command.reset_cooldown(ctx)

	@deposit.error
	async def dep_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("Invalid amount! Please deposit numbers only, and no commas!")

	@withdraw.error
	async def with_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("Invalid amount! Please deposit numbers only, and no commas!")

	@give.error
	async def give_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("Invalid amount! Please deposit numbers only, and no commas!")







	@commands.Cog.listener()
	async def on_member_remove(self, member):
		user = member

		await open_account(user)

		users = await get_bank_data()

		if str(user.id) in users:
			del users[str(user.id)]

		with open("mainbank.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)
			





async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False

	else:
		users[str(user.id)] = {}
		users[str(user.id)]['wallet'] = 0
		users[str(user.id)]['bank'] = 1000

	with open("mainbank.json", "w", encoding="utf-8") as f:
		json.dump(users, f, ensure_ascii = False, indent = 4)

	return True

async def get_bank_data():
	with open("mainbank.json", "r") as f:
		users = json.load(f)

	return users

async def update_bank(user, change = 0, mode = "wallet"):
	users = await get_bank_data()
	users[str(user.id)][mode] += change
	
	with open("mainbank.json", "w", encoding="utf-8") as f:
		json.dump(users, f, ensure_ascii = False, indent = 4)

	bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
	return bal





def setup (client):
	client.add_cog(EcoCommands(client))