import disnake
from disnake.ext import commands, tasks
from random import randint
import random
from utils.colors import Colours
import asyncio
import pymongo
import datetime
from dateutil.relativedelta import relativedelta
from utils import time, menus
from utils.paginator import RoboPages, FieldPageSource
from utils.helpers import format_balance
from utils.context import Context
from main import ViHillCorner


class ShopEcoMenus(menus.ListPageSource):
    def __init__(self, entries, *, per_page=12):
        super().__init__(entries, per_page=per_page)

    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f'{entry}')

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} items)'
            menu.embed.set_footer(text=footer)

        menu.embed.description = 'Use `!shop buy <item_name>` to buy or `!shop sell <item_name>` to sell an item that you have.\n\n{}'.format("\n\n".join(pages))  # noqa
        return menu.embed


class ShopEcoMenu(RoboPages):
    def __init__(self, ctx: Context, entries, *, per_page=12, color=None):
        super().__init__(ShopEcoMenus(entries, per_page=per_page), ctx=ctx)
        if color is None:
            color = disnake.Embed.Empty
        self.embed = disnake.Embed(colour=color, title='Shop Items')


class ShopPageEntry:
    def __init__(self, entry):

        self.name = entry['item_name']
        self.price = '{:,} <:carrots:822122757654577183>'.format(entry['price']) if isinstance(entry['price'], int) else entry['price']
        self.desc = entry['description']
        self.emoji = entry.get('item_emoji', '')

    def __str__(self):
        return f'**{self.emoji} {self.name.title()} — {self.price}**\n{self.desc}'


class ShopMenu(ShopEcoMenu):
    def __init__(self, ctx: Context, entries, *, per_page=5, color=None):
        converted = [ShopPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page, color=color)


_shop = [
    {'item_type': 'Collectable', 'item_name': 'golden carrot', 'price': 100000000,
        'sells_for': 'This item cannot be sold.', 'description': 'Show off to your friends with this item that costs 100M',
        'item_emoji': '<:goldencarrot:885075068797984808>'},
    {'item_type': 'Usable', 'item_name': 'clock', 'price': 25000, 'sells_for': 1200,
        'description': 'Increases luck by 5% for 2h', 'expires_in': {'hours': 2}},
    {'item_type': 'Usable', 'item_name': 'alcohol', 'price': 50000, 'sells_for': 3500,
        'description': 'Increases luck by 10% for 1h', 'expires_in': {'hours': 1}},
    {'item_type': 'Tool', 'item_name': 'fishing pole', 'price': 65000, 'sells_for': 5000,
        'description': 'Use this to fish', 'uses': 13},
    {'item_type': 'Tool', 'item_name': 'hunting rifle', 'price': 75000, 'sells_for': 6300,
        'description': 'Use this to go hunting', 'uses': 14},
    {'item_type': 'Sellable', 'item_name': 'common fish', 'price': 'This item cannot be bought.', 'sells_for': 10000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'uncommon fish', 'price': 'This item cannot be bought.', 'sells_for': 25000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'rare fish', 'price': 'This item cannot be bought.', 'sells_for': 50000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'epic fish', 'price': 'This item cannot be bought.', 'sells_for': 225000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'legendary fish', 'price': 'This item cannot be bought.', 'sells_for': 500000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'mythic fish', 'price': 'This item cannot be bought.', 'sells_for': 1000000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'skunk', 'price': 'This item cannot be bought.', 'sells_for': 10000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'boar', 'price': 'This item cannot be bought.', 'sells_for': 30000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'bear', 'price': 'This item cannot be bought.', 'sells_for': 63000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'crocodile', 'price': 'This item cannot be bought.', 'sells_for': 230000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'lion', 'price': 'This item cannot be bought.', 'sells_for': 560000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
    {'item_type': 'Sellable', 'item_name': 'dragon', 'price': 'This item cannot be bought.', 'sells_for': 1250000,
        'description': 'This item\'s purpose is to be collected or sold. Nothing more, nothing less.'},
]

_fishes = [
    {'fish': 'common fish',
        'chances': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                    24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 155, 160, 154, 136, 137, 116, 117)},
    {'fish': 'uncommon fish',
        'chances': (45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
                    66, 67, 68, 69, 70, 71, 72, 73, 74, 132, 133, 122)},
    {'fish': 'rare fish',
        'chances': (75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89)},
    {'fish': 'epic fish',
        'chances': (90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101)},
    {'fish': 'legendary fish',
        'chances': (102, 103, 104, 105, 106, 107)},
    {'fish': 'mythic fish',
        'chances': (108, 109, 110)}
]

_animals = [
    {'animal': 'skunk',
        'chances': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
                    36, 37, 38, 39, 40, 41, 42, 43, 44, 155, 160, 154, 136, 137, 116, 117)},
    {'animal': 'boar',
        'chances': (45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 132, 133, 122)},
    {'animal': 'bear',
        'chances': (75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89)},
    {'animal': 'crocodile',
        'chances': (90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101)},
    {'animal': 'lion',
        'chances': (102, 103, 104, 105, 106, 107)},
    {'animal': 'dragon',
        'chances': (108, 109, 110)}
]

all_search_choices = (
    'purse', 'discord', 'pocket', 'street', 'dog', 'uber',
    'canals', 'washer', 'sink', 'fridge', 'area51', 'dumpster',
    'couch', 'dress', 'tree', 'glovebox'
)


class EcoSearchView(disnake.ui.View):
    def __init__(self, ctx: Context, *, timeout=10.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'Only {self.ctx.author.display_name} can use the buttons on this message!', ephemeral=True)
            return False
        return True

    async def on_error(self, error: Exception, item, interaction):
        return await self.ctx.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.grey
        await self.message.edit('Guess you didn\'t want to search anywhere 🙄', view=self)

    @disnake.ui.button(label='1', style=disnake.ButtonStyle.blurple)
    async def search_1_result(self, button: disnake.ui.Button, inter: disnake.Interaction):
        for item in self.children:
            item.disabled = True
            if not item.label == button.label:
                item.style = disnake.ButtonStyle.grey
        em = disnake.Embed(color=Colours.light_pink, title=f'{inter.author.display_name} searched {button.label}')
        win_lose = random.choice(['win', 'lose', 'win', 'lose', 'win'])
        if win_lose == 'win':
            _amt = random.randrange(4600, 50001)
            amt = '{:,}'.format(_amt)
            await self.ctx.bot.db1['Economy'].update_one({'_id': inter.author.id}, {'$inc': {'wallet': _amt}})
            em.description = f'You searched `{button.label}` and got **{amt}** <:carrots:822122757654577183>'
        else:
            _amt = random.randrange(1000, 5001)
            amt = '{:,}'.format(_amt)
            await self.ctx.bot.db1['Economy'].update_one({'_id': inter.author.id}, {'$inc': {'wallet': -_amt}})
            em.description = f'You searched `{button.label}` and lost **{amt}** <:carrots:822122757654577183>'
        await inter.response.edit_message(content=None, embed=em, view=self)
        self.stop()

    @disnake.ui.button(label='2', style=disnake.ButtonStyle.blurple)
    async def search_2_result(self, button: disnake.ui.Button, inter: disnake.Interaction):
        for item in self.children:
            item.disabled = True
            if not item.label == button.label:
                item.style = disnake.ButtonStyle.grey
        em = disnake.Embed(color=Colours.light_pink, title=f'{inter.author.display_name} searched {button.label}')
        win_lose = random.choice(['win', 'lose', 'win', 'lose', 'win'])
        if win_lose == 'win':
            _amt = random.randrange(4600, 50001)
            amt = '{:,}'.format(_amt)
            await self.ctx.bot.db1['Economy'].update_one({'_id': inter.author.id}, {'$inc': {'wallet': _amt}})
            em.description = f'You searched `{button.label}` and got **{amt}** <:carrots:822122757654577183>'
        else:
            _amt = random.randrange(1000, 5001)
            amt = '{:,}'.format(_amt)
            await self.ctx.bot.db1['Economy'].update_one({'_id': inter.author.id}, {'$inc': {'wallet': -_amt}})
            em.description = f'You searched `{button.label}` and lost **{amt}** <:carrots:822122757654577183>'
        await inter.response.edit_message(content=None, embed=em, view=self)
        self.stop()

    @disnake.ui.button(label='3', style=disnake.ButtonStyle.blurple)
    async def search_3_result(self, button: disnake.ui.Button, inter: disnake.Interaction):
        for item in self.children:
            item.disabled = True
            if not item.label == button.label:
                item.style = disnake.ButtonStyle.grey
        em = disnake.Embed(color=Colours.light_pink, title=f'{inter.author.display_name} searched {button.label}')
        win_lose = random.choice(['win', 'lose', 'win', 'lose', 'win'])
        if win_lose == 'win':
            _amt = random.randrange(4600, 50001)
            amt = '{:,}'.format(_amt)
            await self.ctx.bot.db1['Economy'].update_one({'_id': inter.author.id}, {'$inc': {'wallet': _amt}})
            em.description = f'You searched `{button.label}` and got **{amt}** <:carrots:822122757654577183>'
        else:
            _amt = random.randrange(1000, 5001)
            amt = '{:,}'.format(_amt)
            await self.ctx.bot.db1['Economy'].update_one({'_id': inter.author.id}, {'$inc': {'wallet': -_amt}})
            em.description = f'You searched `{button.label}` and lost **{amt}** <:carrots:822122757654577183>'
        await inter.response.edit_message(content=None, embed=em, view=self)
        self.stop()


class RPSView(disnake.ui.View):
    def __init__(self, db, ctx, *, timeout=180):
        super().__init__(timeout=timeout)
        self.db = db
        self.ctx = ctx

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'Only {self.ctx.author.display_name} can use the buttons on this message!', ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.gray
        await self.message.edit('Timed Out.', view=self)

    def disable_buttons(self, button):
        for item in self.children:
            if item.label != button.style:
                item.style = disnake.ButtonStyle.gray
            item.disabled = True

    async def check_result(self, button):
        bot_choice = random.choice(('rock', 'paper', 'scissors'))
        choice = button.label.lower()
        won_amt = randint(5000, 35000)
        lost_amt = randint(1000, 7001)
        won_message = f'**__You won__** and got **{won_amt:,}** <:carrots:822122757654577183>\nYou chose `{choice}` while the bot chose `{bot_choice}`'
        lost_message = f'**__The bot won__** and you lost **{lost_amt:,}** <:carrots:822122757654577183>\nYou chose `{choice}` while the bot chose `{bot_choice}`'  # noqa
        self.disable_buttons(button)
        if (
            (choice == 'rock' and bot_choice == 'paper') or
            (choice == 'paper' and bot_choice == 'scissors') or
            (choice == 'scissors' and bot_choice == 'rock')
        ):
            await self.message.edit(lost_message, view=self)
            won = False
        elif choice == bot_choice:
            return await self.message.edit(f'We both chose `{choice}`. Nothing happened, your balance stays the same.', view=self)
        else:
            await self.message.edit(won_message, view=self)
            won = True

        if won is True:
            await self.db.update_one({'_id': self.ctx.author.id}, {'$inc': {'wallet': won_amt}})
        elif won is False:
            await self.db.update_one({'_id': self.ctx.author.id}, {'$inc': {'wallet': -lost_amt}})
        self.stop()

    @disnake.ui.button(label='Rock', style=disnake.ButtonStyle.blurple)
    async def rock(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await self.check_result(button)

    @disnake.ui.button(label='Paper', style=disnake.ButtonStyle.blurple)
    async def paper(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await self.check_result(button)

    @disnake.ui.button(label='Scissors', style=disnake.ButtonStyle.blurple)
    async def scissors(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await self.check_result(button)


class Economy(commands.Cog):
    """Economy related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Economy']
        self.check_items_in_use.start()
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='carrots', id=822122757654577183)

    @tasks.loop(minutes=1.0)
    async def check_items_in_use(self):
        now = datetime.datetime.utcnow()
        users = await self.db.find().to_list(100000)
        for user in users:
            new_in_use = []
            for item_in_use in user['items_in_use']:
                if item_in_use['expires_in'] is not None:
                    if item_in_use['expires_in'] > now:
                        new_in_use.append(item_in_use)
                else:
                    new_in_use.append(item_in_use)
            await self.db.update_one({'_id': user['_id']}, {'$set': {'items_in_use': new_in_use}})

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def daily(self, ctx: Context):
        """Get your daily 75.00K <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        user = ctx.author
        results = await self.db.find_one({"_id": user.id})

        if results is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            return
        else:
            dateNow = datetime.datetime.utcnow()
            next_daily = datetime.datetime.utcnow() + relativedelta(days=1)

            try:
                daily = results['daily']

                if ctx.author.id != 374622847672254466:
                    if dateNow < daily:
                        def format_date(dt):
                            return f"{time.human_timedelta(dt, accuracy=3)}"
                        return await ctx.send(f"{ctx.author.mention} You already claimed your daily for today! Please try again in `{format_date(daily)}`.")

                    elif dateNow >= daily:
                        await self.db.update_one({"_id": user.id}, {"$inc": {"wallet": 75000}})
                        await self.db.update_one({"_id": user.id}, {"$set": {"daily": next_daily}})
                else:
                    await self.db.update_one({"_id": user.id}, {"$inc": {"wallet": 75000}})
                    await self.db.update_one({"_id": user.id}, {"$set": {"daily": next_daily}})

            except KeyError:
                await self.db.update_one({"_id": user.id}, {"$inc": {"wallet": 75000}})
                await self.db.update_one({"_id": user.id}, {"$set": {"daily": next_daily}})

            await ctx.send(
                "Daily successfully claimed, `75,000` <:carrots:822122757654577183>  have been put into your wallet. "
                f"Come back in **24 hours** for the next one. {ctx.author.mention}"
            )

    @daily.group(name='reset', invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def daily_reset(self, ctx: Context, member: disnake.Member = None):
        """Reset the daily for a user. This means that the amount of time that they have to wait until they can get their daily will be reset."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})
        if results is None:
            await ctx.send("User not registered!")
            return

        NewDaily = datetime.datetime.utcnow()
        await self.db.update_one({"_id": member.id}, {"$set": {"daily": NewDaily}})
        await ctx.send("Cooldown for the daily command has been reset for user `{}`.".format(member))

    @daily_reset.command(name='everyone', aliases=['all'])
    @commands.is_owner()
    async def daily_reset_everyone(self, ctx: Context):
        """Reset the daily cooldown for `everyone`"""

        NewDaily = datetime.datetime.utcnow()
        await self.db.update_many({}, {"$set": {"daily": NewDaily}})
        await ctx.send("Cooldown for the daily command has been reset for everyone.")

    @commands.command(name='register')
    async def eco_register(self, ctx: Context):
        """Register yourself to be able to use the economy commands."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        user = ctx.author

        shop = []
        for item in _shop:
            try:
                shop.append({'item_name': item['item_name'], 'owned': 0, 'uses': item['uses']})
            except KeyError:
                shop.append({'item_name': item['item_name'], 'owned': 0})

        post = {
            '_id': user.id,
            'wallet': 0,
            'bank': 0,
            'passive': False,
            'passive_cooldown': datetime.datetime.utcnow(),
            'items': shop,
            'items_in_use': [],
            'daily': datetime.datetime.utcnow()
        }

        try:
            await self.db.insert_one(post)
            await ctx.send("Succesfully registered! %s" % (ctx.author.mention))

        except pymongo.errors.DuplicateKeyError:
            await ctx.send("You are already registered! %s" % (ctx.author.mention))

    @commands.command(name='unregister')
    async def eco_unregister(self, ctx: Context):
        """Unregister yourself, you won't be able to use the economy commands anymore."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        user = ctx.author
        results = await self.db.find_one({"_id": user.id})
        if results is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("You are not registered! %s" % (ctx.author.mention))
            return

        await self.db.delete_one({"_id": user.id})
        await ctx.send("Succesfully unregistered! %s" % (ctx.author.mention))

    @commands.command(aliases=['bag'])
    async def inventory(self, ctx: Context, member: disnake.Member = None):
        """Check your or someone else's inventory."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        member = member or ctx.author

        user_db = await self.db.find_one({'_id': member.id})
        if user_db is None:
            if member.id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            else:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send("User is not registered! %s" % (ctx.author.mention))
        _count = 0
        for item in user_db['items']:
            if item['owned'] == 0:
                _count += 1
        if _count == len(user_db['items']):
            return await ctx.send('The inventory is empty, nothing to see.')
        user_items = []
        inv_worth = 0
        total_items = 0
        for item in user_db['items']:
            if item['owned'] != 0:
                try:
                    item_durr = item['uses']
                except KeyError:
                    item_durr = None
                name = item['item_name'].title
                if item_durr is not None:
                    uses_left = f"{item_durr}/{''.join([str(i['uses']) for i in _shop if i['item_name'] == item['item_name']])} uses left)"
                else:
                    uses_left = ''
                owned = ''.join([i['owned'] for i in _shop if i['item_name'] == item['item_name']])
                try:
                    emoji = ''.join([i['item_emoji'] for i in _shop if i['item_name'] == item['item_name']])
                    to_append = f"— {emoji} {name} {owned} {uses_left}"
                except KeyError:
                    to_append = f"— {name} {owned} {uses_left}"
                try:
                    item_worth = item['owned'] * int(
                        ''.join([str(i['sells_for']) for i in _shop if isinstance(i['sells_for'], int) and i['item_name'] == item['item_name']])
                    )
                    inv_worth += item_worth
                except ValueError:
                    pass
                total_items += item['owned']
                user_items.append(to_append)
        em = disnake.Embed(color=member.color, description='\n'.join(user_items))
        em.set_author(name=f'{member.display_name}\'s inventory', url=member.display_avatar, icon_url=member.display_avatar)
        em.set_thumbnail(url=member.display_avatar)
        _text = f'{total_items:,} total items'
        if inv_worth != 0:
            _text = f'Worth: {inv_worth:,} carrots • {total_items:,} total items'
        em.set_footer(text=_text)
        await ctx.send(embed=em)

    @commands.group(name='shop', invoke_without_command=True, case_insensitive=True)
    async def eco_shop(self, ctx: Context, *, item: str = None):
        """
        See what items there are in the shop.
        These items provide different perks such as luck multipliers, tools to get more <:carrots:822122757654577183>, etc...
        """

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        if item is None:
            shop = []
            for item in _shop:
                if item['item_type'] in ('Tool', 'Usable', 'Collectable'):
                    shop.append(item)
            p = ShopMenu(ctx=ctx, entries=shop)
            await p.start()

        else:
            item_ = item.lower()
            item_found = False
            user_db = await self.db.find_one({'_id': ctx.author.id})
            index = 0
            for _item in _shop:
                if _item['item_name'] == item_:
                    sell_price = '{:,} <:carrots:822122757654577183>'.format(_item['sells_for']) if isinstance(_item['sells_for'], int) else _item['sells_for']
                    buy_price = '{:,} <:carrots:822122757654577183>'.format(_item['price']) if isinstance(_item['price'], int) else _item['price']
                    if user_db is not None:
                        owned = user_db['items'][index]['owned']
                        item_found = True
                        try:
                            em = disnake.Embed(
                                title=f"{_item['item_emoji']} {_item['item_name'].title()} ({owned} owned)",
                                description=f"*{_item['description']}*\n\n**BUY** - {buy_price}\n**SELL** - {sell_price}"
                            )
                        except KeyError:
                            em = disnake.Embed(
                                title=f"{_item['item_name'].title()} ({owned} owned)",
                                description=f"*{_item['description']}*\n\n**BUY** - {buy_price}\n**SELL** - {sell_price}"
                            )
                        em.set_footer(text=f"Item Type: {_item['item_type']}")
                        return await ctx.send(embed=em)
                    else:
                        item_found = True
                        try:
                            em = disnake.Embed(
                                title=f"{_item['item_emoji']} {_item['item_name'].title()}",
                                description=f"*{_item['description']}*\n\n**BUY** - {buy_price}\n**SELL** - {sell_price}"
                            )
                        except KeyError:
                            em = disnake.Embed(
                                title=f"{_item['item_name'].title()}",
                                description=f"*{_item['description']}*\n\n**BUY** - {buy_price}\n**SELL** - {sell_price}"
                            )
                        em.set_footer(text=f"Item Type: {_item['item_type']}")
                        return await ctx.send(embed=em)
                index += 1
            if item_found is False:
                return await ctx.reply(f'Item `{item}` does not exist!')

    @eco_shop.command(name='update')
    @commands.is_owner()
    async def eco_shop_update(self, ctx: Context):
        """Update everyone's inventory to corespond with the updated shop."""

        for user in await self.db.find().to_list(100000):
            items = []
            index = 0
            names = (i['item_name'] for i in _shop)
            for i in names:
                try:
                    if i in user['items'][index]['item_name']:
                        items.append(user['items'][index])
                except IndexError:
                    try:
                        items.append(
                            {
                                'item_name': names[index],
                                'owned': 0,
                                'uses': int(''.join([str(i['uses']) for i in _shop if i['item_name'] == names[index]]))
                            }
                        )
                    except KeyError:
                        items.append({'item_name': names[index], 'owned': 0})
                index += 1
            await self.db.update_one({'_id': user['_id']}, {'$set': {'items': items}})
        await ctx.reply('Successfully updated everyone\'s shop.')

    @eco_shop.command(name='buy')
    async def eco_shop_buy(self, ctx: Context, *, item):
        """Buy an item from the shop."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        item_ = item.lower()
        item_found = False
        for _item in _shop:
            if _item['item_name'] == item_:
                item_found = True
                user_db = await self.db.find_one({'_id': ctx.author.id})
                if user_db is None:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.send(f'You are not registered! Type: `!register` to register {ctx.author.mention}')
                elif _item['item_type'] == 'Sellable':
                    return await ctx.reply(_item['price'])

                if user_db['wallet'] >= _item['price']:
                    items = []
                    for i in user_db['items']:
                        if i['item_name'] == _item['item_name']:
                            if i['owned'] > 0 and _item['item_type'] == 'Tool':
                                return await ctx.reply('You can only have one of this item.')
                            i['owned'] += 1
                        items.append(i)
                    await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items}})
                    await self.db.update_one({'_id': ctx.author.id}, {'$inc': {'wallet': -_item['price']}})
                    bought_for = '{:,}'.format(_item['price'])
                    return await ctx.reply(f"Bought `{_item['item_name']}` for **{bought_for}** <:carrots:822122757654577183>")

                else:
                    return await ctx.reply('Insufficient wallet funds.')

        if item_found is False:
            return await ctx.reply(f'Item `{item}` does not exist!')

    @eco_shop.command(name='sell')
    async def eco_shop_sell(self, ctx: Context, *, item):
        """Sell an item that you own."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        user_db = await self.db.find_one({'_id': ctx.author.id})
        if user_db is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f'You are not registered! Type: `!register` to register {ctx.author.mention}')
        item_ = item.lower()
        if item_ == 'all':
            view = self.bot.confirm_view(ctx)
            view.message = msg = await ctx.send('Are you sure you want to sell all of you sellables?', view=view)
            await view.wait()
            if view.response is True:
                total_sold_for = 0
                items = []
                sellables = 0
                for _item in user_db['items']:
                    if _item['owned'] != 0 and _item['item_name'] in (i['item_name'] for i in _shop if i['item_type'] == 'Sellable'):
                        sold_for = _item['owned'] * int(''.join([str(i_['sells_for']) for i_ in _shop if i_['item_name'] == _item['item_name']]))
                        total_sold_for += sold_for
                        sellables += 1
                        _item['owned'] = 0
                    items.append(_item)
                if sellables == 0:
                    return await ctx.reply('You do not have any sellables in your inventory.')
                await self.db.update_one({'_id': ctx.author.id}, {'$inc': {'wallet': total_sold_for}})
                await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items}})
                return await msg.edit(f'Successfully sold all your sellables for `{total_sold_for:,}` <:carrots:822122757654577183>', view=view)
            elif view.response is False:
                return await msg.edit('Your items have not been sold.', view=view)

        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        await ctx.send('What\'s the amount of this item that you wish to sell?')
        try:
            amt = await self.bot.wait_for('message', check=check, timeout=7)
        except asyncio.TimeoutError:
            amount: str = None
        else:
            amount = amt.content.lower()

        item_found = False
        for _item in _shop:
            if _item['item_name'] == item_:
                item_found = True
                items = []
                for i in user_db['items']:
                    if i['item_name'] == _item['item_name']:
                        try:
                            i['uses'] = _item['uses']
                        except KeyError:
                            pass
                        if i['owned'] == 0:
                            return await ctx.reply('You do not own that item.')
                        elif _item['item_type'] == 'Collectable':
                            return await ctx.reply('This item cannot be sold.')
                        if amount == 'all':
                            amount = i['owned']
                            i['owned'] -= i['owned']
                        elif amount is None:
                            amount = 1
                            i['owned'] -= 1
                        else:
                            try:
                                amount = int(amount)
                                if i['owned'] >= amount:
                                    i['owned'] -= amount
                                else:
                                    return await ctx.reply(f'You do not have `{amount}` **{item}.**')
                            except ValueError:
                                amount = 1
                    items.append(i)
                await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items}})
                await self.db.update_one({'_id': ctx.author.id}, {'$inc': {'wallet': (_item['sells_for'] * amount)}})
                sold_for = '{:,}'.format(_item['sells_for'] * amount)
                return await ctx.reply(f"Sold *{str(amount) + 'x'}* of `{_item['item_name']}` for **{sold_for}** <:carrots:822122757654577183>")

        if item_found is False:
            return await ctx.reply(f'Item `{item}` does not exist!')

    @eco_shop.command(name='use')
    async def eco_shop_use(self, ctx: Context, *, item: str):
        """Use an item that you have."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        usable_items = (i['item_name'] for i in _shop if i['item_type'] == 'Usable')
        user_db = await self.db.find_one({'_id': ctx.author.id})
        item = item.lower()
        if item not in usable_items:
            return await ctx.reply('That item cannot be used.')
        if user_db is None:
            return await ctx.send(f'You are not registered. Type `!register` to register. {ctx.author.mention}')
        items = []
        items_in_use = []
        for i in user_db['items_in_use']:
            if i['name'] == item:
                return await ctx.reply('That item is already in use.')
        index = 0
        for _item in user_db['items']:
            if _item['item_name'] == item:
                if _item['owned'] == 0:
                    return await ctx.reply('You do not have this item.')
                _item['owned'] -= 1
                _item_name = _item['item_name']
                now = datetime.datetime.utcnow()
                _expires_in = _shop[index]['expires_in']
                expires_in = now + relativedelta(**_expires_in)
                items_in_use.append({'name': item, 'expires_in': expires_in})
            items.append(_item)
            index += 1
        await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items_in_use': items_in_use, 'items': items}})
        await ctx.send(f'Now using the item `{_item_name}`')

    @eco_shop.command(name='using')
    async def eco_shop_using(self, ctx: Context):
        """See what items you have in use."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        user_db = await self.db.find_one({'_id': ctx.author.id})
        if user_db is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
        if len(user_db['items_in_use']) == 0:
            return await ctx.reply('You do not have any items in use currently.')

        in_use = []
        for item in user_db['items_in_use']:
            expires_in = time.human_timedelta(item['expires_in'])
            in_use.append({'name': item['name'], 'expires_in': f'Expires in: `{expires_in}`'})

        em = disnake.Embed(title='Here are your in-use items:')
        for i in in_use:
            em.add_field(name=i['name'].title(), value=i['expires_in'], inline=False)
        await ctx.send(embed=em)

    @commands.command(name='fish')
    @commands.cooldown(1, 30.0, commands.BucketType.member)
    async def eco_fish(self, ctx: Context):
        """
        Go fishing and sell the fish that you get, if you get any.
        ***Requires 1x fishing pool.***
        """

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        user_db = await self.db.find_one({'_id': ctx.author.id})
        if user_db is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))

        for item in user_db['items']:
            if item['item_name'] == 'fishing pole':
                if item['owned'] == 0:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply('You do not own a fishing pole.')
                break
        rn = random.randrange(-10, 161)

        items_ = []
        item_broke = False
        for item in user_db['items']:
            if item['item_name'] == 'fishing pole':
                item['uses'] -= 1
                uses = item['uses']
                if uses == 0:
                    item['owned'] -= 1
                    item['uses'] = int(''.join([str(i['uses']) for i in _shop if i['item_name'] == item['item_name']]))
                    item_broke = True
            items_.append(item)
        await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items_}})
        if item_broke is not False:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('Your fishing pole broke.')

        for fish in _fishes:
            chances = fish['chances']
            for i in user_db['items_in_use']:
                if i['name'] == 'clock':
                    chances = list(chances) + [111, 115, 120, 125, 135]
                    chances = tuple(chances)
                if i['name'] == 'alcohol':
                    chances = list(chances) + [-1, -5, -9, -7, 111, 115, 120, 125, 130, 117, 118, 130, 140, 150]
                    chances = tuple(chances)
            if rn in chances:
                items = []
                for item in user_db['items']:
                    if item['item_name'] == fish['fish']:
                        item['owned'] += 1
                    items.append(item)
                await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items}})
                return await ctx.send(f"You found `{fish['fish']}`")
        await ctx.send('You didn\'t find any fishes.')

    @commands.command(name='hunt')
    @commands.cooldown(1, 33.0, commands.BucketType.member)
    async def eco_hunt(self, ctx: Context):
        """
        Go hunting and sell the animals that you get, if you get any.
        ***Requires 1x hunting rifle.***
        """

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            ctx.command.reset_cooldown(ctx)
            return

        user_db = await self.db.find_one({'_id': ctx.author.id})
        if user_db is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))

        for item in user_db['items']:
            if item['item_name'] == 'hunting rifle':
                if item['owned'] == 0:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply('You do not own a hunting rifle.')
                break

        rn = random.randrange(-10, 161)
        items_ = []
        item_broke = False
        for item in user_db['items']:
            if item['item_name'] == 'hunting rifle':
                item['uses'] -= 1
                uses = item['uses']
                if uses == 0:
                    item['owned'] -= 1
                    item['uses'] = int(''.join([str(i['uses']) for i in _shop if i['item_name'] == item['item_name']]))
                    item_broke = True
            items_.append(item)
        await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items_}})
        if item_broke is not False:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('Your hunting rifle broke.')

        for animal in _animals:
            chances = animal['chances']
            for i in user_db['items_in_use']:
                if i['name'] == 'clock':
                    chances = list(chances) + [111, 115, 120, 125, 135]
                    chances = tuple(chances)
                if i['name'] == 'alcohol':
                    chances = list(chances) + [-1, -5, -9, -7, 111, 115, 120, 125, 130, 117, 118, 130, 140, 150]
                    chances = tuple(chances)
            if rn in chances:
                items = []
                for item in user_db['items']:
                    if item['item_name'] == animal['animal']:
                        item['owned'] += 1
                    items.append(item)
                await self.db.update_one({'_id': ctx.author.id}, {'$set': {'items': items}})
                return await ctx.send(f"You found `{animal['animal']}`")
        await ctx.send('You didn\'t find any animals.')

    @commands.command(name='search')
    @commands.cooldown(1, 25.0, commands.BucketType.member)
    async def eco_search(self, ctx: Context):
        """Search and get or lose carrots."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        user_db = await self.db.find_one({'_id': ctx.author.id})
        if user_db is not None:
            view = EcoSearchView(ctx)
            search1 = random.choice(all_search_choices)
            while True:
                search2 = random.choice(all_search_choices)
                if search2 != search1:
                    break
            while True:
                search3 = random.choice(all_search_choices)
                if search3 not in (search1, search2):
                    break
            for item in view.children:
                if item.label == '1':
                    item.label = search1
                elif item.label == '2':
                    item.label = search2
                elif item.label == '3':
                    item.label = search3
            view.message = await ctx.send('**Where do you want to search?**\n*Pick an option below to start searching that location*', view=view)
        else:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))

    @commands.command(name='passive')
    async def eco_passive(self, ctx: Context, *, option: str = None):
        """
        Turn passive `on` or `off`.
        If passive is on, people won't be able to rob you, but you won't be able to rob anyone as well, additionally, you cannot give or receive carrots from other people.

        *Note: There's a cooldown of 1 day between each change.*
        """  # noqa

        user_db = await self.db.find_one({'_id': ctx.author.id})
        if user_db is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
        elif option is None:
            return await ctx.send(f"Your current passive is {'**enabled.**' if user_db['passive'] is True else '**disabled.**'}")
        option = option.lower()
        options = {'on': True, 'off': False}

        if ctx.author.id != 374622847672254466:
            if datetime.datetime.utcnow() >= user_db['passive_cooldown']:
                if option not in ('on', 'off'):
                    return await ctx.reply('Not a valid option')
                elif options[option] == user_db['passive']:
                    return await ctx.reply(f"Your passive is already {'**enabled.**' if option == 'on' else '**disabled.**'}")
                updated_cooldown = datetime.datetime.utcnow() + relativedelta(days=1)
                await self.db.update_one({'_id': ctx.author.id}, {'$set': {'passive': options[option], 'passive_cooldown': updated_cooldown}})
                await ctx.reply(f"Passive has been {'**enabled.**' if option == 'on' else '**disabled.**'}")
            else:
                await ctx.reply(f"You can set your passive again in **{time.human_timedelta(user_db['passive_cooldown'])}**.")
        else:
            if option not in ('on', 'off'):
                return await ctx.reply('Not a valid option')
            elif options[option] == user_db['passive']:
                return await ctx.reply(f"Your passive is already {'**enabled.**' if option == 'on' else '**disabled.**'}")
            updated_cooldown = datetime.datetime.utcnow() + relativedelta(days=1)
            await self.db.update_one({'_id': ctx.author.id}, {'$set': {'passive': options[option], 'passive_cooldown': updated_cooldown}})
            await ctx.reply(f"Passive has been {'**enabled.**' if option == 'on' else '**disabled.**'}")

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bal'])
    async def balance(self, ctx: Context, member: disnake.Member = None):
        """Check your or another member's balance."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        member = member or ctx.author

        user_db = await self.db.find_one({"_id": member.id})
        if user_db is None:
            if member.id == member.id:
                ctx.command.reset_cooldown(ctx)
                await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            else:
                ctx.command.reset_cooldown(ctx)
                await ctx.send("User is not registered! %s" % (ctx.author.mention))
            return

        results = await self.db.find().sort([('wallet', -1)]).to_list(100000)
        index = 1
        for i in results:
            if i['_id'] == member.id:
                break
            index += 1

        em = disnake.Embed(title=f"{member.name}'s balance", color=Colours.light_pink)
        em.add_field(name="Wallet Balance", value="{} <:carrots:822122757654577183> ".format(format_balance(user_db['wallet'])), inline=False)
        em.add_field(name="Bank Balance", value="{} <:carrots:822122757654577183> ".format(format_balance(user_db['bank'])), inline=False)
        em.add_field(name="Total Balance", value="{} <:carrots:822122757654577183> ".format(format_balance(user_db['wallet'] + user_db['bank'])))
        em.set_footer(text="Rank: {}".format(index), icon_url=member.display_avatar)
        em.set_thumbnail(url=member.display_avatar)

        await ctx.send(embed=em)

    @balance.command(name='leaderboard', aliases=['lb', 'top'])
    async def eco_bal_leaderboard(self, ctx: Context):
        """See top richest people."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        index = 0
        data = []
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        guild = self.bot.get_guild(750160850077089853)

        results = await self.db.find().sort([("wallet", -1)]).to_list(100000)
        for result in results:
            if not result['wallet'] in (0, 0.0):
                index += 1
                mem = guild.get_member(result['_id'])
                if index in (1, 2, 3):
                    place = top_3_emojis[index]
                else:
                    place = f'`#{index:,}`'
                if mem == ctx.author:
                    to_append = (f'**{place} {mem.name} (YOU)**', f"**{result['wallet']:,}** <:carrots:822122757654577183>")
                    data.append(to_append)
                else:
                    to_append = (f'{place} {mem.name}', f"**{result['wallet']:,}** <:carrots:822122757654577183>")
                    data.append(to_append)
        source = FieldPageSource(data, per_page=10)
        source.embed.title = 'Top users with highest wallet balance'
        pages = RoboPages(source, ctx=ctx)
        await pages.start()

    @balance.command(name='add-bank')
    @commands.is_owner()
    async def add_bank(self, ctx: Context, amount: str = None, member: disnake.Member = None):
        """Add <:carrots:822122757654577183> in the member's bank."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})
        if results is None:
            await ctx.send("User not registered!")
            return

        if amount is None:
            await ctx.send("Please specify the amount of carrots you want to add!")
            return

        user = member

        amount = amount.replace(",", "")

        amount = int(amount)

        await self.db.update_one({"_id": user.id}, {"$inc": {"bank": amount}})

        await ctx.send("Successfully added **{:,}** <:carrots:822122757654577183> , and deposited them into the bank for `{}`!".format(amount, member))

    @balance.command(name='add-wallet')
    @commands.is_owner()
    async def add_wallet(self, ctx: Context, amount: str = None, member: disnake.Member = None):
        """Add <:carrots:822122757654577183> in the member's wallet."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})
        if results is None:
            await ctx.send("User not registered!")
            return

        if amount is None:
            await ctx.send("Please specify the amount of carrots you want to add!")
            return

        user = member

        amount = amount.replace(",", "")

        amount = int(amount)

        await self.db.update_one({"_id": user.id}, {"$inc": {"wallet": amount}})

        await ctx.send("Successfully added **{:,}** <:carrots:822122757654577183>  to the wallet for `{}`!".format(amount, member))

    @balance.command(name='set-bank')
    @commands.is_owner()
    async def set_bank(self, ctx: Context, amount: str = None, member: disnake.Member = None):
        """Set the amount of <:carrots:822122757654577183> in the member's bank."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})
        if results is None:
            await ctx.send("User not registered!")
            return

        if amount is None:
            await ctx.send("Please specify the amount of carrots you want to set!")
            return

        user = member
        amount = amount.replace(",", "")
        amount = int(amount)

        await self.db.update_one({"_id": user.id}, {"$set": {"bank": amount}})

        await ctx.send("Balance successfully set to **{:,}** <:carrots:822122757654577183>  in the bank for `{}`!".format(amount, member))

    @balance.command(name='reset')
    @commands.is_owner()
    async def eco_bal_reset(self, ctx: Context, member: disnake.Member = None):
        """Reset the member's <:carrots:822122757654577183>."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})
        if results is None:
            await ctx.send("User not registered!")
            return

        user = member

        await self.db.update_one({"_id": user.id}, {"$set": {"wallet": 0}})
        await self.db.update_one({"_id": user.id}, {"$set": {"bank": 0}})

        await ctx.send(f"Reseted balance for `{member}`.")

    @balance.command(name='set-wallet')
    @commands.is_owner()
    async def set_wallet(self, ctx: Context, amount: str = None, member: disnake.Member = None):
        """Set the amount of <:carrots:822122757654577183> in the member's wallet."""

        member = member or ctx.author

        results = await self.db.find_one({"_id": member.id})
        if results is None:
            await ctx.send("User not registered!")
            return

        if amount is None:
            await ctx.send("Please specify the amount of carrots you want to set!")
            return

        user = member

        amount = amount.replace(",", "")
        amount = int(amount)

        await self.db.update_one({"_id": user.id}, {"$set": {"wallet": amount}})

        await ctx.send("Balance successfully set to **{:,}** <:carrots:822122757654577183>  in the wallet for `{}`!".format(amount, member))

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx: Context, amount: str = None):
        """Withdraw the amount of <:carrots:822122757654577183> from your bank."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:

            if amount is None:
                await ctx.send('Please enter the amount you want to withdraw. %s' % (ctx.author.mention))
                return

            bal = results["bank"]

            if amount.lower() == "all":
                amount = bal

            try:
                amount = amount.replace(",", "")
            except AttributeError:
                pass
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.reply("Not a number!")

            if amount > bal:
                await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
                return

            elif bal < 1:
                await ctx.send("{} You do not have that much carrots in your bank. Carrots in bank: **{:,}**".format(ctx.author.mention, bal))
                return

            elif amount < 1:
                await ctx.send('Invalid amount. %s' % (ctx.author.mention))
                return

            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": amount}})
            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"bank": -amount}})

            await ctx.send("Successfully withdrew **{:,}** <:carrots:822122757654577183> ! {}".format(amount, ctx.author.mention))

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx: Context, amount: str = None):
        """Deposit the amount of <:carrots:822122757654577183> in your bank."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:

            if amount is None:
                await ctx.send('Please enter the amount you want to deposit. %s' % (ctx.author.mention))
                return

            bal = results["wallet"]

            if amount.lower() == "all":
                amount = bal
            try:
                amount = amount.replace(",", "")
            except AttributeError:
                pass
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.reply("Not a number!")

            if amount > bal:
                await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
                return

            elif bal < 1:
                await ctx.send("{} You do not have that much carrots in your wallet. Carrots in wallet: **{:,}**".format(ctx.author.mention, bal))
                return

            elif amount < 1:
                await ctx.send(f'Invalid amount. You cannot deposit **0** or **negative number** amount of <:carrots:822122757654577183>. {ctx.author.mention}')
                return

            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -amount}})
            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"bank": amount}})

            await ctx.send("Successfully deposited **{:,}** <:carrots:822122757654577183> ! {}".format(amount, ctx.author.mention))

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command(name='gift', aliases=['give'])
    async def bal_eco_give(self, ctx: Context, member: disnake.Member, amount: str = None):
        """Be a kind person and give some of your <:carrots:822122757654577183> from your **bank** to someone else's."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return

        results = await self.db.find_one({"_id": ctx.author.id})
        member_db = await self.db.find_one({'_id': member.id})

        if results is not None:
            user = member
            author = ctx.author

            if results['passive'] is True:
                return await ctx.reply('You cannot gift/give carrots because you have passive **enabled.**')
            elif member_db['passive'] is True:
                return await ctx.reply('That user cannot receive carrots because they have passive **enabled.**')

            if amount is None:
                await ctx.send('Please enter the amount you want to withdraw. %s' % (ctx.author.mention))
                return

            bal = results["wallet"]

            if amount.lower() == "all":
                amount = bal
            try:
                amount = amount.replace(",", "")
            except AttributeError:
                pass
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.reply("Not a number!")

            if amount > bal:
                await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
                return

            elif bal < 100:
                await ctx.send("{} You do not have that much carrots in your wallet. Carrots in wallet: **{:,}**".format(ctx.author.mention, bal))
                return

            if amount < 100:
                await ctx.send('You cannot give less than `100` <:carrots:822122757654577183> %s.' % (ctx.author.mention))
                return

            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.", member)
            view.message = msg = await ctx.send(f"{ctx.author.mention} wants to give you some carrots. Do you accept them {member.mention}?", view=view)
            await view.wait()
            if view.response is True:
                await self.db.update_one({"_id": author.id}, {"$inc": {"wallet": -amount}})
                await self.db.update_one({"_id": user.id}, {"$inc": {"wallet": amount}})
                e = f"{member.mention} accepted and got **{amount:,}** <:carrots:822122757654577183> from {ctx.author.mention}."
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = f"{member.mention} did not accept your <:carrots:822122757654577183>. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            return

    @commands.command(aliases=["steal"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def rob(self, ctx: Context, member: disnake.Member = None):
        """Rob someone of their <:carrots:822122757654577183> from their wallet."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        if member is None:
            await ctx.send("You must specify the person you want to rob/steal from. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return
        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:
            if member is ctx.author:
                await ctx.send("You cannot rob yourself. %s" % (ctx.author.mention))
                ctx.command.reset_cooldown(ctx)
                return

            user = member
            author = ctx.author

            user_db = await self.db.find_one({"_id": user.id})
            if user_db is None:
                return await ctx.reply('That member is not registered.')
            if results['passive'] is True:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply('You cannot rob because you have passive **enabled.**')
            elif user_db['passive'] is True:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply('You cannot rob that user because they have passive **enabled.**')

            user_bal = user_db["wallet"]

            author_bal = results["wallet"]

            if author_bal < 350:
                await ctx.send("You need `350` <:carrots:822122757654577183>  to rob someone! %s" % (ctx.author.mention))
                ctx.command.reset_cooldown(ctx)
                return

            if user_bal < 250:
                await ctx.send('The user must have at least `250` <:carrots:822122757654577183> ! %s' % (ctx.author.mention))
                ctx.command.reset_cooldown(ctx)
                return

            earnings = randint(250, user_bal)

            chance = randint(1, 10)

            if chance in (1, 3, 7, 10):
                await self.db.update_one({"_id": author.id}, {"$inc": {"wallet": earnings}})
                await self.db.update_one({"_id": user.id}, {"$inc": {"wallet": -earnings}})

                await ctx.send("You robbed **{}** and got **{:,}** <:carrots:822122757654577183> ! {}".format(member.display_name, earnings, ctx.author.mention))  # noqa

            else:
                await self.db.update_one({"_id": author.id}, {"$inc": {"wallet": -350}})

                await ctx.send("You failed in stealing from that person and you lost `350` <:carrots:822122757654577183> %s" % (ctx.author.mention))

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def slots(self, ctx: Context, amount: str = None):
        """Gamble your <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:

            if amount is None:
                await ctx.send('Please enter the amount. %s' % (ctx.author.mention))
                ctx.command.reset_cooldown(ctx)
                return

            bal = results["wallet"]

            if amount.lower() == "all":
                amount = bal
            try:
                amount = amount.replace(",", "")
            except AttributeError:
                pass
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.reply("Not a number!")

            if amount > bal:
                await ctx.send('You do not own that much carrots! %s' % (ctx.author.mention))
                ctx.command.reset_cooldown(ctx)
                return

            if amount < 300:
                await ctx.send('You must bet more than `300` <:carrots:822122757654577183>. %s' % (ctx.author.mention))
                ctx.command.reset_cooldown(ctx)
                return

            prefinal = []
            for i in range(3):
                a = random.choice(["❌", "🇴", "✨", "🔥", "<:tfBruh:784689708890324992>", "👑"])

                prefinal.append(a)

                final = "\u2800┃\u2800".join(prefinal)

            embed = disnake.Embed(
                color=Colours.light_pink,
                title="Slots!",
                description="<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>"
            )
            msg = await ctx.send(embed=embed)

            line1 = prefinal[0]
            line2 = prefinal[1]
            line3 = prefinal[2]

            if prefinal[0] == prefinal[1] == prefinal[2]:
                earned = 2.5 * amount

                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})

                wallet_amt = bal + earned

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title="Slots!",
                    description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>"
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=em)

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title="Slots!",
                    description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>"
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=em)
                winembed = disnake.Embed(
                    color=disnake.Color.green(),
                    title="WIN!",
                    description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800{line3}\n\n"
                    f"You bet a total of **{amount:,}** <:carrots:822122757654577183>  and won **{earned:,}** <:carrots:822122757654577183>. \n"
                    f"Now in wallet: **{wallet_amt:,}** <:carrots:822122757654577183>."
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=winembed)

            elif prefinal[0] == prefinal[1] or prefinal[0] == prefinal[2] or prefinal[2] == prefinal[1]:
                earned = amount

                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})

                wallet_amt = bal + earned

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title="Slots!",
                    description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>"
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=em)

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title="Slots!",
                    description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>"
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=em)

                winembed = disnake.Embed(
                    color=disnake.Color.green(),
                    title="WIN!",
                    description=f"{final}\n\nYou won **{amount:,}** <:carrots:822122757654577183>. \n"
                    f"Now in wallet: **{wallet_amt:,}** <:carrots:822122757654577183>."
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=winembed)

            else:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -amount}})
                wallet_amt = bal - amount

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title="Slots!",
                    description=f"{line1}\u2800┃\u2800<a:slotsshit:795232358306807868>\u2800┃\u2800<a:slotsshit:795232358306807868>"
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=em)

                em = disnake.Embed(
                    color=Colours.light_pink,
                    title="Slots!",
                    description=f"{line1}\u2800┃\u2800{line2}\u2800┃\u2800<a:slotsshit:795232358306807868>"
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=em)

                lostembed = disnake.Embed(
                    color=Colours.red, title="LOST!",
                    description=f"{final}\n\nYou bet a total amount of **{amount:,}** <:carrots:822122757654577183> but you lost them! :c\n"
                    f"Now in wallet: **{wallet_amt:,}** <:carrots:822122757654577183>."
                )
                await asyncio.sleep(0.7)
                await msg.edit(embed=lostembed)

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def beg(self, ctx: Context):
        """Beg for some <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:
            earnings = randint(100, 500)

            await ctx.send(f"Someone gave you **{earnings}** <:carrots:822122757654577183> !!")

            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earnings}})

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx: Context):
        """Work and get <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:

            await ctx.send("You worked and got **5,000** <:carrots:822122757654577183>. The carrots have been deposited into your bank!")

            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"bank": 5000}})

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def crime(self, ctx: Context):
        """Commit crimes that range between `small-medium-big`, and depending on which one you get, the more <:carrots:822122757654577183> you get, but be careful! You can lose the carrots as well."""  # noqa

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:

            aaaa = randint(1, 7)
            earnings = randint(500, 1500)
            earningss = randint(100, 420)
            earningsss = randint(400, 800)
            earningssss = randint(5000, 50000)
            losts = randint(300, 700)

            if aaaa == 2:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earnings}})

                await ctx.send("<:weird:773538796087803934> you commited a bigger crime and got **{:,}** <:carrots:822122757654577183>.".format(earnings))
                return

            if aaaa == 4:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningss}})
                await ctx.send("<:weird:773538796087803934> you commited a smaller crime and got **{:,}** <:carrots:822122757654577183>.".format(earningss))
                return

            if aaaa == 6:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningsss}})
                await ctx.send("<:weird:773538796087803934> you commited a medium crime and got **{:,}** <:carrots:822122757654577183>.".format(earningsss))
                return

            if aaaa == 7:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningssss}})
                await ctx.send("<:weird:773538796087803934> you commited a large crime and got **{:,}** <:carrots:822122757654577183>.".format(earningssss))
                return

            else:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -losts}})
                await ctx.send("You lost **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
                return

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command(name='guess-the-number', aliases=['gtn', 'guess'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eco_gtn(self, ctx: Context):
        """Play a guess the number game and earn <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:
            usercheck = ctx.author.id
            await ctx.send('Pick a number between 1 and 10.')

            lost_amt = randint(100, 400)
            win_amt = randint(130, 570)
            number = random.randint(1, 10)

            def check(message):
                return message.author.id == usercheck and message.channel.id == ctx.channel.id
            index = 0

            for guess in range(0, 3):
                while True:
                    try:
                        msg = await self.bot.wait_for('message', timeout=30, check=check)
                        attempt = int(msg.content)
                        break
                    except ValueError:
                        await msg.reply("Not a number! %s" % (ctx.author.mention))
                if attempt > number:
                    index += 1
                    if index == 3:
                        await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -lost_amt}})
                        await msg.reply(content=f"You didn't get it and lost **{lost_amt}** <:carrots:822122757654577183>. The number was **{number}**.")
                        return
                    await msg.reply('Try going lower.')

                elif attempt < number:
                    index += 1
                    if index == 3:
                        await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -lost_amt}})
                        await msg.reply(content=f"You didn't get it and lost **{lost_amt}** <:carrots:822122757654577183>. The number was **{number}**.")
                        return
                    await msg.reply('Try going higher.')

                else:
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": win_amt}})
                    await msg.reply(f'You guessed it! Good job! You got **{win_amt}** <:carrots:822122757654577183>. The number was **{number}**.')
                    return
        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ppsuck(self, ctx: Context):
        """Suck some pp 😳 for some quick <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:
            aaaa = randint(1, 7)
            bbbb = randint(1, 100)
            earnings = randint(800, 2500)
            earningss = randint(300, 620)
            earningsss = randint(600, 1200)
            earningssss = randint(20000, 150000)
            earningssssss = randint(500000, 5000000)
            losts = randint(1000, 1200)

            try:
                if bbbb == 1:
                    earned = earningssssss
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})

                    await ctx.send(
                        f":smirk: :smirk: :yum: you sucked your crush and they loved it, you ended up dating and got **{earned:,}** <:carrots:822122757654577183>."  # noqa
                    )
                    return

                elif aaaa == 1:
                    earned = earnings
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})

                    await ctx.send(":yum: you sucked ur dad's pp and got **{:,}** <:carrots:822122757654577183>.".format(earned))
                    return

                elif aaaa == 4:
                    earned = earningss
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})

                    await ctx.send(
                        f"<:weird:773538796087803934> you didn't do too good of a job at sucking but it wasn't too bad either and got **{earned:,}** <:carrots:822122757654577183>."  # noqa
                    )
                    return

                elif aaaa == 6:
                    earned = earningsss
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})

                    await ctx.send(
                        f"<:weird:773538796087803934> you didn't do too bad, but u didn't do too good either at sucking ur dog's pp and got **{earned:,}** <:carrots:822122757654577183>."  # noqa
                    )
                    return

                elif aaaa == 7:
                    earned = earningssss
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earned}})
                    await ctx.send(
                        f":smirk: You sucked your best friend and they liked it very much and decided to gave you **{earned:,}** <:carrots:822122757654577183>"
                    )
                    return

                else:
                    await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -losts}})
                    await ctx.send("You did a fucking bad job at sucking and lost **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))

            except Exception:
                ctx.command.reset_cooldown(ctx)
                return
        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def race(self, ctx: Context):
        """Participate in a race and earn <:carrots:822122757654577183>."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})

        if results is not None:

            aaaa = randint(1, 7)
            bbbb = randint(1, 100)
            earnings = randint(800, 2500)
            earningss = randint(300, 620)
            earningsss = randint(600, 1200)
            earningssss = randint(20000, 150000)
            earningssssss = randint(500000, 5000000)
            losts = randint(1000, 1200)

            if aaaa == 1:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earnings}})
                await ctx.send(":third_place: you won the race 3rd place an won: **{:,}** <:carrots:822122757654577183>.".format(earnings))
                return

            elif aaaa == 4:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningss}})
                await ctx.send(
                    f"U were close to lose the race by getting 5th place. You got a total of: **{earningss:,}** <:carrots:822122757654577183>."
                )
                return

            elif aaaa == 6:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningsss}})
                await ctx.send("After winning on 4th place you got: **{:,}** <:carrots:822122757654577183>.".format(earningsss))
                return

            elif aaaa == 7:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningssss}})
                await ctx.send(":sparkles: :second_place: after winning on the 2nd place, you won: **{:,}** <:carrots:822122757654577183>.".format(earningssss))
                return

            elif bbbb == 1:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": earningssssss}})
                await ctx.send(
                    f":sparkles: :first_place: :medal: :sparkles: after winning the race on the first place you won a total of: **{earningssssss:,}** <:carrots:822122757654577183>."  # noqa
                )
                return

            else:
                await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": -losts}})
                await ctx.send("Sadly you lost the race, your lost consists of **{:,}** <:carrots:822122757654577183>  from your wallet.".format(losts))
                return

        else:
            await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))
            ctx.command.reset_cooldown(ctx)
            return

    @commands.command(name='rock-paper-scissors', aliases=['rps'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def eco_rps(self, ctx: Context):
        """Play a game of rock-paper-scissors with the bot and earn <:carrots:822122757654577183> if you win or lose some if you lose the game."""

        if ctx.channel.id not in (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061):
            return ctx.command.reset_cooldown(ctx)

        results = await self.db.find_one({"_id": ctx.author.id})
        if results is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You are not registered! Type: `!register` to register. %s" % (ctx.author.mention))

        view = RPSView(self.db, ctx)
        view.message = await ctx.send('Please choose by clicking one of the buttons below.', view=view)

    @slots.error
    async def slots_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            await self.bot.reraise(ctx, error)

        else:
            await self.bot.reraise(ctx, error)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == 374622847672254466:
            return
        await self.db.delete_one({"_id": member.id})


def setup(bot):
    bot.add_cog(Economy(bot))
