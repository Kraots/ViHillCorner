from typing import Dict
from random import choice

import disnake
from disnake import RawReactionActionEvent, RawMessageDeleteEvent, Embed
from disnake.ui import View, Button
from disnake.ext import commands

from utils.context import Context
from utils.colors import Colours
from utils.paginator import SimplePages
from utils.formats import plural
from utils.databases import Starboard, StarboardStats, StarboardStatus

from main import ViHillCorner

STAR_CHANNEL = 902536749073432576
STAR_EMOJI = '\N{WHITE MEDIUM STAR}'


class StarBoard(commands.Cog):
    """Commands related to the starboard."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = '!'
        self._message_cache: Dict[int, disnake.Message] = {}

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return STAR_EMOJI

    async def increment_user(self, user_id: int, data: dict):
        user = await StarboardStats.find_one({'_id': user_id})
        if user is None:
            user: StarboardStats = StarboardStats(
                id=user_id,
                messages_starred=0,
                stars_received=0,
                stars_given=0
            )
            await user.commit()
        user.update(data)
        await user.commit()

    async def get_message(self, channel, message_id):
        try:
            return self._message_cache[message_id]
        except KeyError:
            message = await channel.fetch_message(message_id)
            self._message_cache[message_id] = message

            return message

    def star_emoji(self, stars):
        if 5 > stars >= 0:
            return '\N{WHITE MEDIUM STAR}'
        elif 10 > stars >= 5:
            return '\N{GLOWING STAR}'
        elif 25 > stars >= 10:
            return '\N{DIZZY SYMBOL}'
        else:
            return '\N{SPARKLES}'

    def is_url_spoiler(self, text, url):
        spoilers = self.spoilers.findall(text)
        for spoiler in spoilers:
            if url in spoiler:
                return True
        return False

    def get_star_message(self, message: disnake.Message, stars):
        emoji = self.star_emoji(stars)

        if stars > 1:
            content = f'{emoji} **{stars}** {message.channel.mention} ID: {message.id}'
        else:
            content = f'{emoji} {message.channel.mention} ID: {message.id}'

        embed = Embed(description=message.content, color=Colours.yellow)
        if message.embeds:
            data = message.embeds[0]
            if data.type == 'image' and not self.is_url_spoiler(message.content, data.url):
                embed.set_image(url=data.url)

        if message.attachments:
            file = message.attachments[0]
            spoiler = file.is_spoiler()
            if not spoiler and file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                embed.set_image(url=file.url)
            elif spoiler:
                embed.add_field(name='Attachment', value=f'||[{file.filename}]({file.url})||', inline=False)
            else:
                embed.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)

        ref = message.reference
        if ref and isinstance(ref.resolved, disnake.Message):
            embed.add_field(name='Replying to...', value=f'[{ref.resolved.author}]({ref.resolved.jump_url})', inline=False)

        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.timestamp = message.created_at
        view = View()
        button = Button(label='Go to original message', url=message.jump_url)
        view.add_item(button)
        return content, embed, view

    async def star_action(self, action, payload: RawReactionActionEvent):
        if str(payload.emoji) != STAR_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        channel = guild.get_channel_or_thread(payload.channel_id)
        if not isinstance(channel, (disnake.Thread, disnake.TextChannel)):
            return

        if channel.id == STAR_CHANNEL:
            return

        message = await self.get_message(channel, payload.message_id)
        if message.author.id == payload.user_id:
            return

        if action == 'star':
            star: Starboard = await Starboard.find_one({'_id': payload.message_id})
            if star is None:
                star_channel = guild.get_channel(STAR_CHANNEL)

                data = self.get_star_message(message, 1)
                msg = await star_channel.send(data[0], embed=data[1], view=data[2])
                star = Starboard(
                    id=payload.message_id,
                    author_id=message.author.id,
                    starrer_id=payload.user_id,
                    starrers=[payload.user_id],
                    channel_id=channel.id,
                    star_message_id=msg.id,
                    stars_count=1
                )
                await self.increment_user(payload.user_id, {'stars_given': 1})
                await self.increment_user(message.author.id, {'stars_received': 1})
                return

            star.stars_count += 1
            star.starrers += [payload.user_id]
            await star.commit()
            data = self.get_star_message(message, star.stars_count)
            ch = guild.get_channel(STAR_CHANNEL)
            msg = await self.get_message(ch, star.star_message_id)
            await msg.edit(content=data[0])
            await self.increment_user(payload.user_id, {'stars_given': 1})
            await self.increment_user(message.author.id, {'stars_received': 1})

        else:
            star: Starboard = await Starboard.find_one({'_id': payload.message_id})
            ch = guild.get_channel(STAR_CHANNEL)
            msg = await self.get_message(ch, star.star_message_id)
            star.stars_count -= 1
            await self.increment_user(payload.user_id, {'stars_given': -1})
            await self.increment_user(message.author.id, {'stars_received': -1})
            if star.stars_count == 0:
                await star.delete()
                await msg.delete()
                return
            star.starrers.pop(star.starrers.index(payload.user_id))
            await star.commit()
            data = self.get_star_message(message, star.stars_count)
            await msg.edit(content=data[0])

    async def is_locked(self) -> bool:
        data: StarboardStatus = await StarboardStatus.find_one({'_id': 1})
        return data.locked

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if not await self.is_locked():
            await self.star_action('star', payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if not await self.is_locked():
            await self.star_action('unstar', payload)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent):
        if not await self.is_locked():
            data: Starboard = await Starboard.find_one({'_id': payload.message_id})
            if data:
                ch = self.bot.get_channel(STAR_CHANNEL)
                message = await ch.fetch_message(data.star_message_id)
                await data.delete()
                await message.delete()

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def star(self, ctx: Context):
        """Base command for all `!star` commands"""

        await ctx.send_help('star')

    @star.command(name='show')
    async def star_show(self, ctx: Context, message: str):
        """Shows a starred message via its ID."""

        try:
            message = int(message, base=10)
        except ValueError:
            return await ctx.send(f'**{message}** is not a valid message ID. Use Developer Mode to get the Copy ID option.')

        data: Starboard = await Starboard.find_one({'_id': message})
        if data is None:
            return await ctx.send('Message not found.')

        if data.channel_id not in (ch.id for ch in ctx.guild.text_channels):
            return await ctx.send('The message\'s channel has been deleted.')

        channel = ctx.guild.get_channel_or_thread(data.channel_id)
        try:
            msg = await self.get_message(channel, data.id)
        except disnake.NotFound:
            await data.delete()
            return await ctx.send('The message has been deleted.')

        content, embed, view = self.get_star_message(msg, data.stars_count)
        await ctx.send(content, embed=embed, view=view)

    @star.command(name='who')
    async def star_who(self, ctx: Context, message: str):
        """Show who starred a message."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061, 787359417674498088):
            return

        try:
            message = int(message, base=10)
        except ValueError:
            return await ctx.send(f'**{message}** is not a valid message ID. Use Developer Mode to get the Copy ID option.')

        data: Starboard = await Starboard.find_one({'_id': message})
        if data is None:
            return await ctx.send('No one starred this message or this is an invalid message ID.')

        starrers = [starrer for starrer in data.starrers]
        members = [str(ctx.guild.get_member(mem)) for mem in starrers]

        p = SimplePages(entries=members, per_page=10, ctx=ctx)
        base = format(plural(len(starrers)), 'star')
        if len(starrers) > len(members):
            p.embed.title = f'{base} ({len(starrers) - len(members)} left server)'
        else:
            p.embed.title = base

        await p.start()

    async def star_guild_stats(self, ctx: Context):
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        em = Embed()
        em.timestamp = (ctx.guild.get_channel(STAR_CHANNEL)).created_at
        em.set_footer(text='Adding stars since')

        total_messages = await Starboard.count_documents({})

        all_starred_posts: list[Starboard] = await Starboard.find().sort('stars_count', -1).to_list(100000000000)
        starred_posts = []
        total_stars = 0
        for star in all_starred_posts:
            total_stars += star.stars_count
            if len(starred_posts) != 3:
                starred_posts.append(f"{top_3_emojis[len(starred_posts) + 1]}: {star.id} ({plural(star.stars_count):star})")

        em.description = f'{plural(total_messages):message} starred with a total of {total_stars} stars.'
        em.color = Colours.yellow

        star_receivers: list[StarboardStats] = await StarboardStats.find().sort('stars_received', -1).to_list(3)
        star_givers: list[StarboardStats] = await StarboardStats.find().sort('stars_given', -1).to_list(3)

        total_star_receivers = []
        for rec in star_receivers:
            usr = ctx.guild.get_member(rec.id)
            total_star_receivers.append(f"{top_3_emojis[len(total_star_receivers) + 1]}: {usr.mention} ({plural(rec.stars_received):star})")

        total_star_givers = []
        for giv in star_givers:
            usr = ctx.guild.get_member(giv.id)
            total_star_givers.append(f"{top_3_emojis[len(total_star_givers) + 1]}: {usr.mention} ({plural(giv.stars_given):star})")

        em.add_field(name='Top Starred Posts', value='\n'.join(starred_posts), inline=False)
        em.add_field(name='Top Star Receivers', value='\n'.join(total_star_receivers), inline=False)
        em.add_field(name='Top Star Givers', value='\n'.join(total_star_givers), inline=False)

        await ctx.send(embed=em)

    async def star_member_stats(self, ctx: Context, member: disnake.Member):
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        em = Embed(color=Colours.yellow)
        em.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        messages_starred = 0
        stars_received = 0
        stars_given = 0
        top_starred_posts = 'None!'

        data: StarboardStats = await StarboardStats.find_one({'_id': member.id})
        if data:
            messages_starred = data.messages_starred
            stars_received = data.stars_received
            stars_given = data.stars_given

            starred_posts: list[Starboard] = await Starboard.find({'author_id': member.id}).sort('stars_count', -1).to_list(3)
            if len(starred_posts) != 0:
                top_starred_posts = []
                for post in starred_posts:
                    top_starred_posts.append(f"{top_3_emojis[len(top_starred_posts) + 1]}: {post.id} ({plural(post.stars_count):star})")
                top_starred_posts = '\n'.join(top_starred_posts)

        em.add_field(name='Messages Starred', value=messages_starred)
        em.add_field(name='Stars Received', value=stars_received)
        em.add_field(name='Stars Given', value=stars_given)
        em.add_field(name='Top Starred Posts', value=top_starred_posts)

        await ctx.send(embed=em)

    @star.command(name='stats')
    async def star_stats(self, ctx: Context, *, member: disnake.Member = None):
        """Shows stats of the starboard usage of the server or of a member."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061, 787359417674498088):
            return

        if member is None:
            await self.star_guild_stats(ctx)
        else:
            await self.star_member_stats(ctx, member)

    @star.command(name='random')
    async def star_random(self, ctx: Context):
        """Sends a random starred message from the starboard."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061, 787359417674498088):
            return

        data = await Starboard.find().to_list(100000000000)
        data = choice(data)

        await self.star_show(ctx, str(data.id))

    @star.command(name='lock')
    @commands.is_owner()
    async def star_lock(self, ctx: Context):
        """
        Locks the starboard.

        This means that all listeners will stop, no stars will be added nor removed anymore until unlocked.
        """

        status: StarboardStatus = await StarboardStatus.find_one({'_id': 1})
        status.locked = True
        await status.commit()
        await ctx.send(f'{ctx.disagree} Starboard is now locked.')

    @star.command(name='unlock')
    @commands.is_owner()
    async def star_unlock(self, ctx: Context):
        """
        Unlocks the starboard.

        This means that all listeners will be activate again.
        """

        status: StarboardStatus = await StarboardStatus.find_one({'_id': 1})
        status.locked = False
        await status.commit()
        await ctx.send(f'{ctx.agree} Starboard is now unlocked.')


def setup(bot):
    bot.add_cog(StarBoard(bot))
