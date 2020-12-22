import discord
from discord.ext import commands, tasks
import json

class WarnsRemove(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.clear_caps_warns.start()
		self.clear_words_warns.start()

	@tasks.loop(seconds=75)
	async def clear_caps_warns(self):
		users = await get_caps_warns_data()
		users.clear()
		
		with open("caps-warns.json", "w") as f:
			json.dump(users, f)

	@tasks.loop(seconds=120)
	async def clear_words_warns(self):
		users = await get_words_warns_data()
		users.clear()
		
		with open("caps-warns.json", "w") as f:
			json.dump(users, f)






async def get_caps_warns_data():
	with open("caps-warns.json", "r") as f:
		users = json.load(f)

	return users

async def get_words_warns_data():
	with open("words-warns.json", "r") as f:
		users = json.load(f)

	return users


def setup(client):
	client.add_cog(WarnsRemove(client))