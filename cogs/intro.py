import asyncio

import disnake
from disnake.ext import commands

from utils.helpers import time_phaser
from utils.context import Context

from main import ViHillCorner


class IntroButton(disnake.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(disnake.ui.Button(label='View on website', url=url))


class Intros(commands.Cog):
    """Intro related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.base('Intros')
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '🙌'

    @commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra=False)
    @commands.cooldown(1, 360, commands.BucketType.user)
    async def intro(self, ctx: Context):
        """Create a new intro if you don't have one or edit an existing one."""

        if ctx.channel.id not in self.bot.ignored_channels:
            return ctx.command.reset_cooldown(ctx)

        results = self.db.get(str(ctx.author.id))

        await ctx.message.delete()

        channel = ctx.message.channel
        usercheck = ctx.author.id

        guild = self.bot.get_guild(750160850077089853)

        introchannel = guild.get_channel(750160850593251449)

        def check(message):
            return message.author.id == usercheck and message.channel.id == channel.id

        if results is not None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send(f"You already have intro set, would you like to edit your intro? {ctx.author.mention}", view=view)
            await view.wait()
            if view.response is None:
                return ctx.command.reset_cooldown(ctx)

            elif view.response is False:
                e = f"Cancelled. {ctx.author.mention}"
                ctx.command.reset_cooldown(ctx)
                return await msg.edit(content=e, view=view)

            elif view.response is True:
                await msg.delete()
                try:
                    intro_id = results['intro_id']
                except KeyError:
                    pass

                await channel.send(f"What's your name? {ctx.author.mention}\n\n*To cancel type `!cancel`*")

                try:
                    name = await self.bot.wait_for('message', timeout=180, check=check)
                    if name.content.lower() == '!cancel':
                        await channel.send(f"Cancelled. {ctx.author.mention}")
                        ctx.command.reset_cooldown(ctx)
                        return

                except asyncio.TimeoutError:
                    await ctx.send(f"Ran out of time. {ctx.author.mention}")
                    ctx.command.reset_cooldown(ctx)
                    return

                else:
                    await channel.send(f"Where are you from? {ctx.author.mention}")

                    try:
                        location = await self.bot.wait_for('message', timeout=180, check=check)
                        if location.content.lower() == '!cancel':
                            await channel.send(f"Cancelled. {ctx.author.mention}")
                            ctx.command.reset_cooldown(ctx)
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(f"Ran out of time. {ctx.author.mention}")
                        ctx.command.reset_cooldown(ctx)
                        return

                    else:
                        await channel.send(f"How old are you? {ctx.author.mention}")

                        try:
                            while True:
                                age = await self.bot.wait_for('message', timeout=180, check=check)
                                if age.content.lower() == '!cancel':
                                    await channel.send(f"Cancelled. {ctx.author.mention}")
                                    ctx.command.reset_cooldown(ctx)
                                    return
                                try:
                                    agenumber = int(age.content)
                                    if agenumber >= 44 or agenumber <= 11:
                                        await channel.send("Please put your real age and not a fake age.")
                                    else:
                                        break
                                except ValueError:
                                    await channel.send("Must be number.")

                        except asyncio.TimeoutError:
                            await ctx.send(f"Ran out of time. {ctx.author.mention}")
                            ctx.command.reset_cooldown(ctx)
                            return

                        else:
                            await channel.send(f"What's your gender? {ctx.author.mention}")

                            try:
                                gender = await self.bot.wait_for('message', timeout=180, check=check)
                                if gender.content.lower() == '!cancel':
                                    await channel.send(f"Cancelled. {ctx.author.mention}")
                                    ctx.command.reset_cooldown(ctx)
                                    return

                            except asyncio.TimeoutError:
                                await ctx.send(f"Ran out of time. {ctx.author.mention}")
                                ctx.command.reset_cooldown(ctx)
                                return

                            else:
                                await channel.send(f"Relationship status? `single` | `taken` | `complicated` {ctx.author.mention}")

                                try:
                                    while True:
                                        prestatuss = await self.bot.wait_for('message', timeout=180, check=check)
                                        status = prestatuss.content.lower()
                                        if status == '!cancel':
                                            await channel.send(f"Cancelled. {ctx.author.mention}")
                                            ctx.command.reset_cooldown(ctx)
                                            return
                                        elif status in ('single', 'taken', 'complicated'):
                                            break
                                        else:
                                            await channel.send("Please only choose from `single` | `taken` | `complicated`")

                                except asyncio.TimeoutError:
                                    await ctx.send(f"Ran out of time. {ctx.author.mention}")
                                    ctx.command.reset_cooldown(ctx)
                                    return

                                else:
                                    await channel.send(f"What are u interested to? {ctx.author.mention}")

                                    try:
                                        interests = await self.bot.wait_for('message', timeout=360, check=check)
                                        if interests.content.lower() == '!cancel':
                                            await channel.send(f"Cancelled. {ctx.author.mention}")
                                            ctx.command.reset_cooldown(ctx)
                                            return

                                    except asyncio.TimeoutError:
                                        await ctx.send(f"Ran out of time. {ctx.author.mention}")
                                        ctx.command.reset_cooldown(ctx)
                                        return

                                    else:
                                        em = disnake.Embed(color=ctx.author.color)
                                        em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                                        em.set_thumbnail(url=ctx.author.display_avatar)
                                        em.add_field(name="Name", value=name.content, inline=True)
                                        em.add_field(name="Location", value=location.content, inline=True)
                                        em.add_field(name="Age", value=agenumber, inline=True)
                                        em.add_field(name="Gender", value=gender.content, inline=False)
                                        em.add_field(name="Relationship Status", value=status, inline=True)
                                        em.add_field(name="Interests", value=interests.content, inline=False)
                                        intro_message = await introchannel.send(embed=em)

                                        self.db.update(
                                            {
                                                "name": name.content,
                                                "location": location.content,
                                                "age": agenumber,
                                                "gender": gender.content,
                                                "status": status,
                                                "interests": interests.content,
                                                "intro_id": str(intro_message.id)
                                            }, str(ctx.author.id)
                                        )

                                        try:
                                            intro_message = await introchannel.fetch_message(intro_id)
                                            await intro_message.delete()
                                        except Exception:
                                            pass

                                        await ctx.send(
                                            f"Intro edited successfully. You can see in <#750160850593251449> {ctx.author.mention}\n",
                                            view=IntroButton(f"{self.bot.url}/intros/{str(ctx.author.id)}")
                                        )

                                        return

        else:

            await channel.send(f"What's your name? {ctx.author.mention}\n\n*To cancel type `!cancel`*")

            try:
                name = await self.bot.wait_for('message', timeout=180, check=check)
                if name.content.lower() == '!cancel':
                    await channel.send(f"Cancelled. {ctx.author.mention}")
                    ctx.command.reset_cooldown(ctx)
                    return

            except asyncio.TimeoutError:
                await ctx.send(f"Ran out of time. {ctx.author.mention}")
                ctx.command.reset_cooldown(ctx)
                return

            else:
                await channel.send(f"Where are you from? {ctx.author.mention}")

                try:
                    location = await self.bot.wait_for('message', timeout=180, check=check)
                    if location.content.lower() == '!cancel':
                        await channel.send(f"Cancelled. {ctx.author.mention}")
                        ctx.command.reset_cooldown(ctx)
                        return

                except asyncio.TimeoutError:
                    await ctx.send(f"Ran out of time. {ctx.author.mention}")
                    ctx.command.reset_cooldown(ctx)
                    return

                else:
                    await channel.send(f"How old are you? {ctx.author.mention}")

                    try:
                        while True:
                            age = await self.bot.wait_for('message', timeout=180, check=check)
                            if age.content.lower() == '!cancel':
                                await channel.send(f"Cancelled. {ctx.author.mention}")
                                ctx.command.reset_cooldown(ctx)
                                return
                            try:
                                agenumber = int(age.content)
                                if agenumber >= 44 or agenumber <= 11:
                                    await channel.send("Please put your real age and not a fake age.")
                                else:
                                    break
                            except ValueError:
                                await channel.send("Must be number.")

                    except asyncio.TimeoutError:
                        await ctx.send(f"Ran out of time. {ctx.author.mention}")
                        ctx.command.reset_cooldown(ctx)
                        return

                    else:
                        await channel.send(f"What's your gender? {ctx.author.mention}")

                        try:
                            gender = await self.bot.wait_for('message', timeout=180, check=check)
                            if gender.content.lower() == '!cancel':
                                await channel.send(f"Cancelled. {ctx.author.mention}")
                                ctx.command.reset_cooldown(ctx)
                                return

                        except asyncio.TimeoutError:
                            await ctx.send(f"Ran out of time. {ctx.author.mention}")
                            ctx.command.reset_cooldown(ctx)
                            return

                        else:
                            await channel.send(f"Relationship status? `single` | `taken` | `complicated` {ctx.author.mention}")

                            try:
                                while True:
                                    prestatuss = await self.bot.wait_for('message', timeout=180, check=check)
                                    status = prestatuss.content.lower()
                                    if status == '!cancel':
                                        await channel.send(f"Cancelled. {ctx.author.mention}")
                                        ctx.command.reset_cooldown(ctx)
                                        return
                                    elif status in ('single', 'taken', 'complicated'):
                                        break
                                    else:
                                        await channel.send("Please only choose from `single` | `taken` | `complicated`")

                            except asyncio.TimeoutError:
                                await ctx.send(f"Ran out of time. {ctx.author.mention}")
                                ctx.command.reset_cooldown(ctx)
                                return

                            else:
                                await channel.send(f"What are u interested to? {ctx.author.mention}")

                                try:
                                    interests = await self.bot.wait_for('message', timeout=360, check=check)
                                    if interests.content.lower() == '!cancel':
                                        await channel.send(f"Cancelled. {ctx.author.mention}")
                                        ctx.command.reset_cooldown(ctx)
                                        return

                                except asyncio.TimeoutError:
                                    await ctx.send(f"Ran out of time. {ctx.author.mention}")
                                    ctx.command.reset_cooldown(ctx)
                                    return

                                else:
                                    em = disnake.Embed(color=ctx.author.color)
                                    em = disnake.Embed(color=ctx.author.color)
                                    em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
                                    em.set_thumbnail(url=ctx.author.display_avatar)
                                    em.add_field(name="Name", value=name.content, inline=True)
                                    em.add_field(name="Location", value=location.content, inline=True)
                                    em.add_field(name="Age", value=agenumber, inline=True)
                                    em.add_field(name="Gender", value=gender.content, inline=False)
                                    em.add_field(name="Relationship Status", value=status, inline=True)
                                    em.add_field(name="Interests", value=interests.content, inline=False)
                                    intro_msg = await introchannel.send(embed=em)
                                    await ctx.send(
                                        f"Intro added successfully. You can see in <#750160850593251449> {ctx.author.mention}\n",
                                        view=IntroButton(f"{self.bot.url}/intros/{str(ctx.author.id)}")
                                    )

                                    post = {
                                        "name": name.content,
                                        "location": location.content,
                                        "age": agenumber,
                                        "gender": gender.content,
                                        "status": status,
                                        "interests": interests.content,
                                        "intro_id": str(intro_msg.id)
                                    }

                                    self.db.insert(post, str(ctx.author.id))

                                    return

    @intro.command(name='delete', aliases=["remove"])
    async def intro_delete(self, ctx: Context):
        """
        Delete your intro.
        This will also delete your intro message in the intros channel.
        """

        results = self.db.get(str(ctx.author.id))

        if results is not None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send(f"Are you sure you want to delete your intro? {ctx.author.mention}", view=view)
            await view.wait()
            if view.response is None:
                return ctx.command.reset_cooldown(ctx)

            elif view.response is True:
                self.db.delete(str(ctx.author.id))
                try:
                    guild = self.bot.get_guild(750160850077089853)
                    intro_id = int(results['intro_id'])
                    channel = guild.get_channel(750160850593251449)
                    intro_message = await channel.fetch_message(intro_id)
                    await intro_message.delete()
                except Exception as e:
                    print(results['intro_id'])
                    print(e)
                e = f"Intro deleted. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = f"Intro has not been deleted. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

        else:
            await ctx.send("You do not have an intro!")
            return

    @commands.command(aliases=['wi'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def whois(self, ctx: Context, member: disnake.Member = None):
        """Check the member's intro if they have one."""

        member = member or ctx.author

        results = self.db.get(str(member.id))

        user = member

        if results is not None:
            intro_name = results['name']
            intro_location = results['location']
            intro_age = results['age']
            intro_gender = results['gender']
            relationship_status = results['status']
            intro_interests = results['interests']

            await ctx.message.delete()
            em = disnake.Embed(color=member.color)
            em.set_author(name=member, icon_url=member.display_avatar)
            em.set_thumbnail(url=member.display_avatar)
            em.add_field(name="Name", value=intro_name, inline=True)
            em.add_field(name="Location", value=intro_location, inline=True)
            em.add_field(name="Age", value=intro_age, inline=True)
            em.add_field(name="Gender", value=intro_gender, inline=False)
            em.add_field(name="Relationship Status", value=relationship_status, inline=True)
            em.add_field(name="Interests", value=intro_interests, inline=False)
            await ctx.send(embed=em, view=IntroButton(f"{self.bot.url}/intros/{str(member.id)}"))

        else:
            if ctx.author.id == user.id:
                await ctx.send("You do not have an intro!")
                ctx.command.reset_cooldown(ctx)
                return

            else:
                await ctx.send("User does not have an intro!")
                ctx.command.reset_cooldown(ctx)
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == 938097236024360960:
            return
        self.db.delete(str(member.id))

    @whois.error
    async def wi_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Please wait {time_phaser(error.retry_after)}.'
            await ctx.send(msg)
        else:
            await self.bot.reraise(ctx, error)

    @intro.error
    async def intro_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            ctx.command.reset_cooldown(ctx)
            await self.bot.reraise(ctx, error)

        elif isinstance(error, commands.CommandOnCooldown):
            msg = f'Please wait {time_phaser(error.retry_after)}.'
            await ctx.send(msg)

        elif isinstance(error, commands.TooManyArguments):
            ctx.command.reset_cooldown(ctx)
        else:
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Intros(bot))
