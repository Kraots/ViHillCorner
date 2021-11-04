import datetime

import disnake
from disnake.ext import commands

from utils import time
from utils.colors import Colours
from utils.context import Context
from utils.databases import Marriage

from main import ViHillCorner


class Marriages(commands.Cog):
    """Marriages related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '❤️'

    @commands.command()
    async def marry(self, ctx: Context, member: disnake.Member = None):
        """Marry the member."""

        if member is None:
            await ctx.send("You must specifiy the user u want to marry.")
            return

        elif member == ctx.author:
            await ctx.send("You cannot marry yourself.")
            return

        elif member.bot:
            await ctx.send("Sad kid u can't marry bots smh.")
            return

        else:
            all_users = []
            marriages: list[Marriage] = await Marriage.find().to_list(1000000)
            for marriage in marriages:
                all_users.append(marriage.id)

            if member.id in all_users:
                mem: Marriage = await Marriage.find_one({"_id": member.id})
                usr = self.bot.get_user(mem.married_to)
                await ctx.send("`{}` is already married to `{}`.".format(member.display_name, usr.display_name))
                return

            elif ctx.author.id in all_users:
                mem: Marriage = await Marriage.find_one({"_id": ctx.author.id})
                usr = self.bot.get_user(mem.married_to)
                await ctx.send("You are already married to `{}`.".format(usr.display_name))

            else:
                view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.", member)
                view.message = msg = await ctx.send(f"{member.mention} do you want to marry {ctx.author.mention}?", view=view)
                await view.wait()
                if view.response is True:
                    mem = Marriage(
                        id=ctx.author.id,
                        married_to=member.id,
                        marry_date=datetime.datetime.utcnow()
                    )
                    usr = Marriage(
                        id=member.id,
                        married_to=ctx.author.id,
                        marry_date=datetime.datetime.utcnow()
                    )
                    await mem.commit()
                    await usr.commit()

                    await ctx.send(f"`{ctx.author.display_name}` married `{member.display_name}`!!! :tada: :tada:")
                    await msg.delete()

                elif view.response is False:
                    await ctx.send(f"`{member.display_name}` does not want to marry with you. {ctx.author.mention} :pensive: :fist:")
                    await msg.delete()

    @commands.command()
    async def divorce(self, ctx: Context):
        """Divorce the person you're married with in case you're married with someone."""

        marriage: Marriage = await Marriage.find_one({"_id": ctx.author.id})

        if marriage is None:
            await ctx.send("You are not married to anyone.")
            return

        else:
            usr = self.bot.get_user(marriage.married_to)

            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send(f"Are you sure you want to divorce `{usr.display_name}`?", view=view)
            await view.wait()
            if view.response is True:
                mem: Marriage = await Marriage.find_one({'_id': usr.id})
                await marriage.delete()
                await mem.delete()

                e = f"You divorced `{usr.display_name}`. :cry:"
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = f"You did not divorce that person :D {usr.mention}"
                return await msg.edit(content=e, view=view)

    @commands.command()
    async def marriedwho(self, ctx: Context, member: disnake.Member = None):
        """See with who are you married, if married with someone."""

        member = member or ctx.author

        marriage: Marriage = await Marriage.find_one({"_id": member.id})

        if member.bot:
            await ctx.send("Bot's cannot marry u dumbo <:pepe_cringe:750755809700348166>")
            return
        elif marriage is None:
            if member == ctx.author:
                await ctx.send("You are not married to anyone.\nType `!marry <user>` to marry to someone!")
                return
            else:
                await ctx.send(f"`{member.display_name}` is not married to anyone.")
                return

        else:
            usr = self.bot.get_user(marriage.married_to)
            if member == ctx.author:
                def format_date(dt):
                    if dt is None:
                        return 'N/A'
                    return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

                em = disnake.Embed(color=Colours.light_pink, title=f"You are married to `{usr.display_name}` :tada: :tada:")
                em.add_field(name="_ _ \nMarried since:", value=f"`{format_date(marriage.marry_date)}`", inline=False)
                em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=em)
            else:
                def format_date(dt):
                    if dt is None:
                        return 'N/A'
                    return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title=f"`{member.display_name}` is married to `{usr.display_name}` :tada: :tada:"
                )
                em.add_field(name=" _ _ \nMarried since:", value=f"`{format_date(marriage.marry_date)}`", inline=False)
                em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != 374622847672254466:
            mem = await Marriage.find_one({'_id': member.id})
            if mem:
                await mem.delete()
                usr = await Marriage.find_one({'married_to': member.id})
                await usr.delete()


def setup(bot):
    bot.add_cog(Marriages(bot))
