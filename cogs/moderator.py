import discord
import asyncio
import utils.colors as color
import re
from utils.helpers import time_phaser
import datetime
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta
from utils import time
from utils.paginator import CustomMenu

class MutePageEntry:
	def __init__(self, entry):
		
		self.name = entry['username']
		self.time_left = entry['time_left']
	
	def __str__(self):
		return f'**{self.name}** (`{self.time_left}`)'

class MutePages(CustomMenu):
	def __init__(self, entries, *, per_page=12, title="", color=None):
		converted = [MutePageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page, color=color, title=title)

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
		self.db1 = bot.db1['Moderation Mutes']
		self.db2 = bot.db1['Filter Mutes']
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

	@tasks.loop(seconds=30)
	async def check_current_mutes(self):
		await self.bot.wait_until_ready()
		currentTime = datetime.datetime.now()
		results = await self.db1.find().to_list(100000)
		results2 = await self.db2.find().to_list(100000)
		for result in results:
			if result['muteDuration'] != None:
				unmuteTime = result['mutedAt'] + relativedelta(seconds=result['muteDuration'])

				if currentTime >= unmuteTime:
					guild = self.bot.get_guild(result['guildId'])
					member = guild.get_member(result['_id'])

					mute_role = guild.get_role(750465726069997658)
					
					if member != None:
						if mute_role in member.roles:
							await member.remove_roles(mute_role)
							await member.send("You have been unmuted in `ViHill Corner`.")
						
						await self.db1.delete_one({"_id": member.id})
					else:
						await self.db1.delete_one({"_id": result['_id']})

		for result2 in results2:
			if result2['muteDuration'] != None:
				unmuteTime = result2['mutedAt'] + relativedelta(seconds=result2['muteDuration'])

				if currentTime >= unmuteTime:
					guild = self.bot.get_guild(result2['guildId'])
					member = guild.get_member(result2['_id'])

					mute_role = guild.get_role(750465726069997658)
					
					if member != None:
						if mute_role in member.roles:
							await member.remove_roles(mute_role)
							await member.send("You have been unmuted in `ViHill Corner`.")
						
						await self.db2.delete_one({"_id": member.id})
					else:
						await self.db2.delete_one({"_id": result2['_id']})

	@commands.command()
	@commands.has_role(754676705741766757)
	async def slowmode(self, ctx, *, how_much: TimeConverter):
		"""Set the slowmode time for the channel that you are using this command in."""

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

	@commands.command()
	@commands.has_role(754676705741766757)
	async def kick(self, ctx, member: discord.Member, *, reason: str = None):
		"""Kicks the member with the specified reason, if any."""

		if reason is None:
			reason = "Reason not specified"

		guild = self.bot.get_guild(750160850077089853)
		staff = guild.get_role(754676705741766757)
		log_channel = guild.get_channel(788377362739494943)
		
		if staff in member.roles:
			return await ctx.reply("Cannot kick staff members.")

		try:
			await member.send("You have been kicked from `ViHill Corner!`")
		except discord.HTTPException:
			pass
		
		await guild.kick(member, reason=f'{ctx.author}: "{reason}"')

		ban = discord.Embed(description=f"{member} was successfully kicked" , color=discord.Color.red())

		await ctx.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___KICK___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value="`Used the kick command.`", inline=False)	
		em.add_field(name="Member", value=f"`{member}`", inline=False)
		em.add_field(name="Reason", value=f"**[{reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)	

		await log_channel.send(embed=em)

	@commands.command()
	@commands.has_role(754676705741766757)
	async def ban(self, ctx, user: discord.User, *, reason: str = None):
		"""Bans the user with the specified reason, if any."""

		if reason is None:
			reason = "Reason not specified."

		guild = self.bot.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		staff = guild.get_role(754676705741766757)

		try:
			member = guild.get_member(user.id)
			if staff in member.roles:
				return await ctx.reply("Cannot perform this action against staff members.")
		except:
			pass

		_reason = discord.Embed(description="**Unban appeal server** \n https://discord.gg/5SratjPmGc")
		_reason.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
		msg="You have been banned from `ViHill Corner`. If you think that this has been applied in error please submit a detailed appeal at the following link."
		
		try:
			await user.send(msg, embed=_reason)
		except discord.HTTPException:
			pass
		await guild.ban(user, reason=f'{ctx.author}: "{reason}"', delete_message_days=0)


		ban = discord.Embed(description=f"The user(s) have been banned from the server.\n**Reason:** **[{reason}]({ctx.message.jump_url})**.", color=discord.Color.red())

		await ctx.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___BAN___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value="`Used the ban command.`", inline=False)	
		em.add_field(name="Member", value=f"`{user}`", inline=False)
		em.add_field(name="Reason", value=f"**[{reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)

	@commands.command()
	@commands.has_role(754676705741766757)
	async def unban(self, ctx, member: discord.User):
		"""Unban's the user."""

		guild = self.bot.get_guild(750160850077089853)
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
		em.add_field(name="Member", value=f"`{member}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)

		try:
			msg="Congrats! You have been unbanned from `ViHill Corner`. Come back: https://discord.gg/mFm5GrQ"
			await member.send(msg)
		except:
			pass
		try:
			await guild2.kick(member)
		except:
			pass

	@commands.command()
	@commands.has_role(754676705741766757)
	async def mute(self, ctx, member : discord.Member, *, muted_time : TimeConverter = None):
		"""
		Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
		!mute @Someone 1d
		"""

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
				return await ctx.reply("Reason is something you must give!")
			
			else:
				post = {
						'_id': member.id,
						'mutedAt': datetime.datetime.utcnow(),
						'muteDuration': muted_time,
						'mutedBy': ctx.author.id,
						'guildId': ctx.guild.id,
					}

				try:
					await self.db1.insert_one(post)
				except:
					await ctx.send("User is already muted!")
					return

				if muted_time != None:
					muted_for = datetime.datetime.utcnow() + relativedelta(seconds = muted_time)
					muted_for = format_time(muted_for)
				else:
					muted_for = "Eternity"

				muted = guild.get_role(750465726069997658)
				await member.add_roles(muted, reason=f'{ctx.author}: "{reason_content}"')
				msg = "You have been muted in `ViHill Corner`"
				em = discord.Embed(description=f"Time: `{muted_for}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**", color=color.inviscolor)
				try:
					await member.send(msg, embed = em)
				except discord.HTTPException:
					pass


				unban = discord.Embed(description= f'{member.mention} has been temporarily muted. \n\nTime: `{muted_for}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**' , color=color.red)
				
				await ctx.send(embed=unban)

				log = discord.Embed(color=color.reds, title="___Mute___", timestamp = ctx.message.created_at)
				log.add_field(name="Member", value=f"`{member}`", inline=False)
				log.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
				log.add_field(name="Time", value=f"`{muted_for}`", inline=False)
				log.add_field(name="Reason", value=f"**[{reason_content}]({ctx.message.jump_url})**", inline=False)
				await log_channel.send(embed=log)

				if muted_time != None:
					await asyncio.sleep(muted_time)
					if muted in member.roles:
						await member.remove_roles(muted)
						await self.db1.delete_one({"_id": member.id})
						try:
							await member.send("You have been unmuted in `ViHill Corner`.")
						except discord.HTTPException:
							pass
					else:
						pass

		else:
			await ctx.send("You can't mute mods or take any moderator action against them.")
			return

	@commands.command(name='checkmute', aliases=['checkmutes'])
	async def check_mutes(self, ctx, member: discord.Member = None):
		"""Check to see if the member is muted if specified any, or in case no member is specified then see all the members that are muted if any."""

		if member is None:
			entries = []
			results1 = await self.db1.find().to_list(100000)
			results2 = await self.db2.find().to_list(100000)
			results = results1+results2
			if results == None:
				return await ctx.reply("No members muted currently.")
			for result in results:
				if result['muteDuration'] != None:
					_time = result['mutedAt'] + relativedelta(seconds = result['muteDuration'])
					_time = f"Time Left: {time.human_timedelta(_time, suffix=False, brief=True)}"
				else:
					_time = "Time Left: Eternity"
				username = self.bot.get_user(result['_id'])
				_dict = {'username': username, 'time_left': _time}
				entries.append(_dict)
			m = MutePages(entries, per_page=5, title="Here's all the current muted members:", color=color.red)
			await m.start(ctx)
		
		else:
			result = await self.db1.find_one({'_id': member.id})
			if result is None:
				result = await self.db2.find_one({'_id': member.id})
				if result is None:
					return await ctx.reply("That member is not muted.")

			if result['muteDuration'] != None:
				_time = result['mutedAt'] + relativedelta(seconds = result['muteDuration'])
				_time = f"Time Left: {time.human_timedelta(_time, suffix=False)}"
			else:
				_time = "Eternity"
			
			em = discord.Embed(color=color.red)
			em.set_author(name=member, url=member.avatar_url, icon_url=member.avatar_url)
			em.description = f"Time Left: `{_time}`"
			em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=em)			

	@commands.command()
	@commands.has_role(754676705741766757)
	async def unmute(self, ctx):
		"""Unmute someone."""

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
				
				result = await self.db1.find_one({'_id':id.id})
				resultt = await self.db2.find_one({'_id': id.id})

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
						await self.db1.delete_one({"_id": id.id})
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

	@commands.command(name='purge', aliases=['clear'])
	@commands.has_role(754676705741766757)
	async def mod_purge(self, ctx, amount=0):
		"""Delete the amount of messages from the chat."""

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

def setup(bot):
	bot.add_cog(Moderation(bot))