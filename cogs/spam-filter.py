import discord
from discord.ext import commands
import json
import asyncio

class SpamFilter(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.bot:
			return
		
		user = message.author
		users = await get_warns_data()

		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		staff = guild.get_role(754676705741766757)
		mod = guild.get_role(750162714407600228)

		if message.guild:
			if not str(user.id) in users:
				users[str(user.id)] = {}
				users[str(user.id)]["warns"] = 0
				users[str(user.id)]["sentence"] = message.content.lower()
				with open("spam-filter.json", "w") as f:
					json.dump(users, f)
				return

			else:
				the_message = users[str(user.id)]["sentence"]
				if message.content.lower() == the_message:
					await message.delete()
					users[str(user.id)]["warns"] += 1

					with open("spam-filter.json", "w") as f:
						json.dump(users, f)
				
				else:
					del users[str(user.id)]
					with open("spam-filter.json", "w") as f:
						json.dump(users, f)
					return

					


			total_warns = users[str(user.id)]["warns"]

			if total_warns > 1:
				if "Staff" in [role.name for role in message.author.roles]:
					await user.remove_roles(staff, mod)
					await user.add_roles(muted)
					msg1 = "You have been muted in `ViHill Corner`."
					em1 = discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
					await user.send(msg1, embed=em1)
					msg2 = f"**{user}** has been muted."
					em2= discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
					await message.channel.send(msg2, embed=em2)
					await asyncio.sleep(720)
					await user.remove_roles(muted)
					await user.add_roles(staff, mod)
					await user.send("You have been unmuted.")

				else:
					await user.add_roles(muted)
					msg1 = "You have been muted in `ViHill Corner`."
					em1 = discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
					await user.send(msg1, embed=em1)
					msg2 = f"**{user}** has been muted."
					em2= discord.Embed(description=f"**Reason:** [Repeated text]({message.jump_url})")
					await message.channel.send(msg2, embed=em2)
					await asyncio.sleep(720)
					await user.remove_roles(muted)
					await user.send("You have been unmuted.")

				del users[str(user.id)]
				with open("spam-filter.json", "w") as f:
					json.dump(users, f)
		
			else:
				return






async def get_warns_data():
	with open("spam-filter.json", "r") as f:
		users = json.load(f)

	return users


def setup (client):
	client.add_cog(SpamFilter(client))