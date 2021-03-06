from typing import List, Union
import os

import disnake
from disnake import Member
from disnake.ext import commands
from disnake.ext.commands import Greedy

from utils.context import Context
from utils.databases import Marriage

from main import ViHillCorner

huggless = os.environ.get("HUGGLES")
grouphugg = os.environ.get("GROUPHUG")
eatt = os.environ.get("EAT")
cheww = os.environ.get("CHEW")
sipp = os.environ.get("SIP")
clapp = os.environ.get("CLAP")
cryy = os.environ.get("CRY")
rofll = os.environ.get("ROFL")
loll = os.environ.get("LOL")
killl = os.environ.get("KILL")
patt = os.environ.get("PAT")
rubb = os.environ.get("RUB")
nomm = os.environ.get("NOM")
catpatt = os.environ.get("CATPAT")
dogpatt = os.environ.get("DOGPAT")
hugg = os.environ.get("HUG")
pilloww = os.environ.get("PILLOW")
sprayy = os.environ.get("SPRAY")
hypee = os.environ.get("HYPE")
kisss = os.environ.get("KISS")
ilyy = os.environ.get("ILY")
nocryy = os.environ.get("NOCRY")
shrugg = os.environ.get("SHRUG")
smugg = os.environ.get("SMUG")
bearhugg = os.environ.get("BEARHUG")
moann = os.environ.get("MOAN")
cuddles = os.getenv("CUDDLE")
specialkiss = os.getenv("SPECIALKISS")
slapp = os.getenv("SLAP")
spankk = os.getenv("SPANK")

all_roles = (
    754676705741766757, 750160850290999332, 750160850290999333, 750160850290999334,
    750160850290999335, 750160850295324744, 750160850295324745, 750160850295324746,
    750160850295324747, 750160850295324748, 750160850295324749, 750160850295324750,
    788127504710762497, 788127526278791240, 788127540459208725, 788127547606827028,
    788127552686129265, 788127561283928115, 788127569198579764, 788127574663495720,
    788127580330655744, 788127589092818994, 788127593386868758, 818562249349660713,
    818562250252091413, 818562250477404173, 818562251644076072, 818562252185534465,
    818562252360777749, 818562252906037259, 818562253501628507, 818562254043480075,
    818562254495547462, 818562254680883241, 818562255188131924, 818562256101965844,
    818562256546824192, 818562257033101372, 818562257653858304, 818562258119950367,
    818562258551832657, 818562259587563523, 818562260254588988, 818562260686995486,
    818562261844230215, 818562262360784977, 818562262520430654, 818562263169368076,
    818562263850025031, 818562264030380033, 818562264554405899, 818562265422757898,
    818562265779273749, 818562266475528242, 818562266760740926, 818562267410726964,
    818562267837628456, 818562268044197889, 818562268966027294, 818562269029466124,
    818562269835034625, 818562270119985163, 818562270375182357, 818562271100928020,
    818562271269486623, 818562271978586132, 818562272791101500, 818562273202405396,
    818562273215774776, 818562274318090260, 818562274502508555, 818562275539550239,
    818562276490870857, 818562276939661343, 818562277514805258, 818562277619400765,
    818562278521569282, 818562278832078939, 818562279725203508, 818562280009760889,
    818562280765390909, 818562281410658344, 818562282019356733
)


class Actions(commands.Cog):
    """Action commands. e.g: ;huggles | ;pat | etc..."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = ";"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='speachless', id=789189473686257674)

    async def send_action(self, ctx: Context, url: str, members: Union[List[Member], None]) -> None:
        """|coro|

        Sends the action.

        Parameters
        ----------
            ctx: `:class:Context`
                The Context object.
            url: `:class:str`
                The url of the action to set the image to.
            members: `List[disnake.Member]`
                The members list to mention, if None is returned then no mentions are applied.

        Return
        ------
            None
        """

        em = disnake.Embed(color=disnake.Color.red())
        em.set_image(url=url)
        mention_list = []
        owner_ignore = ('pillow', 'kill', 'spray', 'slap', 'spank')

        if members is None:
            return await ctx.send(embed=em)

        for member in members:
            if member.id == self.bot._owner_id and ctx.command.name in owner_ignore:
                member = ctx.author
            mention = member.mention

            mention_list.append(mention)

        mentions = ' '.join(mention_list)
        await ctx.send(mentions, embed=em)

    @commands.command()
    async def rape(self, ctx: Context):
        """???? ???? ????"""

        await ctx.send(
            "https://cdn.discordapp.com/attachments/745298904832278530/782729248623427614/video0-1_1.mp4"
        )

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def slap(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a slap <:smort:750751866454802484>"""

        await self.send_action(ctx, slapp, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def spank(self, ctx: Context, members: Greedy[Member] = None):
        """Spank your bae ????"""

        await self.send_action(ctx, spankk, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def cuddle(self, ctx: Context, members: Greedy[Member] = None):
        """Cuddle with someone ??????"""

        await self.send_action(ctx, cuddles, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def huggles(self, ctx: Context, members: Greedy[Member] = None):
        """Have a hug with someone ??????"""

        await self.send_action(ctx, huggless, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def grouphug(self, ctx: Context, members: Greedy[Member] = None):
        """Have a group hug with someone ??????"""

        await self.send_action(ctx, grouphugg, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def eat(self, ctx: Context, members: Greedy[Member] = None):
        """Eat someone ????"""

        await self.send_action(ctx, eatt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def chew(self, ctx: Context, members: Greedy[Member] = None):
        """Chew on someone ????"""

        await self.send_action(ctx, cheww, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def sip(self, ctx: Context):
        """Simply sipping from your cup of tea"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=sipp)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def clap(self, ctx: Context):
        """Clap your hands"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=clapp)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def cry(self, ctx: Context):
        """Let others know how much of a crybaby you are ????"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=cryy)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def rofl(self, ctx: Context):
        """Roll on the floor laughing"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=rofll)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def lol(self, ctx: Context):
        """Lots of laugh"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=loll)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def kill(self, ctx: Context, members: Greedy[Member] = None):
        """Kill someone ????"""

        await self.send_action(ctx, killl, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def pat(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a pat ??????"""

        await self.send_action(ctx, patt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def rub(self, ctx: Context, members: Greedy[Member] = None):
        """Rub on someone ????"""

        await self.send_action(ctx, rubb, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def nom(self, ctx: Context, members: Greedy[Member] = None):
        """Nom someone ????"""

        await self.send_action(ctx, nomm, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def catpat(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a cat pat ??????"""

        await self.send_action(ctx, catpatt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def dogpat(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a dog pat ??????"""

        await self.send_action(ctx, dogpatt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def hug(self, ctx: Context, members: Greedy[Member] = None):
        """Hug someone ????"""

        await self.send_action(ctx, hugg, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def pillow(self, ctx: Context, members: Greedy[Member] = None):
        """Throw a pillow at someone"""

        await self.send_action(ctx, pilloww, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def spray(self, ctx: Context, members: Greedy[Member] = None):
        """Spray someone"""

        await self.send_action(ctx, sprayy, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def hype(self, ctx: Context):
        """Show others that you're on steroids"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=hypee)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def kiss(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a kiss ????"""

        await self.send_action(ctx, kisss, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def ily(self, ctx: Context, members: Greedy[Member] = None):
        """Let someone know that you love them ??????"""

        await self.send_action(ctx, ilyy, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def nocry(self, ctx: Context, members: Greedy[Member] = None):
        """Don't let them cry ????"""

        await self.send_action(ctx, nocryy, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def shrug(self, ctx: Context):
        r"""??\_(???)_/??"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=shrugg)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def smug(self, ctx: Context):
        """UwU ?"""

        version = disnake.Embed(color=disnake.Color.red())
        version.set_image(url=smugg)

        await ctx.send(embed=version)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def bearhug(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a cute bear hug ??????"""

        await self.send_action(ctx, bearhugg, members)

    @commands.command()
    async def moan(self, ctx: Context):
        """????"""

        moan = disnake.Embed(color=disnake.Color.red())
        moan.set_image(url=moann)

        await ctx.send(embed=moan)

    @commands.command()
    async def specialkiss(self, ctx: Context, member: disnake.Member = None):
        """
        Give someone a hot smooch ???? ???? ????
        You must be married to them
        """

        if member is None:
            await ctx.send("You must specify the user you want to kiss.")
            return

        else:
            result: Marriage = await Marriage.find_one({"_id": member.id})
            get_marry: Marriage = await Marriage.find_one({"_id": member.id})

            if result is None:
                return await ctx.send(
                    "You must be married to someone in order to use this command!"
                )
            elif get_marry is None:
                return await ctx.send(
                    "That user is not married to anyone, therefore that member cannot be kissed that way."
                )

            else:
                user = self.bot.get_user(get_marry.married_to)

                if ctx.author.id == user.id:

                    em = disnake.Embed(color=disnake.Color.red())
                    em.set_image(url=specialkiss)

                    await ctx.send(member.mention, embed=em)

                elif not ctx.author.id == user.id:
                    await ctx.send(
                        f"That user is married to `{user.display_name}`, and only they can kiss that person!"
                    )

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send(
                f"You must be at least `level 15+` in order to use this command! {ctx.author.mention}"
            )
        else:
            if hasattr(ctx.command, "on_error"):
                return
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Actions(bot))
