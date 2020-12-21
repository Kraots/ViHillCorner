import discord
from discord.ext import commands
import asyncio

class CapsFilter(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.bot:
			return

		guild = self.client.get_guild(750160850077089853)
		muted = guild.get_role(750465726069997658)
		user = message.author

		check_this = message.content

		result = sum(1 for x in check_this if x.isupper())

		if result > 5:
			await user.add_roles(muted)
			msg1 = "You have been muted in `ViHill Corner`."
			em1 = discord.Embed(description=f"**Reason:** [Caps]({message.jump_url})")
			await user.send(msg1, em1)
			msg2 = f"{user} has been muted."
			em2 = discord.Embed(description=f"**Reason:** [Caps]({message.jump_url})")
			await user.send(msg2, em2)
			await asyncio.sleep(720)
			await user.remove_roles(muted)
			await user.send("You have been unmuted in `ViHill Corner`.")
		else:
			return

def setup (client):
	client.add_cog(CapsFilter(client))