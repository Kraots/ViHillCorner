import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
import os
from utils import time
import datetime
from dateutil.relativedelta import relativedelta

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Birthdays"]


class Birthdays(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
		self.check_bdays.start()
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@tasks.loop(seconds=30)
	async def check_bdays(self):
		await self.client.wait_until_ready()
		get_time = datetime.datetime.now().strftime("%Y/%m/%d")
		currentTime = datetime.datetime.strptime(get_time, "%Y/%m/%d")
		results = collection.find({})
		for result in results:
			bdayDate = result['birthdaydate']
			user = result['_id']

			if currentTime == bdayDate:

				guild = self.client.get_guild(750160850077089853)
				bday_channel = guild.get_channel(797867811967467560)
				user = guild.get_member(user)

				em = discord.Embed(color=user.color, title=f"Happy birthday {user.name}!!! :tada: :tada:")

				msg = await bday_channel.send(user.mention, embed=em)
				await msg.add_reaction("🍰")
				
				new_birthday = bdayDate + relativedelta(years=1)
				collection.update_one({"_id": user.id}, {"$set":{"birthdaydate": new_birthday}})

			elif currentTime > bdayDate:
				
				new_birthday = bdayDate + relativedelta(years=1)
				collection.update_one({"_id": user}, {"$set":{"birthdaydate": new_birthday}})
			

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bday', 'b-day'])
	async def birthday(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		user = member

		if user.id in all_users:

			get_data = collection.find({"_id": user.id})
			for data in get_data:
				birthday = data['birthdaydate']

			def format_date(dt):
				if dt is None:
					return 'N/A'
				return f"{user.mention}'s birthday is in `{time.human_timedelta(dt, accuracy=3)}` **({dt:%Y/%m/%d})**"

			await ctx.send(format_date(birthday))
		
		else:
			if user.id == ctx.author.id:
				await ctx.send("You did not set your birthday! Type: `!birthday set month/day` to set your birthday.\n**Example:**\n\u2800`!birthday set 01/16`")
			else:
				await ctx.send("User did not set their birthday!")



	@birthday.command(aliases=['upcoming'])
	async def top(self, ctx):
		index = 0

		def format_date(dt):
			return f"Birthday in  `{time.human_timedelta(dt, accuracy = 3)}` ( **{dt:%Y/%m/%d}** ) "

		em = discord.Embed(color=discord.Color.blurple(), title="***Top `5` upcoming birthdays***\n _ _ ") 

		results = collection.find().sort([("birthdaydate", 1)]).limit(5)
		for result in results:
			user = self.client.get_user(result['_id'])
			index += 1
			em.add_field(name=f"`{index}`. _ _ _ _ {user.name}", value=f"{format_date(result['birthdaydate'])}", inline = False) 

		await ctx.send(embed=em)



	@birthday.command(aliases=['add'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def set(self, ctx, *, bday = None):
		if bday is None:
			await ctx.send("Please insert a birthday! Please type `!birthday set month/day`.\n**Example:**\n\u2800`!birthday set 01/16`")
			ctx.command.reset_cooldown(ctx)
			return
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		user = ctx.author

		z = datetime.datetime.utcnow().strftime('%Y')
		pre = f'{z}/{bday}'
		
		try:
			birthday = datetime.datetime.strptime(pre, "%Y/%m/%d")
		except ValueError:
			await ctx.send("That is not a valid date!\n**Valid Dates:**\n\u2800`-` 04/24\n\u2800`-` 01/09\n\u2800`-` 12/01\n\n**Example:**\n\u2800`!birthday set 04/27`")
			return

		dateNow = datetime.datetime.now().strftime("%Y/%m/%d")
		dateNow = datetime.datetime.strptime(dateNow, "%Y/%m/%d")

		if dateNow > birthday:
			birthday = birthday + relativedelta(years=1)

		if user.id in all_users:
			collection.update_one({"_id": user.id}, {"$set":{"birthdaydate": birthday}})
		
		else:
			post = {
					"_id": user.id,
					"birthdaydate": birthday
					}
			collection.insert_one(post)

		def format_date(dt):
			if dt is None:
				return 'N/A'
			return f"`{time.human_timedelta(dt, accuracy=3)}` **({dt:%Y/%m/%d})**"

		await ctx.message.delete()
		await ctx.send(f"Birthday set!\nYour birthday is in {format_date(birthday)} {user.mention}")



	@birthday.command(aliases=['remove'])
	async def delete(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		if ctx.author.id in all_users:
			collection.delete_one({"_id": ctx.author.id})
			await ctx.send("Succesfully deleted your birthday from the list! {}".format(ctx.author.mention))

		else:
			await ctx.send("You did not set your birthday, therefore you don't have what to delete! Type: `!birthday set <day | month>` to set your birthday.")




	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection.delete_one({"_id": member.id})










def setup(client):
	client.add_cog(Birthdays(client))