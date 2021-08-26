import discord
from discord.ext import commands
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

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db2['InvalidName Filter']

	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):
		if message.author.bot:
			return
		elif message.author.id == 374622847672254466:
			return
		
		if message.guild:
			user_name = str(message.author.name).lower()
			
			if message.author.nick != None:
				return

			f = remove_emoji(u" %s" % (user_name))
			
			for x in f:
				if x not in allowed_letters:
					user = await self.db.find_one({'_id': message.author.id})
					if user is None:
						kr = await self.db.find_one({'_id': 374622847672254466})
						new_index = kr['TotalInvalidNames'][-1] + 1
						old_list = kr['TotalInvalidNames']
						new_list = old_list + [new_index]
						post = {
							'_id': message.author.id,
							'InvalidNameIndex': new_index
						}
						await self.db.insert_one(post)
						await self.db.update_one({'_id': 374622847672254466}, {'$set':{'TotalInvalidNames': new_list}})
						new_nick = f'UnpingableName{new_index}'
					else:
						new_nick = f"UnpingableName{user['InvalidNameIndex']}"
						
					await message.author.edit(nick=new_nick)
					await message.author.send(f"Hello! Your `username` doesn't follow our naming policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
					return

	@commands.Cog.listener('on_member_remove')
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({'_id': member.id})


def setup(bot):
	bot.add_cog(NameFilter(bot))