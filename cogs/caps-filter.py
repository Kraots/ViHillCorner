import discord
from discord.ext import commands
import asyncio
import json

class CapsFilter(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.bot:
			return

		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		staff = guild.get_role(754676705741766757)
		mod = guild.get_role(750162714407600228)
		user = message.author

		if message.guild:
			check_this = message.content

			if message.content.lower().startswith("https://"):
				return

			else:

				result = sum(1 for x in check_this if x.isupper())

				if result > 5:
					await message.delete()

					await open_warns(user)
					users = await get_warns_data()

					users[str(user.id)]["warns"] += 1

					with open("caps-warns.json", "w") as f:
						json.dump(users, f)
					
					total_warns = users[str(user.id)]["warns"]

					if total_warns > 1:

						del users[str(user.id)]
						with open("caps-warns.json", "w") as f:
							json.dump(users, f)

						if "Staff" in [role.name for role in user.roles]:
							await user.remove_roles(staff, mod)
							await user.add_roles(muted)
							msg1 = "You have been muted in `ViHill Corner`."
							em1 = discord.Embed(description=f"**Reason:** [Caps]({message.jump_url})")
							await user.send(msg1, embed=em1)
							msg2 = f"**{user}** has been muted."
							em2 = discord.Embed(description=f"**Reason:** [Caps]({message.jump_url})")
							await message.channel.send(msg2, embed=em2)
							await asyncio.sleep(840)
							if muted in user.roles:
								await user.remove_roles(muted)
								await user.add_roles(staff, mod)
								await user.send("You have been unmuted in `ViHill Corner`.")
							else:
								pass
						
						else:
							await user.add_roles(muted)
							msg1 = "You have been muted in `ViHill Corner`."
							em1 = discord.Embed(description=f"**Reason:** [Caps]({message.jump_url})")
							await user.send(msg1, embed=em1)
							msg2 = f"**{user}** has been muted."
							em2 = discord.Embed(description=f"**Reason:** [Caps]({message.jump_url})")
							await message.channel.send(msg2, embed=em2)
							await asyncio.sleep(840)
							if muted in user.roles:
								await user.remove_roles(muted)
								await user.send("You have been unmuted in `ViHill Corner`.")

					else:
						return
				else:
					return
			


async def open_warns(user):

	users = await get_warns_data()

	if str(user.id) in users:
		return False

	else:
		users[str(user.id)] = {}
		users[str(user.id)]['warns'] = 0

	with open("caps-warns.json", "w") as f:
		json.dump(users, f)
	
	return True

async def get_warns_data():
	with open("caps-warns.json", "r") as f:
		users = json.load(f)

	return users



def setup(client):
	client.remove_cog(CapsFilter(client))