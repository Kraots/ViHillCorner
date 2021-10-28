import datetime
from dateutil.relativedelta import relativedelta

import pymongo

import disnake
from disnake.ext import commands, tasks

from utils import time
from utils.colors import Colours
from utils.context import Context
from utils.paginator import RoboPages, FieldPageSource

from main import ViHillCorner


class MessagesTopButtons(disnake.ui.View):
    def __init__(self, db, ctx, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.db = db
        self.ctx = ctx

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'Only {self.ctx.author.display_name} can use the buttons on this message!', ephemeral=True)
            return False
        return True

    async def on_error(self, error, item, interaction):
        return await self.ctx.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(content='Did not click any button in time.', view=self)

    @disnake.ui.button(label='Total Messages Top', style=disnake.ButtonStyle.blurple)
    async def total_messages_top(self, button: disnake.Button, inter: disnake.MessageInteraction):
        index = 0
        data = []
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        guild = self.ctx.bot.get_guild(750160850077089853)

        results = await self.db.find().sort("messages_count", -1).to_list(100000)
        for result in results:
            if result['messages_count'] != 0:
                index += 1
                mem = guild.get_member(result['_id'])
                if index in (1, 2, 3):
                    place = top_3_emojis[index]
                else:
                    place = f'`#{index:,}`'
                if mem == self.ctx.author:
                    to_append = (f'**{place} {mem.name} (YOU)**', f"**{result['messages_count']:,}** messages")
                    data.append(to_append)
                else:
                    to_append = (f'{place} {mem.name}', f"**{result['messages_count']:,}** messages")
                    data.append(to_append)
        source = FieldPageSource(data, per_page=10)
        source.embed.title = 'Top most active users'
        await self.message.delete()
        pages = RoboPages(source, ctx=self.ctx)
        await pages.start()
        self.stop()

    @disnake.ui.button(label='Weekly Messages Top', style=disnake.ButtonStyle.blurple)
    async def weekly_messages_top(self, button: disnake.Button, inter: disnake.MessageInteraction):
        index = 0
        data = []
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        guild = self.ctx.bot.get_guild(750160850077089853)

        results = await self.db.find().sort("weekly_messages_count", -1).to_list(100000)
        for result in results:
            if result['weekly_messages_count'] != 0:
                index += 1
                mem = guild.get_member(result['_id'])
                if index in (1, 2, 3):
                    place = top_3_emojis[index]
                else:
                    place = f'`#{index:,}`'
                if mem == self.ctx.author:
                    to_append = (f'**{place} {mem.name} (YOU)**', f"**{result['weekly_messages_count']:,}** messages")
                    data.append(to_append)
                else:
                    to_append = (f'{place} {mem.name}', f"**{result['weekly_messages_count']:,}** messages")
                    data.append(to_append)
        source = FieldPageSource(data, per_page=10)
        source.embed.title = 'This week\'s most active members'
        await self.message.delete()
        pages = RoboPages(source, ctx=self.ctx)
        await pages.start()
        self.stop()

    @disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red)
    async def _stop_view(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await self.message.delete()
        self.stop()


class Messages(commands.Cog):
    """Messages related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db2['Levels']
        self.weekly_reset.start()
        self.prefix = "!"

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '🎫'

    @tasks.loop(minutes=1)
    async def weekly_reset(self):
        await self.bot.wait_until_ready()
        results = await self.db.find_one({"_id": 374622847672254466})
        resetWhen = results['weekly_reset']
        a = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        dateNow = datetime.datetime.strptime(a, '%Y-%m-%d')

        if dateNow >= resetWhen:
            users = {}
            index = 0
            results = await self.db.find().sort("weekly_messages_count", -1).to_list(3)
            for result in results:
                index += 1
                user = self.bot.get_user(result['_id'])
                users[index] = user
            _1stplace = users[1]
            _2ndplace = users[2]
            _3rdplace = users[3]
            await self.db.update_one({'_id': _1stplace.id}, {'$inc': {'xp': 50000}})
            await self.db.update_one({'_id': _2ndplace.id}, {'$inc': {'xp': 30000}})
            await self.db.update_one({'_id': _3rdplace.id}, {'$inc': {'xp': 20000}})
            await _1stplace.send(
                "Congrats. You placed `1st` in the weekly top! Your reward is **50,000** XP.\n"
                f"The others placed:\n\u2800• **{_2ndplace}** -> `2nd`\n\u2800• **{_3rdplace}** -> `3rd`"
            )
            await _2ndplace.send(
                "Congrats. You placed `2nd` in the weekly top! Your reward is **30,000** XP.\n"
                f"The others placed:\n\u2800• **{_1stplace}** -> `1st`\n\u2800• **{_3rdplace}** -> `3rd`"
            )
            await _3rdplace.send(
                "Congrats. You placed `3rd` in the weekly top! Your reward is **20,000** XP."
                f"\nThe others placed:\n\u2800• **{_1stplace}** -> `1st`\n\u2800• **{_2ndplace}** -> `2nd`"
            )

            await self.db.update_many({}, {"$set": {"weekly_messages_count": 0}})
            x = dateNow + relativedelta(weeks=1)
            await self.db.update_one({'_id': 374622847672254466}, {'$set': {'weekly_reset': x}})

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        data = await self.db.find_one({'_id': message.author.id})
        if data is None:
            try:
                newuser = {"_id": message.author.id, "xp": 0, "messages_count": 0, "weekly_messages_count": 0}
                await self.db.insert_one(newuser)
                return
            except pymongo.errors.DuplicateKeyError:
                return
        await self.db.update_one({"_id": message.author.id}, {"$inc": {"messages_count": 1}})

    @commands.group(name='messages', invoke_without_command=True, case_insensitive=True, aliases=['msg'])
    async def _msgs(self, ctx: Context, member: disnake.Member = None):
        """Check your total amount of sent messages or someone else's."""

        member = member or ctx.author

        user_db = await self.db.find_one({'_id': member.id})
        if user_db is None:
            return await ctx.reply(f'`{member.display_name}` sent no messages.')
        em = disnake.Embed(color=Colours.light_pink)
        em.set_author(name=f'{member.display_name}\'s message stats', url=member.display_avatar, icon_url=member.display_avatar)
        em.add_field(name='Total Messages', value=f"`{user_db['messages_count']:,}`")
        em.add_field(name='Weekly Messages', value=f"`{user_db['weekly_messages_count']:,}`")
        em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=em)

    @_msgs.command(name='add')
    @commands.is_owner()
    async def msg_add(self, ctx: Context, member: disnake.Member, amount: str):
        """Add a certain amount of messages for the member."""

        usr_db = await self.db.find_one({'_id': member.id})
        if usr_db is None:
            return await ctx.reply('User not in the database.')

        try:
            amount = amount.replace(',', '')
            amount = int(amount)
        except ValueError:
            return await ctx.reply('Master, the amount must be an integer 🥺')

        await self.db.update_one({'_id': member.id}, {'$inc': {'messages_count': amount}})
        await ctx.send(content=f'Added `{amount:,}` messages to {member.mention}')

    @_msgs.command(name='set')
    @commands.is_owner()
    async def msg_set(self, ctx: Context, member: disnake.Member, amount: str):
        """Set the amount of messages for the member."""

        usr_db = await self.db.find_one({'_id': member.id})
        if usr_db is None:
            return await ctx.reply('User not in the database.')

        try:
            amount = amount.replace(',', '')
            amount = int(amount)
        except ValueError:
            return await ctx.reply('Master, the amount must be an integer 🥺')

        await self.db.update_one({'_id': member.id}, {'$set': {'messages_count': amount}})
        await ctx.send(content=f'Added `{amount:,}` messages to {member.mention}')

    @_msgs.command(name='reset')
    @commands.is_owner()
    async def msg_reset(self, ctx: Context, member: disnake.Member):
        """Reset the amount of total messages for the member."""

        usr_db = await self.db.find_one({'_id': member.id})
        if usr_db is None:
            return await ctx.reply('User not in the database.')

        view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
        view.message = msg = await ctx.send("Are you sure you want to reset the total message count for member %s?" % (member.mention), view=view)
        await view.wait()
        if view.response is True:
            await self.db.update_one({'_id': member.id}, {'$set': {'messages_count': 0}})
            return await msg.edit(content='The total message count for member **%s** has been reset successfully.' % (member), view=view)

        elif view.response is False:
            return await msg.edit(content="Command to reset the message count for user `%s` has been canceled." % (member), view=view)

    @_msgs.group(name='top', invoke_without_command=True, case_insensitive=True, aliases=['lb'])
    async def msg_top(self, ctx: Context):
        """See the top 15 most active members of the server and when the top restarts."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        view = MessagesTopButtons(self.db, ctx)
        em = disnake.Embed(title='Please click the button of the top you wish to see.', color=Colours.reds)
        view.message = await ctx.send(embed=em, view=view)

    @msg_top.command(name='time', aliases=['time-left', 'remaining', 'left'])
    async def msg_top_remaining(self, ctx: Context):
        """Check how much time until the top ends."""

        data = await self.db.find_one({'_id': self.bot._owner_id})
        await ctx.send(f"The weekly top resets in: `{time.human_timedelta(data['weekly_reset'])}`")

    @msg_top.command(name='reset')
    @commands.is_owner()
    async def msg_top_reset(self, ctx: Context, member: disnake.Member):
        """Reset the amount of weekly messages for the member."""

        view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
        view.message = msg = await ctx.send("Are you sure you want to reset the message count for this week for member %s?" % (member.mention), view=view)
        await view.wait()
        if view.response is True:
            await self.db.update_one({'_id': member.id}, {'$set': {'weekly_messages_count': 0}})
            return await msg.edit(content='The message count for this week for member **%s** has been reset successfully.' % (member), view=view)

        elif view.response is False:
            return await msg.edit(content="Command to reset the message count for user `%s` has been canceled." % (member), view=view)

    @msg_top.command(aliases=['reward'])
    async def rewards(self, ctx: Context):
        """See what rewards you can get from the weekly messages top."""

        em = disnake.Embed(color=Colours.light_pink, title="Here are the rewards for the weekly top:")
        em.add_field(name="`1st Place`", value="**50k XP**", inline=False)
        em.add_field(name="`2nd Place`", value="**30k XP**", inline=False)
        em.add_field(name="`3rd Place`", value="**20k XP**", inline=False)
        em.set_footer(text="Requested by: %s" % (ctx.author), icon_url=ctx.author.display_avatar)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Messages(bot))
