import discord
from discord.ext import commands
import json
import asyncio
import os
import motor.motor_asyncio
import datetime
no_mute_these = [374622847672254466, 653611679082348544]
ignored_channels = [790310516266500098, 780374324598145055, 750160851822182487, 750160851822182486, 750160852006469807, 750160852006469810, 790309304422629386, 750160852006469806]

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Filter Mutes"]

class RepeatedTextFilter(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.id in no_mute_these:
			return
		if message.author.bot:
			return

		else:
			if message.channel.id == 750160851822182484:
				if message.content.lower().startswith("!meme"):
					return
				if message.content.lower().startswith("pls meme"):
					return

			user = message.author
			users = await get_repeated_text_warns_data()

			guild = self.client.get_guild(750160850077089853)
			muted = guild.get_role(750465726069997658)
			staff = guild.get_role(754676705741766757)
			mod = guild.get_role(750162714407600228)

			if message.guild:
				if message.channel.id in ignored_channels:
					return


				if not str(user.id) in users:
					users[str(user.id)] = {}
					users[str(user.id)]["warns"] = 0
					users[str(user.id)]["sentence"] = message.content.lower()
					with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
						json.dump(users, f, ensure_ascii = False, indent = 4)
					return

				else:
					the_message = users[str(user.id)]["sentence"]
					if message.content.lower() == the_message:
						users[str(user.id)]["warns"] += 1

						with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
							json.dump(users, f, ensure_ascii = False, indent = 4)
					
					else:
						del users[str(user.id)]
						with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
							json.dump(users, f, ensure_ascii = False, indent = 4)
						return

						


				total_warns = users[str(user.id)]["warns"]

				if total_warns > 1:
					await message.delete()

				if total_warns > 2:

					del users[str(user.id)]
					with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
						json.dump(users, f, ensure_ascii = False, indent = 4)

					if "Staff" in [role.name for role in message.author.roles]:
						post = {
								'_id': user.id,
								'mutedAt': datetime.datetime.now(),
								'muteDuration': 840,
								'guildId': message.guild.id,
								}


						try:
							await collection.insert_one(post)
						except:
							return

						await user.remove_roles(staff, mod)
						await user.add_roles(muted)
						msg1 = "You have been muted in `ViHill Corner`."
						em1 = discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
						await user.send(msg1, embed=em1)
						msg2 = f"**{user}** has been muted."
						em2= discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
						await message.channel.send(msg2, embed=em2)
						await asyncio.sleep(840)
						if muted in user.roles:
							await user.remove_roles(muted)
							await user.add_roles(staff, mod)
							await user.send("You have been unmuted.")
						else:
							pass

					else:
						post = {
								'_id': user.id,
								'mutedAt': datetime.datetime.now(),
								'muteDuration': 840,
								'guildId': message.guild.id,
								}


						try:
							await collection.insert_one(post)
						except:
							return
						await user.add_roles(muted)
						msg1 = "You have been muted in `ViHill Corner`."
						em1 = discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
						await user.send(msg1, embed=em1)
						msg2 = f"**{user}** has been muted."
						em2= discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
						await message.channel.send(msg2, embed=em2)
				else:
					return





class SpamFilter(commands.Cog):

	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.author.id in no_mute_these:
			return
		if message.author.bot :
			return
		
		else:
			user = message.author
			users = await get_spam_warns_data()

			guild = self.client.get_guild(750160850077089853)
			muted = guild.get_role(750465726069997658)
			staff = guild.get_role(754676705741766757)
			mod = guild.get_role(750162714407600228)

			if message.guild:
				if message.channel.id in ignored_channels:
					return
				
				else:
					if not str(user.id) in users:
						users[str(user.id)] = {}
						users[str(user.id)]["warns"] = 0
						with open("spam-warns.json", "w", encoding="utf-8") as f:
							json.dump(users, f, ensure_ascii = False, indent = 4)
						return

					else:
							users[str(user.id)]["warns"] += 1

							with open("spam-warns.json", "w", encoding="utf-8") as f:
								json.dump(users, f, ensure_ascii = False, indent = 4)


					total_warns = users[str(user.id)]["warns"]

					if total_warns > 2:
						await message.delete()
					
					if total_warns > 4:

						del users[str(user.id)]
						with open("spam-warns.json", "w", encoding="utf-8") as f:
							json.dump(users, f, ensure_ascii = False, indent = 4)

						if "Staff" in [role.name for role in message.author.roles]:
							post = {
								'_id': user.id,
								'mutedAt': datetime.datetime.now(),
								'muteDuration': 840,
								'guildId': message.guild.id,
								}


							try:
								await collection.insert_one(post)
							except:
								return
							await user.remove_roles(staff, mod)
							await user.add_roles(muted)
							msg1 = "You have been muted in `ViHill Corner`."
							em1 = discord.Embed(description=f"**Reason:** [Spam]({message.jump_url})")
							await user.send(msg1, embed=em1)
							msg2 = f"**{user}** has been muted."
							em2= discord.Embed(description=f"**Reason:** [Spam]({message.jump_url})")
							await message.channel.send(msg2, embed=em2)
							await asyncio.sleep(840)
							if muted in user.roles:
								await user.remove_roles(muted)
								await user.add_roles(staff, mod)
								await user.send("You have been unmuted.")
							else:
								pass
								
						else:
							post = {
								'_id': user.id,
								'mutedAt': datetime.datetime.now(),
								'muteDuration': 840,
								'guildId': message.guild.id,
								}


							try:
								await collection.insert_one(post)
							except:
								return
							await user.add_roles(muted)
							msg1 = "You have been muted in `ViHill Corner`."
							em1 = discord.Embed(description=f"**Reason:** [Spam]({message.jump_url})")
							await user.send(msg1, embed=em1)
							msg2 = f"**{user}** has been muted."
							em2= discord.Embed(description=f"**Reason:** [Spam]({message.jump_url})")
							await message.channel.send(msg2, embed=em2)

					else:
						return




async def get_repeated_text_warns_data():
	with open("repeated-text-filter.json", "r") as f:
		users = json.load(f)

	return users

async def get_spam_warns_data():
	with open("spam-warns.json", "r") as f:
		users = json.load(f)
	
	return users


def setup (client):
	client.add_cog(RepeatedTextFilter(client))
	client.add_cog(SpamFilter(client))