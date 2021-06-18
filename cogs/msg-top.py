import discord
from discord.ext import commands, tasks
import motor.motor_asyncio
import os
import utils.colors as color
import datetime
from dateutil.relativedelta import relativedelta
from utils import time
import asyncio

BotChannels = [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]

DBKEY = os.getenv("MONGODBLVLKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Levels"]

class MessageTop(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.weekly_reset.start()
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix and ctx.channel.id in BotChannels

	@tasks.loop(minutes=1)
	async def weekly_reset(self):
		await self.client.wait_until_ready()
		results = await collection.find_one({"_id": 374622847672254466})
		resetWhen = results['weekly_reset']
		a = datetime.datetime.utcnow().strftime('%Y-%m-%d')
		dateNow = datetime.datetime.strptime(a, '%Y-%m-%d')
		
		if dateNow >= resetWhen:
			index = 0 
			results = collection.find().sort([("messages_count", -1)])
			for result in await results.to_list(3):
				index += 1
				user = self.client.get_user(result['_id'])
				if index == 1:
					await collection.update_one({'_id': result['_id']}, {'$inc':{'xp': 50000}})
					await user.send("Congrats. You placed `%s` in the weekly top! Your reward is **50,000** XP." % (index))
				elif index == 2:
					await collection.update_one({'_id': result['_id']}, {'$inc':{'xp': 30000}})
					await user.send("Congrats. You placed `%s` in the weekly top! Your reward is **30,000** XP." % (index))
				elif index == 3:
					await collection.update_one({'_id': result['_id']}, {'$inc':{'xp': 20000}})
					await user.send("Congrats. You placed `%s` in the weekly top! Your reward is **20,000** XP." % (index))

			await collection.update_many({}, {"$set": {"messages_count": 0}})
			x = dateNow + relativedelta(weeks = 1)
			await collection.update_one({'_id': 374622847672254466}, {'$set':{'weekly_reset': x}})



	@commands.group(invoke_without_command = True, case_insensitive = True, aliases=['msg-top', 'top-msg'])
	async def top(self, ctx):
		
		def format_time(dt):
			return time.human_timedelta(dt)

		data = await collection.find_one({"_id": 374622847672254466})

		em = discord.Embed(color=color.lightpink)
		
		index = 0
		guild = self.client.get_guild(750160850077089853)
		
		results = collection.find().sort([("messages_count", -1)])
		for result in await results.to_list(15):
			if result['messages_count'] != 0:
				index += 1
				mem = guild.get_member(result['_id'])
				if ctx.author == mem:
					em.add_field(name="**`#%s\u2800%s` (YOU)**" % (index, mem.name), value="`%s` messages" % (result['messages_count']), inline=False)
				else:
					em.add_field(name="`#%s`\u2800%s" % (index, mem.name), value="`%s` messages" % (result['messages_count']), inline=False)
		em.title = "Top `%s` most active members this week" % (index)
		em.set_footer(text="Resets in %s" % (format_time(data['weekly_reset'])), icon_url=ctx.author.avatar_url)

		await ctx.send(embed = em)
	
	@top.command(aliases = ['reset'])
	@commands.is_owner()
	async def __reset(self, ctx, member: discord.Member):
		def check(message):
			return message.author == ctx.author and message.channel == ctx.channel
		
		await ctx.send("Are you sure you want to reset the message count for this week for member %s? `yes` | `no`" % (member.mention))
		try:
			answer = await self.client.wait_for('message', timeout = 180, check=check)
			answer = answer.content.lower()
			if answer in ['no', 'cancel']:
				await ctx.send("Command to reset the message count for user `%s` has been canceled." % (member))
			elif answer == "yes":
				await collection.update_one({'_id': member.id}, {'$set':{'messages_count': 0}})
				await ctx.send('The message count for this week for member **%s** has been reset successfully.' % (member))
		except asyncio.TimeoutError:
			return

	@top.command(aliases=['reward'])
	async def rewards(self, ctx):
		em = discord.Embed(color=color.lightpink, title="Here are the rewards for the weekly top:")
		em.add_field(name="`1st Place`", value="**50k XP**", inline=False)
		em.add_field(name="`2nd Place`", value="**30k XP**", inline=False)
		em.add_field(name="`3rd Place`", value="**20k XP**", inline=False)
		em.set_footer(text="Requested by: %s" % (ctx.author), icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)

def setup(client):
	client.add_cog(MessageTop(client))
