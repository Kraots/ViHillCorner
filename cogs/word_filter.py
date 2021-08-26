import re
import discord
from discord.ext import commands
import utils.colors as color
import json
import datetime
from .spam_filter import get_mute_time

no_mute_these = [374622847672254466, 751724369683677275]

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

bad_words_names_edition = [ "nigga",
							"nigger",
							"niggas",
							"niggers",
							"nigges",
							"nigge"
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

ok_words = ["shoe", "whoever"]

class FilterCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Filter Mutes']
		self.db2 = bot.db2['InvalidName Filter']

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id in no_mute_these:
			return

		if message.guild:
			user = message.author
			words = None
			zalgos = None
			wordss = None
			try:
				words = bad_words
				zalgos = zalgo_vars
				wordss = bad_words_names_edition
			except	:
				words = words or []
				zalgos = zalgos or []
				wordss = wordss or []
			for word in words:
				if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', message.content):
					if "shoe" in message.content.lower():
						return
					elif "whoever" in message.content.lower():
						return
					elif "mustard" in message.content.lower():
						return
					elif "nigeria" in message.content.lower():
						return
					elif "nigerian" in message.content.lower():
						return

					else:
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

								isStaff = False
								if 754676705741766757 in [role.id for role in message.author.roles]:
									isStaff = True
								
								mute_time = get_mute_time(user.id)

								post = {
										'_id': user.id,
										'mutedAt': datetime.datetime.now(),
										'muteDuration': mute_time,
										'guildId': message.guild.id,
										'staff': isStaff
										}
								try:
									await self.db.insert_one(post)
								except:
									return
								guild = self.bot.get_guild(750160850077089853)
								muted = guild.get_role(750465726069997658)
								if isStaff == True:
									new_roles = [role for role in message.author.roles if not role.id in [754676705741766757, 750162714407600228]] + [muted]
								else:
									new_roles = [role for role in message.author.roles] + [muted]
								await message.author.edit(roles=new_roles, reason='Filter Mute (bad words)')
								msg1 = "You have been muted in `ViHill Corner`."
								em = discord.Embed(description="**Reason:** [Bad Words]({})".format(message.jump_url))
								await message.author.send(msg1, embed=em)
								msg2 = f"**{message.author}** has been muted."
								ju = await message.channel.send(msg2, embed=em)
								staff_channel = guild.get_channel(752164200222163016)
								log = discord.Embed(color=color.red, title="___Filter Mute___", description=f"User: `{message.author}`\nReason: [`Bad Words`]({ju.jump_url})", timestamp=datetime.datetime.utcnow())
								em.set_footer(text=f"User ID: {message.author.id}")
								await staff_channel.send(embed=log)
							else:
								return
						except:
							pass
			for zalgo in zalgos:
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', message.author.nick):
						try:
							_user = await self.db2.find_one({'_id': message.author.id})
							if _user is None:
								kr = await self.db2.find_one({'_id': 374622847672254466})
								new_index = kr['TotalInvalidNames'][-1] + 1
								old_list = kr['TotalInvalidNames']
								new_list = old_list + [new_index]
								post = {
									'_id': message.author.id,
									'InvalidNameIndex': new_index
								}
								await self.db2.insert_one(post)
								await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
								new_nick = f'UnpingableName{new_index}'
								new_nick_again = new_nick
							else:
								new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
								new_nick_again = new_nick

							await message.author.edit(nick=new_nick_again)
							await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick_again}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', message.author.name):
						check = True
						if message.author.nick != None:
							check = False
						if check != False:
							try:
								_user = await self.db2.find_one({'_id': message.author.id})
								if _user is None:
									kr = await self.db2.find_one({'_id': 374622847672254466})
									new_index = kr['TotalInvalidNames'][-1] + 1
									old_list = kr['TotalInvalidNames']
									new_list = old_list + [new_index]
									post = {
										'_id': message.author.id,
										'InvalidNameIndex': new_index
									}
									await self.db2.insert_one(post)
									await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
									new_nick = f'UnpingableName{new_index}'
									new_nick_again = new_nick
								else:
									new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
									new_nick_again = new_nick

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
			for wordd in wordss:
				try:
					if message.author.nick:
						if re.search(r'(?i)(\b' + r'+\W*'.join(wordd) + f'|{wordd})', message.author.nick):
							try:
								_user = await self.db2.find_one({'_id': message.author.id})
								if _user is None:
									kr = await self.db2.find_one({'_id': 374622847672254466})
									new_index = kr['TotalInvalidNames'][-1] + 1
									old_list = kr['TotalInvalidNames']
									new_list = old_list + [new_index]
									post = {
										'_id': message.author.id,
										'InvalidNameIndex': new_index
									}
									await self.db2.insert_one(post)
									await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
									new_nick = f'UnpingableName{new_index}'
									new_nick_again = new_nick
								else:
									new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
									new_nick_again = new_nick

								await message.author.edit(nick=new_nick)
								await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
							except:
								pass
				
					elif re.search(r'(?i)(\b' + r'+\W*'.join(wordd) + f'|{wordd})', message.author.name):
						check = True
						if message.author.nick != None:
							check = False
						if check != False:
							try:
								_user = await self.db2.find_one({'_id': message.author.id})
								if _user is None:
									kr = await self.db2.find_one({'_id': 374622847672254466})
									new_index = kr['TotalInvalidNames'][-1] + 1
									old_list = kr['TotalInvalidNames']
									new_list = old_list + [new_index]
									post = {
										'_id': message.author.id,
										'InvalidNameIndex': new_index
									}
									await self.db2.insert_one(post)
									await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
									new_nick = f'UnpingableName{new_index}'
									new_nick_again = new_nick
								else:
									new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
									new_nick_again = new_nick

								await message.author.edit(nick=new_nick)
								await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nnZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
							except:
								pass
				except:
					pass
			

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if after.author.id in no_mute_these:
			return

		if after.guild:
			user = after.author
			words = None
			zalgos = None
			wordss = None
			try:
				words = bad_words
				zalgos = zalgo_vars
				wordss = bad_words_names_edition
			except:
				words = words or []
				zalgos = zalgos or []
				wordss = wordss or []
			for word in words:
				if re.search(r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})', after.content):
					if "shoe" in after.content.lower():
						return
					elif "whoever" in after.content.lower():
						return
					elif "mustard" in after.content.lower():
						return
					elif "nigeria" in after.content.lower():
						return
					elif "nigerian" in after.content.lower():
						return
					else:
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

								isStaff = False
								if 754676705741766757 in [role.id for role in after.author.roles]:
									isStaff = True
								
								mute_time = get_mute_time(user.id)

								post = {
										'_id': user.id,
										'mutedAt': datetime.datetime.now(),
										'muteDuration': mute_time,
										'guildId': after.guild.id,
										'staff': isStaff
										}
								try:
									await self.db.insert_one(post)
								except:
									return
								guild = self.bot.get_guild(750160850077089853)
								muted = guild.get_role(750465726069997658)
								if isStaff == True:
									new_roles = [role for role in after.author.roles if not role.id in [754676705741766757, 750162714407600228]] + [muted]
								else:
									new_roles = [role for role in after.author.roles] + [muted]
								await after.author.edit(roles=new_roles, reason='Filter Mute (bad words)')
								msg1 = "You have been muted in `ViHill Corner`."
								em = discord.Embed(description="**Reason:** [Bad Words]({})".format(after.jump_url))
								await after.author.send(msg1, embed=em)
								msg2 = f"**{after.author}** has been muted."
								ju = await after.channel.send(msg2, embed=em)
								staff_channel = guild.get_channel(752164200222163016)
								log = discord.Embed(color=color.red, title="___Filter Mute___", description=f"User: `{after.author}`\nReason: [`Zalgo`]({ju.jump_url})", timestamp=datetime.datetime.utcnow())
								em.set_footer(text=f"User ID: {after.author.id}")
								await staff_channel.send(embed=log)
							else:
								return
						except:
							pass
			for zalgo in zalgos:
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', after.author.nick):
						try:
							_user = await self.db2.find_one({'_id': after.author.id})
							if _user is None:
								kr = await self.db2.find_one({'_id': 374622847672254466})
								new_index = kr['TotalInvalidNames'][-1] + 1
								old_list = kr['TotalInvalidNames']
								new_list = old_list + [new_index]
								post = {
									'_id': after.author.id,
									'InvalidNameIndex': new_index
								}
								await self.db2.insert_one(post)
								await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
								new_nick = f'UnpingableName{new_index}'
								new_nick_again = new_nick
							else:
								new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
								new_nick_again = new_nick
							await after.author.edit(nick=new_nick_again)
							await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick_again}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(zalgo) + f'|{zalgo})', after.author.name):
						check = True
						if after.author.nick != None:
							check = False
						if check != False:
							try:
								_user = await self.db2.find_one({'_id': after.author.id})
								if _user is None:
									kr = await self.db2.find_one({'_id': 374622847672254466})
									new_index = kr['TotalInvalidNames'][-1] + 1
									old_list = kr['TotalInvalidNames']
									new_list = old_list + [new_index]
									post = {
										'_id': after.author.id,
										'InvalidNameIndex': new_index
									}
									await self.db2.insert_one(post)
									await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
									new_nick = f'UnpingableName{new_index}'
									new_nick_again = new_nick
								else:
									new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
									new_nick_again = new_nick

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
			for wordd in wordss:
				try:
					if re.search(r'(?i)(\b' + r'+\W*'.join(wordd) + f'|{wordd})', after.author.nick):
						try:
							_user = await self.db2.find_one({'_id': after.author.id})
							if _user is None:
								kr = await self.db2.find_one({'_id': 374622847672254466})
								new_index = kr['TotalInvalidNames'][-1] + 1
								old_list = kr['TotalInvalidNames']
								new_list = old_list + [new_index]
								post = {
									'_id': after.author.id,
									'InvalidNameIndex': new_index
								}
								await self.db2.insert_one(post)
								await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
								new_nick = f'UnpingableName{new_index}'
								new_nick_again = new_nick
							else:
								new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
								new_nick_again = new_nick
							await after.author.edit(nick=new_nick)
							await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						except:
							pass

					elif re.search(r'(?i)(\b' + r'+\W*'.join(wordd) + f'|{wordd})', after.author.name):
						check = True
						if after.author.nick != None:
							check = False
						if check != False:
							try:
								_user = await self.db2.find_one({'_id': after.author.id})
								if _user is None:
									kr = await self.db2.find_one({'_id': 374622847672254466})
									new_index = kr['TotalInvalidNames'][-1] + 1
									old_list = kr['TotalInvalidNames']
									new_list = old_list + [new_index]
									post = {
										'_id': after.author.id,
										'InvalidNameIndex': new_index
									}
									await self.db2.insert_one(post)
									await self.db2.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
									new_nick = f'UnpingableName{new_index}'
									new_nick_again = new_nick
								else:
									new_nick = f"UnpingableName{_user['InvalidNameIndex']}"
									new_nick_again = new_nick
								await after.author.edit(nick=new_nick)
								await after.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nnZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
							except:
								pass
				except:
					pass




async def get_warns_data():
	with open("words-warns.json", "r") as f:
		users = json.load(f)

	return users


def setup(bot):
	bot.add_cog(FilterCog(bot))