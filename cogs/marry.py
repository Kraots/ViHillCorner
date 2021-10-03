import disnake
from disnake.ext import commands
import datetime
import utils.colors as color
from utils import time
from utils.context import Context


class Marriage(commands.Cog):
    """Marriage related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db1['Marry Data']
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
            results = await self.db.find().to_list(1000000)
            for result in results:
                all_users.append(result['_id'])

            if member.id in all_users:
                get_mem = await self.db.find_one({"_id": member.id})
                member_married_to = get_mem["married_to"]
                they_already_married_to = self.bot.get_user(member_married_to)
                await ctx.send("`{}` is already married to `{}`.".format(member.display_name, they_already_married_to.display_name))
                return

            elif ctx.author.id in all_users:
                get_auth = await self.db.find_one({"_id": ctx.author.id})
                author_married_to = get_auth["married_to"]
                author_already_married_to = self.bot.get_user(author_married_to)
                await ctx.send("You are already married to `{}`.".format(author_already_married_to.display_name))

            else:
                view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.", member)
                view.message = msg = await ctx.send("{} do you want to marry {}?".format(member.mention, ctx.author.mention), view=view)
                await view.wait()
                if view.response is True:

                    married_since_save_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")

                    save_auth = {"_id": ctx.author.id, "married_to": member.id, "marry_date": married_since_save_time}
                    save_mem = {"_id": member.id, "married_to": ctx.author.id, "marry_date": married_since_save_time}

                    await self.db.insert_many([save_auth, save_mem])

                    await ctx.send("`{}` married `{}`!!! :tada: :tada:".format(ctx.author.display_name, member.display_name))
                    await msg.delete()

                elif view.response is False:
                    await ctx.send("`{}` does not want to marry with you. {} :pensive: :fist:".format(member.display_name, ctx.author.mention))
                    await msg.delete()

    @commands.command()
    async def divorce(self, ctx: Context):
        """Divorce the person you're married with in case you're married with someone."""

        user = ctx.author

        results = await self.db.find_one({"_id": user.id})

        if results is None:
            await ctx.send("You are not married to anyone.")
            return

        else:
            the_married_to_user = self.bot.get_user(results['married_to'])

            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to divorce `{}`?".format(the_married_to_user.display_name), view=view)
            await view.wait()
            if view.response is True:
                auth = {"_id": ctx.author.id}
                mem = {"_id": the_married_to_user.id}
                await self.db.delete_one(auth)
                await self.db.delete_one(mem)

                e = "You divorced `{}`. :cry:".format(the_married_to_user.display_name)
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = "You did not divorce that person :D %s" % (user.mention)
                return await msg.edit(content=e, view=view)

    @commands.command()
    async def marriedwho(self, ctx: Context, member: disnake.Member = None):
        """See with who are you married, if married with someone."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})

        user = member

        if user.bot:
            await ctx.send("Bot's cannot marry u dumbo <:pepe_cringe:750755809700348166>")
            return

        elif results is None:
            if user == ctx.author:
                await ctx.send("You are not married to anyone.\nType `!marry <user>` to marry to someone!")
                return

            else:
                await ctx.send("`{}` is not married to anyone.".format(user.display_name))
                return

        else:
            user_married_to = results["married_to"]
            user_married_to_sincee = results["marry_date"]

            user_married_to_since = datetime.datetime.strptime(user_married_to_sincee, "%Y-%m-%d %H:%M")

            the_married_to_user = self.bot.get_user(user_married_to)

            if member == ctx.author:
                def format_date(dt):
                    if dt is None:
                        return 'N/A'
                    return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

                em = disnake.Embed(color=color.lightpink, title="You are married to `{}` :tada: :tada:".format(the_married_to_user.display_name))
                em.add_field(name="_ _ \nMarried since:", value="`{}`".format(format_date(user_married_to_since)), inline=False)
                em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=em)
            else:
                def format_date(dt):
                    if dt is None:
                        return 'N/A'
                    return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

                em = disnake.Embed(
                    color=color.lightpink,
                    title="`{}` is married to `{}` :tada: :tada:".format(user.display_name, the_married_to_user.display_name)
                )
                em.add_field(name=" _ _ \nMarried since:", value="`{}`".format(format_date(user_married_to_since)), inline=False)
                em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == 374622847672254466:
            return
        await self.db.delete_one({"_id": member.id})
        await self.db.delete_one({'married_to': member.id})


def setup(bot):
    bot.add_cog(Marriage(bot))
