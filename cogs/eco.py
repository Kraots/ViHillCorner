import disnake
from disnake.ext import commands
from random import randint
import random
import utils.colors as color
import asyncio
from utils.helpers import time_phaser, format_balance
import pymongo
import datetime
from dateutil.relativedelta import relativedelta
from utils import time

rps = ['rock', 'paper', 'scissors']

class Economy(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Economy']
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def daily(self, ctx):
		"""Get your daily 75.00K <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		user = ctx.author
		results = await self.db.find_one({"_id": user.id})

		if results == None:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			return
		else:
			dateNow = datetime.datetime.utcnow()
			next_daily = datetime.datetime.utcnow() + relativedelta(days = 1)

			try:
				daily = results['daily']
				
				if dateNow < daily:
					
					def format_date(dt):
						return f"{time.human_timedelta(dt, accuracy=3)}"

					await ctx.send("{} You already claimed your daily for today! Please try again in `{}`.".format(ctx.author.mention, format_date(daily)))
					return
				

				elif dateNow >= daily:
					await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": 75000}})
					await self.db.update_one({"_id": user.id}, {"$set":{"daily": next_daily}})	

			except KeyError:
				await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": 75000}})
				await self.db.update_one({"_id": user.id}, {"$set":{"daily": next_daily}})	
			
			
			await ctx.send("Daily successfully claimed, `75,000` <:carrots:822122757654577183>  have been put into your wallet. Come back in **24 hours** for the next one. %s" % (ctx.author.mention))	

	@daily.group(name='reset', invoke_without_command = True, case_insensitive = True)
	@commands.is_owner()
	async def daily_reset(self, ctx, member: disnake.Member = None):
		"""Reset the daily for a user. This means that the amount of time that they have to wait until they can get their daily will be reset."""

		if member is None:
			member = ctx.author
		
		results = await self.db.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		NewDaily = datetime.datetime.utcnow()
		await self.db.update_one({"_id": member.id}, {"$set":{"daily": NewDaily}})
		await ctx.send("Cooldown for the daily command has been reset for user `{}`.".format(member))

	@daily_reset.command(name='everyone', aliases=['all'])
	@commands.is_owner()
	async def daily_reset_everyone(self, ctx):
		"""Reset the daily cooldown for `everyone`"""

		NewDaily = datetime.datetime.utcnow()
		await self.db.update_many({}, {"$set":{"daily": NewDaily}})
		await ctx.send("Cooldown for the daily command has been reset for everyone.")

	@commands.command(name='register')
	async def eco_register(self, ctx):
		"""Register yourself to be able to use the economy commands."""
		
		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		user = ctx.author

		post = {"_id": user.id, "wallet": 0, "bank": 0, "daily": datetime.datetime.utcnow()}

		try:
			await self.db.insert_one(post)
			await ctx.send("Succesfully registered! %s" % (ctx.author.mention))

		except pymongo.errors.DuplicateKeyError:
			await ctx.send("You are already registered! %s" % (ctx.author.mention))
	
	@commands.command(name='unregister')
	async def eco_unregister(self, ctx):
		"""Unregister yourself, you won't be able to use the economy commands anymore."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		user = ctx.author
		results = await self.db.find_one({"_id": user.id})
		if results == None:
			await ctx.send("You are not registered! %s" % (ctx.author.mention))
			return

		await self.db.delete_one({"_id": user.id})
		await ctx.send("Succesfully unregistered! %s" % (ctx.author.mention))

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bal'])
	async def balance(self, ctx, member: disnake.Member = None):
		"""Check your or another member's balance."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		if member is None:
			member = ctx.author

		user = member
		
		results = await self.db.find_one({"_id": user.id})
		if results == None:
			if member.id == ctx.author.id:
				await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			else:
				await ctx.send("User is not registered! %s" % (ctx.author.mention))
			return

		all_accounts = await self.db.find().to_list(100000)

		leader_board = {}

		for all_results in all_accounts:
			userr = self.bot.get_user(all_results["_id"])
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


		em = disnake.Embed(title=f"{member.name}'s balance", color=color.lightpink)
		em.add_field(name="Wallet Balance", value="{} <:carrots:822122757654577183> ".format(format_balance(wallet_amt)), inline=False)
		em.add_field(name="Bank Balance", value="{} <:carrots:822122757654577183> ".format(format_balance(bank_amt)), inline=False)
		em.add_field(name="Total Balance", value="{} <:carrots:822122757654577183> ".format(format_balance(total_amt)))
		em.set_footer(text="Rank: {}".format(index))
		em.set_thumbnail(url=user.avatar.url)

		await ctx.send(embed=em)

	@balance.command(name='leaderboard', aliases=['lb', 'top'])
	async def eco_bal_leaderboard(self, ctx):
		"""See top `10` richest people."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find().to_list(100000)
		leader_board = {}

		all_users = []

		for result in results:
			user = self.bot.get_user(result["_id"])  
			leader_board[user] = result["wallet"] + result["bank"]  
			all_users.append(result['_id'])
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True)  
		
		em = disnake.Embed(title=f'Top 10 richest people', color=color.lightpink) 
		
		for index, (mem, amt) in enumerate(leader_board[:10], start=1): 
			
			name = mem.name

			em.add_field(name=f"`#{index}` {name}", value="{} <:carrots:822122757654577183> ".format(format_balance(amt)), inline=False)
			if index == 10:
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
			em.set_footer(text=f"Your place: {index}", icon_url=ctx.author.avatar.url)
			
		await ctx.send(embed=em)

	@balance.command(name='add-bank')
	@commands.is_owner()
	async def add_bank(self, ctx, amount = None, member: disnake.Member = None):
		"""Add <:carrots:822122757654577183> in the member's bank."""

		if member is None:
			member = ctx.author

		results = await self.db.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of carrots you want to add!")
			return

		user = member

		amount = amount.replace(",", "")

		amount = int(amount)

		await self.db.update_one({"_id": user.id}, {"$inc":{"bank": amount}})
		
			
		await ctx.send("Successfully added **{:,}** <:carrots:822122757654577183> , and deposited them into the bank for `{}`!".format(amount, member))

	@balance.command(name='add-wallet')
	@commands.is_owner()
	async def add_wallet(self, ctx, amount = None, member: disnake.Member = None):
		"""Add <:carrots:822122757654577183> in the member's wallet."""

		if member is None:
			member = ctx.author

		results = await self.db.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of carrots you want to add!")
			return

		user = member

		amount = amount.replace(",", "")

		amount = int(amount)

		await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": amount}})
		
			
		await ctx.send("Successfully added **{:,}** <:carrots:822122757654577183>  to the wallet for `{}`!".format(amount, member))

	@balance.command(name='set-bank')
	@commands.is_owner()
	async def set_bank(self, ctx, amount = None, member: disnake.Member = None):
		"""Set the amount of <:carrots:822122757654577183> in the member's bank."""

		if member is None:
			member = ctx.author

		results = await self.db.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of carrots you want to set!")
			return

		user = member
		amount = amount.replace(",", "")
		amount = int(amount)


		await self.db.update_one({"_id": user.id}, {"$set":{"bank": amount}})

		await ctx.send("Balance successfully set to **{:,}** <:carrots:822122757654577183>  in the bank for `{}`!".format(amount, member))

	@balance.command(name='reset')
	@commands.is_owner()
	async def eco_bal_reset(self, ctx, member: disnake.Member = None):
		"""Reset the member's <:carrots:822122757654577183>."""

		if member is None:
			member = ctx.author

		results = await self.db.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return


		user = member

		await self.db.update_one({"_id": user.id}, {"$set":{"wallet": 0}})
		await self.db.update_one({"_id": user.id}, {"$set":{"bank": 0}})

		await ctx.send(f"Reseted balance for `{member}`.")

	@balance.command(name='set-wallet')
	@commands.is_owner()
	async def set_wallet(self, ctx, amount = None, member: disnake.Member = None):
		"""Set the amount of <:carrots:822122757654577183> in the member's wallet."""

		if member is None:
			member = ctx.author

		results = await self.db.find_one({"_id": member.id})
		if results == None:
			await ctx.send("User not registered!")
			return

		if amount is None:
			await ctx.send("Please specify the amount of carrots you want to set!")
			return

		user = member
		
		amount = amount.replace(",", "")
		amount = int(amount)

		await self.db.update_one({"_id": user.id}, {"$set":{"wallet": amount}})

		await ctx.send("Balance successfully set to **{:,}** <:carrots:822122757654577183>  in the wallet for `{}`!".format(amount, member))

	@commands.command(aliases=['with'])
	async def withdraw(self, ctx, amount = None):
		"""Withdraw the amount of <:carrots:822122757654577183> from your bank."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
		
			if amount is None:
				await ctx.send('Please enter the amount you want to withdraw. %s' % (ctx.author.mention))
				return
			
			bal = results["bank"]

			if amount.lower() == "all":
				amount = bal

			try:
				amount = amount.replace(",", "")
			except:
				pass
			try:
				amount = int(amount)
			except ValueError:
				return await ctx.reply("Not a number!")

			if amount > bal:
				await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
				return

			elif bal < 1:
				await ctx.send("{} You do not have that much carrots in your bank. Carrots in bank: **{:,}**".format(ctx.author.mention, bal))
				return

			elif amount < 1:
				await ctx.send('Invalid amount. %s' % (ctx.author.mention))
				return

			await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": amount}})
			await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"bank": -amount}})

			await ctx.send("Successfully withdrew **{:,}** <:carrots:822122757654577183> ! {}".format(amount, ctx.author.mention))

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command(aliases=['dep'])
	async def deposit(self, ctx, amount = None):
		"""Deposit the amount of <:carrots:822122757654577183> in your bank."""
		
		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
		
			if amount is None:
				await ctx.send('Please enter the amount you want to deposit. %s' % (ctx.author.mention))
				return
			
			bal = results["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			try:
				amount = int(amount)
			except ValueError:
				return await ctx.reply("Not a number!")

			if amount > bal:
				await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
				return

			elif bal < 1:
				await ctx.send("{} You do not have that much carrots in your wallet. Carrots in wallet: **{:,}**".format(ctx.author.mention, bal))
				return

			elif amount < 1:
				await ctx.send('Invalid amount. You cannot deposit **0** or **negative number** amount of <:carrots:822122757654577183>. %s' % (ctx.author.mention))
				return

			await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -amount}})
			await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"bank": amount}})

			await ctx.send("Successfully deposited **{:,}** <:carrots:822122757654577183> ! {}".format(amount, ctx.author.mention))

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command(name='gift', aliases=['give'])
	async def bal_eco_give(self, ctx, member : disnake.Member, amount = None):
		"""Be a kind person and give some of your <:carrots:822122757654577183> from your **bank** to someone else's."""
		
		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
			user = member
			author = ctx.author
			
			if amount is None:
				await ctx.send('Please enter the amount you want to withdraw. %s' % (ctx.author.mention))
				return
			
			bal = results["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			try:
				amount = int(amount)
			except ValueError:
				return await ctx.reply("Not a number!")

			if amount > bal:
				await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
				return

			elif bal < 100:
				await ctx.send("{} You do not have that much carrots in your wallet. Carrots in wallet: **{:,}**".format(ctx.author.mention, bal))
				return

			if amount < 100:
				await ctx.send('You cannot give less than `100` <:carrots:822122757654577183> %s.' % (ctx.author.mention))
				return

			def check(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == member.id

			msg = await ctx.send(f"{ctx.author.mention} wants to give you some carrots. Do you accept them {member.mention}?")
			await msg.add_reaction('<:agree:797537027469082627>')
			await msg.add_reaction('<:disagree:797537030980239411>')

			try:
				reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)

			except asyncio.TimeoutError:
				new_msg = f"{member.mention} Did not react in time."
				await msg.edit(content=new_msg)
				await msg.clear_reactions()
				return
			
			else:
				if str(reaction.emoji) == '<:agree:797537027469082627>':
					await self.db.update_one({"_id": author.id}, {"$inc":{"wallet": -amount}})
					await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": amount}})
					e = f"{member.mention} accepted and got **{amount:,}** <:carrots:822122757654577183> from {ctx.author.mention}."
					await msg.edit(content=e)
					await msg.clear_reactions()
					return
				
				elif str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = f"{member.mention} did not accept your <:carrots:822122757654577183>. {ctx.author.mention}"
					await msg.edit(content=e)
					await msg.clear_reactions()
					return

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			return

	@commands.command(aliases=["steal"])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def rob(self, ctx, member : disnake.Member = None):
		"""Rob someone of their <:carrots:822122757654577183> from their wallet."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		if member is None:
			await ctx.send("You must specify the person you want to rob/steal from. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return
		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
			if member is None:
				await ctx.send("You must specify the user you want to mention. %s" % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return
			if member is ctx.author:
				await ctx.send("You cannot rob yourself. %s" % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			user = member
			author = ctx.author
			
			get_user_bal = await self.db.find_one({"_id": user.id})

			user_bal = get_user_bal["wallet"]

			author_bal = results["wallet"]

			if author_bal < 350:
				await ctx.send("You need `350` <:carrots:822122757654577183>  to rob someone! %s" % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			if user_bal < 250:
				await ctx.send('The user must have at least `250` <:carrots:822122757654577183> ! %s' % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			earnings = randint(250, user_bal)

			chance = randint(1, 10)


			if chance == 1:
				await self.db.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> ! {}".format(member.display_name, earnings, ctx.author.mention))

			elif chance == 3:
				await self.db.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> ! {}".format(member.display_name, earnings, ctx.author.mention))

			elif chance == 7:
				await self.db.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> ! {}".format(member.display_name, earnings, ctx.author.mention))

			elif chance == 10:
				await self.db.update_one({"_id": author.id}, {"$inc":{"wallet": earnings}})
				await self.db.update_one({"_id": user.id}, {"$inc":{"wallet": -earnings}})

				await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> ! {}".format(member.display_name, earnings, ctx.author.mention))

			else:
				await self.db.update_one({"_id": author.id}, {"$inc":{"wallet": -350}})

				await ctx.send("You failed in stealing from that person and you lost `350` <:carrots:822122757654577183> %s" % (ctx.author.mention))

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def slots(self, ctx, amount = None):
		"""Gamble your <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:

			if amount is None:
				await ctx.send('Please enter the amount. %s' % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			bal = results["wallet"]

			if amount.lower() == "all":
				amount = bal
			try:
				amount = amount.replace(",", "")
			except:
				pass
			try:
				amount = int(amount)
			except ValueError:
				return await ctx.reply("Not a number!")

			if amount > bal:
				await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			if amount < 300:
				await ctx.send('You must bet more than `300` <:carrots:822122757654577183>. %s' % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			prefinal = []
			for i in range(3):
				a = random.choice(["❌", "🇴", "✨", "🔥", "<:tfBruh:784689708890324992>", "👑"])

				prefinal.append(a)

				final = "\u2800┃\u2800".join(prefinal)

			embed = disnake.Embed(color=color.lightpink, title="Slots!", description="<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
			msg = await ctx.send(embed=embed)

			line1 = prefinal[0]
			line2 = prefinal[1]
			line3 = prefinal[2]



			if prefinal[0] == prefinal[1] == prefinal[2]:
				earned = 2.5*amount

				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

				wallet_amt = bal + earned

				em = disnake.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				em = disnake.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)
				
				print("Reached final edit")
				winembed = disnake.Embed(color=disnake.Color.green(), title="WIN!", description="{}\u2800┃\u2800{}\u2800┃\u2800{}\n\nYou bet a total of **{:,}** <:carrots:822122757654577183>  and won **{:,}** <:carrots:822122757654577183>. \nNow in wallet: **{:,}** <:carrots:822122757654577183>.".format(line1, line2, line3, amount, earned, wallet_amt))
				await asyncio.sleep(0.7)
				await msg.edit(embed=winembed)



			elif prefinal[0] == prefinal[1] or prefinal[0] == prefinal[2] or prefinal[2] == prefinal[1]:
				earned = amount

				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

				wallet_amt = bal + earned

				em = disnake.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				em = disnake.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				winembed = disnake.Embed(color=disnake.Color.green(), title="WIN!", description="{}\n\nYou won **{:,}** <:carrots:822122757654577183>. \nNow in wallet: **{:,}** <:carrots:822122757654577183>.".format(final, amount, wallet_amt))
				await asyncio.sleep(0.7)
				await msg.edit(embed=winembed)



			else:

				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -amount}})
				
				wallet_amt = bal - amount
			
				em = disnake.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				em = disnake.Embed(color=color.lightpink, title="Slots!", description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>")
				await asyncio.sleep(0.7)
				await msg.edit(embed=em)

				lostembed = disnake.Embed(color=color.red, title="LOST!", description="{}\n\nYou bet a total amount of **{:,}** <:carrots:822122757654577183>  but you lost them! :c\nNow in wallet: **{:,}** <:carrots:822122757654577183>.".format(final, amount, wallet_amt))
				await asyncio.sleep(0.7)
				await msg.edit(embed=lostembed)

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def beg(self, ctx):
		"""Beg for some <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
			earnings = randint(100, 500)

			await ctx.send(f"Someone gave you **{earnings}** <:carrots:822122757654577183> !!")

			await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def work(self, ctx):
		"""Work and get <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:

			await ctx.send("You worked and got **5,000** <:carrots:822122757654577183>. The carrots have been deposited into your bank!")

			await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"bank": 5000}})
		
		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def crime(self, ctx):
		"""Commit crimes that range between `small-medium-big`, and depending on which one you get, the more <:carrots:822122757654577183> you get, but be careful! You can lose the carrots as well."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:

			aaaa = randint(1, 7)
			earnings = randint(500, 1500)
			earningss = randint(100, 420)
			earningsss = randint(400, 800)
			earningssss = randint(5000, 50000)
			losts = randint(300, 700)

			if aaaa == 2:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})

				await ctx.send("<:weird:773538796087803934> you commited a bigger crime and got **{:,}** <:carrots:822122757654577183>.".format(earnings))
				return

			if aaaa == 4:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningss}})
				await ctx.send("<:weird:773538796087803934> you commited a smaller crime and got **{:,}** <:carrots:822122757654577183>.".format(earningss))
				return

			if aaaa == 6:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningsss}})
				await ctx.send("<:weird:773538796087803934> you commited a medium crime and got **{:,}** <:carrots:822122757654577183>.".format(earningsss))
				return

			if aaaa == 7:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssss}})
				await ctx.send("<:weird:773538796087803934> you commited a large crime and got **{:,}** <:carrots:822122757654577183>.".format(earningssss))
				return

			else:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
				await ctx.send("You lost **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
				return
		
		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command(name='guess-the-number', aliases=['gtn', 'guess'])
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def eco_gtn(self, ctx):
		"""Play a guess the number game and earn <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
			usercheck = ctx.author.id
			await ctx.send('Pick a number between 1 and 10.')

			lost_amt = randint(100, 400)
			win_amt = randint(130, 570)
			number = random.randint(1, 10)

			def check(message):
				return message.author.id == usercheck and message.channel.id == ctx.channel.id
			
			index = 0
			
			for guess in range(0,3):
				while True:
					try:
						msg = await self.bot.wait_for('message', timeout= 30 , check=check)
						attempt = int(msg.content)
						break
					except ValueError:
						await msg.reply("Not a number! %s" % (ctx.author.mention))
				if attempt > number:
					index += 1
					if index == 3:
						await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -lost_amt}})
						await msg.reply(content=f"You didn't get it and lost **{lost_amt}** <:carrots:822122757654577183>. The number was **{number}**.")
						return
					await msg.reply('Try going lower.')


				elif attempt < number:
					index += 1
					if index == 3:
						await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -lost_amt}})
						await msg.reply(content=f"You didn't get it and lost **{lost_amt}** <:carrots:822122757654577183>. The number was **{number}**.")
						return
					await msg.reply('Try going higher.')

					

				else:
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": win_amt}})
					await msg.reply(f'You guessed it! Good job! You got **{win_amt}** <:carrots:822122757654577183>. The number was **{number}**.')
					return
		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return
	
	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def ppsuck(self, ctx):
		"""Suck some pp 😳 for some quick <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

		if results != None:
			aaaa = randint(1, 7)
			bbbb = randint(1, 100)
			earnings = randint(800, 2500)
			earningss = randint(300, 620)
			earningsss = randint(600, 1200)
			earningssss = randint(20000, 150000)
			earningssssss = randint(500000, 5000000)
			losts = randint(1000, 1200)

			try:
				if bbbb == 1:
					earned = earningssssss	
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})	

					await ctx.send(":smirk: :smirk: :yum: you sucked your crush and they loved it, you ended up dating and got **{:,}** <:carrots:822122757654577183>.".format(earned))
					return
						
				elif aaaa == 1:
					earned = earnings	
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

					await ctx.send(":yum: you sucked ur dad's pp and got **{:,}** <:carrots:822122757654577183>.".format(earned))
					return

				elif aaaa == 4:
					earned = earningss	
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})

					await ctx.send("<:weird:773538796087803934> you didn't do too good of a job at sucking but it wasn't too bad either and got **{:,}** <:carrots:822122757654577183>.".format(earned))
					return
				
				elif aaaa == 6:
					earned = earningsss	
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
				
					await ctx.send("<:weird:773538796087803934> you didn't do too bad, but u didn't do too good either at sucking ur dog's pp and got **{:,}** <:carrots:822122757654577183>.".format(earned))
					return
				
				elif aaaa == 7:
					earned = earningssss	
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earned}})
					await ctx.send(":smirk: You sucked your best friend and they liked it very much and decided to gave you **{:,}** <:carrots:822122757654577183>".format(earned))
					return

				else:
					await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
					await ctx.send("You did a fucking bad job at sucking and lost **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
					
			except:
				ctx.command.reset_cooldown(ctx)
				return
		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def race(self, ctx):
		"""Participate in a race and earn <:carrots:822122757654577183>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		results = await self.db.find_one({"_id": ctx.author.id})

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
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earnings}})
				await ctx.send(":third_place: you won the race 3rd place an won: **{:,}** <:carrots:822122757654577183>.".format(earnings))
				return

			elif aaaa == 4:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningss}})
				await ctx.send("U were close to lose the race by getting 5th place. You got a total of: **{:,}** <:carrots:822122757654577183>.".format(earningss))
				return

			elif aaaa == 6:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningsss}})
				await ctx.send("After winning on 4th place you got: **{:,}** <:carrots:822122757654577183>.".format(earningsss))
				return

			elif aaaa == 7:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssss}})
				await ctx.send(":sparkles: :second_place: after winning on the 2nd place, you won: **{:,}** <:carrots:822122757654577183>.".format(earningssss))
				return

			elif bbbb == 1:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": earningssssss}})
				await ctx.send(":sparkles: :first_place: :medal: :sparkles: after winning the race on the first place you won a total of: **{:,}** <:carrots:822122757654577183>.".format(earningssssss))
				return

			else:
				await self.db.update_one({"_id": ctx.author.id}, {"$inc":{"wallet": -losts}})
				await ctx.send("Sadly you lost the race, your lost consists of **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
				return

		else:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return


	@commands.command(name='rock-paper-scissors', aliases=['rps', 'rockpaperscissors'])
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def eco_rps(self, ctx):
		"""Play a game of rock-paper-scissors with the bot and earn <:carrots:822122757654577183> if you win or lose some if you lose the game."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		user = ctx.author
		results = await self.db.find_one({"_id": user.id})
		if results == None:
			await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
			return
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		bot_rps = random.choice(rps)
		earned = randint(5000, 15000)
		await ctx.send("Please choose between `rock`/`paper`/`scissors`. You have **60** seconds to give your answer. %s" % (user.mention))
		try:
			while True:
				user_rps = 	await self.bot.wait_for('message', timeout= 60, check=check)
				user_rps = user_rps.content.lower()
				if not user_rps in rps:
					await ctx.send("You can only choose from `rock`/`paper`/`scissors`. %s" % (user.mention))
				else:
					break
		except asyncio.TimeoutError:
			await ctx.send("You ran out of time. %s" % (user.mention))
			return
		else:

			if user_rps == "rock":
				if bot_rps == "paper":
					await ctx.send("You chose `rock`, and i chose `paper`. You lost **325** <:carrots:822122757654577183>. %s" % (user.mention))
					await self.db.update_one({'_id': user.id}, {'$inc':{'wallet': -325}})
					return
				elif bot_rps == "scissors":
					await ctx.send("You chose `rock`, and i chose `scissors`. You won **{:,}** <:carrots:822122757654577183>. {}".format(earned, user.mention))
					await self.db.update_one({'_id': user.id}, {'$inc':{'wallet': earned}})
					return
				elif bot_rps == "rock":
					await ctx.send("We both chose `rock`. Nothing happened, your balance stays the same. %s" % (user.mention))
					ctx.command.reset_cooldown(ctx)
					return
			
			
			elif user_rps == "paper":
				if bot_rps == "scissors":
					await ctx.send("You chose `paper`, and i chose `scissors`. You lost **325** <:carrots:822122757654577183>. %s" % (user.mention))
					await self.db.update_one({'_id': user.id}, {'$inc':{'wallet': -325}})
					return
				elif bot_rps == "rock":
					await ctx.send("You chose `paper`, and i chose `rock`. You won **{:,}** <:carrots:822122757654577183>. {}".format(earned, user.mention))
					await self.db.update_one({'_id': user.id}, {'$inc':{'wallet': earned}})
					return
				elif bot_rps == "paper":
					await ctx.send("We both chose `paper`. Nothing happened, your balance stays the same. %s" % (user.mention))
					ctx.command.reset_cooldown(ctx)
					return
			
			elif user_rps == "scissors":
				if bot_rps == "rock":
					await ctx.send("You chose `scissors`, and i chose `rock`. You lost **325** <:carrots:822122757654577183>. %s" % (user.mention))
					await self.db.update_one({'_id': user.id}, {'$inc':{'wallet': -325}})
					return
				elif bot_rps == "paper":
					await ctx.send("You chose `scissors`, and i chose `paper`. You won **{:,}** <:carrots:822122757654577183>. {}".format(earned, user.mention))
					await self.db.update_one({'_id': user.id}, {'$inc':{'wallet': earned}})
					return
				elif bot_rps == "scissors":
					await ctx.send("We both chose `scissors`. Nothing happened, your balance stays the same. %s" % (user.mention))
					ctx.command.reset_cooldown(ctx)
					return

	@eco_rps.error
	async def rps_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f"Please wait: **{time_phaser(error.retry_after)}** before playing rps again. {ctx.author.mention}"
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)
		 
	@race.error
	async def race_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f"{ctx.author.mention} You cannot race that fast! Please wait: **{time_phaser(error.retry_after)}**."
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)
		
	@ppsuck.error
	async def ppsuck_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f"{ctx.author.mention} OK OK CHILLE, IK U WANT TO SUCK ON SOMETHING BUT PLEASE WAIT **{time_phaser(error.retry_after)}**."
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)

	@eco_gtn.error
	async def gtn_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f"{ctx.author.mention} You've already played the game, come back in **{time_phaser(error.retry_after)}**."
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)

	@crime.error
	async def crime_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f'{ctx.author.mention} You can commit crimes again in **{time_phaser(error.retry_after)}**.'
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)

	@work.error
	async def work_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f'{ctx.author.mention} You can work again in **{time_phaser(error.retry_after)}**.'
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)

	@beg.error
	async def beg_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f'{ctx.author.mention} You can have more <:carrots:822122757654577183>  in **{time_phaser(error.retry_after)}**.'
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)

	@rob.error
	async def steal_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f'{ctx.author.mention} You can steal more in **{time_phaser(error.retry_after)}**.'
			await ctx.send(msg)
		else:
			await self.bot.reraise(ctx, error)

	@slots.error
	async def slots_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = f'{ctx.author.mention} You can bet your carrots in the slots machine in **{time_phaser(error.retry_after)}**.'
			await ctx.send(msg)

		elif isinstance(error, commands.errors.MissingRequiredArgument):
			ctx.command.reset_cooldown(ctx)
			await self.bot.reraise(ctx, error)
		
		else:
			await self.bot.reraise(ctx, error)


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({"_id": member.id})




def setup(bot):
	bot.add_cog(Economy(bot))