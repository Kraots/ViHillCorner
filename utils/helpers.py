import io
import re
import string
import typing
import asyncio
from traceback import format_exception

import disnake
from disnake.ext import commands

from utils.colors import Colours
from utils import time

import pkg_resources


def get_member_role(member: disnake.Member):
    role = member.top_role.name
    if role == "@everyone":
        role = "N/A"
    return role


def get_member_voice(member: disnake.Member):
    return "Not in VC" if not member.voice else member.voice.channel


def profile(ctx, user):

    def format_date(dt):
        if dt is None:
            return 'N/A'
        return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

    em = disnake.Embed(timestamp=ctx.message.created_at.replace(tzinfo=None), colour=Colours.light_pink)
    em.add_field(name='User ID', value=user.id, inline=False)
    if isinstance(user, disnake.Member):
        em.add_field(name='Nick', value=user.nick, inline=False)
        em.add_field(name='Status', value=user.status, inline=False)
        voice = getattr(user, 'voice', None)
        if voice is not None:
            vc = voice.channel
            other_people = len(vc.members) - 1
            voice = f'`{vc.name}` with {other_people} others' if other_people else f'`{vc.name}` by themselves'
            em.add_field(name='In Voice', value=voice, inline=False)
        em.add_field(name='Game', value=user.activity, inline=False)
        em.add_field(name='Highest Role', value=get_member_role(user), inline=False)
        em.add_field(name='Join Date', value=format_date(user.joined_at.replace(tzinfo=None)), inline=False)
        em.add_field(name="Avatar", value=f'[Click Here]({user.display_avatar.with_static_format("jpg")})', inline=False)
    em.add_field(name='Account Created', value=format_date(user.created_at.replace(tzinfo=None)), inline=False)
    em.set_thumbnail(url=user.display_avatar.with_static_format("jpg"))
    em.set_author(name=user, icon_url=user.display_avatar)
    em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
    return em


def time_phaser(seconds):
    output = ""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    mo, d = divmod(d, 30)
    if mo > 0:
        output = output + str(int(round(m, 0))) + " months "
    if d > 0:
        output = output + str(int(round(d, 0))) + " days "
    if h > 0:
        output = output + str(int(round(h, 0))) + " hours "
    if m > 0:
        output = output + str(int(round(m, 0))) + " minutes "
    if s > 0:
        output = output + str(int(round(s, 0))) + " seconds"
    return output


def NSFW(ctx):
    return ctx.channel.id == 780374324598145055


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


def package_version(package_name: str) -> typing.Optional[str]:
    try:
        return pkg_resources.get_distribution(package_name).version
    except (pkg_resources.DistributionNotFound, AttributeError):
        return None


def format_balance(balance: int):
    cBalance = "{:,}".format(balance)
    sBalance = cBalance.split(",")
    if len(sBalance) == 1:
        return str(balance).replace('.0', '')
    elif len(sBalance) == 2:
        sign = "K"
    elif len(sBalance) == 3:
        sign = "M"
    elif len(sBalance) == 4:
        sign = "B"
    elif len(sBalance) == 5:
        sign = "T"
    elif len(sBalance) >= 6:
        sign = "Q"
    fBalance = sBalance[0] + "." + sBalance[1][0:2] + sign
    return fBalance


async def reraise(ctx, error):
    if isinstance(error, commands.NotOwner):
        error = disnake.Embed(title="ERROR", description="Command Error: You do not own this bot!")
        error.set_footer(text='This is an owner only command')

        await ctx.send(embed=error, delete_after=8)
        await asyncio.sleep(7.5)
        await ctx.message.delete()

    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f'You are on cooldown, **`{time_phaser(error.retry_after)}`** remaining.')

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        return await ctx.send(f"You are missing an argument! See `!help {ctx.command}` if you do not know how to use this.")

    elif isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("Could not find member.")
        ctx.command.reset_cooldown(ctx)
        return

    elif isinstance(error, commands.errors.UserNotFound):
        await ctx.send("Could not find user.")
        ctx.command.reset_cooldown(ctx)
        return

    elif isinstance(error, commands.errors.CheckFailure):
        ctx.command.reset_cooldown(ctx)
        return

    elif (
        isinstance(error, commands.TooManyArguments) or
        isinstance(error, commands.BadArgument) or
        isinstance(error, commands.CommandNotFound)
    ):
        return

    else:
        get_error = "".join(format_exception(error, error, error.__traceback__))
        em = disnake.Embed(description=f'```py\n{get_error}\n```')
        if ctx.guild.id == 750160850077089853:
            await ctx.bot._owner.send(content=f"**An error occured with the command `{ctx.command}`, here is the error:**", embed=em)
            em = disnake.Embed(
                title='Oops... An error has occured.',
                description='An error has occured while invoking this command and has been sent to my master for a fix.',
                color=Colours.red
            )
            await ctx.send(embed=em)
        else:
            await ctx.send(embed=em)


async def slash_reraise(inter: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.NotOwner):
        error = disnake.Embed(title="ERROR", description="Command Error: You do not own this bot!")
        error.set_footer(text='This is an owner only command')
        try:
            return await inter.response.send_message(embed=error, ephemeral=True)
        except disnake.InteractionResponded:
            return await inter.followup.send(embed=error, ephemeral=True)

    elif (
        isinstance(error, commands.TooManyArguments) or
        isinstance(error, commands.BadArgument) or
        isinstance(error, commands.CommandNotFound)
    ):
        return

    elif isinstance(error, commands.errors.CheckFailure):
        return

    else:
        get_error = "".join(format_exception(error, error, error.__traceback__))
        em = disnake.Embed(description=f'```py\n{get_error}\n```')
        if inter.guild.id == 750160850077089853:
            await inter.bot._owner.send(content=f"**An error occured with the slash_command `{inter}`, here is the error:**", embed=em)
            em = disnake.Embed(
                title='Oops... An error has occured.',
                description='An error has occured while invoking this command and has been sent to my master for a fix.',
                color=Colours.red
            )
            try:
                await inter.response.send_message(embed=em, ephemeral=True)
            except disnake.InteractionResponded:
                await inter.followup.send(embed=em, ephemeral=True)
        else:
            try:
                await inter.response.send_message(embed=em, ephemeral=True)
            except disnake.InteractionResponded:
                await inter.followup.send(embed=em, ephemeral=True)


def replace_many(
    sentence: str, replacements: dict, *, ignore_case: bool = False, match_case: bool = False
) -> str:
    """
    Replaces multiple substrings in a string given a mapping of strings.
    By default replaces long strings before short strings, and lowercase before uppercase.

    Example:
        var = replace_many("This is a sentence", {"is": "was", "This": "That"})
        assert var == "That was a sentence"

    If `ignore_case` is given, does a case insensitive match.
    Example:
        var = replace_many("THIS is a sentence", {"IS": "was", "tHiS": "That"}, ignore_case=True)
        assert var == "That was a sentence"

    If `match_case` is given, matches the case of the replacement with the replaced word.
    Example:
        var = replace_many(
            "This IS a sentence", {"is": "was", "this": "that"}, ignore_case=True, match_case=True
        )
        assert var == "That WAS a sentence"
    """
    if ignore_case:
        replacements = dict(
            (word.lower(), replacement) for word, replacement in replacements.items()
        )

    words_to_replace = sorted(replacements, key=lambda s: (-len(s), s))

    # Join and compile words to replace into a regex
    pattern = "|".join(re.escape(word) for word in words_to_replace)
    regex = re.compile(pattern, re.I if ignore_case else 0)

    def _repl(match: re.Match) -> str:
        """Returns replacement depending on `ignore_case` and `match_case`."""
        word = match.group(0)
        replacement = replacements[word.lower() if ignore_case else word]

        if not match_case:
            return replacement

        # Clean punctuation from word so string methods work
        cleaned_word = word.translate(str.maketrans("", "", string.punctuation))
        if cleaned_word.isupper():
            return replacement.upper()
        elif cleaned_word[0].isupper():
            return replacement.capitalize()
        else:
            return replacement.lower()

    return regex.sub(_repl, sentence)


def suppress_links(message: str) -> str:
    """Accepts a message that may contain links, suppresses them, and returns them."""
    for link in set(re.findall(r"https?://[^\s]+", message, re.IGNORECASE)):
        message = message.replace(link, f"<{link}>")
    return message


class ConfirmView(disnake.ui.View):
    """
    This class is a view with `Confirm` and `Cancel` buttons,
    this checks which button the user has pressed and returns
    True via the self.response if the button they clicked was
    Confirm else False if the button they clicked is Cancel.
    """

    def __init__(self, ctx, new_message: str = 'Time Expired.', react_user: disnake.Member = None, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.new_message = new_message
        self.member = react_user
        self.response = None

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        check_for = self.ctx.author.id if self.member is None else self.member.id
        if interaction.author.id != check_for:
            await interaction.response.send_message(
                f'Only {self.ctx.author.display_name if self.member is None else self.member.display_name} can use the buttons on this message!',
                ephemeral=True
            )
            return False
        return True

    async def on_error(self, error: Exception, item, interaction):
        if isinstance(self.ctx, disnake.ApplicationCommandInteraction):
            return await self.ctx.bot.slash_reraise(self.ctx, error)
        return await self.ctx.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.grey
        if self.message:
            await self.message.edit(content=self.new_message, embed=None, view=self)
        else:
            await self.ctx.edit_original_message(content=self.new_message, embed=None, view=self)

    @disnake.ui.button(label='Confirm', style=disnake.ButtonStyle.green)
    async def yes_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        self.response = True
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.grey
            if item.label == button.label:
                item.style = disnake.ButtonStyle.blurple
        self.stop()

    @disnake.ui.button(label='Cancel', style=disnake.ButtonStyle.red)
    async def no_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        self.response = False
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.grey
            if item.label == button.label:
                item.style = disnake.ButtonStyle.blurple
        self.stop()


class ConfirmViewDMS(disnake.ui.View):
    """
    This class is a view with `Confirm` and `Cancel` buttons
    which only works in dms, this checks which button the user
    has pressed and returns True via the self.response if the
    button they clicked was Confirm else False if the button
    they clicked is Cancel.
    """

    def __init__(self, ctx, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.response = None

    async def on_error(self, error: Exception, item, interaction):
        return await self.ctx.bot.reraise(self.ctx, error)

    @disnake.ui.button(label='Confirm', style=disnake.ButtonStyle.green)
    async def yes_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        self.response = True
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.grey
            if item.label == button.label:
                item.style = disnake.ButtonStyle.blurple
        self.stop()

    @disnake.ui.button(label='Cancel', style=disnake.ButtonStyle.red)
    async def no_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        self.response = False
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.grey
            if item.label == button.label:
                item.style = disnake.ButtonStyle.blurple

        self.stop()


def clean_inter_content(
    *,
    fix_channel_mentions: bool = False,
    use_nicknames: bool = True,
    escape_markdown: bool = False,
    remove_markdown: bool = False,
):
    async def convert(inter: disnake.ApplicationCommandInteraction, argument: str):
        if inter.guild:
            def resolve_member(id: int) -> str:
                m = inter.guild.get_member(id)
                return f'@{m.display_name if use_nicknames else m.name}' if m else '@deleted-user'

            def resolve_role(id: int) -> str:
                r = inter.guild.get_role(id)
                return f'@{r.name}' if r else '@deleted-role'
        else:
            def resolve_member(id: int) -> str:
                m = inter.bot.get_user(id)
                return f'@{m.name}' if m else '@deleted-user'

            def resolve_role(id: int) -> str:
                return '@deleted-role'

        if fix_channel_mentions and inter.guild:
            def resolve_channel(id: int) -> str:
                c = inter.guild.get_channel(id)
                return f'#{c.name}' if c else '#deleted-channel'
        else:
            def resolve_channel(id: int) -> str:
                return f'<#{id}>'

        transforms = {
            '@': resolve_member,
            '@!': resolve_member,
            '#': resolve_channel,
            '@&': resolve_role,
        }

        def repl(match: re.Match) -> str:
            type = match[1]
            id = int(match[2])
            transformed = transforms[type](id)
            return transformed

        result = re.sub(r'<(@[!&]?|#)([0-9]{15,20})>', repl, argument)
        if escape_markdown:
            result = disnake.utils.escape_markdown(result)
        elif remove_markdown:
            result = disnake.utils.remove_markdown(result)

        # Completely ensure no mentions escape:
        return disnake.utils.escape_mentions(result)

    return convert


async def safe_send_prepare(content, **kwargs):
    """Same as send except with some safe guards.
    If the message is too long then it sends a file with the results instead.
    """

    if len(content) > 2000:
        fp = io.BytesIO(content.encode())
        kwargs.pop('file', None)
        return {
            'file': disnake.File(fp, filename='message_too_long.txt'),
            **kwargs
        }
    else:
        return {'content': content}
