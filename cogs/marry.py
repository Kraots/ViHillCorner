import discord
from discord.ext import commands
import json
import asyncio

class MarryCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def marry(self, ctx, member : discord.Member = None):
		if member == None:
			await ctx.send("You must specifiy the user u want to marry.")
			return
		
		elif member == ctx.author:
			await ctx.send("You cannot marry yourself.")
			return
		
		else:
			users = await get_marry_data()

			try:
				member_married_to = users[str(member.id)]["married_to"]
			
			except:
				pass
			
			try:
				author_married_to = users[str(ctx.author.id)]["married_to"]
			
			except:
				pass

			if str(member.id) in users:
				they_already_married_to = self.client.get_user(member_married_to)
				await ctx.send("`{}` is already married to `{}`.".format(member.display_name, they_already_married_to.display_name))
				return

			elif str(ctx.author.id) in users:
					author_already_married_to = self.client.get_user(author_married_to)
					await ctx.send("You are already married to `{}`.".format(author_already_married_to.display_name))
					

			else:
				def message_check(m):
					return m.author.id == member.id and m.channel.id == ctx.channel.id

				await ctx.send("{} do you want to marry {}? `yes` | `no`".format(member.mention, ctx.author.mention))

				try:
					rresponse = await self.client.wait_for('message', timeout=180, check=message_check)
					response = rresponse.content.lower()

					if response == "yes":

						users[str(ctx.author.id)] = {}
						users[str(ctx.author.id)]["married_to"] = member.id

						users[str(member.id)] = {}
						users[str(member.id)]["married_to"] = ctx.author.id

						with open("marry-data.json", "w") as f:
							json.dump(users, f)

						await ctx.send("`{}` married `{}`!!! :tada: :tada:".format(ctx.author.display_name, member.display_name))

					elif response == "no":
						await ctx.send("`{}` does not want to marry with you. :pensive: :fist:".format(member.display_name))

				
				except asyncio.TimeoutError:
					await ctx.send("`{}` did not answer in time!".format(member.display_name))
					return
			

	@commands.command()
	async def divorce(self, ctx):
		users = await get_marry_data()
		user = ctx.author

		try:
			user_married_to = users[str(user.id)]["married_to"]
		except KeyError:
			await ctx.send("You are not married to anyone.")
			return
		
		else:
			the_married_to_user = self.client.get_user(user_married_to)

			def check(m):
				return m.author.id == user.id and m.channel.id == ctx.channel.id

			await ctx.send("Are you sure you want to divorce `{}` ? `yes` | `no`".format(the_married_to_user.display_name))
			
			try:
				rresponse = await self.client.wait_for('message', timeout = 180, check=check)
				response = rresponse.content.lower()

				if response == "yes":
					del users[str(user.id)]
					del users[str(the_married_to_user.id)]

					with open("marry-data.json", "w") as f:
						json.dump(users, f)
					
					await ctx.send("You divorced `{}`. :cry:".format(the_married_to_user.display_name))

				elif response == "no":
					await ctx.send("You did not divorce that person :D")
					return

			except asyncio.TimeoutError:
				await ctx.send("Did not give answer in time :/")
				return


	@commands.command()
	async def marriedwho(self, ctx, member : discord.Member = None):
		if member == None:
			member = ctx.author

		users = await get_marry_data()
		user = member

		try:
			user_married_to = users[str(user.id)]["married_to"]
		except KeyError:
			await ctx.send("You are not married to anyone.\nType `!marry <user>` to marry to someone!")
			return
		
		else:
			the_married_to_user = self.client.get_user(user_married_to)

			if member == ctx.author:
				await ctx.send("You are married to `{}` :tada: :tada: ".format(the_married_to_user.display_name))
			else:
				await ctx.send("`{}` is married to `{}` :tada: :tada: ".format(member.display_name, the_married_to_user.display_name))


async def get_marry_data():
	with open("marry-data.json", "r") as f:
		users = json.load(f)
	
	return users

def setup(client):
	client.add_cog(MarryCommands(client))