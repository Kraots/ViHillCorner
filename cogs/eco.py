import discord
from discord.ext import commands
from random import randint
import random
import utils.colors as color
import asyncio
from utils.helpers import time_phaserr
import pymongo
from pymongo import MongoClient
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Economy"]

class EcoCommands(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


			# REGISTER

	@commands.command()
	async def register(self, ctx):
		user = ctx.author

		post = {"_id": user.id, "wallet": 0, "bank": 0}

		try:
			collection.insert_one(post)
			await ctx.send("Succesfully registered!")

		except pymongo.errors.DuplicateKeyError:
			await ctx.send("You are already registered!")
	

			# UNREGISTER


	@commands.command()
	async def unregister(self, ctx):
		user = ctx.author
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if user.id in all_users:
			collection.delete_one({"_id": user.id})
			await ctx.send("Succesfully unregistered!")
        
		else:
			await ctx.send("You are not registered! Type: `!regiser` to register.")
		  
		  
		    # BALANCE



	@commands.group(invoke_without_command=True, aliases=['bal'])
	async def balance(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		user = member
		
		results = collection.find({"_id": user.id})
		all_accounts = collection.find({})

		leader_board = {}

		for all_results in all_accounts:
			userr = self.client.get_user(all_results["_id"])
			all_wallet_amt = all_results["wallet"]
			all_bank_amt = all_results["bank"]
			leader_board[userr] = all_wallet_amt + all_bank_amt

		for result in results:
			wallet_amt = result["wallet"]
			bank_amt = result["bank"]

		try:
			total_amt = wallet_amt + bank_amt

		except UnboundLocalError:
			if member.id == ctx.author.id:
				await ctx.send("You are not registered! Type: `!register` to register.")
			else:
				await ctx.send("User is not registered!")
			return

		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True)

		for index2, (mem, amt) in enumerate(leader_board, start = 1):
			try:
				list_id = mem.id
			except:
				pass
			
			string1 = f"{index2} {list_id}"
			string2 = f"{index2} {user.id}"
			if string1 == string2:
				index=index2
				break
			else:
				index2 += 1	


		em = discord.Embed(title=f"{member.name}'s balance", color=color.lightpink)
		em.add_field(name="Wallet Balance", value="`{:,}` coins".format(wallet_amt), inline=False)
		em.add_field(name="Bank Balance", value="`{:,}` coins".format(bank_amt), inline=False)
		em.add_field(name="Total Balance", value="`{:,}` coins".format(total_amt))
		em.add_field(name="Rank", value="`#{}`".format(index))
		em.set_thumbnail(url=user.avatar_url)

		await ctx.reply(embed=em)

			# LEADERBOARD

	@commands.command(aliases=['lb', 'baltop'])
	async def leaderboard(self, ctx, x = 10):
		results = collection.find({})
		leader_board = {}

		all_users = []

		for result in results:
			user = self.client.get_user(result["_id"])  
			leader_board[user] = result["wallet"] + result["bank"]  
			all_users.append(result['_id'])
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True)  
		
		em = discord.Embed(title=f'Top {x} richest people', color=color.reds) 
		
		for index, (mem, amt) in enumerate(leader_board[:x], start=1): 
			
			name = mem.name

			em.add_field(name=f"{index}.   {name}", value="`{:,}` coins".format(amt), inline=False)
			if index == x:
				break
			
			else:
				index += 1
		if ctx.author.id in all_users:
			for index2, (mem, amt) in enumerate(leader_board, start = 1):
				try:
					id = mem.id
				except:
					pass
				string1 = f"{index2} {id} {amt}"
				string2 = f"{index2} {ctx.author.id} {amt}"
				if string1 == string2:
					index=index2
					break
				else:
					index2 += 1
			em.add_field(name="_ _ \nYour place:", value=f"`#{index}`")
			
		await ctx.reply(embed=em)


	@balance.command(aliases=['add-bank'])
	@commands.is_owner()
	async def add_bank(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if member.id in all_users:

			if amount is None:
				await ctx.send("Please specify the amount of money you want to add!")
				return

			user = member

			amount = amount.replace(",", "")

			amount = int(amount)

			collection.update_one({"_id": user.id}, {"$inc":{"bank": amount}})
			
				
			await ctx.send("Successfully added `{:,}` coins, and deposited them into the bank for `{}`!".format(amount, member))

			if ctx.author.id == kraots.id:
				return
			else:
				embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description="`{}` added `{:,}` coins to `{}`.\n\n`{}` - person who added the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
		
				await kraots.send(embed=embed)

		else:
			await ctx.send("User not registered!")
			return

	@balance.command(aliases=['add-wallet'])
	@commands.is_owner()
	async def add_wallet(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if member.id in all_users:

			if amount is None:
				await ctx.send("Please specify the amount of money you want to add!")
				return

			user = member

			amount = amount.replace(",", "")

			amount = int(amount)

			collection.update_one({"_id": user.id}, {"$inc":{"wallet": amount}})
			
				
			await ctx.send("Successfully added `{:,}` coins to the wallet for `{}`!".format(amount, member))

			if ctx.author.id == kraots.id:
				return
			else:
				embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description="`{}` added `{:,}` coins to `{}`.\n\n`{}` - person who added the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
		
				await kraots.send(embed=embed)

		else:
			await ctx.send("User not registered!")
			return

	@balance.command(aliases=['set-bank'])
	@commands.is_owner()
	async def set_bank(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if member.id in all_users:
			if amount is None:
				await ctx.send("Please specify the amount of money you want to set!")
				return

			user = member
			amount = amount.replace(",", "")
			amount = int(amount)


			collection.update_one({"_id": user.id}, {"$set":{"bank": amount}})

			await ctx.send("Balance successfully set to `{:,}` coins in the bank for `{}`!".format(amount, member))
			
			if ctx.author.id == kraots.id:
				return		
			
			else:
				embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description="`{}` set balance to `{:,}` coins in the bank for `{}`.\n\n`{}` - person who set the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
				await kraots.send(embed=embed)
		
		else:
			await ctx.send("User not registered!")
			return

	@balance.command()
	@commands.is_owner()
	async def reset(self, ctx, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if member.id in all_users:

			user = member

			collection.update_one({"_id": user.id}, {"$set":{"wallet": 0}})
			collection.update_one({"_id": user.id}, {"$set":{"bank": 0}})

			await ctx.send(f"Reseted balance for `{member}`.")
			
			if ctx.author.id == kraots.id:
				return
		
			else:
				embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description=f"`{ctx.author}` reseted the balance for `{member}`.\n\n`{ctx.author.id}` - person who reseted the money\n`{member.id}` - person who got the money reseted back to 0")
				await kraots.send(embed=embed)
		
		else:
			await ctx.send("User not registered!")
			return

	@balance.command(aliases=['set-wallet'])
	@commands.is_owner()
	async def set_wallet(self, ctx, amount = None, member: discord.Member = None):

		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if member.id in all_users:
			if amount is None:
				await ctx.send("Please specify the amount of money you want to set!")
				return

			user = member
			
			amount = amount.replace(",", "")
			amount = int(amount)

			collection.update_one({"_id": user.id}, {"$set":{"wallet": amount}})

			await ctx.send("Balance successfully set to `{:,}` coins in the wallet for `{}`!".format(amount, member))
			
			if ctx.author.id == kraots.id:
				return
			
			else:
				embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description="`{}` set balance to `{:,}` coins in the wallet for `{}`.\n\n`{}` - person who set the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
			
				await kraots.send(embed=embed)

		else:
			await ctx.send("User not registered!")
			return



 			# WITHDRAW


	@commands.group(aliases=['with'])
	async def withdraw(self, ctx, amount = None):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
		
			if amount is None:
				await ctx.send('Please enter the amount you want to withdraw.')
				return

			results = collection.find({"_id": ctx.author.id})

			for result in results:
				bal = result["bank"]

			if amount.lower() == "all":
				amount = bal

			try:
				amount = amount.replace(",", "")
			except:
				pass
			amount = int(amount)

			if amount > bal:
				await ctx.send('You do not own that much money!')
				return

			elif amount < 1:
				await ctx.send('Invalid amount.')
				return

			collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": amount}})
			collection.update_one({"_id": ctx.author.id}, {"$inc":{"bank": -amount}})

			await ctx.send("Successfully withdrew `{:,}` coins!".format(amount))

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# DEPOSIT


	@commands.command(aliases=['dep'])
	async def deposit(self, ctx, amount = None):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
		
			if amount is None:
				await ctx.send('Please enter the amount you want to deposit.')
				return
		
			results = collection.find({"_id": ctx.author.id})

			for result in results:
				bal = result["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			amount = int(amount)

			if amount > bal:
				await ctx.send('You do not own that much money!')
				return

			elif amount < 1:
				await ctx.send('Invalid amount.')
				return

			collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -amount}})
			collection.update_one({"_id": ctx.author.id}, {"$inc":{"bank": amount}})

			await ctx.send("Successfully deposited `{:,}` coins!".format(amount))

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# GIVE


	@commands.command()
	async def give(self, ctx, member : discord.Member, amount = None):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
			user = member
			author = ctx.author
			
			if amount is None:
				await ctx.send('Please enter the amount you want to withdraw.')
				return
			
			results = collection.find({"_id": author.id})

			for result in results:
				bal = result["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			amount = int(amount)

			if amount > bal:
				await ctx.send('You do not own that much money!')
				return

			if amount < 100:
				await ctx.send('You cannot give less than `100` coins.')
				return

			collection.update_one({"_id": author.id}, {"$inc":{"wallet": -amount}})
			collection.update_one({"_id": user.id}, {"$inc":{"wallet": amount}})

			await ctx.send("You gave `{:,}` coins to `{}`.".format(amount, member.name))

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return
			

			# ROB


	@commands.command(aliases=["steal"])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def rob(self, ctx, member : discord.Member = None):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
			if member is None:
				await ctx.send("You must specify the user you want to mention, dumbass.")
				ctx.command.reset_cooldown(ctx)
				return
			if member is ctx.author:
				await ctx.send("You cannot rob yourself, dumbass.")
				ctx.command.reset_cooldown(ctx)
				return

			user = member
			author = ctx.author
			
			get_user_bal = collection.find({"_id": user.id})
			get_author_bal = collection.find({"_id": author.id})

			for result in get_user_bal:
				user_bal = result["wallet"]

			for result in get_author_bal:
				author_bal = result["wallet"]

			if author_bal < 350:
				await ctx.send("You need `350` coins to rob someone!")
				ctx.command.reset_cooldown(ctx)
				return

			if user_bal < 250:
				await ctx.send('The user must have at least `250` coins!')
				ctx.command.reset_cooldown(ctx)
				return

			earnings = randint(250, user_bal)

			chance = randint(1, 10)


			if chance == 1:
				collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got `{:,}` coins!".format(member.display_name, earnings))

			elif chance == 3:
				collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got `{:,}` coins!".format(member.display_name, earnings))

			elif chance == 7:
				collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got `{:,}` coins!".format(member.display_name, earnings))

			elif chance == 10:
				collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got `{:,}` coins!".format(member.display_name, earnings))

			else:
				collection.update_one({"_id": author.id}, {"$inc":{"wallet": -350}})

				await ctx.send(f"You failed in stealing from that person and you lost `350` coins")

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# SLOTS


	@commands.command()
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def slots(self, ctx, amount = None):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
			if amount is None:
				await ctx.reply('Please enter the amount.')
				ctx.command.reset_cooldown(ctx)
				return

			results = collection.find({"_id": ctx.author.id})
			
			for result in results:
				bal = result["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			amount = int(amount)

			if amount > bal:
				await ctx.reply('You do not own that much money!')
				ctx.command.reset_cooldown(ctx)
				return

			if amount < 300:
				await ctx.reply('You must bet more than `300` coins.')
				ctx.command.reset_cooldown(ctx)
				return

			prefinal = []
			for i in range(3):
				a = random.choice(["❌", "🇴", "✨", "🔥", "<:tfBruh:784689708890324992>", "👑"])

				prefinal.append(a)

				final = "\u2800┃\u2800".join(prefinal)

			embed = discord.Embed(color=color.lightpink, title="Slots!", description=f"<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
			embed.set_footer(text= "If it gliches then you won with 3rd in a row, if it does happen we apologize for the inconvenience")
			msg = await ctx.reply(embed=embed)

			line1 = prefinal[0] 
			line2 = prefinal[1]
			line3 = prefinal[2]



			if prefinal[0] == prefinal[1] == prefinal[2]:
				earned = 2.5*amount

				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

				wallet_amt = bal + earned

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

				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

				wallet_amt = bal + earned

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

				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -amount}})
				
				wallet_amt = bal - amount
			
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

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return



			# BEG


	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def beg(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
			earnings = randint(100, 500)

			await ctx.send(f"Someone gave you `{earnings}` coins!!")

			collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# WORK
	

	@commands.command()
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def work(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:

			await ctx.send("You worked and got `5,000` coins. The money have been deposited into your bank!")

			collection.update_one({"_id": ctx.author.id}, {"$inc":{"bank": 5000}})
		
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return


				# CRIME

	@commands.command()
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def crime(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:

			aaaa = randint(1, 7)
			earnings = randint(500, 1500)
			earningss = randint(100, 420)
			earningsss = randint(400, 800)
			earningssss = randint(5000, 50000)
			losts = randint(300, 700)

			if aaaa == 2:
				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})

				await ctx.send("<:weird:773538796087803934> you commited a bigger crime and got `{:,}` coins.".format(earnings))
				return

			if aaaa == 4:
				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningss}})
				await ctx.send("<:weird:773538796087803934> you commited a smaller crime and got `{:,}` coins.".format(earningss))
				return

			if aaaa == 6:
				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningsss}})
				await ctx.send("<:weird:773538796087803934> you commited a medium crime and got `{:,}` coins.".format(earningsss))
				return

			if aaaa == 7:
				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssss}})
				await ctx.send("<:weird:773538796087803934> you commited a large crime and got `{:,}` coins.".format(earningssss))
				return

			else:
				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
				await ctx.send("You lost `{:,}` coins from your wallet.".format(losts))
				return
		
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

				# GUESS THE NUMBER


	@commands.command(aliases=['guess'])
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def gtn(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
			usercheck = ctx.author.id
			await ctx.send('Pick a number between 1 and 10.')

			lost_amt = randint(100, 400)
			win_amt = randint(130, 570)
			number = random.randint(1, 10)

			def check(message):
				return message.author.id == usercheck and message.channel.id == ctx.channel.id
				try:
					int(message.content)
					return True
				except ValueError:
					return False
			
			for guess in range(0,3):
				msg = await self.client.wait_for('message', timeout= 30 , check=check)
				attempt = int(msg.content)
				if attempt > number:
					await msg.reply('Try going lower.')
					

				elif attempt < number:
					await msg.reply('Try going higher.')
					

				else:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": win_amt}})
					await ctx.send(f'You guessed it! Good job! You got `{win_amt}` coins. The number was {number}.')
					return
			else:
				collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -lost_amt}})
				await ctx.send(f"You didn't get it and lost `{lost_amt}` coins. The number was `{number}`.")
				return
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return


                # PP SUCK (credigs : PANDIE)
	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def ppsuck(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
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
					if ctx.author.id == 374622847672254466:
						earned = kraotscheat1
					else:
						earned = earnings
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

					await ctx.send(":yum: you sucked ur dad's pp and got `{:,}` coins.".format(earned))
					return

				elif aaaa == 4:
					if ctx.author.id == 374622847672254466:
						earned = kraotscheat2
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					else:
						earned = earningss
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

					await ctx.send("<:weird:773538796087803934> you didn't do too good of a job at sucking but it wasn't too bad either and got `{:,}` coins.".format(earned))
					return

				elif aaaa == 6:
					if ctx.author.id == 374622847672254466:
						earned = kraotscheat3
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					else:
						earned = earningsss
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					
					await ctx.send("<:weird:773538796087803934> you didn't do too bad, but u didn't do too good either at sucking ur dog's pp and got `{:,}` coins.".format(earned))
					return

				elif aaaa == 7:
					if ctx.author.id == 374622847672254466:
						earned = kraotscheat4
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					else:
						earned = earningssss
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

					await ctx.send(":smirk: You sucked your best friend and they liked it very much and decided to gave you `{:,}`".format(earned))
					return

				elif bbbb == 1:
					if ctx.author.id == 374622847672254466:
						earned = kraotscheat5
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					else:
						earned = earningssssss
						collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

					await ctx.send(":smirk: :smirk: :yum: you sucked your crush and they loved it, you ended up dating and got `{:,}` coins.".format(earned))
					return

				else:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
					await ctx.send("You did a fucking bad job at sucking and lost `{:,}` coins from your wallet.".format(losts))
					return

			except:
				ctx.command.reset_cooldown(ctx)
				return
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def race(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		if ctx.author.id in all_users:
			kraots = self.client.get_user(374622847672254466)

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
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})
					await ctx.send(":third_place: you won the race 3rd place an won: `{:,}` coins.".format(earnings))
					return

				elif aaaa == 4:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningss}})
					await ctx.send("U were close to lose the race by getting 5th place. You got a total of: `{:,}` coins.".format(earningss))
					return

				elif aaaa == 6:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningsss}})
					await ctx.send("After winning on 4th place you got: `{:,}` coins.".format(earningsss))
					return

				elif aaaa == 7:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssss}})
					await ctx.send(":sparkles: :second_place: after winning on the 2nd place, you won: `{:,}` coins.".format(kraots.name, earningssss))
					return

				elif bbbb == 1:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssssss}})
					await ctx.send(":sparkles: :first_place: :medal: :sparkles: after winning the race on the first place you won a total of: `{:,}` coins.".format(kraots.name, earningssssss))
					return

				else:
					collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
					await ctx.send("Sadly you lost the race, your lost consists of `{:,}` coins from your wallet.".format(losts))
					return

			except:
				ctx.command.reset_cooldown(ctx)
				return
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
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
			await ctx.send("Invalid amount! Please deposit numbers only!")

	@withdraw.error
	async def with_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("Invalid amount! Please deposit numbers only!")

	@give.error
	async def give_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("Invalid amount! Please deposit numbers only!")







	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection.delete_one({"_id": member.id})




def setup (client):
	client.add_cog(EcoCommands(client))	