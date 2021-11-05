import asyncio
import datetime

import disnake
from disnake.ext import commands

from utils.colors import Colours
from utils.context import Context
from utils.paginator import SimplePages
from utils.databases import Snippet

from main import ViHillCorner

nono_names = (
    "huggles", "grouphug", "eat", "chew", "sip", "clap", "cry", "rofl", "lol", "kill",
    "pat", "rub", "nom", "catpat", "hug", "pillow", "spray", "hype", "specialkiss",
    "kiss", "ily", "nocry", "shrug", "smug", "bearhug", "moan"
)


class SnippetPageEntry:
    def __init__(self, entry: Snippet):

        self.name = entry.name
        self.id = entry.owner_id

    def __str__(self):
        return f'{self.name}\u2800•\u2800(`Owner:` <@!{self.id}>)'


class SnippetPages(SimplePages):
    def __init__(self, ctx: Context, entries, *, per_page=12, color=None):
        converted = [SnippetPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page, color=color)


class Snippets(commands.Cog):
    """Snippet related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '✂️'

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=('snippets',), ignore_extra=False)
    async def snippet(self, ctx: Context):
        """
        Get a list with all the snippets.
        To use a snippet you must type `;snippet_name`
        """

        entries = await Snippet.find().to_list(100000)
        p = SnippetPages(ctx=ctx, entries=entries, per_page=7, color=Colours.reds)
        await p.start()

    @snippet.command(name='search')
    async def snippet_search(self, ctx: Context, *, query):
        """Search for snippet matches based on the query that you've given."""

        query = str(query).lower()
        entries = await Snippet.find({'_id': {'$regex': query, '$options': 'i'}}).to_list(100000)
        try:
            p = SnippetPages(ctx=ctx, entries=entries, per_page=7, color=Colours.reds)
            await p.start()
        except Exception:
            await ctx.send('No snippets found. %s' % (ctx.author.mention))

    @snippet.command(name='leaderboard', aliases=('lb', 'top',))
    async def snippet_leaderboard(self, ctx: Context):
        """See top **10** most used snippets."""

        snippets: list[Snippet] = await Snippet.find().sort("uses_count", -1).to_list(10)
        index = 0
        em = disnake.Embed(color=Colours.reds)
        for snippet in snippets:
            owner = self.bot.get_user(snippet.owner_id)
            index += 1
            em.add_field(
                name=f"`{index}`.\u2800{snippet.name}",
                value=f"Uses: `{snippet.uses_count}`\n Owner: `{owner}`",
                inline=False
            )

        await ctx.send(embed=em)

    @snippet.command(name='list')
    async def snippet_list(self, ctx: Context, member: disnake.Member = None):
        """Get a list with all the snippets that the member has."""

        member = member or ctx.author
        entries: list[Snippet] = await Snippet.find({'owner_id': member.id}).to_list(100000)
        try:
            p = SnippetPages(ctx=ctx, entries=entries, per_page=7, color=Colours.reds)
            await p.start()
        except Exception:
            await ctx.send('You do not own any snippets. %s' % (ctx.author.mention))

    @snippet.command(name='info')
    async def snippet_info(self, ctx: Context, *, snippet_name: str = None):
        """Get some info about the snippet."""

        if snippet_name is None:
            return await ctx.reply("**!snippet info <snippet_name>**")

        snippet: Snippet = await Snippet.find_one({'_id': snippet_name.lower()})

        if snippet is None:
            return await ctx.send("Snippet **%s** does not exist! %s" % (snippet_name, ctx.author.mention))

        _sorted: list[Snippet] = await Snippet.find().sort('uses_count', -1).to_list(100000)
        rank = 0
        for e in _sorted:
            rank += 1
            if e.name == snippet.name:
                break

        snippet_owner = self.bot.get_user(snippet.owner_id)

        em = disnake.Embed(color=Colours.reds, title=snippet_name)
        em.set_author(name=snippet_owner, icon_url=snippet_owner.display_avatar)
        em.add_field(name="Owner", value=snippet_owner.mention)
        em.add_field(name="Uses", value=snippet.uses_count)
        em.add_field(name="Rank", value="`#{}`".format(rank))
        em.set_footer(text="Snippet created at • {}".format(snippet.created_at))

        await ctx.send(embed=em)

    @snippet.command(name='create', aliases=('make', 'add',))
    @commands.has_any_role(
        'Staff', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+",
        "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+",
        "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+",
        "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+",
        "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+",
        "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+",
        "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+",
        "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+",
        "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+",
        "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+"
    )
    async def snippet_create(self, ctx: Context, *, snippet_name: str = None):
        """Create a snippet."""

        if snippet_name is None:
            def check(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            await ctx.send("What do you want to name this snippet?")
            try:
                presnippet_name = await self.bot.wait_for('message', timeout=120, check=check)
                snippet_name = presnippet_name.content
            except asyncio.TimeoutError:
                return await ctx.reply("Ran out of time")

        snippet: Snippet = await Snippet.find_one({'_id': snippet_name.lower()})
        if snippet is not None:
            return await ctx.send("Snippet name (`%s`) is already taken. %s" % (snippet_name, ctx.author.mention))
        for x in ('kraots', 'carrots', 'carots', 'carot', 'carrot'):
            if x in snippet_name.lower():
                if ctx.author.id != 374622847672254466:
                    return await ctx.send("You cannot create a snippet with that name. %s" % (ctx.author.mention))

        if len(snippet_name) >= 50:
            await ctx.send("Snippet's name cannot be that long! Max is: `50`")
            return

        elif len(snippet_name) < 3:
            await ctx.send("Snippet's name cannot be less than `3` characters long!")
            return

        elif snippet_name.isnumeric():
            await ctx.send("Snippet name cannot be a number!")
            return

        elif snippet_name.lower() in nono_names:
            await ctx.send("That names are invalid! Reason: `They are used in other commands, actions, to be more specific.`")
            return

        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        await ctx.send("Please send the image of the snippet.")
        try:
            _content = await self.bot.wait_for('message', timeout=180, check=check)
            content = _content.attachments[0].url

        except asyncio.TimeoutError:
            return await ctx.reply("Ran out of time.")

        except IndexError:
            return await ctx.reply("That is not an image! Please send an image and nothing else!")

        get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")

        snippet = Snippet(
            name=snippet_name.lower(),
            content=content,
            owner_id=ctx.author.id,
            created_at=get_time,
            uses_count=0
        )
        await snippet.commit()

        await ctx.send("Snippet Added!")

    @snippet.command(name='delete')
    @commands.has_any_role(
        'Staff', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+",
        "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+",
        "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+",
        "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+",
        "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+",
        "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+",
        "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+",
        "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+",
        "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+",
        "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+"
    )
    async def snippet_delete(self, ctx: Context, *, snippet_name: str = None):
        """Delete a snippet, you must own it."""

        if snippet_name is None:
            return await ctx.reply("**!snippet delete <snippet_name>**")

        snippet: Snippet = await Snippet.find_one({'_id': snippet_name.lower()})
        if snippet is None:
            return await ctx.send("Snippet `%s` does not exist! %s" % (snippet_name, ctx.author.mention))

        if ctx.author.id != 374622847672254466:
            if ctx.author.id != snippet.owner_id:
                await ctx.send("You do not own this snippet!")
                return
        else:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to delete the snippet `%s`? %s" % (snippet_name, ctx.author.mention), view=view)
            await view.wait()
            if view.response is True:
                await snippet.delete()

                e = f"`{snippet_name}` deleted succesfully! {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = f"Snippet was not deleted. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):

        if message.author.bot:
            return
        presnippet_name = message.content.lower()
        snippet_name = "".join(presnippet_name.split(";", 1))

        snippet: Snippet = await Snippet.find_one({'_id': snippet_name})
        if snippet is None:
            return

        owner = self.bot.get_user(snippet.owner_id)
        snippet.uses_count += 1
        await snippet.commit()

        if message.content.lower().startswith(f";{snippet_name}"):
            em = disnake.Embed(color=disnake.Color.red())
            em.set_image(url=snippet.content)
            em.set_footer(text=f"Credits: {owner}", icon_url=owner.display_avatar)
            await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != 374622847672254466:
            async for snippet in Snippet.find({'owner_id': member.id}):
                await snippet.delete()

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send("You must be at least `level 55+` in order to use this command! %s" % (ctx.author.mention))
        else:
            if hasattr(ctx.command, 'on_error'):
                return
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Snippets(bot))
