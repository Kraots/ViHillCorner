import discord
from discord.ext import commands
import asyncio
import utils.colors as color
import re
from utils.helpers import time_phaserr

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

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	# SLOWMODE
	@commands.command()
	@commands.has_role('Staff')
	async def slowmode(self, ctx, *, time : TimeConverter):
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		await ctx.message.delete()

		if time:
			await ctx.channel.edit(slowmode_delay=time)
			await ctx.author.send(f'Set slowmode for <#{ctx.channel.id}> to {time_phaserr(time)} !')
			
			em = discord.Embed(color=color.reds, title="___SLOWMODE___", timestamp = ctx.message.created_at)
			em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
			em.add_field(name="Action", value=f"`Set slowmode to {time_phaserr(time)}`", inline=False)
			em.add_field(name="Channel", value=f"<#{ctx.channel.id}>",inline=False)

			await log_channel.send(embed=em)
			return

		else:
			await ctx.channel.edit(slowmode_delay=0)
			await ctx.author.send(f'Disabled slowmode for <#{ctx.channel.id}> !')

			em = discord.Embed(color=color.reds, title="___SLOWMODE___", timestamp = ctx.message.created_at)
			em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
			em.add_field(name="Action", value=f"`Disabled slowmode`", inline=False)
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
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to kick?")
		try:
			before_members = await self.client.wait_for('message', timeout=180, check=check)
			kicked_members = before_members.mentions

		except asyncio.TimeoutError:
			return
		
		else:
			await ctx.send("What's the reason for the kick?")
			try:
				before_reason = await self.client.wait_for('message', timeout=360, check=check)
				kicked_reason = before_reason.content

			except asyncio.TimeoutError:
				return
			
			else:
				for id in kicked_members:
						a = id
						mem_list.append(a)
						mem_list_final = " | ".join(str(id) for id in mem_list)

						try:
							await id.send("You have been kicked from `Anime Hangouts!`")
						except discord.UnboundLocalError:
							pass
						await guild.kick(id, reason=kicked_reason)

		ban = discord.Embed(description=f"The user(s) have been kicked from the server.\n**Reason**: **[{kicked_reason}]({ctx.message.jump_url})**" , color=discord.Color.red())

		await ctx.channel.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___KICK___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value=f"`Used the kick command.`", inline=False)	
		em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		em.add_field(name="Reason", value=f"**[{kicked_reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)	

		await log_channel.send(embed=em)


			# BAN

	@commands.command()
	@commands.has_role('Staff')
	async def ban(self, ctx):
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		reasonn = discord.Embed(description="**Unban appeal server** \n https://discord.gg/m3Zyaj5Vc4")
		reasonn.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
		msg="You have been banned from `Anime Hangouts`. If you think that this has been applied in error please submit a detailed appeal at the following link."
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to ban?")
		try:
			before_members = await self.client.wait_for('message', timeout=180, check=check)
			banned_members = before_members.mentions

		except asyncio.TimeoutError:
			return
		
		else:
			await ctx.send("What's the reason for the ban?")
			try:
				before_reason = await self.client.wait_for('message', timeout=360, check=check)
				banned_reason = before_reason.content

			except asyncio.TimeoutError:
				return
			
			else:
				for id in banned_members:
					a = id
					mem_list.append(a)
					mem_list_final = " | ".join(str(id) for id in mem_list)
					await id.send(msg, embed=reasonn)
					await guild.ban(id, reason=banned_reason)

		ban = discord.Embed(description=f"The user(s) have been banned from the server.\n**Reason**: **[{banned_reason}]({ctx.message.jump_url})**" , color=discord.Color.red())

		await ctx.channel.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___BAN___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value=f"`Used the ban command.`", inline=False)	
		em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		em.add_field(name="Reason", value=f"**[{banned_reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


		# UNBAN

	@commands.command()
	@commands.has_role('Staff')
	async def unban(self, ctx, member: discord.User):
		guild = self.client.get_guild(750160850077089853)
		guild2 = self.client.get_guild(788384492175884299)
		await guild.fetch_ban(member)
		await guild.unban(discord.Object(id=member.id))
		
		unban = discord.Embed(description= f"`{member}` has been unbanned from the server" , color=discord.Color.red())

		await ctx.send(embed=unban)

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___UNBAN___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the unban command`", inline=False)
		em.add_field(name="Member", value=f"`{member}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)

		try:
			msg="Congrats! You have been unbanned from `Anime Hangouts`. Come back: https://discord.gg/mFm5GrQ"
			try:
				await member.send(msg)
			except discord.HTTPException:
				pass
			await guild2.kick(member)
		
		except discord.HTTPException:
			await guild2.kick(member)

	
		# MUTE

	@commands.command()
	@commands.has_role('Staff')
	async def mute(self, ctx):
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		muted = guild.get_role(750465726069997658)
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to mute?")
		try:
			before_members = await self.client.wait_for('message', timeout=180, check=check)
			muted_members = before_members.mentions

		except asyncio.TimeoutError:
			return
		
		else:
			await ctx.send("What's the reason for the mute?")
			try:
				before_reason = await self.client.wait_for('message', timeout=360, check=check)
				mute_reason = before_reason.content

			except asyncio.TimeoutError:
				return
			
			else:
				for id in muted_members:
					mute = discord.Embed(description=f'**Reason:** [{mute_reason}]({ctx.message.jump_url}).', color=color.inviscolor)
					msg="You were muted in `Anime Hangouts`."
					a = id
					mem_list.append(a)
					mem_list_final = " | ".join(str(id) for id in mem_list)
					try:
						await id.send(msg, embed=mute)
					except discord.HTTPException:
						pass
					await id.add_roles(muted, reason=mute_reason)

		ban = discord.Embed(description=f"The user(s) have been muted!\n**Reason**: **[{mute_reason}]({ctx.message.jump_url})**" , color=discord.Color.red())

		await ctx.channel.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___MUTE___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value=f"`Used the mute command.`", inline=False)	
		em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		em.add_field(name="Reason", value=f"**[{mute_reason}]({ctx.message.jump_url})**", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


		# UNMUTE

	@commands.command()
	@commands.has_role('Staff')
	async def unmute(self, ctx):
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		mem_list = []
		muted = guild.get_role(750465726069997658)
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What member(s) do you wish to unmute?")
		try:
			before_members = await self.client.wait_for('message', timeout=180, check=check)
			unmuted_members = before_members.mentions

		except asyncio.TimeoutError:
			return

		else:
			for id in unmuted_members:
				msg="You were unmuted in `Anime Hangouts`."
				a = id
				mem_list.append(a)
				mem_list_final = " | ".join(str(id) for id in mem_list)
				try:
					await id.send(msg)
				except discord.HTTPException:
					pass
				await id.remove_roles(muted, reason="Unmute")

		ban = discord.Embed(description=f"The user(s) have been unmuted!" , color=discord.Color.red())

		await ctx.channel.send(embed=ban)

		em = discord.Embed(color=color.reds, title="___UNMUTE___", timestamp = ctx.message.created_at)	
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)	
		em.add_field(name="Action", value=f"`Used the unmute command.`", inline=False)	
		em.add_field(name="Member(s)", value=f"`{mem_list_final}`", inline=False)	
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


		# TEMP MUTE

	@commands.command()
	@commands.has_role("Staff")
	async def tempmute(self, ctx, member : discord.Member, *, time : TimeConverter = None):
		"""Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
		!mute @Someone 1d"""
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)

		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
		
		await ctx.send("What's the reason?")
		try:
			get_reason = await self.client.wait_for('message', timeout=180, check=check)
			reason_content = get_reason.content

		except asyncio.TimeoutError:
			return
		
		else:

			if time is None:
				await ctx.send("You need to specify time.")
				return
			else:
				muted = guild.get_role(750465726069997658)
				await member.add_roles(muted, reason=reason_content)
				msg = ("You have been muted in `Anime Hangouts`")
				em = discord.Embed(description=f"Time: `{time_phaserr(time)}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**", color=color.inviscolor)
				try:
					await member.send(msg, embed = em)
				except discord.HTTPException:
					pass


				unban = discord.Embed(description= f'{member.mention} has been temporarily muted. \n\nTime: `{time_phaserr(time)}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**' , color=color.red)
				
				await ctx.send(embed=unban)

				log = discord.Embed(color=color.reds, title="___Mute___", timestamp = ctx.message.created_at)
				log.add_field(name="Member", value=f"`{member}`", inline=False)
				log.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
				log.add_field(name="Time", value=f"`{time_phaserr(time)}`", inline=False)
				log.add_field(name="Reason", value=f"**[{reason_content}]({ctx.message.jump_url})**", inline=False)
				await log_channel.send(embed=log)

				await asyncio.sleep(time)
				await member.remove_roles(muted)
				try:
					await member.send("You have been unmuted in `Anime Hangouts`.")
				except discord.HTTPException:
					pass


		# CLEAR  /  PURGE

	@commands.command()
	@commands.has_role('Staff')
	async def clear(self, ctx, amount=0):
			await ctx.message.delete()
			await ctx.channel.purge(limit=amount)

			guild = self.client.get_guild(750160850077089853)
			log_channel = guild.get_channel(788377362739494943)

			em = discord.Embed(color=color.reds, title="___PURGE / CLEAR___", timestamp = ctx.message.created_at)
			em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
			em.add_field(name="Action", value=f"`Used the clear / purge command`", inline=False)
			em.add_field(name="Amount", value=f"`{amount}` messages", inline=False)
			em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

			await log_channel.send(embed=em)


		# PARTNERSHIP

	@commands.command(aliases=["ps"])
	@commands.has_role('Staff')
	async def partnership(self, ctx, *, arg):
		guild = self.client.get_guild(750160850077089853)
		await ctx.message.delete()
		embed = discord.Embed(title="NEW PARTNERSHIP", description=f'{arg}', color=discord.Color.red())
		embed.set_footer(text=f'Partnership by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.channel.send(embed=embed)


		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___PARTNERSHIP___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the partnership command`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)

def setup (client):
	client.add_cog(Moderation(client))