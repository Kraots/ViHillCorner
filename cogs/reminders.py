import textwrap
import datetime

import disnake
from disnake.ext import commands, tasks
from disnake.ui import View, Button

from utils import time
from utils.colors import Colours
from utils.context import Context

from main import ViHillCorner


class Reminders(commands.Cog):
    """Reminder related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Reminders']
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

        results = await self.db.find().sort("_id", -1).to_list(1)

        for result in results:
            newID = result['_id'] + 1

        try:
            newID = newID
        except UnboundLocalError:
            newID = 1324

        post = {
            "_id": newID,
            "user_id": ctx.author.id,
            "channel_id": ctx.channel.id,
            "remind_when": when.dt,
            "remind_what": when.arg,
            "time_now": datetime.datetime.utcnow(),
            "message_url": ctx.message.jump_url
        }

        await self.db.insert_one(post)
        delta = time.human_timedelta(when.dt, accuracy=3)
        await ctx.send(f"Alright {ctx.author.mention}, in **{delta}**: {when.arg}")

    @remind.command(name='list')
    async def remind_list(self, ctx: Context):
        """See your list of reminders, if you have any."""

        results = await self.db.find({"user_id": ctx.author.id}).sort("remind_when", 1).to_list(10)
        em = disnake.Embed(color=Colours.light_pink, title="Reminders")
        index = 0
        total_reminders = 0
        z = await self.db.find({"user_id": ctx.author.id}).sort("remind_when", 1).to_list(100000)

        for x in z:
            total_reminders += 1

        for result in results:
            index += 1
            shorten = textwrap.shorten(result['remind_what'], width=320)
            em.add_field(
                name=f"(ID)`{result['_id']}`: In {time.human_timedelta(result['remind_when'])}",
                value=f"{shorten}\n[Click here to go there]({result['message_url']})",
                inline=False
            )

        if len(em) < 12:
            await ctx.send("No currently running reminders.")
            return
        em.set_footer(text="Showing %s/%s reminders." % (index, total_reminders))
        await ctx.send(embed=em)

    @remind.command(name='remove', aliases=['delete', 'cancel'])
    async def remind_remove(self, ctx: Context, remind_id: int):
        """Remove a reminder from your list based on its id."""

        results = await self.db.find_one({"_id": remind_id})
        if results is not None:
            if results['user_id'] == ctx.author.id:
                view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
                view.message = msg = await ctx.send("Are you sure you want to cancel that reminder? %s" % (ctx.author.mention), view=view)
                await view.wait()
                if view.response is True:
                    await self.db.delete_one({"_id": remind_id})
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

        results = await self.db.find_one({"user_id": ctx.author.id})
        if results is not None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to clear your reminders? %s" % (ctx.author.mention), view=view)
            await view.wait()
            if view.response is True:
                await self.db.delete_many({"user_id": ctx.author.id})
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
        results = await self.db.find().sort('remind_when', 1).to_list(1)
        for result in results:
            expire_date = result['remind_when']
            remind_id = result['_id']
            user = result['user_id']
            reminded_when = result['time_now']
            remind_what = result['remind_what']
            remind_url = result['message_url']
            channel_id = result['channel_id']

            if current_time >= expire_date:
                remindChannel = self.bot.get_channel(channel_id)
                msg = f"<@!{user}>, **{time.human_timedelta(reminded_when)}**: {remind_what}"
                view = View()
                button = Button(label='Go to original message', url=remind_url)
                view.add_item(button)
                await remindChannel.send(msg, view=view)
                await self.db.delete_one({"_id": remind_id})

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        await self.db.delete_many({"user_id": member.id})

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
