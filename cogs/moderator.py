from typing import List
import re
import asyncio
import datetime
from dateutil.relativedelta import relativedelta

import disnake
from disnake.ext import commands, tasks

from utils import time
from utils.colors import Colours
from utils.context import Context
from utils.helpers import time_phaser
from utils.paginator import CustomMenu, SimplePages

from main import ViHillCorner

NUMBER_EMOJIS = (
    '1️⃣', '2️⃣', '3️⃣',
    '4️⃣', '5️⃣', '6️⃣',
    '7️⃣', '8️⃣',
)


class MutePageEntry:
    def __init__(self, entry):

        self.name = entry['username']
        self.time_left = entry['time_left']

    def __str__(self):
        return f'**{self.name}** (`{self.time_left}`)'


class MutePages(CustomMenu):
    def __init__(self, ctx: Context, entries, *, per_page=12, title="", color=None):
        converted = [MutePageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page, color=color, title=title)


time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx: Context, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


class NumberedButtons(disnake.ui.Button):
    def __init__(self, emoji: str, db, *, custom_id: str, bot: ViHillCorner, label: str = '0'):
        super().__init__(label=label, emoji=emoji, custom_id=custom_id)
        self.db = db
        self.bot = bot

    async def callback(self, inter: disnake.MessageInteraction):
        data = await self.db.find_one({'_id': inter.message.id})
        if data is not None:
            voted_users = data.get('voted_users')

            if voted_users is not None:
                if inter.author.id in voted_users:
                    return await inter.response.send_message('You already voted for this poll!', ephemeral=True)

            to_update = voted_users + [inter.author.id] if voted_users is not None else [inter.author.id]
            await self.db.update_one({'_id': inter.message.id}, {'$set': {'voted_users': to_update}})
            index = str(NUMBER_EMOJIS.index(str(self.emoji)) + 1)
            info = data[index]
            info[0] += 1
            new_label = info[0]
            await self.db.update_one({'_id': inter.message.id}, {'$set': {index: info}})

            for child in self.view.children:
                if child.emoji == self.emoji:
                    child.label = str(new_label)

            self.bot.poll_views[inter.message.id] = self.view
            await inter.message.edit(view=self.view)
            await inter.response.send_message(f'You voted for option: ({self.emoji}) `{info[1]}`', ephemeral=True)
            v = disnake.ui.View()
            v.add_item(disnake.ui.Button(label='Jump!', url=inter.message.jump_url))
            await self.bot._owner.send(f'`{inter.author}` voted for: **{self.emoji}**', view=v)
        else:
            await inter.response.send_message('This poll is over!', ephemeral=True)


class PollInteractiveMenu(disnake.ui.View):
    def __init__(self, ctx: Context, channel: disnake.TextChannel, duration: int, question: str):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.channel = channel
        self.duration = duration
        self.db = ctx.bot.db1['Poll']
        self.question = question
        self.adding_option = False
        self.options = []

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        if inter.author.id != self.ctx.author.id:
            await inter.response.send_message(f'Only `{self.ctx.author.display_name}` can use this poll menu!', ephemeral=True)
            return False
        return True

    @disnake.ui.button(label='Add Option', style=disnake.ButtonStyle.blurple)
    async def add_option_button(self, button: disnake.Button, inter: disnake.MessageInteraction):
        if self.adding_option:
            return await inter.response.send_message('You are already adding an option!', ephemeral=True)
        if len(self.options) == 8:
            return await inter.response.send_message('There already are a total of 8 options. No more can be added.', ephemeral=True)

        await inter.response.defer()
        self.adding_option = True
        while True:
            try:
                await self.ctx.send(f'Please send the option. (Total: `#{len(self.options) + 1}`)')
                msg = await self.ctx.bot.wait_for(
                    'message',
                    timeout=90.0,
                    check=lambda m: m.author.id == self.ctx.author.id and m.channel.id == self.ctx.channel.id
                )
                if self.is_finished():
                    return
            except asyncio.TimeoutError:
                pass
            else:
                if len(msg.content) >= 200:
                    await msg.delete()
                    await inter.followup.send('Content too large. Limit is of `200` characters.\nTry again.', ephemeral=True)
                else:
                    break

        self.adding_option = False
        self.options.append(msg.content)
        em = disnake.Embed(
            title='Creating the poll',
            description='\n'.join([f'{NUMBER_EMOJIS[index]} **->** {option}' for index, option in enumerate(self.options)]),
            color=disnake.Colour.blurple()
        )
        await self.message.edit(embed=em)

    @disnake.ui.button(label='Confirm', style=disnake.ButtonStyle.green)
    async def confirm_button(self, button: disnake.Button, inter: disnake.MessageInteraction):
        if len(self.options) == 0:
            return await inter.response.send_message('You didn\'t add any options yet! Add some options and confirm later.', ephemeral=True)
        await inter.response.defer()
        expire_date = datetime.datetime.utcnow() + relativedelta(seconds=self.duration)
        em = disnake.Embed(
            color=disnake.Color.green(),
            title='Expires: ' + disnake.utils.format_dt(expire_date, 'R'),
            description='\n'.join([f'{NUMBER_EMOJIS[index]} **->** {option}' for index, option in enumerate(self.options)])
        )
        em.set_author(name=f'Poll by: {self.ctx.author}', icon_url=self.ctx.author.display_avatar.url)
        em.set_footer(text='Once you voted you cannot remove your vote or vote again! Choose wisely.')
        em.add_field('Question', f'`{self.question}`')
        msg = await self.channel.send(embed=em)
        await msg.pin(reason='Poll started.')
        await self.channel.purge(limit=1)

        button_view = disnake.ui.View(timeout=self.duration)
        data = {
            '_id': msg.id,
            'expire_date': expire_date,
            'user_id': self.ctx.author.id,
            'question': self.question
        }
        for index, option in enumerate(self.options):
            data[str(index + 1)] = [0, option]
            button_view.add_item(NumberedButtons(
                NUMBER_EMOJIS[index],
                self.db,
                bot=self.ctx.bot,
                custom_id=f'vhc:poll:{index}'
            ))
        await self.db.insert_one(data)
        await msg.edit(view=button_view)
        self.ctx.bot.poll_views[msg.id] = button_view

        for child in self.children:
            child.disabled = True
            child.style = disnake.ButtonStyle.grey
        em = self.message.embeds[0]
        em.color = disnake.Colour.green()
        em.title = 'Poll created!'
        em.description = disnake.Embed.Empty
        v = disnake.ui.View()
        btn = disnake.ui.Button(label='Jump!', url=msg.jump_url)
        v.add_item(btn)
        await self.message.edit(embed=em, view=v)
        await self.message.reply('Poll successfully created.')
        self.stop()

    @disnake.ui.button(label='Cancel', style=disnake.ButtonStyle.red)
    async def cancel_button(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        for child in self.children:
            child.disabled = True
            child.style = disnake.ButtonStyle.grey
        em = self.message.embeds[0]
        em.color = disnake.Colour.red()
        em.title = 'Poll creation cancelled!'
        em.description = '\n'.join([f'{NUMBER_EMOJIS[index]} **->** {option}' for index, option in enumerate(self.options)])
        await self.message.edit(embed=em, view=self)
        await self.message.reply('Poll creation cancelled.')
        self.stop()


class DummyPollView(disnake.ui.View):
    def __init__(self, buttons: List[NumberedButtons]):
        super().__init__(timeout=None)
        for button in buttons:
            self.add_item(button)


class Moderator(commands.Cog):
    """Moderator related commands."""
    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db1 = bot.db1['Moderation Mutes']
        self.db2 = bot.db1['Filter Mutes']
        self.prefix = "!"
        self.check_current_mutes.start()
        self.check_polls.start()
        self.ignored_channels = (
            750645852237987891, 750160850303582236, 779388444304211991, 750160850303582237, 750160850593251449,
            797867811967467560, 752164200222163016, 783304066691235850, 770209436488171530, 779280794530086952,
            788377362739494943, 750160852380024895, 781777255885570049, 750432155179679815, 750160850593251454,
            902536749073432576, 902677227307679797,
        )

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '⚙️'

    @tasks.loop(seconds=30)
    async def check_current_mutes(self):
        currentTime = datetime.datetime.utcnow()
        results = await self.db1.find().to_list(100000)
        results2 = await self.db2.find().to_list(100000)
        for result in results:
            if result['mute_duration'] is not None:
                unmute_time = result['muted_at'] + relativedelta(seconds=result['mute_duration'])

                if currentTime >= unmute_time:
                    guild = self.bot.get_guild(result['guild_id'])
                    member = guild.get_member(result['_id'])
                    is_staff = result['staff']

                    if member is not None:
                        if is_staff is True:
                            staff = guild.get_role(754676705741766757)
                            mod = guild.get_role(750162714407600228)
                            new_roles = [role for role in member.roles if role.id != 750465726069997658] + [staff, mod]
                        else:
                            new_roles = [role for role in member.roles if role.id != 750465726069997658]

                        await member.edit(roles=new_roles, reason='Auto-Unmute because of mute time expiration.')
                        await member.send("You have been unmuted in `ViHill Corner`.")

                        await self.db1.delete_one({"_id": member.id})
                    else:
                        await self.db1.delete_one({"_id": result['_id']})

        for result2 in results2:
            if result2['mute_duration'] is not None:
                unmute_time = result2['muted_at'] + relativedelta(seconds=result2['mute_duration'])

                if currentTime >= unmute_time:
                    guild = self.bot.get_guild(result2['guild_id'])
                    member = guild.get_member(result2['_id'])
                    is_staff = result2['staff']

                    if member is not None:
                        if is_staff is True:
                            staff = guild.get_role(754676705741766757)
                            mod = guild.get_role(750162714407600228)
                            new_roles = [role for role in member.roles if role.id != 750465726069997658] + [staff, mod]
                        else:
                            new_roles = [role for role in member.roles if role.id != 750465726069997658]

                        await member.edit(roles=new_roles, reason='Auto-Unmute because of mute time expiration.')
                        await member.send("You have been unmuted in `ViHill Corner`.")

                        await self.db2.delete_one({"_id": member.id})
                    else:
                        await self.db2.delete_one({"_id": result2['_id']})

    @tasks.loop(seconds=5.0)
    async def check_polls(self):
        db = self.bot.db1['Poll']
        data = await db.find().sort('expire_date', 1).to_list(1)
        if len(data) != 0:
            for i in data:
                if datetime.datetime.utcnow() >= i['expire_date']:
                    await db.delete_one({'_id': i['_id']})
                    won = None
                    ignored = ('_id', 'expire_date', 'voted_users', 'user_id', 'question')
                    for k in i:
                        if k not in ignored:
                            if won is None:
                                won = [k, i[k][0], i[k][1]]
                            else:
                                if i[k][0] > won[1]:
                                    won = [k, i[k][0], i[k][1]]
                    em = disnake.Embed(title='Poll ended!', color=disnake.Colour.red())
                    em.add_field('Question', f'`{i["question"]}`', inline=False)
                    em.add_field('Winner', f'{NUMBER_EMOJIS[int(won[0]) - 1]} **->** {won[2]} (**`{won[1]} votes`**)', inline=False)

                    guild = self.bot.get_guild(750160850077089853)
                    channel = guild.get_channel(902677227307679797)
                    message = await channel.fetch_message(i['_id'])
                    user = await self.bot.fetch_user(i['user_id'])
                    em.set_author(name=f'Poll by: {user}', icon_url=user.display_avatar.url)
                    await channel.send(embed=em, reference=message)
                    em = message.embeds[0]
                    em.color = disnake.Color.red()
                    em.title = em.title.replace('Expires', 'Expired')
                    await message.edit(embed=em)
                    await message.unpin(reason='Poll expired.')
                    try:
                        view = self.bot.poll_views[message.id]
                        view.stop()
                        for btn in view.children:
                            btn.disabled = True
                        await message.edit(view=view)
                        del self.bot.poll_views[message.id]
                    except KeyError:
                        v = disnake.ui.View()
                        for comp in message.components:
                            for btn in comp.children:
                                btn = btn.to_dict()
                                del btn['type']
                                btn['disabled'] = True
                                btn['emoji'] = btn['emoji']['name']
                                button = disnake.ui.Button(**btn)
                                v.add_item(button)
                        await message.edit(view=v)

    @check_current_mutes.before_loop
    @check_polls.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self, 'added_views'):
            messages = await self.bot.db1['Poll'].find().to_list(100000000)
            if len(messages) != 0:
                ignored = ('_id', 'expire_date', 'voted_users', 'user_id', 'question')
                for message in messages:
                    buttons = []
                    for i, k in enumerate([key for key in message if key not in ignored]):
                        buttons.append(NumberedButtons(
                            emoji=NUMBER_EMOJIS[i],
                            db=self.bot.db1['Poll'],
                            custom_id=f'vhc:poll:{i}',
                            bot=self.bot,
                            label=str(message[k][0])
                        ))
                    view = DummyPollView(buttons)
                    self.bot.add_view(view, message_id=message['_id'])
                    self.bot.poll_views[message['_id']] = view
                self.added_views = True

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.has_role(754676705741766757)
    async def poll(self, ctx: Context, *, duration: TimeConverter):
        """Starts the interactive poll creation, the poll message is sent in <#902677227307679797>

        Example:
            !poll 5m
        """

        if duration:
            em = disnake.Embed(
                title='Creating the poll',
                description='No Options.',
                color=disnake.Colour.blurple()
            )
            while True:
                try:
                    await ctx.reply('What is the poll\'s question?')
                    msg = await self.bot.wait_for('message', timeout=180.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
                except asyncio.TimeoutError:
                    return await ctx.send(f'Ran out of time. {ctx.author.mention}')
                else:
                    if len(msg.content) >= 300:
                        await ctx.send('Question cannot have more than `300` characters.')
                    else:
                        question = msg.content
                        break
            guild = self.bot.get_guild(750160850077089853)
            channel = guild.get_channel(902677227307679797)
            view = PollInteractiveMenu(ctx, channel, duration, question)
            view.message = await ctx.send(embed=em, view=view)

    @poll.command(name='show')
    async def poll_show(self, ctx: Context):
        """Shows the current running polls, in expire order."""

        data = await self.bot.db1['Poll'].find().sort('expire_date', 1).to_list(1000000)
        if data is None:
            return await ctx.reply('No current running polls found!')

        channel_url = 'https://discord.com/channels/750160850077089853/902677227307679797/'
        entries = []
        for poll in data:
            usr = ctx.guild.get_member(poll['user_id'])
            url = channel_url + str(poll['_id'])
            entries.append(
                f"Poll id: **{poll['_id']}**\n"
                f"Poll by: `{usr}`\n"
                f"Expires: {disnake.utils.format_dt(poll['expire_date'], 'R')}\n"
                f"[Jump!]({url})\n"
            )
        pages = SimplePages(ctx, entries, per_page=5)
        await pages.start()

    @poll.command(name='cancel')
    @commands.has_role(754676705741766757)
    async def poll_cancel(self, ctx: Context, poll_id: int):
        """Cancels a poll based on its id.

        You can find the id by using `!poll show` and finding your poll
        or by getting the poll's message id.
        """

        poll = await self.bot.db1['Poll'].find_one({'_id': poll_id})
        if poll is None:
            return await ctx.reply(f'No poll with the id `{poll_id}` found.')
        elif poll['user_id'] != ctx.author.id and ctx.author.id != self.bot._owner_id:
            return await ctx.reply(
                'You did not create this poll!'
                f'Only `{ctx.guild.get_member(poll["user_id"])}` can cancel it.'
            )

        await self.bot.db1['Poll'].delete_one({'_id': poll_id})
        guild = self.bot.get_guild(750160850077089853)
        ch = guild.get_channel(902677227307679797)
        msg = await ch.fetch_message(poll['_id'])
        em = msg.embeds[0]
        em.title = 'This poll has been cancelled.'
        em.color = Colours.red
        v = self.bot.poll_views[msg.id]
        v.stop()
        await msg.edit(embed=em, view=v)
        await msg.unpin()

        view = disnake.ui.View()
        button = disnake.ui.Button(label='Poll Message', url=msg.jump_url)
        view.add_item(button)
        await ctx.reply('Successfully cancelled the poll.', view=view)

    @commands.command()
    @commands.has_role(754676705741766757)
    async def slowmode(self, ctx: Context, *, how_much: TimeConverter):
        """Set the slowmode time for the channel that you are using this command in."""

        guild = self.bot.get_guild(750160850077089853)
        log_channel = guild.get_channel(788377362739494943)
        await ctx.message.delete()

        if how_much:
            await ctx.channel.edit(slowmode_delay=how_much)
            await ctx.author.send(f'Set slowmode for <#{ctx.channel.id}> to {time_phaser(how_much)} !')

            em = disnake.Embed(color=Colours.reds, title="___SLOWMODE___", timestamp=ctx.message.created_at.replace(tzinfo=None))
            em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
            em.add_field(name="Action", value=f"`Set slowmode to {time_phaser(how_much)}`", inline=False)
            em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

            await log_channel.send(embed=em)
            return

        else:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.author.send(f'Disabled slowmode for <#{ctx.channel.id}> !')

            em = disnake.Embed(color=Colours.reds, title="___SLOWMODE___", timestamp=ctx.message.created_at.replace(tzinfo=None))
            em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
            em.add_field(name="Action", value="`Disabled slowmode`", inline=False)
            em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

            await log_channel.send(embed=em)

    @commands.command()
    @commands.has_role(754676705741766757)
    async def kick(self, ctx: Context, member: disnake.Member, *, reason: str = None):
        """Kicks the member with the specified reason, if any."""

        if reason is None:
            reason = "Reason not specified"

        guild = self.bot.get_guild(750160850077089853)
        staff = guild.get_role(754676705741766757)
        log_channel = guild.get_channel(788377362739494943)

        if staff in member.roles:
            return await ctx.reply("Cannot kick staff members.")

        try:
            await member.send("You have been kicked from `ViHill Corner!`")
        except disnake.HTTPException:
            pass

        await guild.kick(member, reason=f'{ctx.author}: "{reason}"')

        ban = disnake.Embed(description=f"`{member}` has been kicked.\n**Reason:** **[{reason}]({ctx.message.jump_url})**", color=disnake.Color.red())

        await ctx.send(embed=ban)

        em = disnake.Embed(color=Colours.reds, title="___KICK___", timestamp=ctx.message.created_at.replace(tzinfo=None))
        em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
        em.add_field(name="Action", value="`Used the kick command.`", inline=False)
        em.add_field(name="Member", value=f"`{member}`", inline=False)
        em.add_field(name="Reason", value=f"**[{reason}]({ctx.message.jump_url})**", inline=False)
        em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

        await log_channel.send(embed=em)

    @commands.command()
    @commands.has_role(754676705741766757)
    async def ban(self, ctx: Context, user: disnake.User, *, reason: str = None):
        """Bans the user with the specified reason, if any."""

        if reason is None:
            reason = "Reason not specified."

        guild = self.bot.get_guild(750160850077089853)
        log_channel = guild.get_channel(788377362739494943)

        try:
            member = guild.get_member(user.id)
            if 754676705741766757 in (role.id for role in member.roles):
                return await ctx.reply("Cannot perform this action against staff members.")
        except Exception:
            pass

        _reason = disnake.Embed(description="**Unban appeal server** \n https://discord.gg/5SratjPmGc")
        _reason.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
        msg = "You have been banned from `ViHill Corner`. If you think that this has been applied in error please submit a detailed appeal at the following link."  # noqa

        try:
            await user.send(msg, embed=_reason)
        except disnake.HTTPException:
            pass
        await guild.ban(user, reason=f'{ctx.author}: "{reason}"', delete_message_days=0)

        ban = disnake.Embed(description=f"`{user}` has been banned.\n**Reason:** **[{reason}]({ctx.message.jump_url})**", color=disnake.Color.red())

        await ctx.send(embed=ban)

        em = disnake.Embed(color=Colours.reds, title="___BAN___", timestamp=ctx.message.created_at.replace(tzinfo=None))
        em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
        em.add_field(name="Action", value="`Used the ban command.`", inline=False)
        em.add_field(name="Member", value=f"`{user}`", inline=False)
        em.add_field(name="Reason", value=f"**[{reason}]({ctx.message.jump_url})**", inline=False)
        em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

        await log_channel.send(embed=em)

    @commands.command()
    @commands.has_role(754676705741766757)
    async def unban(self, ctx: Context, member: disnake.User):
        """Unban's the user."""

        guild = self.bot.get_guild(750160850077089853)
        guild2 = self.bot.get_guild(788384492175884299)
        if ctx.channel.id == 788488359306592316:
            return await ctx.reply("This command cannot be performed in the staff chat. Please go in the chat where the member you wish to unban exists.")
        try:
            await guild.fetch_ban(member)
            await guild.unban(disnake.Object(id=member.id))
        except Exception:
            return await ctx.send("Failed. Did you input the correct member that is in the same guild?")

        unban = disnake.Embed(description=f"`{member}` has been unbanned from the server", color=disnake.Color.red())

        await ctx.send(embed=unban)

        log_channel = guild.get_channel(788377362739494943)

        em = disnake.Embed(color=Colours.reds, title="___UNBAN___", timestamp=ctx.message.created_at.replace(tzinfo=None))
        em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
        em.add_field(name="Action", value="`Used the unban command`", inline=False)
        em.add_field(name="Member", value=f"`{member}`", inline=False)
        em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

        await log_channel.send(embed=em)

        try:
            msg = "Congrats! You have been unbanned from `ViHill Corner`. Come back: https://discord.gg/mFm5GrQ"
            await member.send(msg)
        except Exception:
            pass
        try:
            await guild2.kick(member)
        except Exception:
            pass

    @commands.command()
    @commands.has_role(754676705741766757)
    async def mute(self, ctx: Context, member: disnake.Member, *, muted_time: TimeConverter = None):
        """
        Mute the member.
        If the time is specified (1s|1m|1h|1d), the member will be unmuted after that amount of time expires.
        """

        is_staff = False
        if 754676705741766757 in (role.id for role in member.roles):
            if ctx.author.id != 374622847672254466:
                return await ctx.send("You can't mute mods or take any moderator action against them.")
            is_staff = True

        result1 = await self.db1.find_one({'_id': member.id})
        result2 = await self.db2.find_one({'_id': member.id})

        if result1 is not None:
            return await ctx.reply("Member is already muted.")
        elif result2 is not None:
            return await ctx.reply("Member is already muted.")

        def format_time(dt):
            return time.human_timedelta(dt, accuracy=3)

        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        await ctx.send("What's the reason?")
        try:
            get_reason = await self.bot.wait_for('message', timeout=180, check=check)
            reason_content = get_reason.content

        except asyncio.TimeoutError:
            return await ctx.reply("Reason is something you must give!")

        else:
            post = {
                '_id': member.id,
                'muted_at': datetime.datetime.utcnow(),
                'mute_duration': muted_time,
                'muted_by': ctx.author.id,
                'guild_id': ctx.guild.id,
                'staff': is_staff
            }

            await self.db1.insert_one(post)

            if muted_time is not None:
                muted_for = datetime.datetime.utcnow() + relativedelta(seconds=muted_time)
                muted_for = format_time(muted_for)
            else:
                muted_for = "Eternity"

            guild = self.bot.get_guild(750160850077089853)
            log_channel = guild.get_channel(788377362739494943)
            muted = guild.get_role(750465726069997658)
            if is_staff is True:
                new_roles = [role for role in member.roles if role.id not in (754676705741766757, 750162714407600228)] + [muted]
            else:
                new_roles = [role for role in member.roles] + [muted]
            await member.edit(roles=new_roles, reason=f'{ctx.author}: "{reason_content}"')
            msg = "You have been muted in `ViHill Corner`"
            em = disnake.Embed(description=f"Time: `{muted_for}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**", color=Colours.invisible)
            try:
                await member.send(msg, embed=em)
            except disnake.HTTPException:
                pass

            _mute = disnake.Embed(
                description=f'{member.mention} has been muted. \n\nTime: `{muted_for}`\n**Reason: [{reason_content}]({ctx.message.jump_url})**',
                color=Colours.red
            )
            await ctx.send(embed=_mute)

            log = disnake.Embed(color=Colours.reds, title="___Mute___", timestamp=ctx.message.created_at.replace(tzinfo=None))
            log.add_field(name="Member", value=f"`{member}`", inline=False)
            log.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
            log.add_field(name="Time", value=f"`{muted_for}`", inline=False)
            log.add_field(name="Reason", value=f"**[{reason_content}]({ctx.message.jump_url})**", inline=False)
            await log_channel.send(embed=log)

    @commands.command(name='checkmute', aliases=['checkmutes', 'mutecheck', 'mutescheck'])
    async def check_mutes(self, ctx: Context, member: disnake.Member = None):
        """Check to see if the member is muted if specified any, or in case no member is specified then see all the members that are muted if any."""

        if member is None:
            entries = []
            results1 = await self.db1.find().to_list(100000)
            results2 = await self.db2.find().to_list(100000)
            results = results1 + results2
            if len(results) == 0:
                return await ctx.reply("No members muted currently.")
            for result in results:
                if result['mute_duration'] is not None:
                    _time = result['muted_at'] + relativedelta(seconds=result['mute_duration'])
                    _time = f"Time Left: {time.human_timedelta(_time, suffix=False, brief=True)}"
                else:
                    _time = "Time Left: Eternity"
                username = self.bot.get_user(result['_id'])
                _dict = {'username': username, 'time_left': _time}
                entries.append(_dict)
            m = MutePages(ctx=ctx, entries=entries, per_page=5, title="Here's all the current muted members:", color=Colours.red)
            await m.start()

        else:
            result = await self.db1.find_one({'_id': member.id})
            if result is None:
                result = await self.db2.find_one({'_id': member.id})
                if result is None:
                    return await ctx.reply("That member is not muted.")

            if result['mute_duration'] is not None:
                _time = result['muted_at'] + relativedelta(seconds=result['mute_duration'])
                _time = time.human_timedelta(_time, suffix=False)
            else:
                _time = "Eternity"

            em = disnake.Embed(color=Colours.red)
            em.set_author(name=member, icon_url=member.display_avatar)
            em.description = f"Time Left: `{_time}`"
            em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=em)

    @commands.command()
    @commands.has_role(754676705741766757)
    async def unmute(self, ctx: Context, member: disnake.Member):
        """Unmute the member."""

        result = await self.db1.find_one({'_id': member.id})
        resultt = await self.db2.find_one({'_id': member.id})

        if result is not None:
            is_staff = result['staff']
            muted_by = result['muted_by']
            if muted_by == 374622847672254466 and ctx.author.id != 374622847672254466:
                return await ctx.send(f"`{member}` cannot be unmuted since the one who muted them was none other than my master <:yamete:857163308427902987>")
        else:
            if resultt is not None:
                is_staff = resultt['staff']
                if ctx.author.id != 374622847672254466:
                    return await ctx.send("Members muted by filters cannot be unmuted by anyone except from my master <:yamete:857163308427902987>")
            else:
                return await ctx.reply("Member is not muted.")

        guild = self.bot.get_guild(750160850077089853)
        log_channel = guild.get_channel(788377362739494943)
        if is_staff is True:
            staff = guild.get_role(754676705741766757)
            mod = guild.get_role(750162714407600228)
            new_roles = [role for role in member.roles if role.id != 750465726069997658] + [staff, mod]
        else:
            new_roles = [role for role in member.roles if role.id != 750465726069997658]
        await self.db1.delete_one({'_id': member.id})
        await self.db2.delete_one({'_id': member.id})
        msg = "You were unmuted in `ViHill Corner`."
        try:
            await member.send(msg)
        except disnake.HTTPException:
            pass
        await member.edit(roles=new_roles, reason='{}: "Unmute"'.format(ctx.author))
        await ctx.send(embed=disnake.Embed(color=Colours.red, description=f"`{member}` has been unmuted."))

        em = disnake.Embed(color=Colours.reds, title="___UNMUTE___", timestamp=ctx.message.created_at.replace(tzinfo=None))
        em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
        em.add_field(name="Action", value="`Used the unmute command.`", inline=False)
        em.add_field(name="Member", value=f"`{member}`", inline=False)
        em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

        await log_channel.send(embed=em)

    @commands.command(name='purge', aliases=['clear'])
    @commands.has_role(754676705741766757)
    async def mod_purge(self, ctx: Context, amount: int = None):
        """Delete the amount of messages from the chat."""

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount or 0)

        guild = self.bot.get_guild(750160850077089853)
        log_channel = guild.get_channel(788377362739494943)

        em = disnake.Embed(color=Colours.reds, title="___PURGE / CLEAR___", timestamp=ctx.message.created_at.replace(tzinfo=None))
        em.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
        em.add_field(name="Action", value="`Used the clear / purge command`", inline=False)
        em.add_field(name="Amount", value=f"`{amount}` messages", inline=False)
        em.add_field(name="Channel", value=f"<#{ctx.channel.id}>", inline=False)

        await log_channel.send(embed=em)

    @commands.group(name='lock', invoke_without_command=True, case_insensitive=True)
    @commands.has_role(754676705741766757)
    async def lock_channel(self, ctx: Context, channel: disnake.TextChannel = None):
        """
        Locks the channel.
        No one will be able to talk in that channel except the mods, but everyone will still see the channel.
        """

        channel = channel or ctx.channel

        role = channel.guild.default_role
        if channel.id not in self.ignored_channels:
            overwrites = channel.overwrites_for(role)
            overwrites.send_messages = False
            await channel.set_permissions(role, overwrite=overwrites, reason=f'Channel locked by: "{ctx.author}"')
        else:
            return await ctx.reply('That channel cannot be unlocked.')
        await ctx.reply('Channel Locked! 🔒')

    @lock_channel.command(name='all')
    @commands.has_role(754676705741766757)
    async def lock_all_channels(self, ctx: Context):
        """
        Locks *all* the channels that are have not been locked, but omits the channels that the users can't see or talk in already.
        """

        role = ctx.guild.default_role
        for channel in ctx.guild.text_channels:
            if channel.id not in self.ignored_channels:
                if channel.overwrites_for(role).send_messages is not False:
                    overwrites = channel.overwrites_for(role)
                    overwrites.send_messages = False
                    await channel.set_permissions(role, overwrite=overwrites, reason=f'Channel locked by: "{ctx.author}"')
        await ctx.reply('All the unlocked channels have been locked! 🔒')

    @commands.group(name='unlock', invoke_without_command=True, case_insensitive=True)
    @commands.has_role(754676705741766757)
    async def unlock_channel(self, ctx: Context, channel: disnake.TextChannel = None):
        """
        Unlocks the channel.
        """

        channel = channel or ctx.channel

        role = channel.guild.default_role
        if channel.id not in self.ignored_channels:
            overwrites = channel.overwrites_for(role)
            overwrites.send_messages = None
            await channel.set_permissions(role, overwrite=overwrites, reason=f'Channel unlocked by: "{ctx.author}"')
        else:
            return await ctx.reply('That channel cannot be unlocked.')
        await ctx.reply('Channel Unlocked! 🔓')

    @unlock_channel.command(name='all')
    @commands.has_role(754676705741766757)
    async def unlock_all_channels(self, ctx: Context):
        """
        Unlocks *all the already locked* channels, but omits the channels that the users can't see or talk in already.
        """

        role = ctx.guild.default_role
        for channel in ctx.guild.text_channels:
            if channel.id not in self.ignored_channels:
                if channel.overwrites_for(role).send_messages is not None:
                    overwrites = channel.overwrites_for(role)
                    overwrites.send_messages = None
                    await channel.set_permissions(role, overwrite=overwrites, reason=f'Channel unlocked by: "{ctx.author}"')
        await ctx.reply('All locked channels have been unlocked! 🔓')


def setup(bot):
    bot.add_cog(Moderator(bot))
