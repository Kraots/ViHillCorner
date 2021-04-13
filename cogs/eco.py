import discord
from discord.ext import commands
from random import randint
import random
import utils.colors as color
import asyncio
from utils.helpers import time_phaserr
import pymongo
import motor.motor_asyncio
import os
import datetime
from dateutil.relativedelta import relativedelta
from utils import time
bot_channels = [752164200222163016, 750160851822182486, 750160851822182487]

rps = ['rock', 'paper', 'scissors']

gf_carrots = [822755470422442044, 374622847672254466]

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Economy"]

class EcoCommands(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix and ctx.channel.id in bot_channels


			# DAILY

	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def daily(self, ctx):
		user = ctx.author
		results = await collection.find_one({"_id": user.id})

		if results == None:
			await ctx.send("You are not registered! Type: `!register` to register.")
			return
		else:
			dateNow = datetime.datetime.utcnow()
			next_daily = datetime.datetime.utcnow() + relativedelta(days = 1)

			try:
				daily = results['daily']
				
				if dateNow < daily:
					
					def format_date(dt):
						return f"{time.human_timedelta(dt, accuracy=3)}"

					await ctx.send("You already claimed your daily for today! Please try again in `{}`.".format(format_date(daily)))
					return
				

				elif dateNow >= daily:
					await collection.update_one({"_id": user.id}, {"$inc":{"wallet": 75000}})
					await collection.update_one({"_id": user.id}, {"$set":{"daily": next_daily}})	

			except KeyError:
				await collection.update_one({"_id": user.id}, {"$inc":{"wallet": 75000}})
				await collection.update_one({"_id": user.id}, {"$set":{"daily": next_daily}})	
			
			
			await ctx.send("Daily successfully claimed, `75,000` <:carrots:822122757654577183>  have been put into your wallet. Come back in **24 hours** for the next one.")	


	@daily.group(invoke_without_command = True, case_insensitive = True, aliases=['reset'])
	@commands.is_owner()
	async def _reset(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		results = await collection.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		NewDaily = datetime.datetime.utcnow()
		await collection.update_one({"_id": member.id}, {"$set":{"daily": NewDaily}})
		await ctx.send("Cooldown for the daily command has been reset for user `{}`.".format(member))

	@_reset.command(aliases=['all', 'everyone'])
	@commands.is_owner()
	async def _all(self, ctx):
		NewDaily = datetime.datetime.utcnow()
		await collection.update_many({}, {"$set":{"daily": NewDaily}})
		await ctx.send("Cooldown for the daily command has been reset for everyone.")

			# REGISTER


	@commands.command()
	async def register(self, ctx):
		user = ctx.author

		post = {"_id": user.id, "wallet": 0, "bank": 0, "daily": datetime.datetime.utcnow()}

		try:
			await collection.insert_one(post)
			await ctx.send("Succesfully registered!")

		except pymongo.errors.DuplicateKeyError:
			await ctx.send("You are already registered!")
	

			# UNREGISTER


	@commands.command()
	async def unregister(self, ctx):
		user = ctx.author
		results = await collection.find_one({"_id": user.id})
		if results == None:
			await ctx.send("You are not registered! Type: `!regiser` to register.")
			return

		await collection.delete_one({"_id": user.id})
		await ctx.send("Succesfully unregistered!")
		  
		  
		    # BALANCE



	@commands.group(invoke_without_command=True, aliases=['bal'])
	async def balance(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		user = member
		
		results = await collection.find_one({"_id": user.id})
		if results == None:
			if member.id == ctx.author.id:
				await ctx.send("You are not registered! Type: `!register` to register.")
			else:
				await ctx.send("User is not registered!")
			return

		all_accounts = collection.find()

		leader_board = {}

		for all_results in await all_accounts.to_list(99999999999999999999999999):
			userr = self.client.get_user(all_results["_id"])
			all_wallet_amt = all_results["wallet"]
			all_bank_amt = all_results["bank"]
			leader_board[userr] = all_wallet_amt + all_bank_amt

		wallet_amt = results["wallet"]
		bank_amt = results["bank"]

		total_amt = wallet_amt + bank_amt

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
		em.add_field(name="Wallet Balance", value="**{:,}** <:carrots:822122757654577183> ".format(wallet_amt), inline=False)
		em.add_field(name="Bank Balance", value="**{:,}** <:carrots:822122757654577183> ".format(bank_amt), inline=False)
		em.add_field(name="Total Balance", value="**{:,}** <:carrots:822122757654577183> ".format(total_amt))
		em.add_field(name="Rank", value="`#{}`".format(index))
		em.set_thumbnail(url=user.avatar_url)

		await ctx.send(embed=em)

			# LEADERBOARD

	@commands.command(aliases=['lb', 'baltop'])
	async def leaderboard(self, ctx, x = 10):
		results = collection.find()
		leader_board = {}

		all_users = []

		for result in await results.to_list(9999999999999):
			user = self.client.get_user(result["_id"])  
			leader_board[user] = result["wallet"] + result["bank"]  
			all_users.append(result['_id'])
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True)  
		
		em = discord.Embed(title=f'Top {x} richest people\n _ _', color=color.reds) 
		
		for index, (mem, amt) in enumerate(leader_board[:x], start=1): 
			
			name = mem.name

			em.add_field(name=f"{index}.   {name}", value="**{:,}** <:carrots:822122757654577183> ".format(amt), inline=False)
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
			
		await ctx.send(embed=em)


	@balance.command(aliases=['add-bank'])
	@commands.is_owner()
	async def add_bank(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of money you want to add!")
			return

		user = member

		amount = amount.replace(",", "")

		amount = int(amount)

		await collection.update_one({"_id": user.id}, {"$inc":{"bank": amount}})
		
			
		await ctx.send("Successfully added **{:,}** <:carrots:822122757654577183> , and deposited them into the bank for `{}`!".format(amount, member))

		if ctx.author.id == kraots.id:
			return
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description="`{}` added **{:,}** <:carrots:822122757654577183>  to `{}`.\n\n`{}` - person who added the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
	
			await kraots.send(embed=embed)

	@balance.command(aliases=['add-wallet'])
	@commands.is_owner()
	async def add_wallet(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of money you want to add!")
			return

		user = member

		amount = amount.replace(",", "")

		amount = int(amount)

		await collection.update_one({"_id": user.id}, {"$inc":{"wallet": amount}})
		
			
		await ctx.send("Successfully added **{:,}** <:carrots:822122757654577183>  to the wallet for `{}`!".format(amount, member))

		if ctx.author.id == kraots.id:
			return
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description="`{}` added **{:,}** <:carrots:822122757654577183>  to `{}`.\n\n`{}` - person who added the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
	
			await kraots.send(embed=embed)


	@balance.command(aliases=['set-bank'])
	@commands.is_owner()
	async def set_bank(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of money you want to set!")
			return

		user = member
		amount = amount.replace(",", "")
		amount = int(amount)


		await collection.update_one({"_id": user.id}, {"$set":{"bank": amount}})

		await ctx.send("Balance successfully set to **{:,}** <:carrots:822122757654577183>  in the bank for `{}`!".format(amount, member))
		
		if ctx.author.id == kraots.id:
			return		
		
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description="`{}` set balance to **{:,}** <:carrots:822122757654577183>  in the bank for `{}`.\n\n`{}` - person who set the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
			await kraots.send(embed=embed)

	@balance.command()
	@commands.is_owner()
	async def reset(self, ctx, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return


		user = member

		await collection.update_one({"_id": user.id}, {"$set":{"wallet": 0}})
		await collection.update_one({"_id": user.id}, {"$set":{"bank": 0}})

		await ctx.send(f"Reseted balance for `{member}`.")
		
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

		results = await collection.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of money you want to set!")
			return

		user = member
		
		amount = amount.replace(",", "")
		amount = int(amount)

		await collection.update_one({"_id": user.id}, {"$set":{"wallet": amount}})

		await ctx.send("Balance successfully set to **{:,}** <:carrots:822122757654577183>  in the wallet for `{}`!".format(amount, member))
		
		if ctx.author.id == kraots.id:
			return
		
		else:
			embed = discord.Embed(color=color.lightpink, title="BALANCE SET", description="`{}` set balance to **{:,}** <:carrots:822122757654577183>  in the wallet for `{}`.\n\n`{}` - person who set the money\n`{}` - person who got the money".format(ctx.author, amount, member, ctx.author.id, member.id))
		
			await kraots.send(embed=embed)


 			# WITHDRAW


	@commands.group(aliases=['with'])
	async def withdraw(self, ctx, amount = None):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
		
			if amount is None:
				await ctx.send('Please enter the amount you want to withdraw.')
				return
			
			bal = results["bank"]

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

			elif bal < 1:
				await ctx.send("You do not have that much money in your bank. Money in bank: **{:,}**".format(bal))
				return

			elif amount < 1:
				await ctx.send('Invalid amount.')
				return

			await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": amount}})
			await collection.update_one({"_id": ctx.author.id}, {"$inc":{"bank": -amount}})

			await ctx.send("Successfully withdrew **{:,}** <:carrots:822122757654577183> !".format(amount))

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# DEPOSIT


	@commands.command(aliases=['dep'])
	async def deposit(self, ctx, amount = None):
		
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
		
			if amount is None:
				await ctx.send('Please enter the amount you want to deposit.')
				return
			
			bal = results["wallet"]

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

			elif bal < 1:
				await ctx.send("You do not have that much money in your wallet. Money in wallet: **{:,}**".format(bal))
				return

			elif amount < 1:
				await ctx.send('Invalid amount. You cannot deposit **0** or **negative number** amount of <:carrots:822122757654577183> .')
				return

			await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -amount}})
			await collection.update_one({"_id": ctx.author.id}, {"$inc":{"bank": amount}})

			await ctx.send("Successfully deposited **{:,}** <:carrots:822122757654577183> !".format(amount))

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# GIVE


	@commands.command()
	async def give(self, ctx, member : discord.Member, amount = None):
		
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
			user = member
			author = ctx.author
			
			if amount is None:
				await ctx.send('Please enter the amount you want to withdraw.')
				return
			
			bal = results["wallet"]

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

			elif bal < 100:
				await ctx.send("You do not have that much money in your wallet. Money in wallet: **{:,}**".format(bal))
				return

			if amount < 100:
				await ctx.send('You cannot give less than `100` <:carrots:822122757654577183> .')
				return

			await collection.update_one({"_id": author.id}, {"$inc":{"wallet": -amount}})
			await collection.update_one({"_id": user.id}, {"$inc":{"wallet": amount}})

			await ctx.send("You gave **{:,}** <:carrots:822122757654577183>  to `{}`.".format(amount, member.name))

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return
			

			# ROB


	@commands.command(aliases=["steal"])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def rob(self, ctx, member : discord.Member = None):
		if member is None:
			await ctx.send("You must specify the person you want to rob/steal from.")
			ctx.command.reset_cooldown(ctx)
			return
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
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
			
			get_user_bal = await collection.find_one({"_id": user.id})

			user_bal = get_user_bal["wallet"]

			author_bal = results["wallet"]

			if author_bal < 350:
				await ctx.send("You need `350` <:carrots:822122757654577183>  to rob someone!")
				ctx.command.reset_cooldown(ctx)
				return

			if user_bal < 250:
				await ctx.send('The user must have at least `250` <:carrots:822122757654577183> !')
				ctx.command.reset_cooldown(ctx)
				return

			earnings = randint(250, user_bal)

			chance = randint(1, 10)


			if chance == 1:
				await collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> !".format(member.display_name, earnings))

			elif chance == 3:
				await collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> !".format(member.display_name, earnings))

			elif chance == 7:
				await collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> !".format(member.display_name, earnings))

			elif chance == 10:
				await collection.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await collection.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> !".format(member.display_name, earnings))

			else:
				await collection.update_one({"_id": author.id}, {"$inc":{"wallet": -350}})

				await ctx.send("You failed in stealing from that person and you lost `350` <:carrots:822122757654577183> ")

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# SLOTS


	@commands.command()
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def slots(self, ctx, amount = None):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:

			if amount is None:
				await ctx.send('Please enter the amount.')
				ctx.command.reset_cooldown(ctx)
				return

			bal = results["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			amount = int(amount)

			if amount > bal:
				await ctx.send('You do not own that much money!')
				ctx.command.reset_cooldown(ctx)
				return

			if amount < 300:
				await ctx.send('You must bet more than `300` <:carrots:822122757654577183> .')
				ctx.command.reset_cooldown(ctx)
				return

			prefinal = []
			for i in range(3):
				a = random.choice(["❌", "🇴", "✨", "🔥", "<:tfBruh:784689708890324992>", "👑"])

				prefinal.append(a)

				final = "\u2800┃\u2800".join(prefinal)

			embed = discord.Embed(color=color.lightpink, title="Slots!", description="<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
			msg = await ctx.send(embed=embed)

			line1 = prefinal[0]
			line2 = prefinal[1]
			line3 = prefinal[2]



			if prefinal[0] == prefinal[1] == prefinal[2]:
				earned = 2.5*amount

				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

				wallet_amt = bal + earned

				em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)
				
				print("Reached final edit")
				winembed = discord.Embed(color=discord.Color.green(), title="WIN!", description="{}\u2800┃\u2800{}\u2800┃\u2800{}\n\nYou bet a total of **{:,}** <:carrots:822122757654577183>  and won **{:,}** <:carrots:822122757654577183> . \nNow in wallet: **{:,}** <:carrots:822122757654577183>.".format(line1, line2, line3, amount, earned, wallet_amt))
				await asyncio.sleep(0.7)
				await msg.edit(embed=winembed)



			elif prefinal[0] == prefinal[1] or prefinal[0] == prefinal[2] or prefinal[2] == prefinal[1]:
				earned = amount

				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

				wallet_amt = bal + earned

				em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				winembed = discord.Embed(color=discord.Color.green(), title="WIN!", description="{}\n\nYou won **{:,}** <:carrots:822122757654577183> . \nNow in wallet: **{:,}** <:carrots:822122757654577183>.".format(final, amount, wallet_amt))
				await asyncio.sleep(0.7)
				await msg.edit(embed=winembed)



			else:

				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -amount}})
				
				wallet_amt = bal - amount
			
				em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				em = discord.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				lostembed = discord.Embed(color=color.red, title="LOST!", description="{}\n\nYou bet a total amount of **{:,}** <:carrots:822122757654577183>  but you lost them! :c\nNow in wallet: **{:,}** <:carrots:822122757654577183>.".format(final, amount, wallet_amt))
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
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
			earnings = randint(100, 500)

			await ctx.send(f"Someone gave you **{earnings}** <:carrots:822122757654577183> !!")

			await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

			# WORK
	

	@commands.command()
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def work(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:

			await ctx.send("You worked and got **5,000** <:carrots:822122757654577183> . The money have been deposited into your bank!")

			await collection.update_one({"_id": ctx.author.id}, {"$inc":{"bank": 5000}})
		
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return


				# CRIME

	@commands.command()
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def crime(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:

			aaaa = randint(1, 7)
			earnings = randint(500, 1500)
			earningss = randint(100, 420)
			earningsss = randint(400, 800)
			earningssss = randint(5000, 50000)
			losts = randint(300, 700)

			if aaaa == 2:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})

				await ctx.send("<:weird:773538796087803934> you commited a bigger crime and got **{:,}** <:carrots:822122757654577183> .".format(earnings))
				return

			if aaaa == 4:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningss}})
				await ctx.send("<:weird:773538796087803934> you commited a smaller crime and got **{:,}** <:carrots:822122757654577183> .".format(earningss))
				return

			if aaaa == 6:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningsss}})
				await ctx.send("<:weird:773538796087803934> you commited a medium crime and got **{:,}** <:carrots:822122757654577183> .".format(earningsss))
				return

			if aaaa == 7:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssss}})
				await ctx.send("<:weird:773538796087803934> you commited a large crime and got **{:,}** <:carrots:822122757654577183> .".format(earningssss))
				return

			else:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
				await ctx.send("You lost **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
				return
		
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return

				# GUESS THE NUMBER


	@commands.command(aliases=['guess'])
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def gtn(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
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
			
			index = 0
			
			for guess in range(0,3):
				msg = await self.client.wait_for('message', timeout= 30 , check=check)
				attempt = int(msg.content)
				if attempt > number:
					index += 1
					if index == 3:
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -lost_amt}})
						await msg.reply(content=f"You didn't get it and lost **{lost_amt}** <:carrots:822122757654577183> . The number was **{number}**.")
						return
					await msg.reply('Try going lower.')


				elif attempt < number:
					index += 1
					if index == 3:
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -lost_amt}})
						await msg.reply(content=f"You didn't get it and lost **{lost_amt}** <:carrots:822122757654577183> . The number was **{number}**.")
						return
					await msg.reply('Try going higher.')

					

				else:
					await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": win_amt}})
					await msg.reply(f'You guessed it! Good job! You got **{win_amt}** <:carrots:822122757654577183> . The number was **{number}**.')
					return
		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return


                # PP SUCK (credigs : PANDIE)
	
	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def ppsuck(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
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

			if ctx.author.id in gf_carrots:	
				bbbb = randint(1, 25)	
				aaaa = randint(1, 7)

			try:
				if bbbb == 1:
					if ctx.author.id in gf_carrots:
						if ctx.author.id == 822755470422442044:
							earned = kraotscheat5
							await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})	

							await ctx.send(":smiling_imp: :smiling_imp: :smirk: :smirk: :yum: :yum: :drooling_face: :drooling_face: you sucked `Kraots` and peed inside his mouth, and then kept fucking and having sex all night, he drank your saliva and licked you clean. Then he kept fucking your holes until you started to bleed but he still kept moving until you passed out, you woke up and u were bleeding his cum out of every hole and they were hurting you so badly you couldn't move for months. You got: **{:,}** <:carrots:822122757654577183>. :smiling_imp:".format(earned))	
							return	

						elif ctx.author.id == 374622847672254466:	
							earned = kraotscheat5	
							await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})	

							await ctx.send(":smiling_imp: :smiling_imp: :smirk: :smirk: :yum: :yum: :drooling_face: :drooling_face: you let `Melaina` pee inside your mouth, and then kept fucking and having sex all night, you drank her saliva and licked her clean. Then you kept fucking her holes until she started to bleed but you still kept moving until she passed out, she woke up and she were bleeding your cum out of every hole and they were hurting her so badly she couldn't move for months. You got: **{:,}** <:carrots:822122757654577183> . :smiling_imp:".format(earned))	
							return
					else:
						earned = earningssssss	
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})	

						await ctx.send(":smirk: :smirk: :yum: you sucked your crush and they loved it, you ended up dating and got **{:,}** <:carrots:822122757654577183> .".format(earned))
						return
						
				elif aaaa == 1:
					if ctx.author.id in gf_carrots:
						earned = kraotscheat1
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
						if ctx.author.id == 822755470422442044:
							await ctx.send(":yum: :yum: You sucked `Kraots`'s dick and he came deep inside your throat and you choked on his cum and passed out with his dick in your mouth, tied up above the ground upside down. You got: **{:,}** <:carrots:822122757654577183> . :smiling_imp:".format(earned))	
							return	

						elif ctx.author.id == 374622847672254466:	

							await ctx.send(":yum: :yum: You sucked `Melaina`'s wet juicy pussy and her cum ended up all the way inside your throat and you choked on it and passed out with her pussy in your mouth. You got: **{:,}** <:carrots:822122757654577183> . :smiling_imp:".format(earned))	
							return	
						
					else:	
						earned = earnings	
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

						await ctx.send(":yum: you sucked ur dad's pp and got **{:,}** <:carrots:822122757654577183> .".format(earned))
						return

				elif aaaa == 4:
					if ctx.author.id in gf_carrots:
						earned = kraotscheat2	
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
						if ctx.author.id == 822755470422442044:	
							await ctx.send("You did so good at peeing insides `Kraots`'s mouth that after he drank it he was very happy and then he even licked your juicy pussy very clean and then he put his tongue inside your pee hole and you started to cum right in his throat. You got: **{:,}** <:carrots:822122757654577183> :smiling_imp:".format(earned))	
							return	

						elif ctx.author.id == 374622847672254466:	
							await ctx.send("You let `Melaina` pee right in your mouth and drank it and then you kept putting your tongue inside her pee hole and then she started to cum right in your throat. You got: **{:,}** <:carrots:822122757654577183> :smiling_imp:".format(earned))	
							return	

					else:	
						earned = earningss	
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

						await ctx.send("<:weird:773538796087803934> you didn't do too good of a job at sucking but it wasn't too bad either and got **{:,}** <:carrots:822122757654577183> .".format(earned))
						return
				
				elif aaaa == 6:
					if ctx.author.id in gf_carrots:
						earned = kraotscheat3
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})	
						if ctx.author.id == 822755470422442044:	
							await ctx.send("You fucked with `Kraots` all night long, and at the end you both fell asleep naked while cuddling in the bed with his dick inside your vagina while you were peeing on his hard warm dick. You got: **{:,}** <:carrots:822122757654577183> :smiling_imp:".format(earned))	
							return	

						elif ctx.author.id == 374622847672254466:	
							await ctx.send("You fucked with `Melaina` all night long, and at the end you both fell asleep naked while cuddling in the bed with your dick inside her vagina and while she was peeing on your hard warm dick. You got: **{:,}** <:carrots:822122757654577183> :smiling_imp:".format(earned))	
							return	
					else:	
						earned = earningsss	
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					
						await ctx.send("<:weird:773538796087803934> you didn't do too bad, but u didn't do too good either at sucking ur dog's pp and got **{:,}** <:carrots:822122757654577183> .".format(earned))
						return
				
				elif aaaa == 7:
					if ctx.author.id in gf_carrots:
						earned = kraotscheat4
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})	
						if ctx.author.id == 822755470422442044:	

							await ctx.send(":drooling_face: You fucked `Kraots` and peed on him, and he loved it very much that he tied you up and then fucked you in every way possible and came in your throat and in your ass and all his cum got deep inside your tummy and you could feel his warm cum inside your belly. You got: **{:,}** <:carrots:822122757654577183> . :smiling_imp:".format(earned))	
							return	

						elif ctx.author.id == 374622847672254466:	

							await ctx.send(":drooling_face: You fucked `Melaina` and she peed on you, and she loved it very much, then you tied her up and then fucked her in every way possible and came in her throat and in her ass and all your cum got deep inside her tummy and she could feel your warm cum inside her belly. You got: **{:,}** <:carrots:822122757654577183> . :smiling_imp:".format(earned))	
							return

					else:	
						earned = earningssss	
						await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
						await ctx.send(":smirk: You sucked your best friend and they liked it very much and decided to gave you **{:,}** <:carrots:822122757654577183>".format(earned))
						return

				else:
					await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
					await ctx.send("You did a fucking bad job at sucking and lost **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
					
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
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:

			aaaa = randint(1, 7)
			bbbb = randint(1, 100)
			earnings = randint(800, 2500)
			earningss = randint(300, 620)
			earningsss = randint(600, 1200)
			earningssss = randint(20000, 150000)
			earningssssss = randint(500000, 5000000)
			losts = randint(1000, 1200)

			if aaaa == 1:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})
				await ctx.send(":third_place: you won the race 3rd place an won: **{:,}** <:carrots:822122757654577183> .".format(earnings))
				return

			elif aaaa == 4:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningss}})
				await ctx.send("U were close to lose the race by getting 5th place. You got a total of: **{:,}** <:carrots:822122757654577183> .".format(earningss))
				return

			elif aaaa == 6:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningsss}})
				await ctx.send("After winning on 4th place you got: **{:,}** <:carrots:822122757654577183> .".format(earningsss))
				return

			elif aaaa == 7:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssss}})
				await ctx.send(":sparkles: :second_place: after winning on the 2nd place, you won: **{:,}** <:carrots:822122757654577183> .".format(earningssss))
				return

			elif bbbb == 1:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssssss}})
				await ctx.send(":sparkles: :first_place: :medal: :sparkles: after winning the race on the first place you won a total of: **{:,}** <:carrots:822122757654577183> .".format(earningssssss))
				return

			else:
				await collection.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
				await ctx.send("Sadly you lost the race, your lost consists of **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
				return

		else:
			await ctx.send("You are not registered! Type: `!register` to register.")
			ctx.command.reset_cooldown(ctx)
			return


	@commands.command(aliases=['rps', 'rockpaperscissors', 'rock-paper-scissors'])
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def _rps(self, ctx):
		user = ctx.author
		results = await collection.find_one({"_id": user.id})
		if results == None:
			await ctx.send("You are not registered! Type: `!register` to register.")
			return
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		bot_rps = random.choice(rps)
		earned = randint(5000, 15000)
		await ctx.send("Please choose between `rock`/`paper`/`scissors`. You have **60** seconds to give your answer. %s" % (user.mention))
		try:
			user_rps = 	await self.client.wait_for('message', timeout= 60, check=check)
			user_rps = user_rps.content.lower()
			if not user_rps in rps:
				await ctx.send("You can only choose from `rock`/`paper`/`scissors`. Type the command again. %s" % (user.mention))
				ctx.command.reset_cooldown(ctx)
				return
		except asyncio.TimeoutError:
			await ctx.send("You ran out of time. %s" % (user.mention))
			return
		else:

			if user_rps == "rock":
				if bot_rps == "paper":
					await ctx.send("You chose `rock`, and i chose `paper`. You lost **325** <:carrots:822122757654577183> . %s" % (user.mention))
					await collection.update_one({'_id': user.id}, {'$inc':{'wallet': -325}})
					return
				elif bot_rps == "scissors":
					await ctx.send("You chose `rock`, and i chose `scissors`. You won **{:,}** <:carrots:822122757654577183> . {}".format(earned, user.mention))
					await collection.update_one({'_id': user.id}, {'$inc':{'wallet': earned}})
					return
				elif bot_rps == "rock":
					await ctx.send("We both chose `rock`. Nothing happened, your balance stays the same. %s" % (user.mention))
					ctx.command.reset_cooldown(ctx)
					return
			
			
			elif user_rps == "paper":
				if bot_rps == "scissors":
					await ctx.send("You chose `paper`, and i chose `scissors`. You lost **325** <:carrots:822122757654577183> . %s" % (user.mention))
					await collection.update_one({'_id': user.id}, {'$inc':{'wallet': -325}})
					return
				elif bot_rps == "rock":
					await ctx.send("You chose `paper`, and i chose `rock`. You won **{:,}** <:carrots:822122757654577183> . {}".format(earned, user.mention))
					await collection.update_one({'_id': user.id}, {'$inc':{'wallet': earned}})
					return
				elif bot_rps == "paper":
					await ctx.send("We both chose `paper`. Nothing happened, your balance stays the same. %s" % (user.mention))
					ctx.command.reset_cooldown(ctx)
					return
			
			elif user_rps == "scissors":
				if bot_rps == "rock":
					await ctx.send("You chose `scissors`, and i chose `rock`. You lost **325** <:carrots:822122757654577183> . %s" % (user.mention))
					await collection.update_one({'_id': user.id}, {'$inc':{'wallet': -325}})
					return
				elif bot_rps == "paper":
					await ctx.send("You chose `scissors`, and i chose `paper`. You won **{:,}** <:carrots:822122757654577183> . {}".format(earned, user.mention))
					await collection.update_one({'_id': user.id}, {'$inc':{'wallet': earned}})
					return
				elif bot_rps == "scissors":
					await ctx.send("We both chose `scissors`. Nothing happened, your balance stays the same. %s" % (user.mention))
					ctx.command.reset_cooldown(ctx)
					return

	@_rps.error
	async def rps_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"Please wait: **{time_phaserr(error.retry_after)}** before playing rps again."
				await ctx.channel.send(msg)

	@race.error
	async def race_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"You cannot race that fast! Please wait: **{time_phaserr(error.retry_after)}**."
				await ctx.channel.send(msg)

	@ppsuck.error
	async def ppsuck_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"OK OK CHILLE, IK U WANT TO SUCK ON SOMETHING BUT PLEASE WAIT **{time_phaserr(error.retry_after)}**."
				await ctx.channel.send(msg)

	@gtn.error
	async def gtn_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f"You've already played the game, come back in **{time_phaserr(error.retry_after)}**."
				await ctx.channel.send(msg)

	@crime.error
	async def crime_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can commit crimes again in **{time_phaserr(error.retry_after)}**.'
				await ctx.channel.send(msg)


	@work.error
	async def work_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can work again in **{time_phaserr(error.retry_after)}**.'
				await ctx.channel.send(msg)

	@beg.error
	async def beg_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can have more <:carrots:822122757654577183>  in **{time_phaserr(error.retry_after)}**.'
				await ctx.channel.send(msg)



	@rob.error
	async def steal_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can steal more in **{time_phaserr(error.retry_after)}**.'
				await ctx.channel.send(msg)


	@slots.error
	async def slots_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = f'You can bet your money in the slots machine in **{time_phaserr(error.retry_after)}**.'
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
		if member.id == 374622847672254466:
			return
		await collection.delete_one({"_id": member.id})




def setup (client):
	client.add_cog(EcoCommands(client))	