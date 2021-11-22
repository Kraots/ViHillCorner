import disnake
from disnake.ext import commands
from disnake import Member
from disnake.ext.commands import Greedy

from utils.context import Context

from .actions import all_roles

from main import ViHillCorner


class Info(commands.Cog):
    """Information/warn commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = ";"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='pink_warning', id=851505721127862302)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def sfw(self, ctx: Context, members: Greedy[Member] = None):
        """Warn someone that the chat needs to be sfw."""

        sfw = disnake.Embed(title="NSFW Warning", description="Please keep the chat appropiate and sfw.", color=disnake.Color.red())
        mention_list = []

        if members is None:
            await ctx.send(embed=sfw, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=sfw, reference=ctx.replied_reference)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def intros(self, ctx: Context, members: Greedy[Member] = None):
        """Warn someone that the chat needs to be sfw."""

        sfw = disnake.Embed(title="How do I create/edit my introduction?", description="Send `!intro` in <#750160851822182486>", color=disnake.Color.red())
        mention_list = []

        if members is None:
            await ctx.send(embed=sfw, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=sfw, reference=ctx.replied_reference)

    @commands.command(name='howtolvl', aliases=['lvlinfo', 'levelinfo', 'lvl-info', 'level-info', 'howtolevel'])
    @commands.has_any_role(*all_roles)
    async def level_info(self, ctx: Context, members: Greedy[Member] = None):
        """Sends info to the member for how to level up."""

        lvl = disnake.Embed(
            title="How to lvl up",
            description="You can level up in this server by chatting in any channel. Spamming or `XP farming` would result in level reset. "
                        "\n\nTo check your rank, send `!rank` in <#750160851822182486>",
            color=disnake.Color.red()
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=lvl, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=lvl, reference=ctx.replied_reference)

    @commands.command(name='rankinfo', aliases=['rank-info', 'rankcheck'])
    @commands.has_any_role(*all_roles)
    async def rank_info(self, ctx: Context, members: Greedy[Member] = None):
        """Sends info to the member for how to check their rank."""

        rank = disnake.Embed(title="How to check your rank", description="Send `!rank` in <#750160851822182486> to check your rank.", color=disnake.Color.red())
        mention_list = []

        if members is None:
            await ctx.send(embed=rank, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=rank, reference=ctx.replied_reference)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def spam(self, ctx: Context, members: Greedy[Member] = None):
        """Warn someone to not spam."""

        em = disnake.Embed(
            color=disnake.Color.red(),
            title="Spam warning",
            description="Please do not spam the chat <:heartato:789581738124640256> <:cry_why:789581737873244160>"
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=em, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=em, reference=ctx.replied_reference)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def english(self, ctx: Context, members: Greedy[Member] = None):
        """Warn someone that the chat is english only, if they keep talking not in english then please @ a mod, ***once*** or dm one with the problem."""

        em = disnake.Embed(
            color=disnake.Color.red(),
            title="Warning",
            description="This is an English only server! Speaking any other languages will lead to a mute. <:satania_love:789809969049632768>"
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=em, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=em, reference=ctx.replied_reference)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def cam(self, ctx: Context, members: Greedy[Member] = None):
        """Sends info to the member for what level do they need in order to use the camera in a vc."""

        em = disnake.Embed(
            color=disnake.Color.red(),
            title="How to Stream or Enable Webcam in VCs:",
            description="You need to be **lvl 5+** in order to stream or enable your webcam in voice channels. <:bloblove:758378159015723049>"
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=em, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=em, reference=ctx.replied_reference)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def vc(self, ctx: Context, members: Greedy[Member] = None):
        """Sends info to the member for what level do they need in order to use a vc."""

        em = disnake.Embed(
            color=disnake.Color.red(),
            title="How to gain acces to VC:",
            description="To speak in a voice channel on VHC, you must be **lvl 3+**.  Send `!rank` in <#750160851822182486> to check your rank."
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=em, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=em, reference=ctx.replied_reference)

    @commands.command(aliases=['attachments', 'videos', 'links', 'files'])
    @commands.has_any_role(*all_roles)
    async def images(self, ctx: Context, members: Greedy[Member] = None):
        """Sends info to the member for what level do they need in order to be able to send images in every channel."""

        em = disnake.Embed(
            color=disnake.Color.red(),
            title="Why i can't send images?",
            description="To send images/videos in all channels, you must be **lvl 40+**, until then please use the images/videos channels. "
                        "Send `!rank` in <#750160851822182486> to check your rank."
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=em, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=em, reference=ctx.replied_reference)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def age(self, ctx: Context, members: Greedy[Member] = None):
        """Warn the member that they're under discord's TOS minimal age and/or to not joke about their age."""

        em = disnake.Embed(
            color=disnake.Color.red(),
            title="Warning",
            description="Please do not joke about being under the minimum age for discord as per its ToS."
        )
        mention_list = []

        if members is None:
            await ctx.send(embed=em, reference=ctx.replied_reference)

        else:
            for member in members:
                a = member.mention

                mention_list.append(a)
                mentions = " ".join(mention_list)

            await ctx.send(mentions, embed=em, reference=ctx.replied_reference)

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send(f"You must be at least `level 20+` in order to use this command! {ctx.author.mention}")
        else:
            if hasattr(ctx.command, 'on_error'):
                return
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Info(bot))
