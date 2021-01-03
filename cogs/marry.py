import discord
from discord.ext import commands
import json
import asyncio
import datetime
from datetime import date
import utils.colors as color
from utils import time

class MarryCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command()
	async def marry(self, ctx, member : discord.Member = None):
		if member == None:
			await ctx.send("You must specifiy the user u want to marry.")
			return

		elif member == ctx.author:
			await ctx.send("You cannot marry yourself.")
			return
		
		elif member.id == 374622847672254466:
			await ctx.send("no...")
			return

		elif member.bot:
			await ctx.send("Sad kid u can't marry bots smh.")
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
						
						married_since_save_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")

						users[str(ctx.author.id)] = {}
						users[str(ctx.author.id)]["married_to"] = member.id
						users[str(ctx.author.id)]["marry_date"] = married_since_save_time

						users[str(member.id)] = {}
						users[str(member.id)]["married_to"] = ctx.author.id
						users[str(member.id)]["marry_date"] = married_since_save_time

						with open("marry-data.json", "w", encoding="utf-8") as f:
							json.dump(users, f, ensure_ascii = False, indent = 4)

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

					with open("marry-data.json", "w", encoding="utf-8") as f:
							json.dump(users, f, ensure_ascii = False, indent = 4)
					
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
			user_married_to_sincee = users[str(user.id)]["marry_date"]
			user_married_to_since = datetime.datetime.strptime(user_married_to_sincee, "%Y-%m-%d %H:%M")
		
		except KeyError:
			if user == ctx.author:
				await ctx.send("You are not married to anyone.\nType `!marry <user>` to marry to someone!")
				return

			else:
				await ctx.send("`{}` is not married to anyone.".format(user.display_name))
				return

		else:
			the_married_to_user = self.client.get_user(user_married_to)

			if member == ctx.author:
				def format_date(dt):
					if dt is None:
						return 'N/A'
					return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

				em = discord.Embed(color=color.lightpink, title="You are married to `{}` :tada: :tada:".format(the_married_to_user.display_name))
				em.add_field(name="_ _ \nMarried since:", value="`{}`".format(format_date(user_married_to_since)), inline=False)
				em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=em)
			else:
				def format_date(dt):
					if dt is None:
						return 'N/A'
					return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

				em = discord.Embed(color=color.lightpink, title="`{}` is married to `{}` :tada: :tada:".format(user.display_name, the_married_to_user.display_name))
				em.add_field(name=" _ _ \nMarried since:", value="`{}`".format(format_date(user_married_to_since)), inline=False)
				em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=em)


async def get_marry_data():
	with open("marry-data.json", "r") as f:
		users = json.load(f)
	
	return users

def setup(client):
	client.add_cog(MarryCommands(client))