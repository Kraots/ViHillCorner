import discord
from discord.ext import commands, tasks
from utils import time
import datetime
from dateutil.relativedelta import relativedelta
import asyncio


class Birthdays(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Birthdays']
		self.prefix = "!"
		self.check_bdays.start()
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@tasks.loop(minutes=30)
	async def check_bdays(self):
		await self.bot.wait_until_ready()
		currentTime = datetime.datetime.utcnow()
		results = await self.db.find().to_list(100000)
		for result in results:
			preBday = result['birthdaydate']
			bdayDate = result['region_birthday']
			user = result['_id']

			if currentTime >= bdayDate:

				guild = self.bot.get_guild(750160850077089853)
				bday_channel = guild.get_channel(797867811967467560)
				user = guild.get_member(user)

				em = discord.Embed(color=user.color, title=f"Happy birthday {user.name}!!! :tada: :tada:")

				msg = await bday_channel.send(user.mention, embed=em)
				await msg.add_reaction("🍰")
				
				new_birthday = bdayDate + relativedelta(years = 1)
				new_preBday = preBday + relativedelta(years = 1)
				await self.db.update_one({"_id": user.id}, {"$set":{"birthdaydate": new_preBday, "region_birthday": new_birthday}})
			

			

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bday', 'b-day'])
	async def birthday(self, ctx, member: discord.Member = None):
		"""See when the member's birthday is, if any"""

		if member is None:
			member = ctx.author
		user = member
		results = await self.db.find_one({"_id": user.id})

		if results is None:
			if user.id == ctx.author.id:
				await ctx.send("You did not set your birthday! Type: `!birthday set month/day` to set your birthday.\n**Example:**\n\u2800`!birthday set 01/16`")
			else:
				await ctx.send("User did not set their birthday!")
			return

		birthday = results['birthdaydate']
		region_birthday = results['region_birthday']

		def format_date(dt1, dt2):
			return f"{user.mention}'s birthday is in `{time.human_timedelta(dt1, accuracy=3)}` **({dt2:%Y/%m/%d})**"

		await ctx.send(format_date(region_birthday, birthday))



	@birthday.command(name='top', aliases=['upcoming'])
	async def bday_top(self, ctx):
		"""See top 5 upcoming birthdays"""

		index = 0

		def format_date(dt1, dt2):
			return f"Birthday in  `{time.human_timedelta(dt1, accuracy = 3)}` ( **{dt2:%Y/%m/%d}** ) "

		em = discord.Embed(color=discord.Color.blurple(), title="***Top `5` upcoming birthdays***\n _ _ ") 

		results = await self.db.find().sort([("birthdaydate", 1)]).to_list(5)
		for result in results:
			user = self.bot.get_user(result['_id'])
			index += 1
			em.add_field(name=f"`{index}`. _ _ _ _ {user.name}", value=f"{format_date(result['region_birthday'], result['birthdaydate'])}", inline = False) 

		await ctx.send(embed=em)



	@birthday.command(name='set', aliases=['add'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def bday_set(self, ctx, *, bday = None):
		"""Set your birthday"""

		if bday is None:
			await ctx.send("Please insert a birthday! Please type `!birthday set month/day`.\n**Example:**\n\u2800`!birthday set 01/16`")
			ctx.command.reset_cooldown(ctx)
			return
		user = ctx.author
		results = await self.db.find_one({"_id": user.id})

		z = datetime.datetime.utcnow().strftime('%Y')
		pre = f'{z}/{bday}'

		try:
			birthday = datetime.datetime.strptime(pre, "%Y/%m/%d")

		except ValueError:
			await ctx.reply("That is not a valid date!\n**Valid Dates:**\n\u2800`-` 04/24\n\u2800`-` 01/09\n\u2800`-` 12/01\n\n**Example:**\n\u2800`!birthday set 04/27`")
			

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

		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel

		try:
			while True:
				pre_region = await self.bot.wait_for('message', timeout = 180, check = check)
				try:
					region = int(pre_region.content)
					if region > 14 or region < 1:
						await pre_region.reply("Please choose a number that is shown there that corresponds with your region, not another that is higher or smaller.")
					else:
						break
				except ValueError:
					await pre_region.reply("That is not a number.")

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
				region_birthday = birthday + relativedelta(hours = 3)
			elif region == 8:
				region = "moscow, russian federation"
				region_birthday = birthday + relativedelta(hours = 4)
			elif region == 9:
				region = "dubai, united arab emirates"
				region_birthday = birthday + relativedelta(hours = 6)
			elif region == 10:
				region = "mumbai, india"
				region_birthday = birthday + relativedelta(hours = 7, minutes = 30)
			elif region == 11:
				region = "singapore, singapore"
				region_birthday = birthday + relativedelta(hours = 10)
			elif region == 12:
				region = "tokyo, japan"
				region_birthday = birthday + relativedelta(hours = 11)
			elif region == 13:
				region = "sydney, australia"
				region_birthday = birthday + relativedelta(hours = 13)
			elif region == 14:
				region = "auckland, new zealand"
				region_birthday = birthday + relativedelta(hours = 15)


			def format_date(dt1, dt2):
				return f"`{time.human_timedelta(dt1, accuracy=3)}` **({dt2:%Y/%m/%d})**"


			if results != None:
				await self.db.update_one({"_id": user.id}, {"$set":{"birthdaydate": birthday, "region": region, "region_birthday": region_birthday}})
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
				await self.db.insert_one(post)

				await ctx.message.delete()
				await msg.delete()
				await pre_region.delete()
				await ctx.send(f"Birthday set!\nYour birthday is in {format_date(region_birthday, birthday)} {user.mention}")



		except asyncio.TimeoutError:
			await ctx.send("Ran out of time.")
			return



	@birthday.command(name='delete', aliases=['remove'])
	async def bday_delete(self, ctx):
		"""Delete your birthday"""

		results = await self.db.find_one({"_id": ctx.author.id})
		if results != None:
			def check(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
			msg = await ctx.send("Are you sure you want to remove your birthday? %s" % (ctx.author.mention))
			await msg.add_reaction('<:agree:797537027469082627>')
			await msg.add_reaction('<:disagree:797537030980239411>')
			try:
				reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)

			except asyncio.TimeoutError:
				new_msg = f"{ctx.author.mention} Did not react in time."
				await msg.edit(content=new_msg)
				await msg.clear_reactions()
				return
			
			else:
				if str(reaction.emoji) == '<:agree:797537027469082627>':
					await self.db.delete_one({"_id": ctx.author.id})
					e = "Succesfully removed your birthday from the list! {}".format(ctx.author.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return
				
				elif str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = "Birthday has not been removed. %s" % (ctx.author.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return

		else:
			await ctx.send("You did not set your birthday, therefore you don't have what to delete! Type: `!birthday set <day | month>` to set your birthday.")




	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({"_id": member.id})




	@bday_set.error
	async def bday_set_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandOnCooldown):
			await ctx.send(f"You are on cooldown! Please try again in `{str(error.retry_after)[:4]}` seconds.")
		else:
			await self.bot.reraise(ctx, error)




def setup(bot):
	bot.add_cog(Birthdays(bot))