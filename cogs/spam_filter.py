import json
import datetime

import disnake
from disnake.ext import commands

from utils.colors import Colours

from main import ViHillCorner

no_mute_these = (938097236024360960,)
ignored_channels = (
    790310516266500098, 780374324598145055, 750160851822182487, 750160851822182486, 750160852006469807, 750160852006469810,
    790309304422629386, 750160852006469806, 750160851822182484, 752164200222163016
)

time_convert = {900: '15 minutes', 1800: '30 minutes', 2700: '45 minutes', 3600: '60 minutes', 43200: '12 hours', 86400: '24 hours', None: 'Forever'}
muted_amount_count = {}


def get_mute_time(user_id) -> int:
    try:
        curr_amount = muted_amount_count[user_id]
        curr_amount += 1
        muted_amount_count[user_id] = curr_amount
    except KeyError:
        curr_amount = 1
        muted_amount_count[user_id] = 1

    if curr_amount == 1:
        return 900  # 15 mins
    elif curr_amount == 2:
        return 1800  # 30 mins
    elif curr_amount == 3:
        return 2700  # 45 mins
    elif curr_amount == 4:
        return 3600  # 60 mins
    elif curr_amount == 5:
        return 43200  # 12 hours
    elif curr_amount == 6:
        return 86400  # 24 hours


class RepeatedTextFilter(commands.Cog):

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Filter Mutes']

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.id in no_mute_these:
            return
        elif message.author.bot:
            return

        else:
            user = message.author
            users = await get_repeated_text_warns_data()

            if message.guild:
                if message.channel.id in ignored_channels:
                    return

                if not str(user.id) in users:
                    users[str(user.id)] = {}
                    users[str(user.id)]["warns"] = 0
                    users[str(user.id)]["sentence"] = message.content.lower()
                    with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
                        json.dump(users, f, ensure_ascii=False, indent=4)
                    return

                else:
                    the_message = users[str(user.id)]["sentence"]
                    if message.content.lower() == the_message:
                        users[str(user.id)]["warns"] += 1

                        with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, ensure_ascii=False, indent=4)

                    else:
                        del users[str(user.id)]
                        with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, ensure_ascii=False, indent=4)
                        return

                total_warns = users[str(user.id)]["warns"]

                if total_warns > 1:
                    await message.delete()

                if total_warns > 2:

                    del users[str(user.id)]
                    with open("repeated-text-filter.json", "w", encoding="utf-8") as f:
                        json.dump(users, f, ensure_ascii=False, indent=4)

                    is_staff = False
                    if 754676705741766757 in (role.id for role in message.author.roles):
                        is_staff = True

                    mute_time = get_mute_time(message.author.id)

                    post = {
                        '_id': user.id,
                        'muted_at': datetime.datetime.utcnow(),
                        'mute_duration': mute_time,
                        'guild_id': message.guild.id,
                        'staff': is_staff
                    }
                    try:
                        await self.db.insert_one(post)
                    except Exception:
                        return

                    guild = self.bot.get_guild(750160850077089853)
                    muted = guild.get_role(750465726069997658)
                    if is_staff is True:
                        new_roles = [role for role in message.author.roles if role.id not in (754676705741766757, 750162714407600228)] + [muted]
                    else:
                        new_roles = [role for role in message.author.roles] + [muted]
                    await message.author.edit(roles=new_roles, reason='Filter Mute (Repeated Text)')
                    msg1 = "You have been muted in `ViHill Corner`."
                    em = disnake.Embed(description=f"**Reason:** [Repeated Text]({message.jump_url})\n**Time:** `{time_convert[mute_time]}`")
                    await user.send(msg1, embed=em)
                    msg2 = f"**{user}** has been muted."
                    ju = await message.channel.send(msg2, embed=em)
                    staff_channel = guild.get_channel(752164200222163016)
                    log = disnake.Embed(
                        color=Colours.red,
                        title="___Filter Mute___",
                        description=f"User: `{message.author}`\nReason: [`Repeated Text`]({ju.jump_url})\nTime: `{time_convert[mute_time]}`",
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_footer(text=f"User ID: {message.author.id}")
                    await staff_channel.send(embed=log)
                else:
                    return


class SpamFilter(commands.Cog):

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Filter Mutes']

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.id in no_mute_these:
            return
        if message.author.bot:
            return

        else:
            user = message.author
            users = await get_spam_warns_data()

            if message.guild:
                if message.channel.id in ignored_channels:
                    return

                else:
                    if not str(user.id) in users:
                        users[str(user.id)] = {}
                        users[str(user.id)]["warns"] = 0
                        with open("spam-warns.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, ensure_ascii=False, indent=4)
                        return

                    else:
                        users[str(user.id)]["warns"] += 1

                        with open("spam-warns.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, ensure_ascii=False, indent=4)

                    total_warns = users[str(user.id)]["warns"]

                    if total_warns > 2:
                        await message.delete()

                    if total_warns > 4:
                        del users[str(user.id)]
                        with open("spam-warns.json", "w", encoding="utf-8") as f:
                            json.dump(users, f, ensure_ascii=False, indent=4)

                        is_staff = False
                        if 754676705741766757 in (role.id for role in message.author.roles):
                            is_staff = True

                        mute_time = get_mute_time(message.author.id)

                        post = {
                            '_id': user.id,
                            'muted_at': datetime.datetime.utcnow(),
                            'mute_duration': mute_time,
                            'guild_id': message.guild.id,
                            'staff': is_staff
                        }

                        try:
                            await self.db.insert_one(post)
                        except Exception:
                            return
                        guild = self.bot.get_guild(750160850077089853)
                        muted = guild.get_role(750465726069997658)
                        if is_staff is True:
                            new_roles = [role for role in message.author.roles if role.id not in (754676705741766757, 750162714407600228)] + [muted]
                        else:
                            new_roles = [role for role in message.author.roles] + [muted]
                        await message.author.edit(roles=new_roles, reason='Filter Mute (Spam)')
                        msg1 = "You have been muted in `ViHill Corner`."
                        em = disnake.Embed(description=f"**Reason:** [Spam]({message.jump_url})\n**Time:** `{time_convert[mute_time]}`")
                        await user.send(msg1, embed=em)
                        msg2 = f"**{user}** has been muted."
                        ju = await message.channel.send(msg2, embed=em)
                        staff_channel = guild.get_channel(752164200222163016)
                        log = disnake.Embed(
                            color=Colours.red,
                            title="___Filter Mute___",
                            description=f"User: `{message.author}`\nReason: [`Spam`]({ju.jump_url})\nTime: `{time_convert[mute_time]}`",
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_footer(text=f"User ID: {message.author.id}")
                        await staff_channel.send(embed=log)
                    else:
                        return


async def get_repeated_text_warns_data():
    with open("repeated-text-filter.json", "r") as f:
        users = json.load(f)

    return users


async def get_spam_warns_data():
    with open("spam-warns.json", "r") as f:
        users = json.load(f)

    return users


def setup(bot):
    bot.add_cog(RepeatedTextFilter(bot))
    bot.add_cog(SpamFilter(bot))
