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
	
	def __init__(self, bot):
		self.bot = bot
		self.weekly_reset.start()
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix and ctx.channel.id in BotChannels

	@tasks.loop(minutes=1)
	async def weekly_reset(self):
		await self.bot.wait_until_ready()
		results = await collection.find_one({"_id": 374622847672254466})
		resetWhen = results['weekly_reset']
		a = datetime.datetime.utcnow().strftime('%Y-%m-%d')
		dateNow = datetime.datetime.strptime(a, '%Y-%m-%d')
		
		if dateNow >= resetWhen:
			users = {}
			index = 0 
			results = collection.find().sort([("messages_count", -1)])
			for result in await results.to_list(3):
				index += 1
				user = self.bot.get_user(result['_id'])
				users[index] = user
			_1stplace = users[1]
			_2ndplace = users[2]
			_3rdplace = users[3]
			await collection.update_one({'_id': _1stplace.id}, {'$inc':{'xp': 50000}})
			await collection.update_one({'_id': _2ndplace.id}, {'$inc':{'xp': 30000}})
			await collection.update_one({'_id': _3rdplace.id}, {'$inc':{'xp': 20000}})
			await _1stplace.send(f"Congrats. You placed `1st` in the weekly top! Your reward is **50,000** XP.\nThe others placed:\n\u2800• **{_2ndplace}** -> `2nd`\n\u2800• **{_3rdplace}** -> `3rd`")
			await _1stplace.send(f"Congrats. You placed `2nd` in the weekly top! Your reward is **30,000** XP.\nThe others placed:\n\u2800• **{_1stplace}** -> `1st`\n\u2800• **{_3rdplace}** -> `3rd`")
			await _1stplace.send(f"Congrats. You placed `3rd` in the weekly top! Your reward is **20,000** XP.\nThe others placed:\n\u2800• **{_1stplace}** -> `1st`\n\u2800• **{_2ndplace}** -> `2nd`")

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
		guild = self.bot.get_guild(750160850077089853)
		
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
		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
		
		msg = await ctx.send("Are you sure you want to reset the message count for this week for member %s?" % (member.mention))
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
				await collection.update_one({'_id': member.id}, {'$set':{'messages_count': 0}})
				await msg.clear_reactions()
				await msg.edit(content='The message count for this week for member **%s** has been reset successfully.' % (member))
			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				await msg.clear_reactions()
				await msg.edit(content="Command to reset the message count for user `%s` has been canceled." % (member))


	@top.command(aliases=['reward'])
	async def rewards(self, ctx):
		em = discord.Embed(color=color.lightpink, title="Here are the rewards for the weekly top:")
		em.add_field(name="`1st Place`", value="**50k XP**", inline=False)
		em.add_field(name="`2nd Place`", value="**30k XP**", inline=False)
		em.add_field(name="`3rd Place`", value="**20k XP**", inline=False)
		em.set_footer(text="Requested by: %s" % (ctx.author), icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(MessageTop(bot))
