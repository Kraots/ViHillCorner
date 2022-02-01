import re

import disnake
from disnake.ext import commands

from .name_filter import allowed_letters

from main import ViHillCorner


def remove_emoji(string):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300"
        u"\U0001F251"  # symbols & pictographs
        u"\U0001F680"  # transport & map symbols
        u"\U00002702-\U000027B0"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', string)


class NickFilter(commands.Cog):

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db2['InvalidName Filter']

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        elif message.author.id == 938097236024360960:
            return

        if message.guild:
            user_nickname = str(message.author.nick).lower()
            f = remove_emoji(u" %s" % (user_nickname))

            good_count = 0
            for x in f:
                if good_count < 4:
                    if x not in allowed_letters:
                        x = x
                        good_count = 0
                    else:
                        good_count += 1
                else:
                    break

            if good_count < 4:
                user = await self.db.find_one({'_id': message.author.id})
                if user is None:
                    kr = await self.db.find_one({'_id': 938097236024360960})
                    new_index = kr['TotalInvalidNames'][-1] + 1
                    old_list = kr['TotalInvalidNames']
                    new_list = old_list + [new_index]
                    post = {
                        '_id': message.author.id,
                        'InvalidNameIndex': new_index
                    }
                    await self.db.insert_one(post)
                    await self.db.update_one({'_id': 938097236024360960}, {'$set': {'TotalInvalidNames': new_list}})
                    new_nick = f'UnpingableName{new_index}'
                else:
                    new_nick = f"UnpingableName{user['InvalidNameIndex']}"

                await message.author.edit(nick=new_nick)
                await message.author.send(
                    f"Hello! Your `nickname` doesn't follow our naming policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n "
                    "If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡"
                    "\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner"
                )
                await self.bot._owner.send(f'**{message.author}** got nick changed, letter that lead to this: `{x}`')


def setup(bot):
    bot.add_cog(NickFilter(bot))
