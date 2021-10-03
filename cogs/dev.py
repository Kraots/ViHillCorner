import disnake
from disnake.ext import commands
import asyncio
import utils.colors as color
from disnake.ext.commands import Greedy
from disnake import Member
import os
import sys
from utils.helpers import clean_code, Pag  # noqa
import contextlib
import io
import textwrap
from traceback import format_exception
import time
from utils.context import Context
from utils.paginator import TextPage


def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


class QuitButton(disnake.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180.0)
        self.ctx = ctx

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(
                f'Only {self.ctx.author.display_name} can use the buttons on this message!',
                ephemeral=True
            )
            return False
        return True

    async def on_error(self, error, item, interaction):
        return await self.ctx.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        await self.message.edit(view=None)

    @disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red)
    async def stop_pages(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """Deletes the user's message along with the bot's message."""
        await self.message.delete()
        await self.ctx.message.delete()
        self.stop()


class Developer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = '!'

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @commands.command(name='eval', aliases=['e'])
    @commands.is_owner()
    async def _eval(self, ctx: Context, *, content=None):
        """Evaluate code."""

        if content is None:
            return await ctx.send("Please give code that you want to evaluate!")

        code = clean_code(content)

        local_variables = {
            "disnake": disnake,
            "commands": commands,
            "_bot": self.bot,
            "_ctx": ctx,
            "_channel": ctx.channel,
            "_author": ctx.author,
            "_guild": ctx.guild,
            "_message": ctx.message
        }
        start = time.perf_counter()

        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        end = time.perf_counter()
        took = f"{end-start:.3f}"
        if took == "0.000":
            took = f"{end-start:.7f}"

        if len(result) >= 4000:
            pager = TextPage(
                ctx,
                [result[i: i + 4000] for i in range(0, len(result), 4000)],
                footer=f'Took {took}s'
            )
            return await pager.start()
        em = disnake.Embed(description=f'```py\n{result}\n```')
        em.set_footer(text=f'Took {took}s')
        view = QuitButton(ctx)
        view.message = await ctx.send(embed=em, view=view)

    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx: Context):
        """This sends an embed of the rules, the exact ones like in <#750160850303582236>."""

        em = disnake.Embed(
            color=color.lightpink,
            title="ViHill Corner Rerver Rules",
            description="We have a small but strict set of rules on our server. Please read over them and take them on board. If you don't understand anything "
                        "or need some clarification, feel free to ask any staff member!"
        )
        em.add_field(
            name="Rule 1",
            value="Follow the [Discord Community Guidelines](https://discord.com/guidelines) and [Terms Of Service](https://discord.com/terms).",
            inline=False
        )
        em.add_field(
            name="Rule 2",
            value="Follow the [ViHill Corner Code Of Conduct](https://medium.com/vihill-corner/vihill-corner-code-of-conduct-7f187ab0c56).",
            inline=False
        )
        em.add_field(
            name="Rule 3",
            value="Listen to and respect staff members and their instructions.",
            inline=False
        )
        em.add_field(
            name="Rule 4",
            value="This is an English-speaking server, so please speak English to the best of your ability",
            inline=False
        )
        em.add_field(
            name="Rule 5",
            value="No advertising of any kind, including in a server member’s DM.",
            inline=False
        )

        await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def mail(self, ctx: Context, members: Greedy[Member] = None, *, args=None):
        """Sends a dm to the memeber(s)."""

        if members is None:
            await ctx.send("You must provide a user!")
            return

        if args is None:
            await ctx.send("You must provide args!")
            return

        for member in members:
            await member.send(f'{args}')
            await ctx.message.add_reaction('<:agree:797537027469082627>')

    @commands.command()
    @commands.is_owner()
    async def makemod(self, ctx: Context, members: Greedy[Member]):
        """Adds mod/staff roles to the member."""

        guild = self.bot.get_guild(750160850077089853)
        staff = guild.get_role(754676705741766757)
        mod = guild.get_role(750162714407600228)

        for member in members:
            new_roles = [role for role in member.roles] + [staff, mod]
            await member.edit(roles=new_roles, reason='Master gave them staff/mod.')

            makemod = disnake.Embed(color=color.red, description=f'{member.mention} is now a mod!')
            await ctx.send(embed=makemod)

    @commands.command()
    @commands.is_owner()
    async def removemod(self, ctx: Context, members: Greedy[Member]):
        """Removes the mod/staff roles from a member."""

        for member in members:
            new_roles = [role for role in member.roles if role.id not in (754676705741766757, 750162714407600228)]
            await member.edit(roles=new_roles, reason='Master removed their staff/mod.')

            removemod = disnake.Embed(color=color.red, description=f'{member.mention} is no longer a mod!')
            await ctx.send(embed=removemod)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: Context):
        """Closes the bot."""

        await ctx.message.add_reaction('<:agree:797537027469082627>')
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx: Context):
        """Restarts the bot."""

        await ctx.send("*Restarting...*")
        restart_program()

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def status(self, ctx: Context):
        """Change the bot's presence status."""

        statuses = disnake.Embed(title="Statuses:", color=color.lightpink)
        statuses.add_field(
            name="Online:",
            value="!status online\n!status online playing [custom status]\n  !status online listening [custom status]\n!status online watching [custom status]",
            inline=False
        )
        statuses.add_field(
            name="Idle:",
            value="!status idle\n!status idle playing [custom status]\n  !status idle listening [custom status]\n!status idle watching [custom status]",
            inline=False
        )
        statuses.add_field(
            name="Dnd:",
            value="!status dnd\n!status dnd playing [custom status]\n!status dnd listening [custom status]\n!status dnd watching [custom status]",
            inline=False)
        statuses.add_field(name="Offline:", value="!status offline", inline=False)
        await ctx.send(embed=statuses, delete_after=5)
        await asyncio.sleep(4)
        await ctx.message.delete()

    @status.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def online(self, ctx: Context):
        """
        Set the presence status to online.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()
        await self.bot.change_presence(status=disnake.Status.online)
        await ctx.send("**[ONLINE]** Status succesfully changed.", delete_after=5)

    @online.command(name='playing')
    @commands.is_owner()
    async def online_playing(self, ctx: Context, *, args=None):
        """
        Set the presence status to online playing.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.playing, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.online, activity=listening)
            await ctx.send("**[ONLINE] [PLAYING]** Status succesfully changed.", delete_after=5)

    @online.command(name='listening')
    @commands.is_owner()
    async def online_listening(self, ctx: Context, *, args=None):
        """
        Set the presence status to online listening.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.listening, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.online, activity=listening)
            await ctx.send("**[ONLINE] [LISTENING]** Status succesfully changed.", delete_after=5)

    @online.command(name='watching')
    @commands.is_owner()
    async def online_watching(self, ctx: Context, *, args=None):
        """
        Set the presence status to online watching.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.watching, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.online, activity=listening)
            await ctx.send("**[ONLINE] [WATCHING]** Status succesfully changed.", delete_after=5)

    @status.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def idle(self, ctx: Context):
        """
        Set the presence status to idle.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()
        await self.bot.change_presence(status=disnake.Status.idle)
        await ctx.send("**[IDLE]** Status succesfully changed.", delete_after=5)

    @idle.command(name='playing')
    @commands.is_owner()
    async def idle_playing(self, ctx: Context, *, args=None):
        """
        Set the presence status to idle playing.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.playing, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.idle, activity=listening)
            await ctx.send("**[IDLE] [PLAYING]** Status succesfully changed.", delete_after=5)

    @idle.command(name='listening')
    @commands.is_owner()
    async def idle_listening(self, ctx: Context, *, args=None):
        """
        Set the presence status to idle listening.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.listening, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.idle, activity=listening)
            await ctx.send("**[IDLE] [LISTENING]** Status succesfully changed.", delete_after=5)

    @idle.command(name='watching')
    @commands.is_owner()
    async def idle_watching(self, ctx: Context, *, args=None):
        """
        Set the presence status to idle watching.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.watching, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.idle, activity=listening)
            await ctx.send("**[IDLE] [WATCHING]** Status succesfully changed.", delete_after=5)

    @status.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def dnd(self, ctx: Context):
        """
        Set the presence status to dnd.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()
        await self.bot.change_presence(status=disnake.Status.do_not_disturb)
        await ctx.send("**[DND]** Status succesfully changed.", delete_after=5)

    @dnd.command(name='playing')
    @commands.is_owner()
    async def dnd_playing(self, ctx: Context, *, args=None):
        """
        Set the presence status to dnd playing.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.playing, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.do_not_disturb, activity=listening)
            await ctx.send("**[DND] [PLAYING]** Status succesfully changed.", delete_after=5)

    @dnd.command(name='listening')
    @commands.is_owner()
    async def dnd_listening(self, ctx: Context, *, args=None):
        """
        Set the presence status to dnd listening.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.listening, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.do_not_disturb, activity=listening)
            await ctx.send("**[DND] [LISTENING]** Status succesfully changed.", delete_after=5)

    @dnd.command(name='watching')
    @commands.is_owner()
    async def dnd_watching(self, ctx: Context, *, args=None):
        """
        Set the presence status to dnd watching.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()

        if args is None:
            await ctx.send("You must provide args!", delete_after=5)

        else:

            listening = disnake.Activity(type=disnake.ActivityType.watching, name=f"{args}")
            await self.bot.change_presence(status=disnake.Status.do_not_disturb, activity=listening)
            await ctx.send("**[DND] [WATCHING]** Status succesfully changed.", delete_after=5)

    @status.command()
    @commands.is_owner()
    async def offline(self, ctx: Context):
        """
        Set the presence status to offline.
        Remember to disable the loop for changing the presence.
        """

        await ctx.message.delete()
        await self.bot.change_presence(status=disnake.Status.offline)
        await ctx.send("**[OFFLINE]** Status succesfully changed.", delete_after=5)


def setup(bot):
    bot.add_cog(Developer(bot))
