import discord
from discord.ext import commands
import asyncio
import utils.colors as color
from discord.ext.commands import Greedy
from discord import Member
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
	# Say
	@commands.command()
	@commands.is_owner()
	async def say(self, ctx, *, arg):
		await ctx.message.delete()
		await ctx.send(arg)
	
	# Kick
	@commands.command()
	@commands.has_role('Staff')
	async def kick(self, ctx):
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What members do you wish to kick?")
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
					await guild.kick(id, reason=kicked_reason)


	#	 MASS KICK 
	@commands.command()
	@commands.has_role('Staff')
	async def masskick(self, ctx, members : Greedy[Member], *, reason="Toxicity & Insult"):
		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)
		kicked_list = []
		for member in members:
			try:
				a = f"{member.name}#{member.discriminator}"
				kicked_list.append(a)
				kicked_members = f" | ".join(kicked_list)

				msg = "You have been kicked from `Anime Hangouts`!"
				reasonn = discord.Embed(description=f'`Reason:` [{reason}]({ctx.message.jump_url}).', color=color.inviscolor)
				await member.send(msg, embed=reasonn)
				await guild.kick(member, reason=reason)

			except discord.HTTPException:
				await guild.kick(member, reason=reason)

		kick = discord.Embed(description=f"The user has been kicked for the reason: [{reason}]({ctx.message.jump_url})" , color=discord.Color.red())
	
		await ctx.channel.send(embed=kick)

		em = discord.Embed(color=color.reds, title="___MASSKICK___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the masskick command`", inline=False)
		em.add_field(name="Members", value=f"`{kicked_members}`", inline=False)
		em.add_field(name="Reason", value=f"`{reason}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)
	
		await log_channel.send(embed=em)

	# Ban
	@commands.command(help=".ban [user] <reason>")
	@commands.has_role("Staff")
	async def ban(self, ctx, member : discord.User, *, reason="Toxicty & Insult"):
		guild = self.client.get_guild(750160850077089853)

		reasonn = discord.Embed(description="Unban appeal server \n https://discord.gg/m3Zyaj5Vc4")
		reasonn.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
		msg="You have been banned from `Anime Hangouts`. If you think that this has been applied in error please submit a detailed appeal at the following link."

		try: 
			await member.send(msg, embed=reasonn)
			await guild.ban(discord.Object(id=member.id), reason=reason)
			bann = discord.Embed(description=f"`{member}` has been banned from the server." , color=discord.Color.red())

			await ctx.send(embed=bann)

		except discord.HTTPException:
			await guild.ban(discord.Object(id=member.id), reason=reason)
			bann = discord.Embed(description=f"`{member}` has been banned from the server." , color=discord.Color.red())

			await ctx.send(embed=bann)

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___BAN___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the ban command`", inline=False)
		em.add_field(name="Member", value=f"`{member}`", inline=False)
		em.add_field(name="Reason", value=f"`{reason}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


	# MASS BAN 
	@commands.command()
	@commands.has_role('Staff')
	async def massban(self, ctx, members : Greedy[Member], *, reason="Toxicity & Insult"):
		
		reasonn = discord.Embed(description="**Unban appeal server** \n https://discord.gg/m3Zyaj5Vc4")
		reasonn.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
		msg="You have been banned from `Anime Hangouts`. If you think that this has been applied in error please submit a detailed appeal at the following link."
		banned_list = []
		for member in members:
			try:
				a = f"{member.name}#{member.discriminator}"
				banned_list.append(a)
				banned_members = f" | ".join(banned_list)
				await member.send(msg, embed=reasonn)
			
				await member.ban()

			except discord.HTTPException:
				await member.ban()

			except discord.Forbidden:
				await member.ban()

		ban = discord.Embed(description=f"The users have been banned from the server." , color=discord.Color.red())

		await ctx.channel.send(embed=ban)


		guild = self.client.get_guild(750160850077089853)
		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___MASSBAN___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the massban command`", inline=False)
		em.add_field(name="Members", value=f"`{banned_members}`", inline=False)
		em.add_field(name="Reason", value=f"`{reason}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)




		

	# Unban
	@commands.command(help=".unban [user_ID]")
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
			await member.send(msg)
			await guild2.kick(member)
		
		except discord.HTTPException:
			await guild2.kick(member)

	# MASS UNBAN
	@commands.command(help=".unban [user_ID]")
	@commands.has_role('Staff')
	async def massunban(self, ctx, members: Greedy[Member]):
		guild = self.client.get_guild(750160850077089853)
		guild2 = self.client.get_guild(788384492175884299)
		members_list = []
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			members_list.append(a)
			unbaned_members = f" | ".join(members_list)	
			await guild.unban(member)

			try:
				msg = "Congrats! You have been unbanned from `Anime Hangouts`. Come back: https://discord.gg/mFm5GrQ"
				await member.send(msg)
				await guild2.kick(member)

			except discord.HTTPException:
				await guild2.kick(member)
		unban = discord.Embed(description= "The user has been unbanned from the server" , color=discord.Color.red())

		await ctx.send(embed=unban)

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___MASSUNBAN___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the massunban command`", inline=False)
		em.add_field(name="Members", value=f"`{unbaned_members}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)




	# Clear/Purge
	@commands.command(help=".clear [amount]")
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

	# Mute
	@commands.command(help=".mute [user] <reason>")
	@commands.has_role('Staff')
	async def mute(self, ctx, member : discord.Member, *, reason="Toxicity & Insult"):
		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		await member.add_roles(muted)     
		unban = discord.Embed(description= f'{member.mention} has been muted for the reason: [{reason}]({ctx.message.jump_url}).' , color=discord.Color.red())
		
		await ctx.send(embed=unban)
		mute = discord.Embed(description=f'**Reason:** [{reason}]({ctx.message.jump_url}).', color=color.inviscolor)
		msg="You were muted in `Anime Hangouts`."

		await member.send(msg, embed=mute)

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___MUTE___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the mute command`", inline=False)
		em.add_field(name="Member", value=f"`{member}`", inline=False)
		em.add_field(name="Reason", value=f"[{reason}]({ctx.message.jump_url})", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


	# MASS MUTE
	@commands.command(help=".mute [user] <reason>")
	@commands.has_role('Staff')
	async def massmute(self, ctx, members : Greedy[Member], *, reason="Toxicity & Insult"):
		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		muted_members = []
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			muted_members.append(a)
			muted_member = f" | ".join(muted_members)
			await member.add_roles(muted)     
			reasonn = discord.Embed(description=f'**Reason:** [{reason}]({ctx.message.jump_url}).', color=color.inviscolor)
			msg="You were muted in `Anime Hangouts`."

			await member.send(msg, embed=reasonn)
		
		unban = discord.Embed(description= f'The users have been muted for the reason: [{reason}]({ctx.message.jump_url}).' , color=discord.Color.red())
		
		await ctx.send(embed=unban)

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___MASSMUTE___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the massmute command`", inline=False)
		em.add_field(name="Members", value=f"`{muted_member}`", inline=False)
		em.add_field(name="Reason", value=f"[{reason}]({ctx.message.jump_url})")
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)




	# Unmute
	@commands.command(help=".unmute [user]")
	@commands.has_role('Staff')
	async def unmute(self, ctx, member : discord.Member):
		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		await member.remove_roles(muted)     
		unban = discord.Embed(description= f'{member.mention} has been unmuted.' , color=discord.Color.red())
		
		await ctx.send(embed=unban)

		await member.send("You have been unmuted in `Anime Hangouts`.")

		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___UNMUTE___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the unmute command`", inline=False)
		em.add_field(name="Member", value=f"`{member}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)

	# MASS UNMUTE 
	@commands.command(help=".unmute [user]")
	@commands.has_role('Staff')
	async def massunmute(self, ctx, members : Greedy[Member]):
		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		unmuted_members = []
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			unmuted_members.append(a)
			unmuted_member = f" | ".join(unmuted_members)
			await member.remove_roles(muted)     
			await member.send("You have been unmuted in `Anime Hangouts`.")
		unban = discord.Embed(description= f'The members have been unmuted.' , color=discord.Color.red())
		
		await ctx.send(embed=unban)


		log_channel = guild.get_channel(788377362739494943)

		em = discord.Embed(color=color.reds, title="___MASSUNMUTE___", timestamp = ctx.message.created_at)
		em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
		em.add_field(name="Action", value=f"`Used the massunmute command`", inline=False)
		em.add_field(name="Members", value=f"`{unmuted_member}`", inline=False)
		em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

		await log_channel.send(embed=em)


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

		await asyncio.sleep(1)
		await ctx.channel.send("<@&750160850077089861>")


		


def setup (client):
	client.add_cog(Moderation(client))