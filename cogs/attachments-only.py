import discord
from discord.ext import commands

class ImagesChannel(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.channel.id == 790310516266500098:
			try:
				allow_this = message.attachments[0].url
			except IndexError:
				await message.delete()
				await message.author.send("You can only send images / videos in this channel.")
			if message.content == allow_this:
				return
			else:
				return
		elif message.channel.id == 790309304422629386:
			try:
				allow_this = message.attachments[0].url
			except IndexError:
				await message.delete()
				await message.author.send("You cannot send text in this channel.")
			if message.content == allow_this:
				return
			else:
				return

		elif message.channel.id == 750160852006469810:
			try:
				allow_this = message.attachments[0].url
			except IndexError:
				await message.delete()
				await message.author.send("You cannot send text in this channel.")
			if message.content == allow_this:
				return
			else:
				return

		elif message.channel.id == 750160852006469806:
			try:
				allow_this = message.attachments[0].url
			except IndexError:
				await message.delete()
				await message.author.send("You cannot send text in this channel.")
			if message.content == allow_this:
				return
			else:
				return

		elif message.channel.id == 790309648213213205:
			try:
				allow_this = message.attachments[0].url
			except IndexError:
				await message.delete()
				await message.author.send("You cannot send text in this channel.")
			if message.content == allow_this:
				return
			else:
				return

		else:
			return

def setup (client):
	client.add_cog(ImagesChannel(client))