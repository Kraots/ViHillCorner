from disnake.ext import commands, tasks
import json


class WarnsRemove(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.clear_caps_warns.start()
        self.clear_words_warns.start()
        self.clear_spam_warns.start()
        self.clear_repeated_text_warns.start()

    @tasks.loop(seconds=45)
    async def clear_caps_warns(self):
        users = await get_caps_warns_data()
        users.clear()

        with open("caps-warns.json", "w") as f:
            json.dump(users, f)

    @tasks.loop(seconds=120)
    async def clear_words_warns(self):
        users = await get_words_warns_data()
        users.clear()

        with open("words-warns.json", "w") as f:
            json.dump(users, f)

    @tasks.loop(seconds=10)
    async def clear_spam_warns(self):
        users = await get_spam_warns_data()
        users.clear()

        with open("spam-warns.json", "w") as f:
            json.dump(users, f)

    @tasks.loop(seconds=360)
    async def clear_repeated_text_warns(self):
        users = await get_repeated_text_warns_data()
        users.clear()

        with open("repeated-text-filter.json", "w") as f:
            json.dump(users, f)


async def get_caps_warns_data():
    with open("caps-warns.json", "r") as f:
        users = json.load(f)

    return users


async def get_words_warns_data():
    with open("words-warns.json", "r") as f:
        users = json.load(f)

    return users


async def get_spam_warns_data():
    with open("spam-warns.json", "r") as f:
        users = json.load(f)

    return users


async def get_repeated_text_warns_data():
    with open("repeated-text-filter.json", "r") as f:
        users = json.load(f)

    return users


def setup(bot):
    bot.add_cog(WarnsRemove(bot))
