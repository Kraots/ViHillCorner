import re
import discord
from discord.ext import commands
from secrets import choice
import string
import asyncio
import json
import os
import pymongo
from pymongo import MongoClient
import datetime
DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Moderation Mutes"]

bad_words = [
				"nigga",
				"nigger",
				"niga",
				"niger",
				"niggas",
				"niggers",
				"nigges",
				"nigge",
				"tard",
				"commie",
				"T-bagger",
				"faggot",
				"dyke",
				"fatso",
				"druggie",
				"whore",
				"handicapped",
				"hoe",
				"wheelchair-bound",
				"slut",
				"cunt"
				]

zalgo_vars = ['\u030D', '\u030E', '\u0304', '\u0305', '\u033F',
           '\u0311', '\u0306', '\u0310', '\u0352', '\u0357',
           '\u0351', '\u0307', '\u0308', '\u030A', '\u0342',
           '\u0343', '\u0344', '\u034A', '\u034B', '\u034C',
           '\u0303', '\u0302', '\u030C', '\u0350', '\u0300',
           '\u0301', '\u030B', '\u030F', '\u0312', '\u0313',
           '\u0314', '\u033D', '\u0309', '\u0363', '\u0364',
           '\u0365', '\u0366', '\u0367', '\u0368', '\u0369',
           '\u036A', '\u036B', '\u036C', '\u036D', '\u036E',
           '\u036F', '\u033E', '\u035B', '\u0346', '\u031A',
		   '\u0315', '\u031B', '\u0340', '\u0341', '\u0358',
            '\u0321', '\u0322', '\u0327', '\u0328', '\u0334',
            '\u0335', '\u0336', '\u034F', '\u035C', '\u035D',
            '\u035E', '\u035F', '\u0360', '\u0362', '\u0338',
            '\u0337', '\u0361', '\u0489',
			'\u0316', '\u0317', '\u0318', '\u0319', '\u031C',
             '\u031D', '\u031E', '\u031F', '\u0320', '\u0324',
             '\u0325', '\u0326', '\u0329', '\u032A', '\u032B',
             '\u032C', '\u032D', '\u032E', '\u032F', '\u0330',
             '\u0331', '\u0332', '\u0333', '\u0339', '\u033A',
             '\u033B', '\u033C', '\u0345', '\u0347', '\u0348',
             '\u0349', '\u034D', '\u034E', '\u0353', '\u0354',
             '\u0355', '\u0356', '\u0359', '\u035A', '\u0323']


alphabet_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "", "]", "^", "_", "`", "{", "|", "}", "~"]


class FilterCog(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self,message):
		guild = self.client.get_guild(750160850077089853)
		if message.guild:
			staff = guild.get_role(754676705741766757)
			mod = guild.get_role(750162714407600228)
			muted = guild.get_role(750465726069997658)
			user = message.author
			new_nick = ''.join([choice(string.ascii_lowercase) for _ in range(7)])
			new_nick_again = ''.join([choice(string.ascii_lowercase) for _ in range(7)])
			words = None
			zalgos = None
			try:
				words = bad_words
				zalgos = zalgo_vars
			except	:
				words = words or []
				zalgos = zalgos or []
			for word in words:
				if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', message.content):
					if not "shoe" in message.content.lower():
						try:
							await message.delete()

							users = await get_warns_data()
							
							if str(user.id) in users:
								users[str(user.id)]["warns"] += 1

								with open("words-warns.json", "w", encoding="utf-8") as f:
									json.dump(users, f, ensure_ascii = False, indent = 4)

							else:
								users[str(user.id)] = {}
								users[str(user.id)]["warns"] = 0
								with open("words-warns.json", "w", encoding="utf-8") as f:
									json.dump(users, f, ensure_ascii = False, indent = 4)

							total_warns = users[str(user.id)]["warns"]


							if total_warns > 1:
								del users[str(user.id)]
								with open("words-warns.json", "w", encoding="utf-8") as f:
									json.dump(users, f, ensure_ascii = False, indent = 4)

								if "Staff" in [role.name for role in message.author.roles]:
									post = {
											'_id': user.id,
											'mutedAt': datetime.datetime.now(),
											'muteDuration': 840,
											'guildId': message.guild.id,
											}


									try:
										collection.insert_one(post)
									except pymongo.errors.DuplicateKeyError:
										return
									await message.author.add_roles(muted, reason="Bad Words")
									await message.author.remove_roles(staff, mod)
									msg1 = "You have been muted in `ViHill Corner`."
									em1 = discord.Embed(description="**Reason:** [Bad Words]({})".format(message.jump_url))
									await message.author.send(msg1, embed=em1)
									msg2 = f"**{message.author}** has been muted."
									em2 = discord.Embed(description="**Reason:** [Bad Words]({})".format(message.jump_url))
									await message.channel.send(msg2, embed=em2)
									await asyncio.sleep(840)
									if muted in user.roles:
										await message.author.remove_roles(muted)
										await message.author.add_roles(staff, muted)
										await message.author.send("You have been unmuted in `ViHill Corner`")
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
										collection.insert_one(post)
									except pymongo.errors.DuplicateKeyError:
										return
									await message.author.add_roles(muted, reason="Bad Words")
									msg1 = "You have been muted in `ViHill Corner`."
									em1 = discord.Embed(description="**Reason:** [Bad Words]({})".format(message.jump_url))
									await message.author.send(msg1, embed=em1)
									msg2 = f"**{message.author}** has been muted."
									em2 = discord.Embed(description="**Reason:** [Bad Words]({})".format(message.jump_url))
									await message.channel.send(msg2, embed=em2)
									await asyncio.sleep(840)
									if muted in user.roles:
										await message.author.remove_roles(muted)
										await message.author.send("You have been unmuted in `ViHill Corner`")
									else:
										pass
							else:
								return
						except:
							pass
					
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', message.author.nick):
						try:
							await message.author.edit(nick=new_nick)
							await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', message.author.name):
						try:
							await message.author.edit(nick=new_nick)
							await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nnZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass
				except:
					pass
			for zalgo in zalgos:
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', message.author.nick):
						try:
							await message.author.edit(nick=new_nick_again)
							await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick_again}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', message.author.name):
						try:
							await message.author.edit(nick=new_nick_again)
							await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick_again}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass
						
					if re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', message.content):
						try:
							await message.delete()
							await message.author.send("Zalgo not allowed.")
						except:
							pass
				except:
					pass
			

	@commands.Cog.listener()
	async def on_message_edit(self,before,after):
		guild = self.client.get_guild(750160850077089853)
		staff = guild.get_role(754676705741766757)
		if after.guild:
			mod = guild.get_role(750162714407600228)
			muted = guild.get_role(750465726069997658)
			user = after.author
			new_nick = ''.join([choice(string.ascii_lowercase) for _ in range(7)])
			new_nick_again = ''.join([choice(string.ascii_lowercase) for _ in range(7)])
			words = None
			zalgos = None
			try:
				words = bad_words
				zalgos = zalgo_vars
			except	:
				words = words or []
				zalgos = zalgos or []
			for word in words:
				if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', after.content):
					if not "shoe" in after.content.lower():
						try:
							await after.delete()

							users = await get_warns_data()
							
							if str(user.id) in users:
								users[str(user.id)]["warns"] += 1

								with open("words-warns.json", "w", encoding="utf-8") as f:
									json.dump(users, f, ensure_ascii = False, indent = 4)

							else:
								users[str(user.id)] = {}
								users[str(user.id)]["warns"] = 0
								with open("words-warns.json", "w", encoding="utf-8") as f:
									json.dump(users, f, ensure_ascii = False, indent = 4)

							total_warns = users[str(user.id)]["warns"]


							if total_warns > 2:
								del users[str(user.id)]
								with open("words-warns.json", "w", encoding="utf-8") as f:
									json.dump(users, f, ensure_ascii = False, indent = 4)

								
								if "Staff" in [role.name for role in after.author.roles]:
									post = {
											'_id': user.id,
											'mutedAt': datetime.datetime.now(),
											'muteDuration': 840,
											'guildId': after.guild.id,
											}


									try:
										collection.insert_one(post)
									except pymongo.errors.DuplicateKeyError:
										return
									
									await after.author.add_roles(muted, reason="Bad Words")
									await after.author.remove_roles(staff, mod)
									msg1 = "You have been muted in `ViHill Corner`."
									em1 = discord.Embed(description="**Reason:** [Bad Words]({})".format(after.jump_url))
									await after.author.send(msg1, embed=em1)
									msg2 = f"**{after.author}** has been muted."
									em2 = discord.Embed(description="**Reason:** [Bad Words]({})".format(after.jump_url))
									await after.channel.send(msg2, embed=em2)
									await asyncio.sleep(840)
									if muted in user.roles:
										await after.author.remove_roles(muted)
										await after.author.add_roles(staff, muted)
										await after.author.send("You have been unmuted in `ViHill Corner`")
									else:
										pass
								
								else:
									post = {
											'_id': user.id,
											'mutedAt': datetime.datetime.now(),
											'muteDuration': 840,
											'guildId': after.guild.id,
											}


									try:
										collection.insert_one(post)
									except pymongo.errors.DuplicateKeyError:
										return
									await after.author.add_roles(muted, reason="Bad Words")
									msg1 = "You have been muted in `ViHill Corner`."
									em1 = discord.Embed(description="**Reason:** [Bad Words]({})".format(after.jump_url))
									await after.author.send(msg1, embed=em1)
									msg2 = f"**{after.author}** has been muted."
									em2 = discord.Embed(description="**Reason:** [Bad Words]({})".format(after.jump_url))
									await after.channel.send(msg2, embed=em2)
									await asyncio.sleep(840)
									if muted in user.roles:
										await after.author.remove_roles(muted)
										await after.author.send("You have been unmuted in `ViHill Corner`")
									else:
										pass
							else:
								return
						except:
							pass
					
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', after.author.nick):
						try:
							await after.author.edit(nick=new_nick)
							await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', after.author.name):
						try:
							await after.author.edit(nick=new_nick)
							await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nnZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass
				except:
					pass
			for zalgo in zalgos:
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', after.author.nick):
						try:
							await after.author.edit(nick=new_nick_again)
							await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick_again}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', after.author.name):
						try:
							await after.author.edit(nick=new_nick_again)
							await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick_again}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass
						
					if re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', after.content):
						try:
							await after.delete()
							await after.author.send("Zalgo not allowed.")
						except:
							pass
				except:
					pass




async def get_warns_data():
	with open("words-warns.json", "r") as f:
		users = json.load(f)

	return users


def setup (client):
	client.add_cog(FilterCog(client))