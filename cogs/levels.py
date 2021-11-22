import pymongo

import disnake
from disnake.ext import commands

from utils.colors import Colours
from utils.context import Context
from utils.pillow import rank_card
from utils.paginator import RoboPages, FieldPageSource
from utils.databases import Level

from main import ViHillCorner

bot_channel = (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061, 787359417674498088)
no_talk_channels = (750160852006469807, 780374324598145055)
bot_channels = (750160851822182486, 750160851822182487)

# LEVEL: LEVEL_ROLE_ID
levels = {
    3: 758278459645755392, 5: 750160850290999330, 10: 750160850290999331, 15: 750160850290999332, 20: 750160850290999333,
    25: 750160850290999334, 30: 750160850290999335, 40: 750160850295324744, 45: 750160850295324745, 50: 750160850295324746,
    55: 750160850295324747, 60: 750160850295324748, 65: 750160850295324749, 69: 750160850295324750, 75: 788127504710762497,
    80: 788127526278791240, 85: 788127540459208725, 90: 788127547606827028, 95: 788127552686129265, 100: 788127561283928115,
    105: 788127569198579764, 110: 788127574663495720, 120: 788127580330655744, 130: 788127589092818994, 150: 788127593386868758,
    155: 818562249349660713, 160: 818562250252091413, 165: 818562250477404173, 170: 818562251644076072, 175: 818562252185534465,
    180: 818562252360777749, 185: 818562252906037259, 190: 818562253501628507, 195: 818562254043480075, 200: 818562254495547462,
    205: 818562254680883241, 210: 818562255188131924, 215: 818562256101965844, 220: 818562256546824192, 230: 818562257033101372,
    240: 818562257653858304, 250: 818562258119950367, 255: 818562258551832657, 260: 818562259587563523, 265: 818562260254588988,
    270: 818562260686995486, 275: 818562261844230215, 280: 818562262360784977, 285: 818562262520430654, 290: 818562263169368076,
    300: 818562263850025031, 305: 818562264030380033, 310: 818562264554405899, 315: 818562265422757898, 320: 818562265779273749,
    330: 818562266475528242, 340: 818562266760740926, 350: 818562267410726964, 355: 818562267837628456, 360: 818562268044197889,
    365: 818562268966027294, 370: 818562269029466124, 375: 818562269835034625, 380: 818562270119985163, 385: 818562270375182357,
    390: 818562271100928020, 395: 818562271269486623, 400: 818562271978586132, 405: 818562272791101500, 410: 818562273202405396,
    415: 818562273215774776, 420: 818562274318090260, 430: 818562274502508555, 440: 818562275539550239, 450: 818562276490870857,
    455: 818562276939661343, 460: 818562277514805258, 465: 818562277619400765, 470: 818562278521569282, 475: 818562278832078939,
    480: 818562279725203508, 485: 818562280009760889, 490: 818562280765390909, 495: 818562281410658344, 500: 818562282019356733
}


class Levels(commands.Cog):
    """Level related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='super_mario_green_shroom', id=894627264162045962)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.guild:
            ch_id = message.channel.id
            if ch_id not in no_talk_channels:
                if not message.author.bot:
                    guild = self.bot.get_guild(750160850077089853)
                    stats: Level = await Level.find_one({"_id": message.author.id})
                    if stats is None:
                        try:
                            await Level(
                                id=message.author.id,
                                xp=0,
                                messages_count=0,
                                weekly_messages_count=0
                            ).commit()
                            return
                        except pymongo.errors.DuplicateKeyError:
                            return

                    kraots_doc: Level = await Level.find_one({'_id': self.bot._owner_id})

                    if ch_id not in bot_channels:
                        stats.weekly_messages_count += 1
                        await stats.commit()

                    xp = stats.xp
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                            break
                        lvl += 1
                    xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                    if xp < 0:
                        lvl = lvl - 1
                        xp = stats.xp
                        xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                    if lvl >= 500:
                        return

                    else:
                        if message.author.id == 374622847672254466:
                            xp = stats.xp + (30 * kraots_doc.kraots_xp_multiplier)
                        elif 754676705741766757 in (role.id for role in message.author.roles):
                            xp = stats.xp + (20 * kraots_doc.mod_xp_multiplier)
                        elif 759475712867565629 in (role.id for role in message.author.roles):
                            xp = stats.xp + (15 * kraots_doc.booster_xp_multiplier)
                        else:
                            xp = stats.xp + (5 * kraots_doc.xp_multiplier)

                        stats.xp = xp
                        await stats.commit()
                        lvl = 0
                        while True:
                            if xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                                break
                            lvl += 1
                        xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                        if xp < 0:
                            lvl = lvl - 1
                            xp = stats.xp
                            xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                        elif xp >= 0:
                            if lvl >= 3:
                                if message.guild.id == 750160850077089853:
                                    try:
                                        role_id = levels[lvl]
                                        roles_id = [role.id for role in message.author.roles if role.id not in (levels[k] for k in levels)] + [role_id]
                                        newroles = []
                                        for role in roles_id:
                                            newrole = guild.get_role(role)
                                            newroles.append(newrole)
                                        await message.author.edit(roles=newroles)
                                    except KeyError:
                                        role_id = 0
                                        for k in levels:
                                            if k < lvl:
                                                role_id = levels[k]
                                            else:
                                                break
                                        roles_id = [role.id for role in message.author.roles if role.id not in (levels[k] for k in levels)] + [role_id]
                                        newroles = []
                                        for role in roles_id:
                                            newrole = guild.get_role(role)
                                            newroles.append(newrole)
                                        await message.author.edit(roles=newroles)

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['lvl', 'level'])
    async def rank(self, ctx: Context, member: disnake.Member = None):
        """
        Check the member's level.
        This will send you a image with their data.
        """
        member = member or ctx.author

        if ctx.channel.id in bot_channel:
            stats: Level = await Level.find_one({"_id": member.id})
            if stats is None:
                if member.id == ctx.author.id:
                    await ctx.send("You haven't sent any messages, therefore you don't have a level.")
                    return
                elif member.bot:
                    await ctx.send("Bots do not have levels.")
                    return
                else:
                    await ctx.send(f"`{member.display_name}` did not send any messages, therefore they do not have any level.")
                    return
            else:
                xp = stats.xp
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                        break
                    lvl += 1
                xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                rankings: list[Level] = await Level.find().sort('xp', -1).to_list(100000)
                for data in rankings:
                    rank += 1
                    if stats.id == data.id:
                        break

                if xp < 0:
                    lvl = lvl - 1
                    xp = stats.xp
                    xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))

                guild = self.bot.get_guild(750160850077089853)
                members_count = len([m for m in guild.members if not m.bot])

                if str(xp).endswith(".0"):
                    x = str(xp).replace(".0", "")
                    x = int(x)
                else:
                    x = int(xp)

                current_xp = x
                needed_xp = int(200 * ((1 / 2) * lvl))
                percent = round(float(current_xp * 100 / needed_xp), 2)

                f = await rank_card(member, lvl, rank, members_count, current_xp, needed_xp, percent)
                await ctx.send(file=f)

    @rank.command(name='set')
    @commands.is_owner()
    async def rank_set(self, ctx: Context, lvl: int, member: disnake.Member = None):
        """Set the rank for the member."""

        member = member or ctx.author
        mem: Level = await Level.find_one({'_id': member.id})
        if not mem:
            return await ctx.reply('Member not in the database.')

        xp = ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
        mem.xp = xp
        await mem.commit()
        await ctx.send("Set level `{}` for **{}**.".format(lvl, member.display_name))

    @rank.command(name='leaderboard', aliases=['lb', 'top'])
    async def rank_leaderboard(self, ctx: Context):
        """Leaderboard for levels."""

        if ctx.channel.id in bot_channel:
            top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
            data = []
            results: list[Level] = await Level.find().sort('xp', -1).to_list(100000)
            index = 0
            for result in results:
                xp = result.xp
                user = result.id
                user = self.bot.get_user(user)

                lvl = 0
                while True:
                    if xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                        break
                    lvl += 1

                xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))

                if xp < 0:
                    lvl = lvl - 1
                    xp = result.xp

                index += 1
                f = result.xp
                if lvl == 500:
                    lvl = "500(MAX)"

                if str(f).endswith(".0"):
                    f = str(f).replace(".0", "")
                    f = int(f)
                else:
                    f = int(f)

                if index in (1, 2, 3):
                    place = top_3_emojis[index]
                else:
                    place = f'`#{index:,}`'
                if user == ctx.author:
                    to_append = (f"**{place} {user.name} (YOU)**", f"Level: `{lvl}`\nTotal XP: `{f:,}`")
                    data.append(to_append)
                else:
                    to_append = (f"{place} {user.name}", f"Level: `{lvl}`\nTotal XP: `{f:,}`")
                    data.append(to_append)

            source = FieldPageSource(data, per_page=10)
            source.embed.title = 'Rank top'
            pages = RoboPages(source, ctx=ctx)
            await pages.start()

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['multipliers'])
    async def multiplier(self, ctx: Context):
        """See the multipliers."""

        kraots_doc: Level = await Level.find_one({'_id': 374622847672254466})
        members_multiplier = float(kraots_doc.xp_multiplier)
        boosters_multiplier = float(kraots_doc.booster_xp_multiplier)
        mod_multiplier = float(kraots_doc.mod_xp_multiplier)
        kraots_multiplier = float(kraots_doc.kraots_xp_multiplier)

        em = disnake.Embed(color=Colours.light_pink, title="**Current Multipliers:**")
        em.add_field(
            name="Mod/Staff",
            value=f"{mod_multiplier}x ({20 * mod_multiplier} XP per message)",
            inline=False
        )
        em.add_field(
            name="Server Boosters",
            value=f"{boosters_multiplier}x ({15 * boosters_multiplier} XP per message)",
            inline=False
        )
        em.add_field(
            name="Members",
            value=f"{members_multiplier}x ({5 * members_multiplier} XP per message)",
            inline=False
        )
        em.add_field(
            name="Kraots",
            value=f"{kraots_multiplier}x ({30 * kraots_multiplier} XP per message)",
            inline=False
        )
        em.set_footer(text=f"Requested By: {ctx.author}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=em)

    @multiplier.command(name='set')
    @commands.is_owner()
    async def multiplier_set(self, ctx: Context, group: str = None, multiplier: float = None):
        """Set the multiplier for a group."""

        if group is None:
            await ctx.send(
                "You must specify which group you want to set the multiplier for.\nGroups:\n\u2800 • **Mod/Staff**\n\u2800 • **Boosters**\n\u2800 "
                "• **Members**\n\u2800 • **Kraots**\n\u2800 • **all**"
            )
            return

        elif multiplier is None:
            await ctx.send("You must give the number that you want to multiply the XP with.")
            return

        elif multiplier > 1000000:
            await ctx.send("You can't set the multiplier more than `1,000,000`, or else it will break the bot.")
            return

        else:
            group = group.lower()

            if str(multiplier).endswith(".0"):
                x = str(multiplier).replace(".0", "")
            else:
                x = multiplier
            data: Level = Level.find_one({'_id': self.bot._owner_id})

            if group in ('mod', 'staff', 'mods'):
                data.mod_xp_multiplier = multiplier
                await data.commit()
                await ctx.send(f"Set the multiplier for Mods/Staff members to **{x}**.")
                return

            elif group in ('booster', 'boosters', 'serverbooster', 'serverboosters'):
                data.booster_xp_multiplier = multiplier
                await data.commit()
                await ctx.send(f"Set the multiplier for Server Boosters to **{x}**.")
                return

            elif group in ('member', 'members'):
                data.xp_multiplier = multiplier
                await data.commit()
                await ctx.send(f"Set the multiplier for Members to **{x}**.")
                return

            elif group in ('kraots', 'kraot'):
                data.kraots_xp_multiplier = multiplier
                await data.commit()
                await ctx.send(f"Set the multiplier for Kraots to **{x}**.")
                return

            elif group == "all":
                data.kraots_xp_multiplier = multiplier
                data.xp_multiplier = multiplier
                data.mod_xp_multiplier = multiplier
                data.booster_xp_multiplier = multiplier
                await data.commit()
                await ctx.send(f"Set the multiplier for every group to **{x}**.")

    @multiplier.command()
    @commands.is_owner()
    async def multiplier_reset(self, ctx: Context, group: str = None):
        """Reset the multipliers of a group."""

        if group is None:
            await ctx.send(
                "You must specify which group you want to reset the multiplier for.\nGroups:\n\u2800 • **Mod/Staff**\n\u2800 • **Boosters**\n\u2800 "
                "• **Members**\n\u2800 • **Kraots**\n\u2800 • **all**"
            )
            return

        else:
            group = group.lower()
            data: Level = await Level.find_one({'_id': self.bot._owner_id})

            if group in ('mod', 'staff', 'mods'):
                data.mod_xp_multiplier = 1
                await data.commit()
                await ctx.send("Set the multiplier for Mods/Staff members back to **1**.")
                return

            elif group in ('booster', 'boosters', 'serverbooster', 'serverboosters'):
                data.booster_xp_multiplier = 1
                await data.commit()
                await ctx.send("Set the multiplier for Server Boosters back to **1**.")
                return

            elif group in ('member', 'members'):
                data.xp_multiplier = 1
                await data.commit()
                await ctx.send("Set the multiplier for Members back to **1**.")
                return

            elif group in ('kraots', 'kraot'):
                data.kraots_xp_multiplier = 1
                await data.commit()
                await ctx.send("Set the multiplier for Kraots to **1**.")
                return

            elif group == "all":
                data.kraots_xp_multiplier = 1
                data.xp_multiplier = 1
                data.mod_xp_multiplier = 1
                data.booster_xp_multiplier = 1
                await data.commit()
                await ctx.send("Set the multiplier for every group back to **1**.")

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != 374622847672254466:
            data: Level = await Level.find_one({'_id': member.id})
            if data:
                await data.delete()


def setup(bot):
    bot.add_cog(Levels(bot))
