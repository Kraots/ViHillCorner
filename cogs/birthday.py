import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
import os
from utils import time
import datetime
from dateutil.relativedelta import relativedelta
import asyncio

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
			preBday = result['birthdaydate']
			bdayDate = result['region_birthday']
			user = result['_id']

			if currentTime >= bdayDate:

				guild = self.client.get_guild(750160850077089853)
				bday_channel = guild.get_channel(797867811967467560)
				user = guild.get_member(user)

				em = discord.Embed(color=user.color, title=f"Happy birthday {user.name}!!! :tada: :tada:")

				msg = await bday_channel.send(user.mention, embed=em)
				await msg.add_reaction("🍰")
				
				new_birthday = bdayDate + relativedelta(years = 1)
				new_preBday = preBday + relativedelta(years = 1)
				collection.update_one({"_id": user.id}, {"$set":{"birthdaydate": new_preBday, "region_birthday": new_birthday}})
			

			

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
				region_birthday = data['region_birthday']

			def format_date(dt1, dt2):
				return f"{user.mention}'s birthday is in `{time.human_timedelta(dt1, accuracy=3)}` **({dt2:%Y/%m/%d})**"

			await ctx.send(format_date(region_birthday, birthday))
		
		else:
			if user.id == ctx.author.id:
				await ctx.send("You did not set your birthday! Type: `!birthday set month/day` to set your birthday.\n**Example:**\n\u2800`!birthday set 01/16`")
			else:
				await ctx.send("User did not set their birthday!")



	@birthday.command(aliases=['upcoming'])
	async def top(self, ctx):
		index = 0

		def format_date(dt1, dt2):
			return f"Birthday in  `{time.human_timedelta(dt1, accuracy = 3)}` ( **{dt2:%Y/%m/%d}** ) "

		em = discord.Embed(color=discord.Color.blurple(), title="***Top `5` upcoming birthdays***\n _ _ ") 

		results = collection.find().sort([("birthdaydate", 1)]).limit(5)
		for result in results:
			user = self.client.get_user(result['_id'])
			index += 1
			em.add_field(name=f"`{index}`. _ _ _ _ {user.name}", value=f"{format_date(result['region_birthday'], result['birthdaydate'])}", inline = False) 

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

		msg = """What is your timezone from this list (approx.):

`1` ->  **Pacific Time (US)** `UTC-8`
`2` ->  **Mountain Time (US)** `UTC-7`
`3` ->  **Central Time (US)** `UTC-6`
`4` ->  **Eastern Time (US)** `UTC-5`
`5` ->  **Rio de Janeiro, Brazil** `UTC-3`
`6` ->  **London, United Kingdom (UTC)** `GMT`
`7` ->  **Berlin, Germany** `UTC+1 / UTC+2`
`8` ->  **Moscow, Russian Federation** `UTC+3`
`9` ->  **Dubai, United Arab Emirates** `UTC+4`
`10` ->   **Mumbai, India** `UTC+5:30`
`11` ->   **Singapore, Singapore** `UTC+8`
`12` ->   **Tokyo, Japan** `UTC+9`
`13` ->   **Sydney, Australia** `UTC+11`
`14` ->   **Auckland, New Zealand** `UTC+13`\n\n***Please enter just the number!***""" 
		
		msg = await ctx.send(msg)

		def check(message):
			return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
			try:
				int(message.content)
				return True
			except ValueError:
				return False

		try:
			pre_region = await self.client.wait_for('message', timeout = 180, check = check)
			region = int(pre_region.content)

			if region == 1:
				region = "pacific time (us)"
				region_birthday = birthday + relativedelta(hours = 10)
			elif region == 2:
				region = "mountain time (us)"
				region_birthday = birthday + relativedelta(hours = 9)
			elif region == 3:
				region = "central time (us)"
				region_birthday = birthday + relativedelta(hours = 8)
			elif region == 4:
				region = "eastern time (us)"
				region_birthday = birthday + relativedelta(hours = 7)
			elif region == 5:
				region = "rio de janeiro, brazil"
				region_birthday = birthday + relativedelta(hours = 5)
			elif region == 6:
				region = "london, united kingdom (utc)"
				region_birthday = birthday
			elif region == 7:
				region = "berlin, germany"
				region_birthday = birthday - relativedelta(hours = 3)
			elif region == 8:
				region = "moscow, russian federation"
				region_birthday = birthday - relativedelta(hours = 4)
			elif region == 9:
				region = "dubai, united arab emirates"
				region_birthday = birthday - relativedelta(hours = 6)
			elif region == 10:
				region = "mumbai, india"
				region_birthday = birthday - relativedelta(hours = 7, minutes = 30)
			elif region == 11:
				region = "singapore, singapore"
				region_birthday = birthday - relativedelta(hours = 10)
			elif region == 12:
				region = "tokyo, japan"
				region_birthday = birthday - relativedelta(hours = 11)
			elif region == 13:
				region = "sydney, australia"
				region_birthday = birthday - relativedelta(hours = 13)
			elif region == 14:
				region = "auckland, new zealand"
				region_birthday = birthday - relativedelta(hours = 15)


			def format_date(dt1, dt2):
				return f"`{time.human_timedelta(dt1, accuracy=3)}` **({dt2:%Y/%m/%d})**"


			if user.id in all_users:
				collection.update_one({"_id": user.id}, {"$set":{"birthdaydate": birthday, "region": region, "region_birthday": region_birthday}})
				await ctx.message.delete()
				await msg.delete()
				await pre_region.delete()
				await ctx.send(f"Birthday set!\nYour birthday is in {format_date(region_birthday, birthday)} {user.mention}")
			
			else:
				post = {
						"_id": user.id,
						"birthdaydate": birthday,
						"region": region,
						"region_birthday": region_birthday
						}
				collection.insert_one(post)

				await ctx.message.delete()
				await msg.delete()
				await pre_region.delete()
				await ctx.send(f"Birthday set!\nYour birthday is in {format_date(region_birthday, birthday)} {user.mention}")



		except asyncio.TimeoutError:
			return



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




	@set.error
	async def bday_set(self, ctx, error):
		if isinstance(error, commands.errors.CommandOnCooldown):
			await ctx.send(f"You are on cooldown! Please try again in `{str(error.retry_after)[:4]}` seconds.")





def setup(client):
	client.add_cog(Birthdays(client))