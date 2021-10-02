import disnake
from disnake.ext import commands
import psutil
import os
import utils.colors as color
from utils import time
import datetime
import random
import sys
import urllib.request
import urllib.parse
import inspect
from utils.context import Context

ss_key = os.getenv("SS_KEY")


def take_ss(url):
    options = {
                'url': str(url),
                'dimension': '1920x1080',
                'format': 'png',
                'hide': '.cookie-banner',
                'click': '.button-close',
                'delay': '600',
                'cacheLimit': '0.041666'
                }
    api_url = 'https://api.screenshotmachine.com/?key=' + ss_key
    api_url = api_url + '&' + urllib.parse.urlencode(options)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', '-')]
    urllib.request.install_opener(opener)
    output = 'ss.png'
    urllib.request.urlretrieve(api_url, output)


addd = """
୨୧ VIHILL CORNER ୨୧
♥︎ Your chance to meet and chat with awesome people ♥︎

♡︎ What we offer ♡︎:
╭・Exclusive bots
﹕・Lots of fun channels
﹕・Lots of emotes
﹕・Intros (Instead of reaction roles :D)
﹕・Not that active unless there's someone to start the convo, then there's a 80% chance it'll be active
╰・Horny Peeps

♥︎ server link: https://discord.gg/Uf2kA8q ♥︎
° . · . ✧ °  .  ₊˚ˑ˚₊ . ° ✧ . · .°
"""

nono_list = (
    'pornhub.com', 'https://pornhub.com', 'hentaiheaven.com', 'https://hentaiheaven.com', 'nhentai.net', 'https://nhentai.net', 'hanime.tv',
    'https://hanime.tv', 'xvideos.com', 'https://xvideos.com', 'hentai.com', 'https://hentai.com', 'hentai.net', 'https://hentai.net',
    'https://www.pornhub.com/', 'www.pornhub.com/'
)


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @commands.command(aliases=["ss"])
    async def scrs(self, ctx: Context, url):
        """Take a screenshot of the website."""

        if ctx.author.id != 374622847672254466:
            if str(url) in nono_list:
                return await ctx.send("( ͡° ͜ʖ ͡°)")

        else:
            await self.bot.loop.run_in_executor(None, take_ss, url)
            f = disnake.File(fp='ss.png', filename='ss.png')
            em = disnake.Embed(color=color.lightpink, title="Here's your screen shot of `{}`".format(url))
            em.set_image(url='attachment://ss.png')
            em.set_footer(text="Requested by: {}".format(ctx.author), icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em, file=f, reference=ctx.replied_reference)

    @commands.command(name="perm-calc")
    async def perm_calc(self, ctx: Context):
        """Sends the link for the permission calculator for bots."""

        em = disnake.Embed(
            color=color.lightpink,
            title="Here's the link to the permission calculator for bots.",
            description="https://discordapi.com/permissions.html#8589934591"
        )
        await ctx.send(embed=em, reference=ctx.replied_reference)

    @commands.command(name="dev-portal")
    async def dev_portal(self, ctx: Context):
        """Sends a link for the developer portal."""

        em = disnake.Embed(color=color.lightpink, title=" Here's the link to dev portal. ", description="https://discord.com/developers/applications")
        await ctx.send(embed=em, reference=ctx.replied_reference)

    @commands.command()
    async def joined(self, ctx: Context, member: disnake.Member = None):
        """See when the member has joined the server."""

        member = member or ctx.author

        def format_date(dt):
            return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

        if member.id == 374622847672254466:
            x = "2020-09-01 01:11"
            kraots_joined = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
            embed = disnake.Embed(color=color.lightpink)
            embed.add_field(name='Join Date:', value=f"{member} **--->** {format_date(kraots_joined)}")
            await ctx.send(embed=embed, reference=ctx.replied_reference)

        elif member.id == 747329236695777340:
            x = "2020-09-30 12:12"
            twil_joined = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
            embed = disnake.Embed(color=color.lightpink)
            embed.add_field(name='Join Date:', value=f"{member} **--->** {format_date(twil_joined)}")
            await ctx.send(embed=embed, reference=ctx.replied_reference)

        else:
            embed = disnake.Embed(color=color.lightpink)
            embed.add_field(name='Join Date:', value=f"{member} **--->** {format_date(member.joined_at.replace(tzinfo=None))}")
            await ctx.send(embed=embed, reference=ctx.replied_reference)

    @commands.command()
    async def created(self, ctx: Context, user: disnake.User = None):
        """See when a user created their account."""

        if user is None:
            user = ctx.author

        def format_date(dt):
            return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

        embed = disnake.Embed(color=color.lightpink)
        embed.add_field(name='Create Date:', value=f"{user} **--->** {format_date(user.created_at.replace(tzinfo=None))}")
        await ctx.send(embed=embed, reference=ctx.replied_reference)

    @commands.command(aliases=["inv"])
    async def invite(self, ctx: Context):
        """Get the invite for the server."""

        inv = disnake.Embed(title="https://discord.gg/Uf2kA8q", color=color.lightpink)
        inv.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=inv, reference=ctx.replied_reference)

    @commands.command()
    async def membercount(self, ctx: Context):
        """
        See how many members there are in the server
        *This does not include bots, only human members
        """

        guild = self.bot.get_guild(750160850077089853)
        member_count = len([m for m in guild.members if not m.bot])
        member_count = f'`{member_count}` members.'
        await ctx.send(member_count, reference=ctx.replied_reference)

    @commands.command(name='av', aliases=["avatar"])
    async def _av(self, ctx: Context, member: disnake.Member = None):
        """Get an embedded image of the member's avatar."""

        member = member or ctx.author

        avatar = disnake.Embed(title=f"Here's {member.display_name}'s avatar", url=member.display_avatar, color=color.blue)
        avatar.set_image(url=member.display_avatar)
        avatar.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=avatar, reference=ctx.replied_reference)

    @commands.command()
    async def ee(self, ctx: Context, emoji: disnake.PartialEmoji):
        """Get an embedded image of the emoji."""

        await ctx.message.delete()

        embed = disnake.Embed(color=color.lightpink)
        embed.set_image(url=emoji.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed, reference=ctx.replied_reference)

    @commands.command(aliases=['ad'])
    async def serverad(self, ctx: Context):
        """See the server's ad."""

        await ctx.message.delete()
        ad = disnake.Embed(color=color.lightpink, title="Here's the ad to the server:", description=addd)
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=ad, reference=ctx.replied_reference)

    @commands.command(aliases=["ra"])
    async def rawad(self, ctx: Context):
        """See the server's ad but in raw format."""

        await ctx.message.delete()
        ad = disnake.Embed(color=color.lightpink, title="Here's the raw ad version of the server:", description="```%s```" % (addd))
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=ad, reference=ctx.replied_reference)

    @commands.command(aliases=["untill-partner"])
    async def up(self, ctx: Context):
        """See how many members there are left until the server can apply for the disnake partnership program."""

        guild = self.bot.get_guild(750160850077089853)
        member_count = len([m for m in guild.members if not m.bot])
        await ctx.send(f'Members left untill the server can apply for the *disnake partnership program:* \n\n`{500 - member_count}`')

    @commands.command(name='randomnumber', aliases=['rn'])
    async def random_number(self, ctx: Context, num1: int = None, num2: int = None, num3: int = None):
        """
        Get a random number depending on the amount of numbers you give
        If you don't provide any number, the bot will give a random number between `0` and the `largest positive integer supported by the machine`.

        If you provide only one number, then the bot will give a random number between `0` and `your chosen number (num1)`.

        If you provide two numbers only, then the bot will give you a random number between `your first number (num1)` and `your second number (num2)`.

        If you provide all three numbers, then the bot will give a random number between `your first number (num1)` and `your second number (num2)`, that is not `your third number (num3)`, this can be used if you want a random number between 2 numbers that is not a specific one, here's some examples:
        • `10 15 13 - will give a number between 10 and 15 that is not 13`
        • `0 10 5 - will give a number between 0 and 10 that is not 5`
        • `20 100 50 - will give a number between 20 and 100 that is not 50`
        • `10 20 15 - will give a number between 10 and 20 that is not 15`
        """  # noqa

        if num1 is None and num2 is None:
            number = random.randint(0, sys.maxsize)
            await ctx.send("Random number between `0` and the largest positive integer supported by the machine is: \n`%s`" % (number))
            return

        elif num2 is None:
            number = random.randint(0, num1)
            await ctx.send("Random number from `0` to `%s`: \n`%s`" % (num1, number))
            return

        elif num3 is None:
            number = random.randint(num1, num2)
            await ctx.send("Random number between `%s` and `%s`: \n`%s`" % (num1, num2, number))
            return

        else:
            while True:
                number = random.randint(num1, num2)
                if number != num3:
                    await ctx.send("Random number between `%s` and `%s` that is not `%s`: \n`%s`" % (num1, num2, num3, number))
                    return
                else:
                    pass

    @commands.command(aliases=['src'])
    async def source(self, ctx: Context, *, command: str = None):
        """Sends the source of code for the specified command if any, if not then just the link to the github repository."""

        source_url = 'https://github.com/Kraots/ViHillCorner'
        branch = 'master'
        if command is None:
            return await ctx.send('<' + source_url + '>')
        elif command.lower() in ('jsk', 'jishaku'):
            return await ctx.send("That is an extension's command, code unavailable.")
        elif command.lower() == 'help':
            src = type(self.bot.help_command)
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace('.', ' ')) or self.bot.get_slash_command(command.replace('.', ' '))
            if obj is None:
                return await ctx.send('Could not find command.')
            src = obj.callback.__code__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        location = os.path.relpath(filename).replace('\\', '/')
        final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'

        await ctx.send(final_url, reference=ctx.replied_reference)


def setup(bot):
    bot.add_cog(General(bot))
