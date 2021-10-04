import disnake
from disnake.ext import commands
import os
from disnake import Member
from disnake.ext.commands import Greedy
from utils.context import Context
from main import ViHillCorner
from typing import List, Union

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
    'Staff', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', 'lvl 75+', 'lvl 80+',
    'lvl 85+', 'lvl 90+', 'lvl 95+', 'lvl 100+', 'lvl 105+', 'lvl 110+', 'lvl 120+', 'lvl 130+', 'lvl 150+', 'lvl 155+', 'lvl 160+', 'lvl 165+', 'lvl 170+',
    'lvl 175+', 'lvl 180+', 'lvl 185+', 'lvl 190+', 'lvl 195+', 'lvl 200+', 'lvl 205+', 'lvl 210+', 'lvl 215+', 'lvl 220+', 'lvl 230+', 'lvl 240+',
    'lvl 250+', 'lvl 255+', 'lvl 260+', 'lvl 265+', 'lvl 270+', 'lvl 275+', 'lvl 275+', 'lvl 280+', 'lvl 285+', 'lvl 290+', 'lvl 300+', 'lvl 305+',
    'lvl 310+', 'lvl 315+', 'lvl 320+', 'lvl 330+', 'lvl 340+', 'lvl 350+', 'lvl 355+', 'lvl 360+', 'lvl 365+', 'lvl 370+', 'lvl 375+', 'lvl 380+',
    'lvl 385+', 'lvl 390+', 'lvl 395+', 'lvl 400+', 'lvl 405+', 'lvl 410+', 'lvl 415+', 'lvl 420+', 'lvl 430+', 'lvl 440+', 'lvl 450+', 'lvl 455+',
    'lvl 460+', 'lvl 465+', 'lvl 470+', 'lvl 475+', 'lvl 480+', 'lvl 485+', 'lvl 490+', 'lvl 495+', 'lvl 500+'
)


class Actions(commands.Cog):
    """Action commands. e.g: ;huggles | ;pat | etc..."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Marry Data']
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
            ctx: [`:class:Context`]
                The Context object.
            url: [`:class:str`]
                The url of the action to set the image to.
            members: [`List[disnake.Member]`]
                The members list to mention, if None is returned then no mentions are applied.

        Return
        ------
            `None`
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
        """😳 😳 😳"""

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
        """Spank your bae 😏"""

        await self.send_action(ctx, spankk, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def cuddle(self, ctx: Context, members: Greedy[Member] = None):
        """Cuddle with someone ❤️"""

        await self.send_action(ctx, cuddles, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def huggles(self, ctx: Context, members: Greedy[Member] = None):
        """Have a hug with someone ❤️"""

        await self.send_action(ctx, huggless, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def grouphug(self, ctx: Context, members: Greedy[Member] = None):
        """Have a group hug with someone ❤️"""

        await self.send_action(ctx, grouphugg, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def eat(self, ctx: Context, members: Greedy[Member] = None):
        """Eat someone 😈"""

        await self.send_action(ctx, eatt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def chew(self, ctx: Context, members: Greedy[Member] = None):
        """Chew on someone 😈"""

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
        """Let others know how much of a crybaby you are 🙄"""

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
        """Kill someone 🔪"""

        await self.send_action(ctx, killl, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def pat(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a pat ❤️"""

        await self.send_action(ctx, patt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def rub(self, ctx: Context, members: Greedy[Member] = None):
        """Rub on someone 😳"""

        await self.send_action(ctx, rubb, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def nom(self, ctx: Context, members: Greedy[Member] = None):
        """Nom someone 😳"""

        await self.send_action(ctx, nomm, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def catpat(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a cat pat ❤️"""

        await self.send_action(ctx, catpatt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def dogpat(self, ctx: Context, members: Greedy[Member] = None):
        """Give someone a dog pat ❤️"""

        await self.send_action(ctx, dogpatt, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def hug(self, ctx: Context, members: Greedy[Member] = None):
        """Hug someone 🤗"""

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
        """Give someone a kiss 😳"""

        await self.send_action(ctx, kisss, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def ily(self, ctx: Context, members: Greedy[Member] = None):
        """Let someone know that you love them ❤️"""

        await self.send_action(ctx, ilyy, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def nocry(self, ctx: Context, members: Greedy[Member] = None):
        """Don't let them cry 💔"""

        await self.send_action(ctx, nocryy, members)

    @commands.command()
    @commands.has_any_role(*all_roles)
    async def shrug(self, ctx: Context):
        r"""¯\_(ツ)_/¯"""

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
        """Give someone a cute bear hug ❤️"""

        await self.send_action(ctx, bearhugg, members)

    @commands.command()
    async def moan(self, ctx: Context):
        """😏"""

        moan = disnake.Embed(color=disnake.Color.red())
        moan.set_image(url=moann)

        await ctx.send(embed=moan)

    @commands.command()
    async def specialkiss(self, ctx: Context, member: disnake.Member = None):
        """
        Give someone a hot smooch 😳 😏 😏
        You must be married to them
        """

        if member is None:
            await ctx.send("You must specify the user you want to kiss.")
            return

        else:
            result = await self.db.find_one({"_id": member.id})
            get_marry = await self.db.find_one({"_id": member.id})

            if result is None:
                return await ctx.send(
                    "You must be married to someone in order to use this command!"
                )
            elif get_marry is None:
                return await ctx.send(
                    "That user is not married to anyone, therefore that member cannot be kissed that way."
                )

            else:
                user = self.bot.get_user(get_marry["married_to"])

                if ctx.author.id == user.id:

                    em = disnake.Embed(color=disnake.Color.red())
                    em.set_image(url=specialkiss)

                    await ctx.send(member.mention, embed=em)

                elif not ctx.author.id == user.id:
                    await ctx.send(
                        "That user is married to `{}`, and only they can kiss that person!".format(
                            user.display_name
                        )
                    )

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send(
                "You must be at least `level 15+` in order to use this command! %s"
                % (ctx.author.mention)
            )
        else:
            if hasattr(ctx.command, "on_error"):
                return
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Actions(bot))
