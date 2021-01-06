import discord 
from discord.ext import commands
import asyncio
import json
from utils.helpers import BotChannels, time_phaserr

status_pos=[
			"taken",
			"single",
			"complicated"
			]

class Intros(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix




	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra=False)
	@commands.cooldown(1, 360, commands.BucketType.user)
	@commands.check(BotChannels)
	async def intro(self, ctx):
		await ctx.message.delete()
		
		user = ctx.author
		users = await get_intro_data()

		channel = ctx.message.channel
		usercheck = ctx.author.id

		guild = self.client.get_guild(750160850077089853)

		introchannel = guild.get_channel(750160850593251449)
		
		def check(message):
			return message.author.id == usercheck and message.channel.id == channel.id

		def checkk(message):
			return message.author.id == usercheck and message.channel.id == channel.id
			try:
				int(message.content)
				return True
			except ValueError:
				return False

		def alreadyhas(message):
			return message.author.id == usercheck and message.channel.id == channel.id

		def status_reply(message):
			return message.content.lower() in status_pos and message.author.id == usercheck and message.channel.id == channel.id

		
		if str(user.id) in users:
			await ctx.send("You already have intro set, would you like to edit your intro? `yes` | `no`")
			
			try:
				ahem = await self.client.wait_for('message', timeout= 15, check=alreadyhas)
				if ahem.content.lower() == "no":
					await ctx.send("Canceled.")
					ctx.command.reset_cooldown(ctx)
					return

			except asyncio.TimeoutError:
				return

			else:
				if ahem.content.lower() == "yes":


					await channel.send("What's your name? {}".format(ctx.author.mention))

					try:
						name = await self.client.wait_for('message', timeout= 180, check=check)

					except asyncio.TimeoutError:
						return

					else:
						await channel.send("Where are you from? {}".format(ctx.author.mention))
						
						try:
							location = await self.client.wait_for('message', timeout= 180, check=check)

						except asyncio.TimeoutError:
							return

						else:
							await channel.send("How old are you? {}".format(ctx.author.mention))

							try:
								age = await self.client.wait_for('message', timeout= 180, check=checkk)
								agenumber = int(age.content)

								if agenumber > 44:
									return
								elif agenumber < 10:
									return

							except asyncio.TimeoutError:
								return

							else:
								await channel.send("What's your gender? {}".format(ctx.author.mention))
								
								try:
									gender = await self.client.wait_for('message', timeout= 180, check=check) 

								except asyncio.TimeoutError:
									return

								else:
									await channel.send("Relationship status? `single` | `taken` | `complicated` {}".format(ctx.author.mention))
									
									try:
										prestatuss = await self.client.wait_for('message', timeout= 180, check=status_reply)
										status = prestatuss.content
										
									except asyncio.TimeoutError:
										return

									else:
										await channel.send("What are u interested to? {}".format(ctx.author.mention))

										try:
											interests = await self.client.wait_for('message', timeout= 360, check=check)

										except asyncio.TimeoutError:
											return

										else:
											em = discord.Embed(color=ctx.author.color)
											em = discord.Embed(color=ctx.author.color)
											em.set_author(name=ctx.author, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
											em.set_thumbnail(url=ctx.author.avatar_url)
											em.add_field(name="Name", value=name.content, inline=True)
											em.add_field(name="Location", value=location.content, inline=True)
											em.add_field(name="Age", value=agenumber, inline=True)
											em.add_field(name="Gender", value=gender.content, inline=False)
											em.add_field(name="Relationship Status", value=status, inline=True)
											em.add_field(name="Interests", value=interests.content, inline=False)
											await introchannel.send(embed=em)
											await ctx.channel.send("Intro edited successfully. You can see in <#750160850593251449>")

											users[str(user.id)]["name"] = name.content
											users[str(user.id)]["location"] = location.content
											users[str(user.id)]["age"] = agenumber
											users[str(user.id)]["gender"] = gender.content
											users[str(user.id)]["status"] = status
											users[str(user.id)]["interests"] = interests.content

											with open("intros.json", "w", encoding="utf-8") as f:
												json.dump(users, f, ensure_ascii = False, indent = 4)

											return

		else:
			
			await channel.send("What's your name? {}".format(ctx.author.mention))

			try:
				name = await self.client.wait_for('message', timeout= 180, check=check)

			except asyncio.TimeoutError:
				return

			else:
				await channel.send("Where are you from? {}".format(ctx.author.mention))
				
				try:
					location = await self.client.wait_for('message', timeout= 180, check=check)

				except asyncio.TimeoutError:
					return

				else:
					await channel.send("How old are you? {}".format(ctx.author.mention))

					try:
						age = await self.client.wait_for('message', timeout= 180, check=checkk)
						agenumber = int(age.content)

						if agenumber > 44:
							return
						elif agenumber < 10:
							return

					except asyncio.TimeoutError:
						return

					else:
						await channel.send("What's your gender? {}".format(ctx.author.mention))
						
						try:
							gender = await self.client.wait_for('message', timeout= 180, check=check) 

						except asyncio.TimeoutError:
							return

						else:
							await channel.send("Relationship status? `single` | `taken` | `complicated` {}".format(ctx.author.mention))
							
							try:
								prestatuss = await self.client.wait_for('message', timeout= 180, check=status_reply)
								status = prestatuss.content
							
							except asyncio.TimeoutError:
								return

							else:
								await channel.send("What are u interested to? {}".format(ctx.author.mention))

								try:
									interests = await self.client.wait_for('message', timeout= 360, check=check)

								except asyncio.TimeoutError:
									return

								else:
									em = discord.Embed(color=ctx.author.color)
									em = discord.Embed(color=ctx.author.color)
									em.set_author(name=ctx.author, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
									em.set_thumbnail(url=ctx.author.avatar_url)
									em.add_field(name="Name", value=name.content, inline=True)
									em.add_field(name="Location", value=location.content, inline=True)
									em.add_field(name="Age", value=agenumber, inline=True)
									em.add_field(name="Gender", value=gender.content, inline=False)
									em.add_field(name="Relationship Status", value=status, inline=True)
									em.add_field(name="Interests", value=interests.content, inline=False)
									await introchannel.send(embed=em)
									await ctx.channel.send("Intro added successfully. You can see in <#750160850593251449>")

									users[str(user.id)] = {}
									users[str(user.id)]["name"] = name.content
									users[str(user.id)]["location"] = location.content
									users[str(user.id)]["age"] = agenumber
									users[str(user.id)]["gender"] = gender.content
									users[str(user.id)]["status"] = status
									users[str(user.id)]["interests"] = interests.content

									with open("intros.json", "w", encoding="utf-8") as f:
										json.dump(users, f, ensure_ascii = False, indent = 4)

									return



	@intro.command(aliases=["remove"])
	async def delete(self, ctx):

		users = await get_intro_data()

		try:
			del users[str(ctx.author.id)]

		except KeyError:
			await ctx.send("User does not have an intro!")
			return

		with open("intros.json", "w", encoding = 'utf-8') as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Intro deleted.")




	@commands.command(aliases=['wi'])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def whois(self, ctx, member: discord.Member= None):
		if member is None:
			member = ctx.author

		user = member

		users = await get_intro_data()

		introname = users[str(user.id)]["name"]
		introlocation = users[str(user.id)]["location"]
		introage = users[str(user.id)]["age"]
		introgender = users[str(user.id)]["gender"]
		relationshipstatus = users[str(user.id)]["status"]
		introinterests = users[str(user.id)]["interests"]
		
		if str(user.id) not in users:
			await ctx.send("User does not have any intro!")
			return

		else:
			await ctx.message.delete()
			em = discord.Embed(color=member.color)
			em.set_author(name=member, url=member.avatar_url, icon_url=member.avatar_url)
			em.set_thumbnail(url=member.avatar_url)
			em.add_field(name="Name", value=introname, inline=True)
			em.add_field(name="Location", value=introlocation, inline=True)
			em.add_field(name="Age", value=introage, inline=True)
			em.add_field(name="Gender", value=introgender, inline=False)
			em.add_field(name="Relationship Status", value=relationshipstatus, inline=True)
			em.add_field(name="Interests", value=introinterests, inline=False)
			await ctx.send(embed=em)


	@commands.Cog.listener()
	async def on_member_remove(self, member):

		users = await get_intro_data()

		try:
			del users[str(member.id)]

		except KeyError:
			return

		with open("intros.json", "w", encoding = 'utf-8') as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)




	@whois.error
	async def wi_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.channel.send("User does not have any intro!")
			ctx.command.reset_cooldown(ctx)

		elif isinstance(error, commands.CommandOnCooldown):
				msg = f'Please wait {time_phaserr(error.retry_after)}.'
				await ctx.channel.send(msg)

	@intro.error
	async def intro_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.CommandOnCooldown):
			msg = f'Please wait {time_phaserr(error.retry_after)}.'
			await ctx.channel.send(msg)

		elif isinstance(error, commands.TooManyArguments):
			ctx.command.reset_cooldown(ctx)
			return



		

async def get_intro_data():
	with open("intros.json", "r") as f:
		users = json.load(f)

	return users



def setup(client):
	client.add_cog(Intros(client))