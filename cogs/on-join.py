import discord
from discord.ext import commands
import utils.colors as color
import json
import asyncio

positive_messages=["yes",
				   "sure",
				   "yeah why not",
				   "yeah",
				   "sure why not"
				   ]

class on_join(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener('on_member_join')
	async def on_member_join(self, member):
		guild = self.client.get_guild(750160850077089853)
		welcomechannel = guild.get_channel(750160850303582237)

		welcome = discord.Embed(description='\n\n***Go get roles from*** <#779276428045975573>\n***Go get a color from*** <#779388444304211991>\n***Go get read the rules and see the punishment if u break them at*** <#750160850303582236>\n***Go introduce yourself at*** <#750160850593251449>\n\nEnjoy your stay\n\n', color=color.pastel)
		welcome.set_thumbnail(url=member.avatar_url)
		msg = f'Hey {member.mention}, welcome to **Anime Hangouts!** \nYou are our **{guild.member_count - 11}** member.\n\n\n<@&750160850077089856>'
		await welcomechannel.send(msg, embed=welcome)
		role1 = discord.utils.get(member.guild.roles, name="Member")        
		await member.add_roles(role1)
		role2 = discord.utils.get(member.guild.roles, name="≻─────── ⋆ Epic Roles ⋆ ───────≺")
		await member.add_roles(role2)
		role3 = discord.utils.get(member.guild.roles, name="≻──────── ⋆ Pings  ⋆ ────────≺")
		await member.add_roles(role3)

		
		
		await open_intro(member)
		user = member
		users = await get_intro_data()
		
		
		introchannel = guild.get_channel(750160850593251449)
		
		await member.send("Welcome to `Anime Hangouts`, would you like to introduce yourself?")

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

		try:

			await self.client.wait_for('message', timeout= 360, check=newmember)

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
								em.add_field(name="Interests", value=interests.content, inline=False)
								await introchannel.send(embed=em)
								await member.send("Intro added successfully.")

								users[str(user.id)] = {}
								users[str(user.id)]["name"] = name.content
								users[str(user.id)]["location"] = location.content
								users[str(user.id)]["age"] = agenumber
								users[str(user.id)]["gender"] = gender.content
								users[str(user.id)]["interests"] = interests.content

								with open("intros.json", "w") as f:
									json.dump(users, f)

								return









async def open_intro(user):

	users = await get_intro_data()

	if str(user.id) in users:
		return False

async def get_intro_data():
	with open("intros.json", "r") as f:
		users = json.load(f)

	return users

def setup (client):
	client.add_cog(on_join(client))
