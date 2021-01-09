import discord
from discord.ext import commands
import utils.colors as color
import asyncio
from random import randint
from utils import time
from pymongo import MongoClient
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Intros"]

positive_messages=["yes",
				   "sure",
				   "yeah why not",
				   "yeah",
				   "sure why not"
				   ]

status_pos=[
			"taken",
			"single",
			"complicated"
			]

class on_join(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener('on_member_join')
	async def on_member_join(self, member):


		VHguild = self.client.get_guild(750160850077089853)
		welcomechannel = VHguild.get_channel(750160850303582237)
		member_count = len([m for m in VHguild.members if not m.bot])

		if member.guild == VHguild:
			def format_date(dt):
				if dt is None:
					return 'N/A'
				return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'
			welcome = discord.Embed(description="\n\n***Go get a color from*** <#779388444304211991>\n***Go read the rules at*** <#750160850303582236>\n***Don't forget to introduce yourself by typing `!intro` in a bots channel!***\n***Go vote the server by clicking the link:*** **[Click Here](https://top.gg/servers/750160850077089853/vote)**\n\nEnjoy your stay\n\n", color=color.pastel)
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

			
			
			user = member
			
			
			introchannel = VHguild.get_channel(750160850593251449)
			
			await member.send("Welcome to `ViHill Corner`, would you like to introduce yourself to us? `yes` | `no`")

			channel = member.dm_channel
			
			def check(message):
				return message.channel.id == channel.id and message.author.id == user.id

			def checkk(message):
				return message.channel.id == channel.id and message.author.id == user.id
				try:
					int(message.content)
					return True
				except ValueError:
					return False

			def newmember(message):
				return message.content.lower() in positive_messages and message.channel.id == channel.id and message.author.id == user.id

			def rel_reply(message):
				return message.content.lower() in status_pos and message.channel.id == channel.id and message.author.id == user.id

			try:

				answer = await self.client.wait_for('message', timeout= 360, check=newmember)
				if answer.content.lower() == "no":
					await member.send("Alrighty, you can do your intro later by typing `!intro` in a `bots only` channel. Enjoy your stay! :wave:")
			except asyncio.TimeoutError:
				return

			else:

				await channel.send("What's your name?")

				try:
					name = await self.client.wait_for('message', timeout= 180, check=check)

				except asyncio.TimeoutError:
					return

				else:
					await channel.send("Where are you from?")
					
					try:
						location = await self.client.wait_for('message', timeout= 180, check=check)

					except asyncio.TimeoutError:
						return

					else:
						await channel.send("How old are you?")

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
							await channel.send("What's your gender?")
							
							try:
								gender = await self.client.wait_for('message', timeout= 180, check=check) 

							except asyncio.TimeoutError:
								return

							else:
								await channel.send("Relationship status? `single` | `taken` | `complicated`")
								
								try:
									prestatuss = await self.client.wait_for('message', timeout= 180, check=rel_reply)
									status = prestatuss.content

								except asyncio.TimeoutError:
									return

								else:
									await channel.send("What are u interested to?")

									try:
										interests = await self.client.wait_for('message', timeout= 360, check=check)

									except asyncio.TimeoutError:
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
										await introchannel.send(embed=em)
										await member.send("Intro added successfully.")

										post = {"_id": member.id, 
											"name": name.content,
											"location": location.content,
											"age": agenumber,
											"gender": gender.content,
											"status": status,
											"interests": interests.content
											}
											
										collection.insert_one(post)

										return


		else:
			return








def setup (client):
	client.add_cog(on_join(client))
