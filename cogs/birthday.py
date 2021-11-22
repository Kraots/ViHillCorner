import asyncio
import datetime
from dateutil.relativedelta import relativedelta

import disnake
from disnake.ext import commands, tasks

from utils import time
from utils.context import Context
from utils.databases import Birthday

from main import ViHillCorner


class Birthdays(commands.Cog):
    """Birthday related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"
        self.check_bdays.start()

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '🍰'

    @tasks.loop(minutes=30.0)
    async def check_bdays(self):
        await self.bot.wait_until_ready()
        current_time = datetime.datetime.utcnow()
        bdays: list[Birthday] = await Birthday.find().sort('region_birthday', 1).to_list(1)
        for bday in bdays:
            if current_time >= bday.region_birthday:
                guild = self.bot.get_guild(750160850077089853)
                bday_channel = guild.get_channel(797867811967467560)
                user = guild.get_member(bday.id)

                em = disnake.Embed(color=user.color, title=f"Happy birthday {user.name}!!! :tada: :tada:")
                em.set_image(url='https://cdn.discordapp.com/attachments/787359417674498088/901940653762687037/happy_bday.gif')

                msg = await bday_channel.send(user.mention, embed=em)
                await msg.add_reaction("🍰")

                bday.birthday_date = bday.birthday_date + relativedelta(years=1)
                bday.region_birthday = bday.region_birthday + relativedelta(years=1)
                await bday.commit()

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=('bday', 'b-day',))
    async def birthday(self, ctx: Context, member: disnake.Member = None):
        """See when the member's birthday is, if any."""

        member = member or ctx.author
        bday: Birthday = await Birthday.find_one({"_id": member.id})

        if bday is None:
            if member.id == ctx.author.id:
                await ctx.send(
                    "You did not set your birthday! Type: `!birthday set month/day` to set your birthday.\n**Example:**\n\u2800"
                    "`!birthday set 01/16`"
                )
            else:
                await ctx.send("User did not set their birthday!")
            return

        def format_date(dt1, dt2):
            return f"{member.mention}'s birthday is in `{time.human_timedelta(dt1, accuracy=3)}` **({dt2:%Y/%m/%d})**"

        await ctx.send(format_date(bday.region_birthday, bday.birthday_date))

    @birthday.command(name='top', aliases=('upcoming',))
    async def bday_top(self, ctx: Context):
        """See top 5 upcoming birthdays."""

        index = 0

        def format_date(dt1, dt2):
            return f"Birthday in `{time.human_timedelta(dt1, accuracy = 3)}` ( **{dt2:%Y/%m/%d}** ) "

        em = disnake.Embed(color=disnake.Color.blurple(), title="***Top `5` upcoming birthdays***\n _ _ ")

        bdays: list[Birthday] = await Birthday.find().sort("birthday_date", 1).to_list(5)
        for bday in bdays:
            user = self.bot.get_user(bday.id)
            index += 1
            em.add_field(
                name=f"`{index}`. _ _ _ _ {user.name}",
                value=f"{format_date(bday.region_birthday, bday.birthday_date)}",
                inline=False
            )

        await ctx.send(embed=em)

    @birthday.command(name='set', aliases=('add',))
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bday_set(self, ctx: Context, *, birthday=None):
        """Set your birthday."""

        if birthday is None:
            await ctx.send("Please insert a birthday! Please type `!birthday set month/day`.\n**Example:**\n\u2800`!birthday set 01/16`")
            ctx.command.reset_cooldown(ctx)
            return
        bday: Birthday = await Birthday.find_one({"_id": ctx.author.id})

        z = datetime.datetime.utcnow().strftime('%Y')
        pre = f'{z}/{birthday}'

        try:
            birthday = datetime.datetime.strptime(pre, "%Y/%m/%d")

        except ValueError:
            return await ctx.reply(
                "That is not a valid date!\n**Valid Dates:**\n\u2800`-` 04/24\n\u2800`-` 01/09\n\u2800`-` 12/01\n\n**Example:**\n\u2800`"
                "!birthday set 04/27`"
            )

        date_now = datetime.datetime.utcnow().strftime("%Y/%m/%d")
        date_now = datetime.datetime.strptime(date_now, "%Y/%m/%d")

        if date_now > birthday:
            birthday = birthday + relativedelta(years=1)

        msg = """What is your timezone from this list (approx.):

`1` ->  **Pacific Time (US)** `UTC-8`
`2` ->  **Mountain Time (US)** `UTC-7`
`3` ->  **Central Time (US)** `UTC-6`
`4` ->  **Eastern Time (US)** `UTC-5`
`5` ->  **Rio de Janeiro, Brazil** `UTC-3`
`6` ->  **London, United Kingdom (UTC)** `GMT`
`7` ->  **Berlin, Germany** `UTC+1 / UTC+2`
`8` ->  **Moscow, Russian Federation** `UTC+3`
`9` ->  **Dubai, United Arab Emirates** `UTC+4`
`10` ->   **Mumbai, India** `UTC+5:30`
`11` ->   **Singapore, Singapore** `UTC+8`
`12` ->   **Tokyo, Japan** `UTC+9`
`13` ->   **Sydney, Australia** `UTC+11`
`14` ->   **Auckland, New Zealand** `UTC+13`\n\n***Please enter just the number!***"""

        msg = await ctx.send(msg)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            while True:
                pre_region = await self.bot.wait_for('message', timeout=180, check=check)
                try:
                    region = int(pre_region.content)
                    if region > 14 or region < 1:
                        await pre_region.reply(
                            "Please choose a number that is shown there that corresponds with your region, "
                            "not another that is higher or smaller."
                        )
                    else:
                        break
                except ValueError:
                    await pre_region.reply("That is not a number.")

            if region == 1:
                region = "pacific time (us)"
                region_birthday = birthday + relativedelta(hours=10)
            elif region == 2:
                region = "mountain time (us)"
                region_birthday = birthday + relativedelta(hours=9)
            elif region == 3:
                region = "central time (us)"
                region_birthday = birthday + relativedelta(hours=8)
            elif region == 4:
                region = "eastern time (us)"
                region_birthday = birthday + relativedelta(hours=7)
            elif region == 5:
                region = "rio de janeiro, brazil"
                region_birthday = birthday + relativedelta(hours=5)
            elif region == 6:
                region = "london, united kingdom (utc)"
                region_birthday = birthday
            elif region == 7:
                region = "berlin, germany"
                region_birthday = birthday + relativedelta(hours=3)
            elif region == 8:
                region = "moscow, russian federation"
                region_birthday = birthday + relativedelta(hours=4)
            elif region == 9:
                region = "dubai, united arab emirates"
                region_birthday = birthday + relativedelta(hours=6)
            elif region == 10:
                region = "mumbai, india"
                region_birthday = birthday + relativedelta(hours=7, minutes=30)
            elif region == 11:
                region = "singapore, singapore"
                region_birthday = birthday + relativedelta(hours=10)
            elif region == 12:
                region = "tokyo, japan"
                region_birthday = birthday + relativedelta(hours=11)
            elif region == 13:
                region = "sydney, australia"
                region_birthday = birthday + relativedelta(hours=13)
            elif region == 14:
                region = "auckland, new zealand"
                region_birthday = birthday + relativedelta(hours=15)

            def format_date(dt1, dt2):
                return f"`{time.human_timedelta(dt1, accuracy=3)}` **({dt2:%Y/%m/%d})**"

            if bday is not None:
                bday.birthday_date = birthday
                bday.region = region
                bday.region_birthday = region_birthday
                await bday.commit()
                await ctx.message.delete()
                await msg.delete()
                await pre_region.delete()
                await ctx.send(f"Birthday set!\nYour birthday is in {format_date(region_birthday, birthday)} {ctx.author.mention}")

            else:
                bday = Birthday(
                    id=ctx.author.id,
                    birthday_date=birthday,
                    region=region,
                    region_birthday=region_birthday
                )
                await bday.commit()

                await ctx.message.delete()
                await msg.delete()
                await pre_region.delete()
                await ctx.send(f"Birthday set!\nYour birthday is in {format_date(region_birthday, birthday)} {ctx.author.mention}")

        except asyncio.TimeoutError:
            await ctx.send("Ran out of time.")
            return

    @birthday.command(name='delete', aliases=['remove'])
    async def bday_delete(self, ctx: Context):
        """Delete your birthday."""

        bday: Birthday = await Birthday.find_one({"_id": ctx.author.id})
        if bday is not None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send(f"Are you sure you want to remove your birthday? {ctx.author.mention}", view=view)
            await view.wait()
            if view.response is True:
                await bday.delete()
                e = f"Succesfully removed your birthday from the list! {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = f"Birthday has not been removed. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

        else:
            await ctx.send("You did not set your birthday, therefore you don't have what to delete! Type: `!birthday set <day | month>` to set your birthday.")

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == 374622847672254466:
            return
        bday: Birthday = await Birthday.find_one({'_id': member.id})
        if bday:
            await bday.delete()

    @bday_set.error
    async def bday_set_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"You are on cooldown! Please try again in `{str(error.retry_after)[:4]}` seconds.")
        else:
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Birthdays(bot))
