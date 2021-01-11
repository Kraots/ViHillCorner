import discord
from discord.ext import commands
import asyncio
import datetime
from datetime import date
import utils.colors as color
from utils import time
from pymongo import MongoClient
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Marry Data"]


class MarryCommands(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command()
	async def marry(self, ctx, member : discord.Member = None):
		if member == None:
			await ctx.reply("You must specifiy the user u want to marry.")
			return

		elif member == ctx.author:
			await ctx.reply("You cannot marry yourself.")
			return
		

		elif member.bot:
			await ctx.reply("Sad kid u can't marry bots smh.")
			return

		else:
			all_users = []
			results = collection.find()
			for result in results:
				all_users.append(result['_id'])

			if str(member.id) in all_users:
				get_mem = collection.find({"_id": member.id})
				for data in get_mem:
					member_married_to = data["married_to"]
				they_already_married_to = self.client.get_user(member_married_to)
				await ctx.send("`{}` is already married to `{}`.".format(member.display_name, they_already_married_to.display_name))
				return

			elif str(ctx.author.id) in all_users:
					get_auth = collection.find({"_id": member.id})
					for info in get_auth:
						author_married_to = info["married_to"]
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

						save_auth = {"_id": ctx.author.id, "married_to": member.id, "marry_date": married_since_save_time}
						save_mem = {"_id": member.id, "married_to": ctx.author.id, "marry_date": married_since_save_time}
						
						collection.insert_many([save_auth, save_mem])

						await ctx.send("`{}` married `{}`!!! :tada: :tada:".format(ctx.author.display_name, member.display_name))

					elif response == "no":
						await ctx.send("`{}` does not want to marry with you. :pensive: :fist:".format(member.display_name))

				
				except asyncio.TimeoutError:
					await ctx.send("`{}` did not answer in time!".format(member.display_name))
					return
			

	@commands.command()
	async def divorce(self, ctx):
		user = ctx.author

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		if not user.id in all_users:
			await ctx.reply("You are not married to anyone.")
			return
		
		else:
			get_marry = collection.find({"_id": user.id})
			for married in get_marry:
				the_married_to_user = self.client.get_user(married['married_to'])

			def check(m):
				return m.author.id == user.id and m.channel.id == ctx.channel.id

			await ctx.reply("Are you sure you want to divorce `{}` ? `yes` | `no`".format(the_married_to_user.display_name))
			
			try:
				rresponse = await self.client.wait_for('message', timeout = 180, check=check)
				response = rresponse.content.lower()

				if response == "yes":
					auth = {"_id": ctx.author.id} 
					mem = {"_id": the_married_to_user.id}
					collection.delete_one(auth)
					collection.delete_one(mem)
					
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

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
	
		user = member
		
		if user.bot:
			await ctx.reply("Bot's cannot marry u dumbo <:pepe_cringe:750755809700348166>")
			return

		elif not user.id in all_users:
			if user == ctx.author:
				await ctx.reply("You are not married to anyone.\nType `!marry <user>` to marry to someone!")
				return

			else:
				await ctx.reply("`{}` is not married to anyone.".format(user.display_name))
				return

		else:
			get_info = collection.find({"_id": user.id})
			for data in get_info:
				user_married_to = data["married_to"]
				user_married_to_sincee = data["marry_date"]

			user_married_to_since = datetime.datetime.strptime(user_married_to_sincee, "%Y-%m-%d %H:%M")

			the_married_to_user = self.client.get_user(user_married_to)

			if member == ctx.author:
				def format_date(dt):
					if dt is None:
						return 'N/A'
					return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

				em = discord.Embed(color=color.lightpink, title="You are married to `{}` :tada: :tada:".format(the_married_to_user.display_name))
				em.add_field(name="_ _ \nMarried since:", value="`{}`".format(format_date(user_married_to_since)), inline=False)
				em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
				await ctx.reply(embed=em)
			else:
				def format_date(dt):
					if dt is None:
						return 'N/A'
					return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

				em = discord.Embed(color=color.lightpink, title="`{}` is married to `{}` :tada: :tada:".format(user.display_name, the_married_to_user.display_name))
				em.add_field(name=" _ _ \nMarried since:", value="`{}`".format(format_date(user_married_to_since)), inline=False)
				em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
				await ctx.reply(embed=em)


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection.delete_one({"_id": member.id})
		collection.delete_one({'married_to': member.id})

def setup(client):
	client.add_cog(MarryCommands(client))