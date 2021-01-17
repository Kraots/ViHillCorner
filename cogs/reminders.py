import discord
from discord.ext import commands, tasks
from utils import time
import motor.motor_asyncio
import os
import utils.colors as color
import textwrap
import datetime

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Reminders"]

class RemindersClass(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
		self.check_current_reminders.start()
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
	
	@commands.group(invoke_without_command = True, case_insensitive = True, aliases=['reminder'])
	async def remind(self, ctx, *, when: time.UserFriendlyTime(commands.clean_content, default='\u2026')):
		results = collection.find().sort([("_id", -1)])

		for result in await results.to_list(1):
			newID = result['_id'] + 1
		
		try:
			newID = newID
		except UnboundLocalError:
			newID = 1324

		post = {"_id": newID,
				"userID": ctx.author.id,
				"channel": ctx.channel.id,
				"remindWhen": when.dt,
				"remindWhat": when.arg,
				"timeNow": datetime.datetime.utcnow(),
				"messageJumpUrl": ctx.message.jump_url	
				}
		
		await collection.insert_one(post)
		delta = time.human_timedelta(when.dt, accuracy=3)
		await ctx.send(f"Alright {ctx.author.mention}, in **{delta}**: {when.arg}")
	
	@remind.command()
	async def list(self, ctx):
		results = collection.find({"userID": ctx.author.id}).sort([("remindWhen", 1)])
		em = discord.Embed(color=color.lightpink, title="Reminders")
		index = 0
		total_reminders = 0
		z = collection.find({"userID": ctx.author.id}).sort([("remindWhen", 1)])
		
		for x in await z.to_list(9999999999999):
			total_reminders += 1

		for result in await results.to_list(10):
			index += 1
			shorten = textwrap.shorten(result['remindWhat'], width=320)
			em.add_field(name=f"(ID)`{result['_id']}`: In {time.human_timedelta(result['remindWhen'])}", value=shorten, inline=False)
		
		if len(em) < 12:
			await ctx.send("No currently running reminders.")
			return
		em.set_footer(text="Showing %s/%s reminders." % (index, total_reminders))
		await ctx.send(embed=em)
	
	@remind.command(aliases=['delete', 'cancel'], ignore_extra = False)
	async def remove(self, ctx, id: int):
		results = await collection.find_one({"_id": id})
		if results != None:
			if results['userID'] == ctx.author.id:
				await collection.delete_one({"_id": id})
				await ctx.send("Succesfully canceled the reminder.")
				return
			else:
				await ctx.send("That reminder is not yours!")
				return
		else:
			await ctx.send("No reminder with that ID.")
			return

	@remind.command(ignore_extra = False)
	async def clear(self, ctx):
		results = await collection.find_one({"userID": ctx.author.id})
		if results != None:
			await collection.delete_many({"userID": ctx.author.id})
			await ctx.send("Succesfully cleared all your reminders.")
			return
		else:
			await ctx.send("No currently running reminders.")


	@tasks.loop(seconds=5)
	async def check_current_reminders(self):
		await self.client.wait_until_ready()
		currentTime = datetime.datetime.now()
		results = collection.find()
		for result in await results.to_list(99999999999999999):
			expireDate = result['remindWhen']
			remindID = result['_id']
			user = result['userID']
			remindedWhen = result['timeNow']
			remindWhat = result['remindWhat']
			remindUrl = result['messageJumpUrl']
			channelID = result['channel']

			if currentTime >= expireDate:
				guild = self.client.get_guild(750160850077089853)
				remindChannel = guild.get_channel(channelID)
				msg = f"<@!{user}>, **{time.human_timedelta(remindedWhen)}**: {remindWhat}\n\n{remindUrl}"
				await remindChannel.send(msg)
				await collection.delete_one({"_id": remindID})

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		await collection.delete_many({"userID": member.id})
	
	@remind.error
	async def remind_error(self, ctx, error):
		await ctx.send(error)
	
	@remove.error
	async def remove_error(self, ctx, error):
		if isinstance(error, commands.errors.TooManyArguments):
			return

def setup (client):
	client.add_cog(RemindersClass(client))