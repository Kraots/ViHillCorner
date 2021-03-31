import discord
from discord.ext import commands
import string
from secrets import choice
import re

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300"
						   u"\U0001F251"  # symbols & pictographs
                           u"\U0001F680"  # transport & map symbols
                           u"\U00002702-\U000027B0"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

allowed_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "", "]", "^", "_", "`", "{", "|", "}", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "♡", " ", "\\"]

class NameFilter(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.bot:
			pass
		
		if message.guild:
			new_nick = ''.join([choice(string.ascii_lowercase) for _ in range(9)])
			user_name = str(message.author.name).lower()
			try:
				user_nickname = message.author.nick
	
				if user_nickname:
					return
			except:
				pass

			f = remove_emoji(u" %s" % (user_name))
			
			for x in f:
				if x not in allowed_letters:
					await message.author.edit(nick=new_nick)
					await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
					return


def setup(client):
	client.add_cog(NameFilter(client))