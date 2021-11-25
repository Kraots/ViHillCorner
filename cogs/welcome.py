import asyncio
import re
from random import randint

from .name_filter import allowed_letters
from .intro import IntroButton

import disnake
from disnake.ext import commands

from utils import time
from utils.helpers import ConfirmViewDMS
from utils.colors import Colours

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


class Welcome(commands.Cog):
    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db1 = bot.base('Intros')
        self.db2 = bot.db1['Moderation Mutes']
        self.db3 = bot.db1['Filter Mutes']
        self.db4 = bot.db2['InvalidName Filter']

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member: disnake.Member):

        VHguild: disnake.Guild = self.bot.get_guild(750160850077089853)
        welcomechannel = VHguild.get_channel(750160850303582237)
        if member.bot:
            role = VHguild.get_role(750160850290999327)
            return await member.add_roles(role, reason='Bot Account.')
        member_count = len([m for m in VHguild.members if not m.bot])

        if member.guild == VHguild:
            def format_date(dt):
                return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'
            welcome = disnake.Embed(
                description="\n\n***Please read the rules at*** <#750160850303582236>\n***You can always get a colour from*** <#779388444304211991>\n"
                            "***For bot commands please use*** <#750160851822182486>\n\n"
                            "Enjoy your stay and don't forget to do your intro by typing `!intro` in a bots channel ^-^\n\n",
                color=Colours.pastel)
            welcome.set_thumbnail(url=member.display_avatar)
            welcome.set_footer(text=f"Created: {format_date(member.created_at.replace(tzinfo=None))}", icon_url=member.display_avatar)
            msg = f'Hey {member.mention}, welcome to **ViHill Corner!** \nYou are our **{member_count}** member.\n\n\n_ _'
            await welcomechannel.send(msg, embed=welcome)

            if member.bot:
                return
            elif member.id == 374622847672254466:
                return

            user_name = str(member.name).lower()
            f = remove_emoji(u" %s" % (user_name))

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
                user = await self.db4.find_one({'_id': member.id})
                if user is None:
                    kr = await self.db4.find_one({'_id': 374622847672254466})
                    new_index = kr['TotalInvalidNames'][-1] + 1
                    old_list = kr['TotalInvalidNames']
                    new_list = old_list + [new_index]
                    post = {
                        '_id': member.id,
                        'InvalidNameIndex': new_index
                    }
                    await self.db4.insert_one(post)
                    await self.db4.update_one({'_id': 374622847672254466}, {'$set': {'TotalInvalidNames': new_list}})
                    new_nick = f'UnpingableName{new_index}'
                else:
                    new_nick = f"UnpingableName{user['InvalidNameIndex']}"

                await member.edit(nick=new_nick)
                await member.send(
                    "Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. "
                    f"(`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:"
                    "**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner"
                )
                await self.bot._owner.send(f'**{member}** got nick changed, letter that lead to this: `{x}`')

            choice = randint(1, 19)
            colors = {
                1: 750272224170082365, 2: 750160850299387977, 3: 750160850299387976, 4: 750160850299387975,
                5: 750160850299387974, 6: 750160850299518985, 7: 750160850299518984, 8: 750160850299518983,
                9: 750160850299518982, 10: 750160850299518981, 11: 750160850299518980, 12: 750160850299518979,
                13: 750160850299518978, 14: 750160850299518977, 15: 750160850295324752, 16: 750160850299518976,
                17: 750160850295324751, 18: 750272729533644850, 19: 788112413261168660
            }
            color_ = VHguild.get_role(colors[choice])
            await member.add_roles(color_)

            results = await self.db2.find_one({'_id': member.id})
            if results is not None:
                guild = self.bot.get_guild(750160850077089853)

                mute_role = guild.get_role(750465726069997658)
                await member.add_roles(mute_role)

            resultss = await self.db3.find_one({'_id': member.id})
            if resultss is not None:
                guild = self.bot.ge(750160850077089853)

                mute_role = guild.get_role(750465726069997658)
                await member.add_roles(mute_role)

            introchannel = VHguild.get_channel(750160850593251449)

            msg1 = await member.send("Welcome to `ViHill Corner`, would you like to introduce yourself to us?")
            ctx = await self.bot.get_context(msg1)
            view = ConfirmViewDMS(ctx)
            await msg1.edit(view=view)
            await view.wait()
            if view.response is None:
                new_msg = "Welcome to `ViHill Corner`, if you wish to do your intro please go in <#750160851822182486> and type `!intro`"
                return await msg1.edit(content=new_msg, view=None)

            elif view.response is False:
                e = "Alrighty, you can do your intro later by typing `!intro` in <#750160851822182486>. Enjoy your stay! :wave:"
                return await msg1.edit(content=e, view=view)

            elif view.response is True:
                channel = msg1.channel

                def check(message):
                    return message.channel.id == channel.id and message.author.id == member.id

                e = "What's your name?\n\n*To cancel type `!cancel`*"
                await msg1.edit(content=e, view=view)
                try:
                    name = await self.bot.wait_for('message', timeout=180, check=check)
                    if name.content.lower() == '!cancel':
                        await channel.send("Cancelled.")
                        return

                except asyncio.TimeoutError:
                    await channel.send("Ran out of time.")
                    return

                else:
                    await channel.send("Where are you from?")

                    try:
                        location = await self.bot.wait_for('message', timeout=180, check=check)
                        if location.content.lower() == '!cancel':
                            await channel.send("Cancelled.")
                            return

                    except asyncio.TimeoutError:
                        await channel.send("Ran out of time.")
                        return

                    else:
                        await channel.send("How old are you?")

                        try:
                            while True:
                                age = await self.bot.wait_for('message', timeout=180, check=check)
                                if age.content.lower() == '!cancel':
                                    await channel.send("Cancelled.")
                                    return
                                try:
                                    agenumber = int(age.content)
                                    if agenumber >= 44 or agenumber <= 11:
                                        await channel.send("Please put your real age and not a fake age.")
                                    else:
                                        break
                                except ValueError:
                                    await channel.send("Must be number.")

                        except asyncio.TimeoutError:
                            await channel.send("Ran out of time.")
                            return

                        else:
                            await channel.send("What's your gender?")

                            try:
                                gender = await self.bot.wait_for('message', timeout=180, check=check)
                                if gender.content.lower() == '!cancel':
                                    await channel.send("Cancelled.")
                                    return

                            except asyncio.TimeoutError:
                                await channel.send("Ran out of time.")
                                return

                            else:
                                await channel.send("Relationship status? `single` | `taken` | `complicated`")

                                try:
                                    while True:
                                        prestatuss = await self.bot.wait_for('message', timeout=180, check=check)
                                        status = prestatuss.content.lower()
                                        if status == '!cancel':
                                            await channel.send("Cancelled.")
                                            return
                                        if status in ('single', 'taken', 'complicated'):
                                            break
                                        else:
                                            await channel.send("Please only choose from `single` | `taken` | `complicated`")

                                except asyncio.TimeoutError:
                                    await channel.send("Ran out of time.")
                                    return

                                else:
                                    await channel.send("What are u interested to?")

                                    try:
                                        interests = await self.bot.wait_for('message', timeout=360, check=check)
                                        if interests.content.lower() == '!cancel':
                                            await channel.send("Cancelled.")
                                            return

                                    except asyncio.TimeoutError:
                                        await channel.send("Ran out of time.")
                                        return

                                    else:
                                        em = disnake.Embed(color=member.color)
                                        em.set_author(name=member, icon_url=member.display_avatar)
                                        em.set_thumbnail(url=member.display_avatar)
                                        em.add_field(name="Name", value=name.content, inline=True)
                                        em.add_field(name="Location", value=location.content, inline=True)
                                        em.add_field(name="Age", value=agenumber, inline=True)
                                        em.add_field(name="Gender", value=gender.content, inline=False)
                                        em.add_field(name="Relationship Status", value=status, inline=True)
                                        em.add_field(name="Interests", value=interests.content, inline=False)
                                        intro_msg = await introchannel.send(embed=em)
                                        await member.send(
                                            "Intro added successfully. You can see in <#750160850593251449>.",
                                            view=IntroButton(f"{self.bot.url}/intros/{str(member.id)}")
                                        )

                                        post = {
                                            "name": name.content,
                                            "location": location.content,
                                            "age": agenumber,
                                            "gender": gender.content,
                                            "status": status,
                                            "interests": interests.content,
                                            "intro_id": str(intro_msg.id)
                                        }

                                        self.db1.insert(post, str(member.id))

                                        return

        else:
            return


def setup(bot):
    bot.add_cog(Welcome(bot))
