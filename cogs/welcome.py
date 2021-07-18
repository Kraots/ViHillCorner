import discord
from discord.ext import commands
import utils.colors as color
import asyncio
from random import randint
from utils import time
import motor.motor_asyncio
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Intros"]
mutes_collection = db['Moderation Mutes']
filter_mutes = db["Filter Mutes"]

class on_join(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener('on_member_join')
	async def on_member_join(self, member):


		VHguild = self.bot.get_guild(750160850077089853)
		welcomechannel = VHguild.get_channel(750160850303582237)
		member_count = len([m for m in VHguild.members if not m.bot])

		if member.guild == VHguild:
			def format_date(dt):
				if dt is None:
					return 'N/A'
				return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'
			welcome = discord.Embed(description="\n\n***Go get a color from*** <#779388444304211991>\n***Go read the rules at*** <#750160850303582236>\n***Go vote the server by clicking the link:*** **[Click Here](https://top.gg/servers/750160850077089853/vote)**\n\nEnjoy your stay\n\n", color=color.pastel)
			welcome.set_thumbnail(url=member.avatar_url)
			welcome.set_footer(text=f"Created: {format_date(member.created_at)}", icon_url=member.avatar_url)
			msg = f'Hey {member.mention}, welcome to **ViHill Corner!** \nYou are our **{member_count}** member.\n\n\n‎'
			await welcomechannel.send(msg, embed=welcome)


			color1 = VHguild.get_role(750272224170082365)
			color2 = VHguild.get_role(750160850299387977)
			color3 = VHguild.get_role(750160850299387976)
			color4 = VHguild.get_role(750160850299387975)
			color5 = VHguild.get_role(750160850299387974)
			color6 = VHguild.get_role(750160850299518985)
			color7 = VHguild.get_role(750160850299518984)
			color8 = VHguild.get_role(750160850299518983)
			color9 = VHguild.get_role(750160850299518982)
			color10 = VHguild.get_role(750160850299518981)
			color11 = VHguild.get_role(750160850299518980)
			color12 = VHguild.get_role(750160850299518979)
			color13 = VHguild.get_role(750160850299518978)
			color14 = VHguild.get_role(750160850299518977)
			color15 = VHguild.get_role(750160850295324752)
			color16 = VHguild.get_role(750160850299518976)
			color17 = VHguild.get_role(750160850295324751)
			color18 = VHguild.get_role(750272729533644850)
			color19 = VHguild.get_role(788112413261168660)

			choice = randint(1, 19)

			if choice == 1:
				await member.add_roles(color1)

			elif choice == 2:
				await member.add_roles(color2)

			elif choice == 3:
				await member.add_roles(color3)

			elif choice == 4:
				await member.add_roles(color4)

			elif choice == 5:
				await member.add_roles(color5)

			elif choice == 6:
				await member.add_roles(color6)

			elif choice == 7:
				await member.add_roles(color7)

			elif choice == 8:
				await member.add_roles(color8)

			elif choice == 9:
				await member.add_roles(color9)

			elif choice == 10:
				await member.add_roles(color10)

			elif choice == 11:
				await member.add_roles(color11)

			elif choice == 12:
				await member.add_roles(color12)

			elif choice == 13:
				await member.add_roles(color13)

			elif choice == 14:
				await member.add_roles(color14)

			elif choice == 15:
				await member.add_roles(color15)

			elif choice == 16:
				await member.add_roles(color16)

			elif choice == 17:
				await member.add_roles(color17)

			elif choice == 18:
				await member.add_roles(color18)
			
			elif choice == 19:
				await member.add_roles(color19)

			results = await mutes_collection.find_one({'_id': member.id})
			if results != None:
				guild = self.bot.get_guild(750160850077089853)

				mute_role = guild.get_role(750465726069997658)
				await member.add_roles(mute_role)
			
			resultss = await filter_mutes.find_one({'_id': member.id})
			if resultss != None:
				guild = self.bot.get_guild(750160850077089853)

				mute_role = guild.get_role(750465726069997658)
				await member.add_roles(mute_role)

			user = member
			
			
			introchannel = VHguild.get_channel(750160850593251449)
			
			msg1 = await member.send("Welcome to `ViHill Corner`, would you like to introduce yourself to us?")
			await msg1.add_reaction('<:agree:797537027469082627>')
			await msg1.add_reaction('<:disagree:797537030980239411>')

			channel = member.dm_channel
			
			def check(message):
				return message.channel.id == channel.id and message.author.id == user.id

			def newmember(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == member.id

			try:
				reaction, user = await self.bot.wait_for('reaction_add', check=newmember, timeout=180)

			except asyncio.TimeoutError:
				await channel.send("Ran out of time.")
				new_msg = "Welcome to `ViHill Corner`, if you wish to do your intro please go in <#750160851822182486> and type `!intro`"
				await msg1.edit(content=new_msg)
				await msg1.remove_reaction('<:agree:797537027469082627>', self.bot.user)
				await msg1.remove_reaction('<:disagree:797537030980239411>', self.bot.user)
				return
			
			else:
				if str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = "Alrighty, you can do your intro later by typing `!intro` in <#750160851822182486>. Enjoy your stay! :wave:"
					await msg1.edit(content=e)
					await msg1.remove_reaction('<:agree:797537027469082627>', self.bot.user)
					await msg1.remove_reaction('<:disagree:797537030980239411>', self.bot.user)
					return

				elif str(reaction.emoji) == '<:agree:797537027469082627>':

					await msg1.remove_reaction('<:agree:797537027469082627>', self.bot.user)
					await msg1.remove_reaction('<:disagree:797537030980239411>', self.bot.user)

					e = "What's your name?\n\n*To cancel type `!cancel`*"
					await msg1.edit(content=e)

					try:
						name = await self.bot.wait_for('message', timeout= 180, check=check)
						if name.content.lower() == '!cancel':
							await channel.send("Canceled.")
							return

					except asyncio.TimeoutError:
						await channel.send("Ran out of time.")
						return

					else:
						await channel.send("Where are you from?")
						
						try:
							location = await self.bot.wait_for('message', timeout= 180, check=check)
							if location.content.lower() == '!cancel':
								await channel.send("Canceled.")
								return

						except asyncio.TimeoutError:
							await channel.send("Ran out of time.")
							return

						else:
							await channel.send("How old are you?")

							try:
								while True:
									age = await self.bot.wait_for('message', timeout= 180, check=check)
									if age.content.lower() == '!cancel':
										await channel.send("Canceled.")
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
								await channel.send("Ran out of time.")
								return

							else:
								await channel.send("What's your gender?")
								
								try:
									gender = await self.bot.wait_for('message', timeout= 180, check=check)
									if gender.content.lower() == '!cancel':
										await channel.send("Canceled.")
										return 

								except asyncio.TimeoutError:
									await channel.send("Ran out of time.")
									return

								else:
									await channel.send("Relationship status? `single` | `taken` | `complicated`")
									
									try:
										while True:
											prestatuss = await self.bot.wait_for('message', timeout= 180, check=check)
											status = prestatuss.content.lower()
											if status == '!cancel':
												await channel.send("Canceled.")
												return
											if status in ['single', 'taken', 'complicated']:
												break
											else:
												await channel.send("Please only choose from single` | `taken` | `complicated`")

									except asyncio.TimeoutError:
										await channel.send("Ran out of time.")
										return

									else:
										await channel.send("What are u interested to?")

										try:
											interests = await self.bot.wait_for('message', timeout= 360, check=check)
											if interests.content.lower() == '!cancel':
												await channel.send("Canceled.")
												return

										except asyncio.TimeoutError:
											await channel.send("Ran out of time.")
											return

										else:
											em = discord.Embed(color=member.color)
											em.set_author(name=member, url=member.avatar_url, icon_url=member.avatar_url)
											em.set_thumbnail(url=member.avatar_url)
											em.add_field(name="Name", value=name.content, inline=True)
											em.add_field(name="Location", value=location.content, inline=True)
											em.add_field(name="Age", value=agenumber, inline=True)
											em.add_field(name="Gender", value=gender.content, inline=False)
											em.add_field(name="Relationship Status", value=status, inline=True)
											em.add_field(name="Interests", value=interests.content, inline=False)
											intro_msg = await introchannel.send(embed=em)
											await member.send("Intro added successfully. You can see it in <#750160850593251449>")

											post = {"_id": member.id, 
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


		else:
			return








def setup(bot):
	bot.add_cog(on_join(bot))