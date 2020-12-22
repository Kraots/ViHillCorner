import discord
from discord.ext import commands
from secrets import choice
import string


class NickFilter(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.bot:
			return

		if message.guild:
			user_nickname = message.author.nick
			new_nick = ''.join([choice(string.ascii_lowercase) for _ in range(7)])
			
			if "a" in str(user_nickname).lower():
				return
			elif "b" in str(user_nickname).lower():
				return
			elif "c" in str(user_nickname).lower():
				return
			elif "d" in str(user_nickname).lower():
				return
			elif "e" in str(user_nickname).lower():
				return
			elif "f" in str(user_nickname).lower():
				return
			elif "g" in str(user_nickname).lower():
				return
			elif "h" in str(user_nickname).lower():
				return
			elif "i" in str(user_nickname).lower():
				return
			elif "j" in str(user_nickname).lower():
				return
			elif "k" in str(user_nickname).lower():
				return
			elif "l" in str(user_nickname).lower():
				return
			elif "m" in str(user_nickname).lower():
				return
			elif "n" in str(user_nickname).lower():
				return
			elif "o" in str(user_nickname).lower():
				return
			elif "p" in str(user_nickname).lower():
				return
			elif "q" in str(user_nickname).lower():
				return
			elif "r" in str(user_nickname).lower():
				return
			elif "s" in str(user_nickname).lower():
				return
			elif "t" in str(user_nickname).lower():
				return
			elif "u" in str(user_nickname).lower():
				return
			elif "v" in str(user_nickname).lower():
				return
			elif "w" in str(user_nickname).lower():
				return
			elif "x" in str(user_nickname).lower():
				return
			elif "z" in str(user_nickname).lower():
				return
			elif "1" in str(user_nickname).lower():
				return
			elif "2" in str(user_nickname).lower():
				return
			elif "3" in str(user_nickname).lower():
				return
			elif "4" in str(user_nickname).lower():
				return
			elif "5" in str(user_nickname).lower():
				return
			elif "6" in str(user_nickname).lower():
				return
			elif "7" in str(user_nickname).lower():
				return
			elif "8" in str(user_nickname).lower():
				return
			elif "9" in str(user_nickname).lower():
				return
			elif "0" in str(user_nickname).lower():
				return
			elif "~" in str(user_nickname).lower():
				return
			elif "`" in str(user_nickname).lower():
				return
			elif "!" in str(user_nickname).lower():
				return
			elif "@" in str(user_nickname).lower():
				return
			elif "#" in str(user_nickname).lower():
				return
			elif "$" in str(user_nickname).lower():
				return
			elif "%" in str(user_nickname).lower():
				return
			elif "^" in str(user_nickname).lower():
				return
			elif "&" in str(user_nickname).lower():
				return
			elif "*" in str(user_nickname).lower():
				return
			elif "(" in str(user_nickname).lower():
				return
			elif ")" in str(user_nickname).lower():
				return
			elif "-" in str(user_nickname).lower():
				return
			elif "_" in str(user_nickname).lower():
				return
			elif "+" in str(user_nickname).lower():
				return
			elif "=" in str(user_nickname).lower():
				return
			elif "]" in str(user_nickname).lower():
				return
			elif "[" in str(user_nickname).lower():
				return
			elif "{" in str(user_nickname).lower():
				return
			elif "}" in str(user_nickname).lower():
				return
			elif "'" in str(user_nickname).lower():
				return
			elif '"' in str(user_nickname).lower():
				return
			elif ":" in str(user_nickname).lower():
				return
			elif ";" in str(user_nickname).lower():
				return
			elif "|" in str(user_nickname).lower():
				return
			elif "," in str(user_nickname).lower():
				return
			elif "<" in str(user_nickname).lower():
				return
			elif ">" in str(user_nickname).lower():
				return
			elif "." in str(user_nickname).lower():
				return
			elif "/" in str(user_nickname).lower():
				return
			elif "?" in str(user_nickname).lower():
				return

			else:
				await message.author.edit(nick=new_nick)
				await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n**❥察爱\n! Champa\nKraots\nViHill Corner")



def setup(client):
	client.add_cog(NickFilter(client))