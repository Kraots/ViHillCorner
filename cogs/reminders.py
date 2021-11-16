import textwrap
import datetime

import disnake
from disnake.ext import commands, tasks
from disnake.ui import View, Button

from utils import time
from utils.colors import Colours
from utils.context import Context
from utils.databases import Reminder
from utils.paginator import RoboPages, FieldPageSource

from main import ViHillCorner


class Reminders(commands.Cog):
    """Reminder related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"
        self.check_current_reminders.start()

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '⏰'

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['reminder'])
    async def remind(self, ctx: Context, *, when: time.UserFriendlyTime(commands.clean_content, default='\u2026')):  # noqa
        """Set your reminder."""

        res: Reminder = await Reminder.find().sort("_id", -1).to_list(1)

        if res:
            new_id = res.id + 1
        else:
            new_id = 1324

        await Reminder(
            id=new_id,
            user_id=ctx.author.id,
            channel_id=ctx.channel.id,
            remind_when=when.dt,
            remind_what=when.arg,
            time_now=datetime.datetime.utcnow(),
            message_url=ctx.message.jump_url
        ).commit()

        delta = time.human_timedelta(when.dt, accuracy=3)
        await ctx.send(f"Alright {ctx.author.mention}, in **{delta}**: {when.arg}")

    @remind.command(name='list')
    async def remind_list(self, ctx: Context):
        """See your list of reminders, if you have any."""

        results: list[Reminder] = await Reminder.find({"user_id": ctx.author.id}).sort("remind_when", 1).to_list(100000)
        reminders = []

        for result in results:
            shorten = textwrap.shorten(result.remind_what, width=320)
            reminders.append((
                f"(ID) `{result.id}`: In {time.human_timedelta(result.remind_when)}",
                f"{shorten}\n[Click here to go there]({result.message_url})"
            ))

        if len(reminders) == 0:
            return await ctx.send("No currently running reminders.")

        src = FieldPageSource(reminders, per_page=5)
        src.embed.title = 'Reminders'
        src.embed.colour = Colours.light_pink
        pages = RoboPages(src, ctx=ctx, compact=True)
        await pages.start()

    @remind.command(name='remove', aliases=['delete', 'cancel'])
    async def remind_remove(self, ctx: Context, remind_id: int):
        """Remove a reminder from your list based on its id."""

        res: Reminder = await Reminder.find_one({"_id": remind_id})
        if res is not None:
            if res.user_id == ctx.author.id:
                view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
                view.message = msg = await ctx.send("Are you sure you want to cancel that reminder? %s" % (ctx.author.mention), view=view)
                await view.wait()
                if view.response is True:
                    await res.delete()
                    e = "Succesfully cancelled the reminder. %s" % (ctx.author.mention)
                    return await msg.edit(content=e, view=view)

                elif view.response is False:
                    e = "Reminder has not been cancelled. %s" % (ctx.author.mention)
                    return await msg.edit(content=e, view=view)
            else:
                await ctx.send("That reminder is not yours!")
                return
        else:
            await ctx.send("No reminder with that id.")
            return

    @remind.command(name='clear')
    async def remind_clear(self, ctx: Context):
        """Delete all of your reminders."""

        res: Reminder = await Reminder.find_one({"user_id": ctx.author.id})
        if res is not None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to clear your reminders? %s" % (ctx.author.mention), view=view)
            await view.wait()
            if view.response is True:
                async for remind in Reminder.find({'user_id': ctx.author.id}):
                    await remind.delete()
                e = "Succesfully cleared all your reminders. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = "Reminders have not been cleared. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)
        else:
            await ctx.send("No currently running reminders.")

    @tasks.loop(seconds=5)
    async def check_current_reminders(self):
        await self.bot.wait_until_ready()
        current_time = datetime.datetime.utcnow()
        results: list[Reminder] = await Reminder.find().sort('remind_when', 1).to_list(1)
        for res in results:
            if current_time >= res.remind_when:
                remind_channel = self.bot.get_channel(res.channel_id)
                msg = f"<@!{res.user_id}>, **{time.human_timedelta(res.remind_when)}**: {res.remind_what}"
                view = View()
                button = Button(label='Go to original message', url=res.message_url)
                view.add_item(button)
                await remind_channel.send(msg, view=view)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != self.bot._owner_id:
            async for remind in Reminder.find({'user_id': member.id}):
                await remind.delete()

    @remind.error
    async def remind_error(self, ctx: Context, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(str(error))
        else:
            return await self.bot.reraise(ctx, error)

    @remind_remove.error
    async def remind_remove_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.TooManyArguments):
            return
        else:
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Reminders(bot))
