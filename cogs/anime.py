from typing import List
import textwrap

import disnake
from disnake.ext import commands

from mal import Anime as AnimeSearchId
from mal import AnimeSearch

from utils.colors import Colours
from utils.context import Context
from utils.paginator import CustomMenu
from utils.databases import Alist

from main import ViHillCorner


class AlistPageEntry:
    def __init__(self, entry):

        self.name = entry

    def __str__(self):
        return f'\u2800{self.name.title()}'


class AlistPages(CustomMenu):
    def __init__(self, ctx: Context, entries: List, *, per_page: int = 12, title: str = "", color=None):
        converted = [AlistPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page, color=color, title=title)


class Anime(commands.Cog):
    """Anime related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = '!'

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='YellowHeartLove', id=787370201297453087)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def alist(self, ctx: Context, member: disnake.Member = None):
        """See the member's anime list."""

        member = member or ctx.author

        data: Alist = await Alist.find_one({'_id': member.id})

        if data and data.alist:
            p = AlistPages(ctx=ctx, entries=data.alist, per_page=10, title=f"Here's `{member.display_name}`'s anime list:", color=Colours.reds)
            await p.start()

        else:
            if ctx.author.id == member.id:
                await ctx.send("You do not have an anime list! Type: `!alist set <recommendations>` to set your anime list!")
                return

            else:
                await ctx.send("User does not have an anime list!")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def mlist(self, ctx: Context, member: disnake.Member = None):
        """See the member's manga list."""

        member = member or ctx.author

        data: Alist = await Alist.find_one({'_id': member.id})

        if data and data.mlist:
            p = AlistPages(ctx=ctx, entries=data.mlist, per_page=10, title=f"Here's `{member.display_name}`'s manga list:", color=Colours.reds)
            await p.start()

        else:
            if ctx.author.id == member.id:
                await ctx.send("You do not have a manga list! Type: `!mlist set <recommendations>` to set your manga list!")
                return

            else:
                await ctx.send("User does not have a manga list!")

    @alist.command(name='set')
    async def alist_set(self, ctx: Context, *, animes: str):
        """Set your anime list."""

        args = animes
        data: Alist = await Alist.find_one({'_id': ctx.author.id})
        alist = list(filter(bool, args.splitlines()))
        if not data:
            await Alist(
                id=ctx.author.id,
                alist=alist
            ).commit()
        else:
            data.alist = alist
            await data.commit()
        await ctx.message.delete()
        await ctx.send(f"Anime list set! {ctx.author.mention}")

    @mlist.command(name='set')
    async def mlist_set(self, ctx: Context, *, mangas: str):
        """Set your manga list."""

        args = mangas
        data: Alist = await Alist.find_one({'_id': ctx.author.id})
        mlist = list(filter(bool, args.splitlines()))
        if not data:
            await Alist(
                id=ctx.author.id,
                mlist=mlist
            ).commit()
        else:
            data.mlist = mlist
            await data.commit()
        await ctx.message.delete()
        await ctx.send(f"Manga list set! {ctx.author.mention}")

    @alist.command(name='add')
    async def alist_add(self, ctx: Context, *, anime: str):
        """Add to your anime list."""

        args = anime
        data: Alist = await Alist.find_one({'_id': ctx.author.id})
        alist = list(filter(bool, args.splitlines()))
        if not data:
            await Alist(
                id=ctx.author.id,
                alist=alist
            ).commit()
        else:
            data.alist += alist
            await data.commit()
        await ctx.message.delete()
        await ctx.send(f"Succesfully added to your anime list! {ctx.author.mention}")

    @mlist.command(name='add')
    async def mlist_add(self, ctx: Context, *, manga: str):
        """Add to your manga list."""

        args = manga
        data: Alist = await Alist.find_one({'_id': ctx.author.id})
        mlist = list(filter(bool, args.splitlines()))
        if not data:
            await Alist(
                id=ctx.author.id,
                mlist=mlist
            ).commit()
        else:
            data.mlist += mlist
            await data.commit()
        await ctx.message.delete()
        await ctx.send(f"Succesfully added to your manga list! {ctx.author.mention}")

    @alist.command(name='delete')
    async def alist_delete(self, ctx: Context, index: str):
        """Delete the recommendation at the given index."""

        try:
            nr = int(index)
        except ValueError:
            return await ctx.send("Must be a number. %s" % (ctx.author.mention))
        data: Alist = await Alist.find_one({'_id': ctx.author.id})
        if (
            (not data) or
            (not data.alist)
        ):
            return await ctx.send("You do not have an anime list. %s" % (ctx.author.mention))
        n = nr - 1

        try:
            rec = data.alist.pop(n)
        except IndexError:
            return await ctx.send(f"No recommendation with that number found. {ctx.author.mention}")

        await data.commit()
        await ctx.send(f"Successfully removed **{rec}** from your anime list. {ctx.author.mention}")

    @mlist.command(name='delete')
    async def mlist_delete(self, ctx: Context, index: str):
        """Delete the recommendation at the given index."""

        try:
            nr = int(index)
        except ValueError:
            return await ctx.send("Must be a number. %s" % (ctx.author.mention))
        data: Alist = await Alist.find_one({'_id': ctx.author.id})
        if (
            (not data) or
            (not data.mlist)
        ):
            return await ctx.send("You do not have a manga list. %s" % (ctx.author.mention))
        n = nr - 1

        try:
            rec = data.mlist.pop(n)
        except IndexError:
            return await ctx.send(f"No recommendation with that number found. {ctx.author.mention}")

        await data.commit()
        await ctx.send(f"Successfully removed **{rec}** from your manga list. {ctx.author.mention}")

    @alist.command(name='clear')
    async def alist_clear(self, ctx: Context):
        """Delete your whole anime list."""

        data: Alist = await Alist.find_one({'_id': ctx.author.id})

        if data and data.alist:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to delete your anime list? %s" % (ctx.author.mention), view=view)
            await view.wait()
            if view.response is True:
                await data.delete()
                e = "Succesfully deleted your anime list! %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = "Your anime list has not been deleted. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)

        else:
            await ctx.send("You do not have an anime list! Type: `!alist set <recommendations>` to set your anime list!")

    @mlist.command(name='clear')
    async def mlist_clear(self, ctx: Context):
        """Delete your whole manga list."""

        data: Alist = await Alist.find_one({'_id': ctx.author.id})

        if data and data.mlist:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send("Are you sure you want to delete your manga list? %s" % (ctx.author.mention), view=view)
            await view.wait()
            if view.response is True:
                await data.delete()
                e = "Succesfully deleted your manga list! %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = "Your manga list has not been deleted. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)

        else:
            await ctx.send("You do not have an manga list! Type: `!mlist set <recommendations>` to set your manga list!")

    @alist.command(name='remove')
    @commands.is_owner()
    async def alist_remove(self, ctx: Context, member: disnake.Member):
        """Remove the member from the database."""

        data: Alist = await Alist.find_one({"_id": member.id})

        if data:
            await data.delete()
            await ctx.send("Succesfully removed `{}` from the database.".format(member.display_name))

        else:
            await ctx.send("User not in the database!")

    @mlist.command(name='remove')
    @commands.is_owner()
    async def mlist_remove(self, ctx: Context, member: disnake.Member):
        """Remove the member from the database."""

        data: Alist = await Alist.find_one({"_id": member.id})

        if data:
            await data.delete()
            await ctx.send("Succesfully removed `{}` from the database.".format(member.display_name))

        else:
            await ctx.send("User not in the database!")

    def search_anime(self, query):
        anime = AnimeSearch(query)
        return anime.results[0]

    def search_anime_id(self, query):
        return AnimeSearchId(query)

    @commands.command(name='myanimelist', aliases=['mal', 'anime'])
    async def anime_mal(self, ctx: Context, *, query):
        """Search an anime and get an embed with it's info based on its name, it can also accept the anime's id from MyAnimeList."""

        try:
            query = int(query)
        except ValueError:
            query = str(query)
        if isinstance(query, str):
            anime_ = await self.bot.loop.run_in_executor(None, self.search_anime, query)
            anime: AnimeSearchId = await self.bot.loop.run_in_executor(None, self.search_anime_id, anime_.mal_id)
        elif isinstance(query, int):
            anime: AnimeSearchId = await self.bot.loop.run_in_executor(None, self.search_anime_id, query)
        else:
            return await ctx.reply('Not a valid query!')

        shortened = textwrap.shorten(text=anime.synopsis.replace("[Written by MAL Rewrite]", ""), width=700, placeholder=f" [[...]]({anime.url})")
        em = disnake.Embed(
            title=anime.title,
            url=anime.url,
            description=f'**Synopsis:** *{shortened}*'
        )
        em.set_thumbnail(url=anime.image_url)
        em.add_field(name='Episodes:', value=anime.episodes)
        em.add_field(name='Genres:', value=', '.join(anime.genres) if len(anime.genres) != 0 else 'Not Specified')
        em.add_field(name='Duration:', value=anime.duration)
        em.add_field(name='Status:', value=anime.status)
        em.add_field(name='Aired:', value=anime.aired)
        em.add_field(name='Premiered:', value=anime.premiered)
        em.add_field(name='Broadcast:', value=anime.broadcast)
        em.add_field(name='Score:', value=f'{anime.score} (by {anime.scored_by:,} users)')
        em.add_field(name='Rank:', value=f'#{anime.rank}')
        em.add_field(name='Popularity:', value=f'#{anime.popularity}')
        em.add_field(name='Studios:', value=', '.join(anime.studios) if len(anime.studios) != 0 else 'Not Specified')
        em.add_field(name='Rating:', value=anime.rating)
        em.add_field(name='Favorites:', value=f'{anime.favorites:,}')
        em.add_field(name='Producers:', value=', '.join(anime.producers) if len(anime.producers) != 0 else 'Not Specified')
        em.add_field(name='Source:', value=anime.source)
        em.set_footer(text=f'Requested by: {ctx.author} • ID: {anime.mal_id}', icon_url=ctx.author.display_avatar)

        ref = ctx.replied_reference
        if ref is None:
            ref = ctx.message

        await ctx.send(embed=em, reference=ref)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != 374622847672254466:
            usr: Alist = await Alist.find_one({"_id": member.id})
            if usr:
                await usr.delete()


def setup(bot):
    bot.add_cog(Anime(bot))
