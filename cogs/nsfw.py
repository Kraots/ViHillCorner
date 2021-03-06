import aiohttp

import pymongo

import disnake
from disnake.ext import commands
from disnake.ext.commands import Greedy
from disnake import Member

from utils.helpers import NSFW
from utils.colors import Colours
from utils.paginator import SimplePages
from utils.context import Context

import hmtai

from main import ViHillCorner

nsfw_url = 'https://nekobot.xyz/api/image?type='
nsfw_categs = (
    'hentai', 'ass', 'thigh', 'hass', 'hboobs',
    'pgif', 'paizuri', 'boobs', 'pussy', 'hyuri',
    'hthigh', 'lewdneko', 'anal', 'hmidriff', 'feet',
    'gonewild', 'hkitsune', '4k', 'blowjob', 'tentacle',
    'hentai_anal'
)
real_categs = (
    'ass', 'thigh', 'pgif', 'boobs', 'pussy', 'anal',
    'feet', 'gonewild', '4k', 'blowjob'
)
hentai_categs_1 = (
    'hentai', 'hass', 'hboobs', 'paizuri', 'hyuri',
    'hthigh', 'lewdneko', 'hmidriff', 'hkitsune',
    'tentacle', 'hentai_anal'
)
hentai_categs_2 = (
    'ass', 'ecchi', 'ero', 'hentai', 'maid', 'milf',
    'oppai', 'oral', 'paizuri', 'selfies', 'uniform'
)


class NSFWPageEntry:
    def __init__(self, entry):

        self.id = entry['_id']

    def __str__(self):
        return f'<@!{self.id}>\u2800•\u2800(`UserID:` {self.id})'


class NSFWPages(SimplePages):
    def __init__(self, ctx: Context, entries, *, per_page=12):
        converted = [NSFWPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page, compact=True)


class NSFW(commands.Cog):
    """Nsfw related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['NSFW blocks']
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='yamete', id=857163308427902987)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def nsfw(self, ctx: Context):
        """See the types of nsfw 😏"""

        await ctx.send(
            "There are only 2 types: `real`, `hentai`\nType `!nsfw <type>` to see all the categories of a type.\n"
            "***Keep in mind that these only work in the nsfw channel.***"
        )

    async def nsfw_hentai_0(self, ctx: Context, category):
        """The old nsfw."""

        if category is None:
            categs = "foot **•** mW **•** elves **•** hentai **•** nsfwNeko **•** ero **•** lick **•** glasses **•** blowjob **•** pussy **•** cum " \
                "**•** femdom **•** cuckold **•** slap **•** ass **•** ahegao **•** incest **•** manga **•** uniform **•** public **•** jahy " \
                "**•** panties **•** creampie **•** boobjob **•** orgy **•** masturbation **•** yuri **•** bdsm **•** thighs **•** nsfwMW " \
                "**•** gangbang **•** tentacles **•** hnt_gifs"
            em = disnake.Embed(title="Here are all the categories for hentai 0", description=categs, color=Colours.blurple)
            em.set_footer(text='They are all case sensitive!')
            return await ctx.send(embed=em)

        try:
            result = hmtai.useHM(version='2_9', category=category)

            em = disnake.Embed(color=Colours.pastel)
            em.set_image(url=result)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)
        except Exception:
            return await ctx.send('Category does not exist.')

    async def nsfw_hentai_1(self, ctx: Context, category):
        """The slightly new nsfw."""

        if category is None:
            categs = "hentai **•** paizuri **•** yuri **•** thighs **•** neko **•** anal **•** hmidriff **•** kitsune **•** tentacle"
            em = disnake.Embed(color=Colours.blurple, title="Here are all the categories for hentai 1:", description=categs)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            return await ctx.send(embed=em)

        categ = category.lower()
        if categ not in hentai_categs_1:
            if categ == 'ass':
                categ = 'hass'
            elif categ in ('boob', 'boobs'):
                categ = 'hboobs'
            elif categ == 'yuri':
                categ = 'hyuri'
            elif categ in ('thigh', 'thighs'):
                categ = 'hthigh'
            elif categ == 'neko':
                categ = 'lewdneko'
            elif categ == 'anal':
                categ = 'hentai_anal'
            elif categ == 'kitsune':
                categ = 'hkitsune'
            elif categ == 'tentacles':
                categ = 'tentacle'
            else:
                return await ctx.reply("Not in the existing hentai categories.")
        try:
            async with self.bot.session.get(nsfw_url + categ) as resp:
                if resp.status != 200:
                    await self.bot._owner.send(f"`{ctx.command} {categ}` returned\n**{await resp.json()}**")
                    return await ctx.send("There has been an error from the **API**, please try again later.")
                content = await resp.json()
                url = content['message']
            em = disnake.Embed(color=Colours.pastel)
            em.set_image(url=url)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)
        except aiohttp.ClientConnectorError:
            await ctx.send('Error connecting to this nsfw API. There is no ETA until it will be fixed so please use the others available APIs for nsfw hentai.')

    async def nsfw_hentai_2(self, ctx: Context, gif, category):
        """The new nsfw."""

        if category is None:
            categs = "ass **•** ecchi **•** ero **•** hentai **•** maid **•** milf **•** oppai **•** oral **•** paizuri **•** selfies **•** uniform"
            em = disnake.Embed(color=Colours.blurple, title="Here are all the categories for hentai 2:", description=categs)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            return await ctx.send(embed=em)

        categ = category.lower()
        if categ not in hentai_categs_2:
            return await ctx.reply("Not in the existing hentai categories.")

        elif categ in ('selfies', 'maid') and gif != '':
            return await ctx.reply(f'`{categ}` doesn\'t have gifs.')

        try:
            async with self.bot.session.get('https://api.waifu.im/nsfw/' + categ + gif) as resp:
                if resp.status != 200:
                    err = await resp.json()
                    if err['error'] == 'Sorry no image were found with the criteria you gave to the API, please retry with a different criteria.':
                        return await ctx.reply('No gif found for this type of category.')
                    await self.bot.owner.send(f"`{ctx.command} {categ}` returned\n**{err}**")
                    return await ctx.send("There has been an error from the **API**, please try again later.")
                content = await resp.json()
                data = content['tags']
            url = data[0]['images'][0]['url']
            em = disnake.Embed(color=Colours.pastel)
            em.set_image(url=url)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)
        except aiohttp.ClientConnectorError:
            await ctx.send('Error connecting to this nsfw API. There is no ETA until it will be fixed so please use the others available APIs for nsfw hentai.')

    @nsfw.command(name='hentai')
    @commands.check(NSFW)
    async def nsfw_hentai(self, ctx: Context, API: int = None, category: str = None, gif: str = None):
        """Get the categories from one of the hentai APIs
        APIs:
        \u2800 • **0**
        \u2800 • **1**
        \u2800 • **2** (SUPPORTS GIF)
        The gif param indicates whether to force the API to return a gif image. Only use this on the APIs that support it.
        Example:
        \u2800 !nsfw hentai 2 ass gif
        """

        if API is None:
            em = disnake.Embed(color=Colours.blurple, description="""
                APIs:
                \u2800 • **0**
                \u2800 • **1**
                \u2800 • **2** (SUPPORTS GIF)
                The gif param indicates whether to force the API to return a gif image. Only use this on the APIs that support it.
                Example:
                \u2800 !nsfw hentai 2 ass gif
                """)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            return await ctx.send(embed=em)

        if gif is None:
            gif = ''
        else:
            if gif.lower() in ('gif', 'true', '1'):
                gif = '?gif=True'
            else:
                gif = ''

        if API == 0:
            return await self.nsfw_hentai_0(ctx, category)
        elif API == 1:
            return await self.nsfw_hentai_1(ctx, category)
        elif API == 2:
            return await self.nsfw_hentai_2(ctx, gif, category)

    @nsfw.command(name='real')
    @commands.check(NSFW)
    async def nsfw_real(self, ctx: Context, category: str = None):
        """Get a real porn random image based on the chosen category 😏"""

        if category is None:
            categs = "ass **•** thigh **•** gif **•** boobs **•** pussy **•** anal **•** feet **•** wild **•** 4k **•** bj/blowjob"
            em = disnake.Embed(color=Colours.blurple, title="Here are all the categories for real porn:", description=categs)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            return await ctx.send(embed=em)

        categ = category.lower()
        if categ not in real_categs:
            if categ == 'thighs':
                categ = 'thigh'
            elif categ == 'bj':
                categ = 'blowjob'
            elif categ == 'gif':
                categ = 'pgif'
            elif categ == 'wild':
                categ = 'gonewild'
            elif categ == 'boob':
                categ = 'boobs'
            else:
                return await ctx.reply("Not in the existing real nsfw categories.")

        try:
            async with self.bot.session.get(nsfw_url + categ) as resp:
                if resp.status != 200:
                    await self.bot._owner.send(f"`{ctx.command} {categ}` returned\n**{resp.status}**")
                    return await ctx.send("There has been an error from the **API**, please try again later.")
                content = await resp.json()
                url = content['message']
            em = disnake.Embed(color=Colours.pastel)
            em.set_image(url=url)
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)
        except aiohttp.ClientConnectorError:
            await ctx.send('Error connecting to this nsfw API. There is no ETA until it will be fixed so please use the nsfw hentai APIs or try again later.')

    @nsfw.command()
    async def me(self, ctx: Context, choice: str):
        """
        The choice must be either `add` or `remove`.
        If you're blocked you won't be able to use any.
        """

        user = ctx.author
        guild = self.bot.get_guild(750160850077089853)
        nsfwchannel = guild.get_channel(780374324598145055)

        result = await self.db.find_one({'_id': user.id})

        if choice == "remove":
            try:
                await nsfwchannel.set_permissions(user, overwrite=None)
                await user.send("You cannot see the nsfw channel anymore. <:weird:773538796087803934>")
                await ctx.message.delete()
            except Exception:
                return

        elif choice == "add":
            if result is not None:
                await ctx.send(f"You are restricted from using that command, therefore your permissions have not been changed! {user.mention}")
                return

            else:
                await nsfwchannel.set_permissions(user, read_messages=True, reason="The user requested by himself the permission using `!nsfw me`")
                await user.send('You can now see the nsfw channel! <#780374324598145055> <:peepo_yay:773535977624698890>')
                await ctx.message.delete()

    @nsfw.group(name='block')
    @commands.has_role(754676705741766757)
    async def nsfw_block(self, ctx: Context, members: Greedy[Member]):
        """Blocks the members from accessing the nsfw channel."""

        guild = self.bot.get_guild(750160850077089853)
        nsfwchannel = guild.get_channel(780374324598145055)

        blocked_list = []
        for member in members:
            try:
                await nsfwchannel.set_permissions(member, overwrite=None)
            except Exception:
                pass

            a = f"{member.name}#{member.discriminator}"
            blocked_list.append(a)

            post = {'_id': member.id}
            try:
                await self.db.insert_one(post)
            except pymongo.errors.DuplicateKeyError:
                pass

        blocked_members = " | ".join(blocked_list)
        await ctx.send(f"`{blocked_members}` have been blocked from seeing the nsfw channel.")

    @nsfw.command(name='blocks')
    @commands.has_role(754676705741766757)
    async def nsfw_blocks(self, ctx: Context):
        """Sends a list with the blocked users for the nsfw channel."""

        try:
            entries = await self.db.find().to_list(100000)
            p = NSFWPages(ctx=ctx, entries=entries, per_page=7)
            await p.start()
        except Exception:
            await ctx.send("There are no members whose acces has been restricted.")

    @nsfw.command(name='unblock')
    @commands.has_role(754676705741766757)
    async def nsfw_unblock(self, ctx: Context, members: Greedy[Member]):
        """Unblock the members from accessing the nsfw channel."""

        blocked_list = []
        for member in members:

            a = f"{member.name}#{member.discriminator}"
            blocked_list.append(a)

            await self.db.delete_one({'_id': member.id})
            await member.send("Your acces for using the `!nsfw me` command has ben re-approved.")

        blocked_members = " | ".join(blocked_list)
        await ctx.send(f"`{blocked_members}` have been unblocked from seeing the nsfw channel.")

    @nsfw.error
    async def nsfw_error(self, ctx: Context, error):
        if isinstance(error, commands.CheckFailure):
            if not isinstance(ctx.channel, disnake.DMChannel):
                if 754676705741766757 in (role.id for role in ctx.author.roles):
                    await ctx.send('Invalid format!\nUse: `!nsfw block <users>` or `!nsfw unblock <users>`!')
        else:
            await self.bot.reraise(ctx, error)

    @nsfw_real.error
    async def nsfw_real_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CheckFailure):
            if not isinstance(ctx.channel, disnake.DMChannel):
                await ctx.reply('This command is only usable in a nsfw marked channel.')
        else:
            await self.bot.reraise(ctx, error)

    @nsfw_hentai.error
    async def nsfw_hentai_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CheckFailure):
            if not isinstance(ctx.channel, disnake.DMChannel):
                await ctx.reply('This command is only usable in a nsfw marked channel.')
        else:
            await self.bot.reraise(ctx, error)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == 938097236024360960:
            return

        await self.db.delete_one({'_id': member.id})


def setup(bot):
    bot.add_cog(NSFW(bot))
