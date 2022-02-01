import re
import os
import random
import datetime
import sys
import psutil
import inspect
import asyncio

import urllib.request
import urllib.parse

import disnake
from disnake.ext import commands

from utils.colors import Colours
from utils.context import Context
from utils import time

from .token_invalidation import TokenInvalidation, GistContent

from main import ViHillCorner

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


SERVER_AD = """
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

LANGUAGE_REGEX = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")


class General(commands.Cog):
    """General commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.process = psutil.Process(os.getpid())
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '❔'

    @commands.command(aliases=["ss"])
    async def scrs(self, ctx: Context, url):
        """Take a screenshot of the website."""

        if ctx.author.id != 938097236024360960:
            if str(url) in nono_list:
                return await ctx.send("( ͡° ͜ʖ ͡°)")

        else:
            await self.bot.loop.run_in_executor(None, take_ss, url)
            f = disnake.File(fp='ss.png', filename='ss.png')
            em = disnake.Embed(color=Colours.light_pink, title=f"Here's your screen shot of `{url}`")
            em.set_image(url='attachment://ss.png')
            em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em, file=f, reference=ctx.replied_reference)

    @commands.command(name="perm-calc")
    async def perm_calc(self, ctx: Context):
        """Sends the link for the permission calculator for bots."""

        em = disnake.Embed(
            color=Colours.light_pink,
            title="Here's the link to the permission calculator for bots.",
            description="https://discordapi.com/permissions.html#1099511627775"
        )
        await ctx.send(embed=em, reference=ctx.replied_reference)

    @commands.command(name="dev-portal")
    async def dev_portal(self, ctx: Context):
        """Sends a link for the developer portal."""

        em = disnake.Embed(color=Colours.light_pink, title=" Here's the link to dev portal. ", description="https://discord.com/developers/applications")
        await ctx.send(embed=em, reference=ctx.replied_reference)

    @commands.command()
    async def joined(self, ctx: Context, member: disnake.Member = None):
        """See when the member has joined the server."""

        member = member or ctx.author

        def format_date(dt):
            return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

        if member.id == 938097236024360960:
            x = "2020-09-01 01:11"
            kraots_joined = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
            embed = disnake.Embed(color=Colours.light_pink)
            embed.add_field(name='Join Date:', value=f"{member} **--->** {format_date(kraots_joined)}")
            await ctx.send(embed=embed, reference=ctx.replied_reference)

        elif member.id == 747329236695777340:
            x = "2020-09-30 12:12"
            twil_joined = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
            embed = disnake.Embed(color=Colours.light_pink)
            embed.add_field(name='Join Date:', value=f"{member} **--->** {format_date(twil_joined)}")
            await ctx.send(embed=embed, reference=ctx.replied_reference)

        else:
            embed = disnake.Embed(color=Colours.light_pink)
            embed.add_field(name='Join Date:', value=f"{member} **--->** {format_date(member.joined_at.replace(tzinfo=None))}")
            await ctx.send(embed=embed, reference=ctx.replied_reference)

    @commands.command()
    async def created(self, ctx: Context, user: disnake.User = None):
        """See when a user created their account."""

        if user is None:
            user = ctx.author

        def format_date(dt):
            return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

        embed = disnake.Embed(color=Colours.light_pink)
        embed.add_field(name='Create Date:', value=f"{user} **--->** {format_date(user.created_at.replace(tzinfo=None))}")
        await ctx.send(embed=embed, reference=ctx.replied_reference)

    @commands.command(aliases=["inv"])
    async def invite(self, ctx: Context):
        """Get the invite for the server."""

        inv = disnake.Embed(title="https://discord.gg/Uf2kA8q", color=Colours.light_pink)
        inv.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=inv, reference=ctx.replied_reference)

    @commands.command()
    async def membercount(self, ctx: Context):
        """
        See how many members there are in the server.
        *This does not include bots, only human members.*
        """

        guild = self.bot.get_guild(750160850077089853)
        member_count = len([m for m in guild.members if not m.bot])
        member_count = f'`{member_count}` humans.'
        await ctx.send(member_count, reference=ctx.replied_reference)

    @commands.command(name='av', aliases=["avatar"])
    async def _av(self, ctx: Context, member: disnake.Member = None):
        """Get an embedded image of the member's avatar."""

        member = member or ctx.author

        avatar = disnake.Embed(title=f"Here's {member.display_name}'s avatar", url=member.display_avatar, color=Colours.blurple)
        avatar.set_image(url=member.display_avatar)
        avatar.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=avatar, reference=ctx.replied_reference)

    @commands.command()
    async def ee(self, ctx: Context, emoji: disnake.PartialEmoji):
        """Get an embedded image of the emoji."""

        await ctx.message.delete()

        embed = disnake.Embed(color=Colours.light_pink)
        embed.set_image(url=emoji.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed, reference=ctx.replied_reference)

    @commands.command(aliases=['ad'])
    async def serverad(self, ctx: Context):
        """See the server's ad."""

        await ctx.message.delete()
        ad = disnake.Embed(color=Colours.light_pink, title="Here's the ad to the server:", description=SERVER_AD)
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=ad, reference=ctx.replied_reference)

    @commands.command(aliases=["ra"])
    async def rawad(self, ctx: Context):
        """See the server's ad but in raw format."""

        await ctx.message.delete()
        ad = disnake.Embed(color=Colours.light_pink, title="Here's the raw ad version of the server:", description=f"```{SERVER_AD}```")
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=ad, reference=ctx.replied_reference)

    @commands.command(aliases=["untill-partner"])
    async def up(self, ctx: Context):
        """See how many members there are left until the server can apply for the discord partnership program."""

        guild = self.bot.get_guild(750160850077089853)
        member_count = len([m for m in guild.members if not m.bot])
        await ctx.send(f'Members left untill the server can apply for the *disnake partnership program:* \n\n`{500 - member_count}`')

    @commands.command(name='randomnumber', aliases=['rn'])
    async def random_number(self, ctx: Context, num1: int = None, num2: int = None, num3: int = None):
        """
        Get a random number depending on the amount of numbers you give
        If you don't provide any number, the bot will give a random number
        between `0` and the `largest positive integer supported by the machine`.

        If you provide only one number, then the bot will give a random number
        between `0` and `your chosen number (num1)`.

        If you provide two numbers only, then the bot will give you a random
        number between `your first number (num1)` and `your second number (num2)`.

        If you provide all three numbers, then the bot will give a random number
        between `your first number (num1)` and `your second number (num2)`,
        that is not `your third number (num3)`, this can be used if you want
        a random number between 2 numbers that is not a specific one, here's some examples:
        • `10 15 13 - will give a number between 10 and 15 that is not 13`
        • `0 10 5 - will give a number between 0 and 10 that is not 5`
        • `20 100 50 - will give a number between 20 and 100 that is not 50`
        • `10 20 15 - will give a number between 10 and 20 that is not 15`
        """  # noqa

        if num1 is None and num2 is None:
            number = random.randint(0, sys.maxsize)
            await ctx.send(f"Random number between `0` and the largest positive integer supported by the machine is: \n`{number}`")
            return

        elif num2 is None:
            number = random.randint(0, num1)
            await ctx.send(f"Random number from `0` to `{num1}`: \n`{number}`")
            return

        elif num3 is None:
            number = random.randint(num1, num2)
            await ctx.send(f"Random number between `{num1}` and `{num2}`: \n`{number}`")
            return

        else:
            while True:
                number = random.randint(num1, num2)
                if number != num3:
                    await ctx.send("Random number between `{num1}` and `{num2}` that is not `{num3}`: \n`{number}`")
                    return
                else:
                    pass

    @commands.command(name='run', aliases=('code',))
    async def run_code(self, ctx: Context, *, code: str):
        r"""Runs the code and returns the result, must be in a codeblock with the markdown of the desired language.

        Example:
        \`\`\`language
        code
        \`\`\`
        """

        if ctx.channel.id not in self.bot.ignored_channels:
            return

        matches = LANGUAGE_REGEX.findall(code)
        if not matches:
            rand = (
                'Your code is not wrapped inside a codeblock.',
                'You forgot your codeblock.',
                'Missing the codeblock.',
            )
            return await ctx.reply(random.choice(rand))

        lang = matches[0][0] or matches[0][1]
        if not lang:
            rand = (
                'You did not specify the language markdown in your codeblock.',
                'Missing the language markdown in your codeblock.',
                'Your codeblock is missing the language markdown.',
            )
            return await ctx.reply(random.choice(rand))

        code = matches[0][2]
        await ctx.trigger_typing()
        _res = await self.bot.session.post(
            'https://emkc.org/api/v1/piston/execute',
            json={'language': lang, 'source': code}
        )
        res = await _res.json()
        if 'message' in res:
            em = disnake.Embed(
                title='An error occured while running the code',
                description=res['message']
            )
            return await ctx.reply(embed=em)

        output = res['output']
        if len(output) > 500:
            gh = TokenInvalidation(self.bot)
            content = GistContent(f'```{res["language"]}\n' + output + '\n```')
            url = await gh.create_gist(
                content.source,
                description=f'(`{ctx.author.id}` {ctx.author}) code result',
                filename='code_output.txt',
                public=False
            )
            msg = await ctx.reply(f'Your output was too long so I sent it to <{url}>')
            data = self.bot.execs.get(ctx.author.id)
            if data is None:
                self.bot.execs[ctx.author.id] = {ctx.command.name: msg}
            else:
                self.bot.execs[ctx.author.id][ctx.command.name] = msg
            return

        em = disnake.Embed(
            title=f'Ran your {res["language"]} code',
            color=Colours.blurple
        )
        output = output[:500].strip()
        lines = output.splitlines()
        shortened = (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * '\n\n**Output shortened**'
        em.add_field(name='Output', value=output or '**<No output>**')

        msg = await ctx.reply(embed=em)
        data = self.bot.execs.get(ctx.author.id)
        if data is None:
            self.bot.execs[ctx.author.id] = {ctx.command.name: msg}
        else:
            self.bot.execs[ctx.author.id][ctx.command.name] = msg

    @commands.Cog.listener('on_message_edit')
    async def repeat_command(self, before: disnake.Message, after: disnake.Message):
        if after.content.lower().startswith(('!run', '!code', '!e', '!eval')):
            ctx = await self.bot.get_context(after)
            cmd = self.bot.get_command(after.content.lower().replace('!', ''))
            await after.add_reaction('🔁')
            try:
                await self.bot.wait_for(
                    'reaction_add',
                    check=lambda r, u: str(r.emoji) == '🔁' and u.id == after.author.id,
                    timeout=360.0
                )
            except asyncio.TimeoutError:
                await after.clear_reaction('🔁')
            else:
                curr: disnake.Message = self.bot.execs[after.author.id].get(cmd.name)
                if curr:
                    await curr.delete()
                await after.clear_reaction('🔁')
                await cmd.invoke(ctx)

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
            command = command.replace('.', ' ')
            obj = self.bot.get_command(command) or self.bot.get_slash_command(command)
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
