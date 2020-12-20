import re
from discord.ext import commands

bad_words = [
				"nigga",
				"nigger",
				"niga",
				"niger",
				"niggas",
				"niggers",
				"nigges",
				"nigge"
			]

class FilterCog(commands.Cog, name = "Filter"):
	"""Commands for filtering things"""

	def __init__(self, client):
		self.client = client
		self.channel = 745390366802575391

	@commands.Cog.listener()
	async def on_message(self,message):
		words = None
		try:
			words = bad_words

		except:
			words = words or []
		for word in words:
			if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})',message.content):
				try:
					await message.delete()
				except:
					pass


def setup (client):
	client.add_cog(FilterCog(client))