import discord 
from discord.ext import commands
import asyncio
from utils.helpers import BotChannels, time_phaser
import motor.motor_asyncio
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Intros"]

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
		results = await collection.find_one({"_id": ctx.author.id})
		
		await ctx.message.delete()

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

		def alreadyhas(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id

		if results != None:
			msg = await ctx.send("You already have intro set, would you like to edit your intro? %s" % (ctx.author.mention))
			await msg.add_reaction('<:agree:797537027469082627>')
			await msg.add_reaction('<:disagree:797537030980239411>')

			try:
				reaction, user = await self.client.wait_for('reaction_add', check=alreadyhas, timeout=30)

			except asyncio.TimeoutError:
				new_msg = f"{ctx.author.mention} Did not react in time."
				await msg.edit(content=new_msg)
				await msg.clear_reactions()
				return
			
			else:
				if str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = "Canceled. %s" % (ctx.author.mention)
					ctx.command.reset_cooldown(ctx)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return

				elif str(reaction.emoji) == '<:agree:797537027469082627>':
					await msg.delete()
					try:
						intro_id = results['intro_id']
					except:
						pass

					await channel.send("What's your name? {}\n\n*To cancel type `!cancel`*".format(ctx.author.mention))

					try:
						name = await self.client.wait_for('message', timeout= 180, check=check)
						if name.content.lower() == '!cancel':
							await channel.send("Canceled. %s" % (ctx.author.mention))
							ctx.command.reset_cooldown(ctx)
							return

					except asyncio.TimeoutError:
						await ctx.send("Ran out of time. %s" % (ctx.author.mention))
						ctx.command.reset_cooldown(ctx)
						return

					else:
						await channel.send("Where are you from? {}".format(ctx.author.mention))
						
						try:
							location = await self.client.wait_for('message', timeout= 180, check=check)
							if location.content.lower() == '!cancel':
								await channel.send("Canceled. %s" % (ctx.author.mention))
								ctx.command.reset_cooldown(ctx)
								return

						except asyncio.TimeoutError:
							await ctx.send("Ran out of time. %s" % (ctx.author.mention))
							ctx.command.reset_cooldown(ctx)
							return

						else:
							await channel.send("How old are you? {}".format(ctx.author.mention))

							try:
								while True:
									age = await self.client.wait_for('message', timeout= 180, check=check)
									if age.content.lower() == '!cancel':
										await channel.send("Canceled. %s" % (ctx.author.mention))
										ctx.command.reset_cooldown(ctx)
										return
									try:
										agenumber = int(age.content)
										if agenumber >= 44 or agenumber <= 11:
											await channel.send("Please put your real age and not a fake age.")
										else:
											break
									except ValueError:
										await channel.send("Must be number.")

							except asyncio.TimeoutError:
								await ctx.send("Ran out of time. %s" % (ctx.author.mention))
								ctx.command.reset_cooldown(ctx)
								return

							else:
								await channel.send("What's your gender? {}".format(ctx.author.mention))
								
								try:
									gender = await self.client.wait_for('message', timeout= 180, check=check)
									if gender.content.lower() == '!cancel':
										await channel.send("Canceled. %s" % (ctx.author.mention))
										ctx.command.reset_cooldown(ctx)
										return

								except asyncio.TimeoutError:
									await ctx.send("Ran out of time. %s" % (ctx.author.mention))
									ctx.command.reset_cooldown(ctx)
									return

								else:
									await channel.send("Relationship status? `single` | `taken` | `complicated` {}".format(ctx.author.mention))
									
									try:
										while True:
											prestatuss = await self.client.wait_for('message', timeout= 180, check=check)
											status = prestatuss.content.lower()
											if status == '!cancel':
												await channel.send("Canceled. %s" % (ctx.author.mention))
												ctx.command.reset_cooldown(ctx)
												return
											elif status in ['single', 'taken', 'complicated']:
												break
											else:
												await channel.send("Please only choose from `single` | `taken` | `complicated`")
										
									except asyncio.TimeoutError:
										await ctx.send("Ran out of time. %s" % (ctx.author.mention))
										ctx.command.reset_cooldown(ctx)
										return

									else:
										await channel.send("What are u interested to? {}".format(ctx.author.mention))

										try:
											interests = await self.client.wait_for('message', timeout= 360, check=check)
											if interests.content.lower() == '!cancel':
												await channel.send("Canceled. %s" % (ctx.author.mention))
												ctx.command.reset_cooldown(ctx)
												return

										except asyncio.TimeoutError:
											await ctx.send("Ran out of time. %s" % (ctx.author.mention))
											ctx.command.reset_cooldown(ctx)
											return

										else:
											em = discord.Embed(color=ctx.author.color)
											em.set_author(name=ctx.author, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
											em.set_thumbnail(url=ctx.author.avatar_url)
											em.add_field(name="Name", value=name.content, inline=True)
											em.add_field(name="Location", value=location.content, inline=True)
											em.add_field(name="Age", value=agenumber, inline=True)
											em.add_field(name="Gender", value=gender.content, inline=False)
											em.add_field(name="Relationship Status", value=status, inline=True)
											em.add_field(name="Interests", value=interests.content, inline=False)
											intro_message = await introchannel.send(embed=em)

											await collection.update_one({"_id": ctx.author.id}, {"$set": {"name": name.content, "location": location.content, "age": agenumber, "gender": gender.content, "status": status, "interests": interests.content, "intro_id": intro_message.id}})
											
											try:
												intro_message = await introchannel.fetch_message(intro_id)
												await intro_message.delete()
											except:
												pass

											await ctx.send("Intro edited successfully. You can see in <#750160850593251449> %s" % (ctx.author.mention))

											return

		else:
			
			await channel.send("What's your name? {}\n\n*To cancel type `!cancel`*".format(ctx.author.mention))

			try:
				name = await self.client.wait_for('message', timeout= 180, check=check)
				if name.content.lower() == '!cancel':
					await channel.send("Canceled. %s" % (ctx.author.mention))
					ctx.command.reset_cooldown(ctx)
					return

			except asyncio.TimeoutError:
				await ctx.send("Ran out of time. %s" % (ctx.author.mention))
				ctx.command.reset_cooldown(ctx)
				return

			else:
				await channel.send("Where are you from? {}".format(ctx.author.mention))
				
				try:
					location = await self.client.wait_for('message', timeout= 180, check=check)
					if location.content.lower() == '!cancel':
						await channel.send("Canceled. %s" % (ctx.author.mention))
						ctx.command.reset_cooldown(ctx)
						return

				except asyncio.TimeoutError:
					await ctx.send("Ran out of time. %s" % (ctx.author.mention))
					ctx.command.reset_cooldown(ctx)
					return

				else:
					await channel.send("How old are you? {}".format(ctx.author.mention))

					try:
						while True:
							age = await self.client.wait_for('message', timeout= 180, check=check)
							if age.content.lower() == '!cancel':
								await channel.send("Canceled. %s" % (ctx.author.mention))
								ctx.command.reset_cooldown(ctx)
								return
							try:
								agenumber = int(age.content)
								if agenumber >= 44 or agenumber <= 11:
									await channel.send("Please put your real age and not a fake age.")
								else:
									break
							except ValueError:
								await channel.send("Must be number.")

					except asyncio.TimeoutError:
						await ctx.send("Ran out of time. %s" % (ctx.author.mention))
						ctx.command.reset_cooldown(ctx)
						return

					else:
						await channel.send("What's your gender? {}".format(ctx.author.mention))
						
						try:
							gender = await self.client.wait_for('message', timeout= 180, check=check)
							if gender.content.lower() == '!cancel':
								await channel.send("Canceled. %s" % (ctx.author.mention))
								ctx.command.reset_cooldown(ctx)
								return

						except asyncio.TimeoutError:
							await ctx.send("Ran out of time. %s" % (ctx.author.mention))
							ctx.command.reset_cooldown(ctx)
							return

						else:
							await channel.send("Relationship status? `single` | `taken` | `complicated` {}".format(ctx.author.mention))
							
							try:
								while True:
									prestatuss = await self.client.wait_for('message', timeout= 180, check=check)
									status = prestatuss.content.lower()
									if status == '!cancel':
										await channel.send("Canceled. %s" % (ctx.author.mention))
										ctx.command.reset_cooldown(ctx)
										return
									elif status in ['single', 'taken', 'complicated']:
										break
									else:
										await channel.send("Please only choose from `single` | `taken` | `complicated`")
							
							except asyncio.TimeoutError:
								await ctx.send("Ran out of time. %s" % (ctx.author.mention))
								ctx.command.reset_cooldown(ctx)
								return

							else:
								await channel.send("What are u interested to? {}".format(ctx.author.mention))

								try:
									interests = await self.client.wait_for('message', timeout= 360, check=check)
									if interests.content.lower() == '!cancel':
										await channel.send("Canceled. %s" % (ctx.author.mention))
										ctx.command.reset_cooldown(ctx)
										return

								except asyncio.TimeoutError:
									await ctx.send("Ran out of time. %s" % (ctx.author.mention))
									ctx.command.reset_cooldown(ctx)
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
									intro_msg = await introchannel.send(embed=em)
									await ctx.send("Intro added successfully. You can see in <#750160850593251449>")

									post = {"_id": ctx.author.id, 
											"name": name.content,
											"location": location.content,
											"age": agenumber,
											"gender": gender.content,
											"status": status,
											"interests": interests.content,
											"intro_id": intro_msg.id
											}
											
									await collection.insert_one(post)

									return



	@intro.command(aliases=["remove"])
	async def delete(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})

		if results != None:
			def check(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
			msg = await ctx.send("Are you sure you want to delete your intro? %s" % (ctx.author.mention))
			await msg.add_reaction('<:agree:797537027469082627>')
			await msg.add_reaction('<:disagree:797537030980239411>')
			try:
				reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)

			except asyncio.TimeoutError:
				new_msg = f"{ctx.author.mention} Did not react in time."
				await msg.edit(content=new_msg)
				await msg.clear_reactions()
				return
			
			else:
				if str(reaction.emoji) == '<:agree:797537027469082627>':
					await collection.delete_one({"_id": ctx.author.id})
					try:
						intro_id = results['intro_id']
						channel = ctx.guild.get_channel(750160850593251449)
						intro_message = await channel.fetch_message(intro_id)
						await intro_message.delete()
					except:
						pass
					e = "Intro deleted. %s" % (ctx.author.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return
				
				elif str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = "Intro has not been deleted. %s" % (ctx.author.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return

		else:
			await ctx.send("You do not have an intro!")
			return


	@commands.command(aliases=['wi'])
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def whois(self, ctx, member: discord.Member= None):
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})
		
		user = member

		if results != None:
			introname = results['name']
			introlocation = results['location']
			introage = results['age']
			introgender = results['gender']
			relationshipstatus = results['status']
			introinterests = results['interests']

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
		
		else:
			if ctx.author.id == user.id:
				await ctx.send("You do not have an intro!")
				ctx.command.reset_cooldown(ctx)
				return
				
			else:
				await ctx.send("User does not have an intro!")
				ctx.command.reset_cooldown(ctx)
				return


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await collection.delete_one({"_id": member.id})




	@whois.error
	async def wi_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("User does not have any intro!")
			ctx.command.reset_cooldown(ctx)

		elif isinstance(error, commands.CommandOnCooldown):
				msg = f'Please wait {time_phaser(error.retry_after)}.'
				await ctx.send(msg)

	@intro.error
	async def intro_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			ctx.command.reset_cooldown(ctx)
			return

		elif isinstance(error, commands.CommandOnCooldown):
			msg = f'Please wait {time_phaser(error.retry_after)}.'
			await ctx.send(msg)

		elif isinstance(error, commands.TooManyArguments):
			ctx.command.reset_cooldown(ctx)
			return




def setup(client):
	client.add_cog(Intros(client))