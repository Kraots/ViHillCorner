import discord
import asyncio
import utils.colors as color
import re
from utils.helpers import time_phaser
import motor.motor_asyncio
import os
import datetime
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta
from utils import time
DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Moderation Mutes"]
collection2 = db['Filter Mutes']

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
	async def convert(self, ctx, argument):
		args = argument.lower()
		matches = re.findall(time_regex, args)
		time = 0
		for v, k in matches:
			try:
				time += time_dict[k]*float(v)
			except KeyError:
				raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
			except ValueError:
				raise commands.BadArgument("{} is not a number!".format(v))
		return time

class Moderation(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
		self.check_current_mutes.start()
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
	async def _mute(self, m: discord.Member):
		g = self.bot.get_guild(750160850077089853)
		r = g.get_role(750465726069997658)
		await m.add_roles(r)
	
	async def _unmute(self, m: discord.Member):
		g = self.bot.get_guild(750160850077089853)
		r = g.get_role(750465726069997658)
		await m.remove_roles(r)

		# LOOP FOR MUTES
	
	@tasks.loop(seconds=30)
	async def check_current_mutes(self):
		await self.bot.wait_until_ready()
		currentTime = datetime.datetime.now()
		results = collection.find()
		results2 = collection2.find()
		for result in await results.to_list(99999999999999999):
			unmuteTime = result['mutedAt'] + relativedelta(seconds=result['muteDuration'])

			if currentTime >= unmuteTime:
				guild = self.bot.get_guild(result['guildId'])
				member = guild.get_member(result['_id'])

				mute_role = guild.get_role(750465726069997658)
				
				if member != None:
					if mute_role in member.roles:
						await member.remove_roles(mute_role)
						await member.send("You have been unmuted in `ViHill Corner`.")
					
					await collection.delete_one({"_id": member.id})
				else:
					await collection.delete_one({"_id": result['_id']})

		for result2 in await results2.to_list(99999999999999999):
			unmuteTime = result2['mutedAt'] + relativedelta(seconds=result2['muteDuration'])

			if currentTime >= unmuteTime:
				guild = self.bot.get_guild(result2['guildId'])
				member = guild.get_member(result2['_id'])

				mute_role = guild.get_role(750465726069997658)
				
				if member != None:
					if mute_role in member.roles:
						await member.remove_roles(mute_role)
						await member.send("You have been unmuted in `ViHill Corner`.")
					
					await collection2.delete_one({"_id": member.id})
				else:
					await collection2.delete_one({"_id": result2['_id']})


	# SLOWMODE
	@commands.command()
	@commands.has_role('Staff')
	async def slowmode(self, ctx, *, how_much: TimeConverter):
		guild = self.bot.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		await ctx.message.delete()

		if how_much:
			await ctx.channel.edit(slowmode_delay=how_much)
			await ctx.author.send(f'Set slowmode for <#{ctx.channel.id}> to {time_phaser(how_much)} !')
			
			em = discord.Embed(color=color.reds, title="___SLOWMODE___", timestamp = ctx.message.created_at)
			em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
			em.add_field(name="Action", value=f"`Set slowmode to {time_phaser(how_much)}`", inline=False)
			em.add_field(name="Channel", value=f"<#{ctx.channel.id}>",inline=False)

			await log_channel.send(embed=em)
			return

		else:
			await ctx.channel.edit(slowmode_delay=0)
			await ctx.author.send(f'Disabled slowmode for <#{ctx.channel.id}> !')

			em = discord.Embed(color=color.reds, title="___SLOWMODE___", timestamp = ctx.message.created_at)
			em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
			em.add_field(name="Action", value="`Disabled slowmode`", inline=False)
			em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)
			
			await log_channel.send(embed=em)


		# SAY

	@commands.command()
	@commands.is_owner()
	async def say(self, ctx, *, arg):
		await ctx.message.delete()
		await ctx.send(arg)
	

		# KICK

	@commands.command()
	@commands.has_role('Staff')
	async def kick(self, ctx):
		guild = self.bot.get_guild(750160850077089853)
		staff = guild.get_role(754676705741766757)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to kick? To cancel type `cancel`")
		try:
			before_members = await self.bot.wait_for('message', timeout=180, check=check)
			if before_members.content.lower() == "cancel":
				await ctx.send("Canceled.")
				return
			else:
				kicked_members = before_members.mentions

		except asyncio.TimeoutError:
			return
		
		else:
			await ctx.send("What's the reason for the kick?")
			try:
				before_reason = await self.bot.wait_for('message', timeout=360, check=check)
				if before_reason.content.lower() == "cancel":
					await ctx.send("Canceled.")
					return
				else:
					kicked_reason = before_reason.content

			except asyncio.TimeoutError:
				return
			
			else:
				for id in kicked_members:
						a = id
						if not staff in a.roles:
							mem_list.append(a)
							mem_list_final = " | ".join(str(id) for id in mem_list)

							try:
								await id.send("You have been kicked from `ViHill Corner!`")
							except discord.HTTPException:
								pass
							await guild.kick(id, reason=f"{ctx.author} ---> {kicked_reason}")

		ban = discord.Embed(description=f"The user(s) have been kicked from the server.\n**Reason:** **[{kicked_reason}]({ctx.message.jump_url})**" , color=discord.Color.red())

		await ctx.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___KICK___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value="`Used the kick command.`", inline=False)	
		try:
			em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)
		except UnboundLocalError:
			em.add_field(name="Member(s)", value="`Invalid Users!`", inline=False)
		em.add_field(name="Reason", value=f"**[{kicked_reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)	

		await log_channel.send(embed=em)


			# ID BAN

	@commands.command()
	async def idban(self, ctx, member: int):
		guild = self.bot.get_guild(750160850077089853)
		get_member = await self.bot.fetch_user(member)
		await guild.ban(get_member)
		em = discord.Embed(color=discord.Color.red(), description=f"`{get_member}` was banned succesfully.")
		await ctx.send(embed=em)


		# ID UNBAN

	@commands.command()
	async def idunban(self, ctx, member: int):
		guild = self.bot.get_guild(750160850077089853)
		get_member = await self.bot.fetch_user(member)
		await guild.unban(get_member)
		em = discord.Embed(color=discord.Color.red(), description=f"`{get_member}` was unbanned succesfully.")
		await ctx.send(embed=em)


			# BAN

	@commands.command()
	@commands.has_role('Staff')
	async def ban(self, ctx):
		guild = self.bot.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		staff = guild.get_role(754676705741766757)
		mem_list = []
		reasonn = discord.Embed(description="**Unban appeal server** \n https://discord.gg/5SratjPmGc")
		reasonn.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
		msg="You have been banned from `ViHill Corner`. If you think that this has been applied in error please submit a detailed appeal at the following link."
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to ban? To cancel type `cancel`")
		try:
			before_members = await self.bot.wait_for('message', timeout=180, check=check)
			if before_members.content.lower() in ["cancel", "!cancel"]:
				await ctx.send("Canceled.")
				return
			else:	
				banned_members = before_members.mentions
				for i in range(len(banned_members)):
					await self._mute(banned_members[i])

		except asyncio.TimeoutError:
			return
		
		else:
			await ctx.send("What's the reason for the ban?")
			try:
				before_reason = await self.bot.wait_for('message', timeout=360, check=check)
				if before_reason.content.lower() in ["cancel", "!cancel"]:
					for i in range(len(banned_members)):
						await self._unmute(banned_members[i])
					await ctx.send("Canceled.")
					return
				else:
					banned_reason = before_reason.content

			except asyncio.TimeoutError:
				return
			
			else:
				await ctx.send("How many days worth of messages from the user do you wish to delete? `0-7` days")
				try:
					while True:
						nr_dayss = await self.bot.wait_for('message', timeout=360, check=check)
						try:
							nr_days = int(nr_dayss.content)
							if -1 > nr_days or nr_days > 7:
								await ctx.send("You can only delete from 0-7 days, no more or less! %s" % (ctx.author.mention))
							else:
								break
						except ValueError:
							if nr_dayss.content.lower() in ["cancel", "!cancel"]:
								await ctx.send("Canceled.")
								for i in range(len(banned_members)):
									await self._unmute(banned_members[i])
								return
							else:
								nr_days = 0
								await nr_dayss.reply("Since there was no number the amount of messages that will be deleted is equivalent to `0` days")
								break				
				
				except asyncio.TimeoutError:
					await ctx.send("Ran out of time. %s" % (ctx.author.mention))
					return

				else:
					for id in banned_members:
						a = id
						if not staff in a.roles:
							mem_list.append(a)
							mem_list_final = " | ".join(str(id) for id in mem_list)
							try:
								await id.send(msg, embed=reasonn)
							except discord.HTTPException:
								pass
							await guild.ban(id, reason=f"{ctx.author} --->{banned_reason}", delete_message_days=nr_days)


		ban = discord.Embed(description=f"The user(s) have been banned from the server.\n**Reason:** **[{banned_reason}]({ctx.message.jump_url})**\n**Deleted:** `{nr_days}` days worth of messages.", color=discord.Color.red())

		await ctx.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___BAN___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value="`Used the ban command.`", inline=False)	
		try:
			em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		except UnboundLocalError:
			em.add_field(name="Member(s)", value="`Invalid Users!`", inline=False)
		em.add_field(name="Reason", value=f"**[{banned_reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)
		em.add_field(name="Days worth of messages that got deleted:", value=f"**{nr_days}**", inline=False)

		await log_channel.send(embed=em)


		# UNBAN

	@commands.command()
	@commands.has_role('Staff')
	async def unban(self, ctx, member: discord.User):
		guild = self.bot.get_guild(750160850077089853)
		if ctx.guild == guild:
			return await ctx.reply("This command can only be performed in the ban appeal server.")
		guild2 = self.bot.get_guild(788384492175884299)
		if ctx.channel.id == 788488359306592316:
			return await ctx.reply("This command cannot be performed in the staff chat. Please go in the chat where the member you wish to unban exists.")
		try:
			await guild.fetch_ban(member)
			await guild.unban(discord.Object(id=member.id))
		except:
			return await ctx.send("Failed. Did you input the correct member that is in the same guild?")
			
		unban = discord.Embed(description= f"`{member}` has been unbanned from the server" , color=discord.Color.red())

		await ctx.send(embed=unban)

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___UNBAN___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value="`Used the unban command`", inline=False)
		try:
			em.add_field(name="Member", value=f"`{member}`", inline=False)
		except UnboundLocalError:
			em.add_field(name="Member(s)", value="`Invalid Users!`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


		msg="Congrats! You have been unbanned from `ViHill Corner`. Come back: https://discord.gg/mFm5GrQ"
		await member.send(msg)
		await guild2.kick(member)

	
		# MUTE

	@commands.command()
	@commands.has_role('Staff')
	async def mute(self, ctx):
		guild = self.bot.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		muted = guild.get_role(750465726069997658)
		staff = guild.get_role(754676705741766757)
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to mute? To cancel type `cancel`")
		try:
			before_members = await self.bot.wait_for('message', timeout=180, check=check)
			if before_members.content.lower() == "cancel":
				await ctx.send("Canceled.")
				return
			else:
				muted_members = before_members.mentions

		except asyncio.TimeoutError:
			return
		
		else:
			await ctx.send("What's the reason for the mute?")
			try:
				before_reason = await self.bot.wait_for('message', timeout=360, check=check)
				if before_reason.content.lower() == "cancel":
					await ctx.send("Canceled.")
					return
				else:
					mute_reason = before_reason.content

			except asyncio.TimeoutError:
				return
			
			else:
				for id in muted_members:
					if not staff in id.roles:
						post = {
							'_id': id.id,
							'muteDuration': None,
							'mutedAt': datetime.datetime.now(),
							'mutedBy': ctx.author.id,
							'guildId': ctx.guild.id,
						}

						try:
							await collection.insert_one(post)
						except:
							await ctx.send("User is already muted!")
							return
						mute = discord.Embed(description=f'**Reason:** **[{mute_reason}]({ctx.message.jump_url}).**', color=color.inviscolor)
						msg="You were muted in `ViHill Corner`."
						a = id
						mem_list.append(a)
						mem_list_final = " | ".join(str(id) for id in mem_list)
						try:
							await id.send(msg, embed=mute)
						except discord.HTTPException:
							pass
						await id.add_roles(muted, reason=f"{ctx.author} ---> {mute_reason}")

		ban = discord.Embed(description=f"The user(s) have been muted!\n**Reason:** **[{mute_reason}]({ctx.message.jump_url})**" , color=discord.Color.red())

		await ctx.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___MUTE___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value="`Used the mute command.`", inline=False)	
		try:
			em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		except UnboundLocalError:
			em.add_field(name="Member(s)", value="`Invalid Users!`", inline=False)		
		em.add_field(name="Reason", value=f"**[{mute_reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


		# UNMUTE

	@commands.command()
	@commands.has_role('Staff')
	async def unmute(self, ctx):
		guild = self.bot.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		muted = guild.get_role(750465726069997658)
		staff = guild.get_role(754676705741766757)
		total_failures = 0
		failed_users = []
		unmute_succes = 0
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to unmute? To cancel type `cancel`")
		try:
			before_members = await self.bot.wait_for('message', timeout=180, check=check)
			if before_members.content.lower() == "cancel":
					await ctx.send("Canceled.")
					return
			else:
				unmuted_members = before_members.mentions

		except asyncio.TimeoutError:
			return

		else:
			for id in unmuted_members:
				if id.id == 747329236695777340:
					if not ctx.author.id == 374622847672254466:
						await ctx.send("%s cannot be unmuted ;)))))" % (id.mention))
						return
				
				result = await collection.find_one({'_id':id.id})
				resultt = await collection2.find_one({'_id': id.id})

				if result != None:
					mutedBy = result['mutedBy']
					if mutedBy == 374622847672254466 and ctx.author.id != 374622847672254466:
						user = guild.get_member(id.id)
						await ctx.send("Carrots muted that user (`%s`), therefore, you cannot unmute them. >;D" % (user))
						return
				
				if resultt != None:
					total_failures += 1
					user = guild.get_member(id.id)
					if total_failures >= 2:
						failed_users.append(user)
					elif total_failures == 1:
						if ctx.author.id != 374622847672254466:
							await ctx.send("That user is muted by a filter. (`%s`)" % (user))
							return
				
				if not staff in id.roles:
					if not id in failed_users:
						await collection.delete_one({"_id": id.id})
						msg="You were unmuted in `ViHill Corner`."
						a = id
						mem_list.append(a)
						mem_list_final = " | ".join(str(id) for id in mem_list)
						try:
							await id.send(msg)
						except discord.HTTPException:
							pass
						await id.remove_roles(muted, reason="{} ---> Unmute".format(ctx.author))
						unmute_succes += 1

		if total_failures >= 2:
			total_failed_users = ", ".join(failed_users)
			await ctx.send("Some of the users you tried to unmute were muted by a filter (`%s`). The others have been unmuted however." % (total_failed_users))

		elif not unmute_succes < 1:
			succes_unmute = discord.Embed(description="The user(s) have been unmuted!" , color=discord.Color.red())
			await ctx.send(embed=succes_unmute)
		
		else:
			await ctx.send("Failed to unmute. Probably because they were never muted.")

		em = discord.Embed(color=color.reds, title="___UNMUTE___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value="`Used the unmute command.`", inline=False)	
		try:
			em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		except UnboundLocalError:
			em.add_field(name="Member(s)", value="`Invalid Users!`", inline=False)		
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


		# TEMP MUTE

	@commands.command()
	@commands.has_role("Staff")
	async def tempmute(self, ctx, member : discord.Member, *, muted_time : TimeConverter = None):
		"""Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
		!mute @Someone 1d"""

		guild = self.bot.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		staff = guild.get_role(754676705741766757)

		if not staff in member.roles:
			
			def format_time(dt):
				return time.human_timedelta(dt, accuracy = 3)

			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
			
			await ctx.send("What's the reason?")
			try:
				get_reason = await self.bot.wait_for('message', timeout=180, check=check)
				reason_content = get_reason.content

			except asyncio.TimeoutError:
				return
			
			else:

				if time is None:
					await ctx.send("You need to specify time.")
					return
				else:
					post = {
							'_id': member.id,
							'mutedAt': datetime.datetime.now(),
							'muteDuration': muted_time,
							'mutedBy': ctx.author.id,
							'guildId': ctx.guild.id,
						}

					try:
						await collection.insert_one(post)
					except:
						await ctx.send("User is already muted!")
						return

					muted_for = datetime.datetime.utcnow() + relativedelta(seconds = muted_time)

					muted = guild.get_role(750465726069997658)
					await member.add_roles(muted, reason=f"{ctx.author} ---> {reason_content}")
					msg = ("You have been muted in `ViHill Corner`")
					em = discord.Embed(description=f"Time: `{format_time(muted_for)}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**", color=color.inviscolor)
					try:
						await member.send(msg, embed = em)
					except discord.HTTPException:
						pass


					unban = discord.Embed(description= f'{member.mention} has been temporarily muted. \n\nTime: `{format_time(muted_for)}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**' , color=color.red)
					
					await ctx.send(embed=unban)

					log = discord.Embed(color=color.reds, title="___Mute___", timestamp = ctx.message.created_at)
					log.add_field(name="Member", value=f"`{member}`", inline=False)
					log.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
					log.add_field(name="Time", value=f"`{format_time(muted_for)}`", inline=False)
					log.add_field(name="Reason", value=f"**[{reason_content}]({ctx.message.jump_url})**", inline=False)
					await log_channel.send(embed=log)

					await asyncio.sleep(muted_time)
					if muted in member.roles:
						await member.remove_roles(muted)
						await collection.delete_one({"_id": member.id})
						try:
							await member.send("You have been unmuted in `ViHill Corner`.")
						except discord.HTTPException:
							pass
					else:
						pass

		else:
			await ctx.send("You can't mute mods or take any moderator action against them.")
			return


		# CLEAR  /  PURGE

	@commands.command()
	@commands.has_role('Staff')
	async def clear(self, ctx, amount=0):
			await ctx.message.delete()
			await ctx.channel.purge(limit=amount)

			guild = self.bot.get_guild(750160850077089853)
			log_channel = guild.get_channel(788377362739494943)

			em = discord.Embed(color=color.reds, title="___PURGE / CLEAR___", timestamp = ctx.message.created_at)
			em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
			em.add_field(name="Action", value="`Used the clear / purge command`", inline=False)
			em.add_field(name="Amount", value=f"`{amount}` messages", inline=False)
			em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

			await log_channel.send(embed=em)


			# ERROR HANDLERS
	
	@unban.error
	async def unban_error(self, ctx, error):
		if isinstance(error, commands.errors.UserNotFound):
			await ctx.reply("User not found")




def setup(bot):
	bot.add_cog(Moderation(bot))