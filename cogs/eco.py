import discord
from discord.ext import commands
import json 
from random import randint
import random
import utils.colors as color
import asyncio

class EcoCommands(commands.Cog):

	def __init__(self, client):
		self.client = client


			# LEADERBOARD

	@commands.command(aliases=['lb'])
	async def leaderboard(self, ctx, x = 10):
		users = await get_bank_data()
		leader_board = {}
		total = []
		for user in users:
			name = int(user)
			total_amount = users[user]["wallet"] + users[user]["bank"]
			leader_board[total_amount] = name
			total.append(total_amount)

		total = sorted(total, reverse = True)

		em = discord.Embed(title=f"Top {x} richest people", color=color.reds)
		index = 1
		for amt in total:
			id_ = leader_board[amt]
			mem = self.client.get_user(id_)
			name = mem.name
			em.add_field(name=f"{index}. {name}", value=f"`{amt}` coins", inline=False)
			if index == x:
				break
			
			else:
				index += 1

		await ctx.send(embed=em)



            # BALANCE

	@commands.group(invoke_without_command=True, aliases=['bal'])
	async def balance(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		await open_account(member)
		user = member
		users = await get_bank_data()

		wallet_amt = users[str(user.id)]['wallet']
		bank_amt = users[str(user.id)]['bank']

		em = discord.Embed(title=f"{member.name}'s balance", color=color.lightpink)
		em.add_field(name="Wallet Balance", value=f"`{wallet_amt}`", inline=False)
		em.add_field(name="Bank Balance", value=f"`{bank_amt}`", inline=False)
		await ctx.send(embed=em)

	@balance.command()
	@commands.has_role('Staff')
	async def add(self, ctx, amount = None, member: discord.Member = None):
		kraots = self.client.get_user(374622847672254466)
		if member is None:
			member = ctx.author

		if amount is None:
			await ctx.send("Please specify the amount of money you want to add!")
			return

		await open_account(member)

		amount = int(amount)

		await update_bank(member, amount, "bank")

		await ctx.send(f"Successfully added `{amount}` coins!")
		embed = discord.Embed(color=color.lightpink, title="BALANCE ADD", description=f"`{ctx.author}` added `{amount}` coins to `{member}`.\n\n`{ctx.author.id}` - person who added the money\n`{member.id}` - person who got the money")
		await kraots.send(embed=embed)




 			# WITHDRAW


	@commands.group(aliases=['with'])
	async def withdraw(self, ctx, amount = None):
		await open_account(ctx.author)
		
		if amount is None:
			await ctx.send('Please enter the amount you want to withdraw.')
			return

		bal = await update_bank(ctx.author)

		if amount == "all":
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

		await ctx.send(f"Successfully withdrew `{amount}` coins!")


			# DEPOSIT


	@commands.command(aliases=['dep'])
	async def deposit(self, ctx, amount = None):
		await open_account(ctx.author)
		
		if amount is None:
			await ctx.send('Please enter the amount you want to withdraw.')
			return

		bal = await update_bank(ctx.author)
		if amount == "all":
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

		await ctx.send(f"Successfully deposited `{amount}` coins!")


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

		await ctx.send(f"You gave `{amount}` coins to {member.name}.")



			# ROB


	@commands.command(aliases=["steal"])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def rob(self, ctx, member : discord.Member):
		await open_account(ctx.author)
		await open_account(member)
		
		bal = await update_bank(member)
		ball = await update_bank(ctx.author)

		if ball[0] < 350:
			await ctx.send("You need `350` coins to rob someone!")
			return

		if bal[0] < 250:
			await ctx.send('The user must have at least `250` coins!')
			return

		earnings = randint(250, bal[0])

		await update_bank(ctx.author, earnings)
		await update_bank(member, -1*earnings, "wallet")

		await ctx.send(f"You robbed {member.name} and got `{earnings}` coins!")



			# SLOTS


	@commands.command()
	#@commands.cooldown(1, 7, commands.BucketType.user)
	async def slots(self, ctx, amount = None):
		await open_account(ctx.author)
		
		if amount is None:
			await ctx.send('Please enter the amount you want to withdraw.')
			return

		
		bal = await update_bank(ctx.author)
		if amount == "all":
			amount = bal[0]
		
		amount = int(amount)
		
		if amount > bal[0]:
			await ctx.send('You do not own that much money!')
			return

		if amount < 300:
			await ctx.send('You must bet more than `300` coins.')
			return

		final = []
		for i in range(3):
			a = random.choice(["❌", "🇴", "🅰️", "✨", "🔥", "<:tfBruh:784689708890324992>", "👑"])

			final.append(a)

			embed = discord.Embed(color=color.lightpink, title="Slots!", description=f"{final}")
		msg = await ctx.send(embed=embed)

		if final[0] == final[1] == final[2]:
			await update_bank(ctx.author, 2.5*amount)
			winembed = discord.Embed(color=discord.Color.green(), title="WIN!", description=f"{final}\n\nYou won `{2.5*amount}` coins")
			await asyncio.sleep(0.2)
			await msg.edit(embed=winembed)

		elif final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
			await update_bank(ctx.author, 2*amount)
			winembed = discord.Embed(color=discord.Color.green(), title="WIN!", description=f"{final}\n\nYou won `{2*amount}` coins")
			await asyncio.sleep(0.2)
			await msg.edit(embed=winembed)

		else:
			await update_bank(ctx.author, -1*amount)
			lostembed = discord.Embed(color=color.red, title="LOST!", description=f"{final}\n\nYou lost `{amount}` coins")
			await asyncio.sleep(0.2)
			await msg.edit(embed=lostembed)




			# BEG


	@commands.command()
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def beg(self, ctx, member : discord.Member = None):
		if member is None:
			member = ctx.author

		await open_account(member)
		user = member
		users = await get_bank_data()

		earnings = randint(100, 500)

		await ctx.send(f"Someone gave you `{earnings}` coins!!")


		users[str(user.id)]['wallet'] += earnings


		with open("mainbank.json", "w") as f:
			json.dump(users, f)

	@beg.error
	async def beg_error(sel, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = 'You can have more coins in **{:.2f}**seconds.'.format(error.retry_after)
				await ctx.channel.send(msg)

	@rob.error
	async def steal_error(sel, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = 'You can steal more in **{:.2f}**seconds.'.format(error.retry_after)
				await ctx.channel.send(msg)

	@slots.error
	async def slots_error(sel, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				msg = 'You can bet your money in te slots machine in **{:.2f}**seconds.'.format(error.retry_after)
				await ctx.channel.send(msg)














async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False

	else:
		users[str(user.id)] = {}
		users[str(user.id)]['wallet'] = 0
		users[str(user.id)]['bank'] = 0

	with open("mainbank.json", "w") as f:
		json.dump(users, f)

	return True

async def get_bank_data():
	with open("mainbank.json", "r") as f:
		users = json.load(f)

	return users

async def update_bank(user, change = 0, mode = "wallet"):
	users = await get_bank_data()
	users[str(user.id)][mode] += change
	
	with open("mainbank.json", "w") as f:
		json.dump(users, f)

	bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
	return bal





def setup (client):
	client.add_cog(EcoCommands(client))