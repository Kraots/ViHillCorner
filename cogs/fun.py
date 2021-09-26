import disnake
from disnake.ext import commands
import random
from random import randint
from utils.helpers import time_phaser
import asyncio
import games
import aiohttp
import utils.colors as color
import functools
from utils.helpers import replace_many, suppress_links
from utils.pillow import invert_pfp
import akinator
import inspect

UWU_WORDS = {
    "fi": "fwi",
    "l": "w",
    "r": "w",
    "some": "sum",
    "th": "d",
    "thing": "fing",
    "tho": "fo",
    "you're": "yuw'we",
    "your": "yur",
    "you": "yuw",
}

class AkinatorView(disnake.ui.View):
    def __init__(self, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.response = None
    
    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'Only {self.ctx.author.display_name} can use the buttons on this message!', ephemeral=True)
            return False
        return True
    
    @disnake.ui.button(label='Yes', style=disnake.ButtonStyle.green)
    async def _yes_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'yes'
        self.stop()

    @disnake.ui.button(label='No', style=disnake.ButtonStyle.red)
    async def _no_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'no'
        self.stop()

    @disnake.ui.button(label='I don\'t know')
    async def _idk_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'idk'
        self.stop()

    @disnake.ui.button(label='Probably', row=1)
    async def _probs_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'probably'
        self.stop()

    @disnake.ui.button(label='Probably not', row=1)
    async def _probs_not_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'probably not'
        self.stop()
    
    @disnake.ui.button(label='Back', row=1)
    async def _back_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'back'
        self.stop()
    
    @disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red, row=2)
    async def _quit_butt(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'quit'
        self.stop()

class BagelsView(disnake.ui.View):
    def __init__(self, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.response = None
        self.ctx = ctx
    
    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'Only {self.ctx.author.display_name} can use the buttons on this message!', ephemeral=True)
            return False
        return True
    
    @disnake.ui.button(label='Start', style=disnake.ButtonStyle.green)
    async def start(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'start'
        for item in self.children:
            item.disabled = True
            if item.label != button.label:
                item.style = disnake.ButtonStyle.grey
            else:
                item.style = disnake.ButtonStyle.blurple
        self.stop()
    
    @disnake.ui.button(label='Cancel', style=disnake.ButtonStyle.red)
    async def cancel(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.response = 'cancel'
        for item in self.children:
            item.disabled = True
            if item.label != button.label:
                item.style = disnake.ButtonStyle.grey
            else:
                item.style = disnake.ButtonStyle.blurple
        self.stop()

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db1['Economy']
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.command()
    async def ppsize(self, ctx, member: disnake.Member = None):
        """How big is your pp 😳"""

        member = member or ctx.author
        
        em = disnake.Embed(color = member.color, title="peepee size machine")
        if member.id == 374622847672254466:
            em.description = "`Kraots`'s penis\n8=============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================D"
        else:
            pre_size = []
            for i in range(randint(0 , 25)):
                pre_size.append("=")
            size = "".join(pre_size)
            em.description = f"`{member.name}`'s penis\n8{size}D"
        em.set_footer(text=f"Requested by: {ctx.author}", icon_url = ctx.author.display_avatar)

        await ctx.send(embed=em)

    @commands.command()
    async def gayrate(self, ctx, member : disnake.Member=None):
        """Are you gay 🤔"""
        
        gayrate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Gay rating machine', description='You are 0% gay :gay_pride_flag:', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Gay rating machine', description=f'You are {gayrate}% gay :gay_pride_flag:', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Gay rating machine', description='You are 0% gay :gay_pride_flag:', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Gay rating machine', description=f'You are {gayrate}% gay :gay_pride_flag:', color=randomcolour)
            
            await ctx.send(embed=embed1)

        else:
            if member.id == 374622847672254466:
                embed2 = disnake.Embed(title='Gay rating machine', description=f'{member.name} is 0% gay :gay_pride_flag:', color=randomcolour)
            
            else:
                embed2 = disnake.Embed(title='Gay rating machine', description=f'{member.name} is {gayrate}% gay :gay_pride_flag:', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def susrate(self, ctx, member : disnake.Member=None):
        """Are you sus 🤔"""
        
        susrate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Sus rating machine', description='You are 0% sus <:pepe_sus:750751092459044926>', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Sus rating machine', description=f'You are {susrate}% sus <:pepe_sus:750751092459044926>', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Sus rating machine', description='You are 0% sus <:pepe_sus:750751092459044926>', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Sus rating machine', description=f'You are {susrate}% sus <:pepe_sus:750751092459044926>', color=randomcolour)
            
            await ctx.send(embed=embed1)

        else:
            if member.id == 374622847672254466:
                embed2 = disnake.Embed(title='Sus rating machine', description=f'{member.name} is 0% sus <:pepe_sus:750751092459044926>', color=randomcolour)
            
            else:
                embed2 = disnake.Embed(title='Sus rating machine', description=f'{member.name} is {susrate}% sus <:pepe_sus:750751092459044926>', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def simprate(self, ctx, member : disnake.Member=None):
        """Are you a simp 🤔"""

        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Simp rating machine', description='You are 0% simp ', color=randomcolour)
            else:
                embed1 = disnake.Embed(title='Simp rating machine', description=f'You are {simprate}% simp ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Simp rating machine', description='You are 0% simp ', color=randomcolour)
            else:
                embed1 = disnake.Embed(title='Simp rating machine', description=f'You are {simprate}% simp ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        else:
            if member.id == 374622847672254466:
                embed2 = disnake.Embed(title='Simp rating machine', description=f'{member.name} is 0% simp ', color=randomcolour)
            else:
                embed2 = disnake.Embed(title='Simp rating machine', description=f'{member.name} is {simprate}% simp ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def straightrate(self, ctx, member : disnake.Member=None):
        """Are you straight 🤔"""

        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Straight rating machine', description='You are 100% straight ', color=randomcolour)
            else:
                embed1 = disnake.Embed(title='Straight rating machine', description=f'You are {simprate}% straight ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Straight rating machine', description='You are 100% straight ', color=randomcolour)
            else:
                embed1 = disnake.Embed(title='Straight rating machine', description=f'You are {simprate}% straight ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        else:
            if member.id == 374622847672254466:
                embed2 = disnake.Embed(title='Straight rating machine', description=f'{member.name} is 100% straight ', color=randomcolour)
            else:
                embed2 = disnake.Embed(title='Straight rating machine', description=f'{member.name} is {simprate}% straight ', color=randomcolour)
            
            await ctx.send(embed=embed2)

    @commands.command()
    async def hornyrate(self, ctx, member : disnake.Member=None):
        """How horny are you 😳 😏"""

        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Horny rating machine', description='You are 100% horny ', color=randomcolour)
            else:
                embed1 = disnake.Embed(title='Horny rating machine', description=f'You are {simprate}% horny ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Horny rating machine', description='You are 100% horny ', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Horny rating machine', description=f'You are {simprate}% horny ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        else:
            if member.id == 374622847672254466:
                embed2 = disnake.Embed(title='Horny rating machine', description=f'{member.name} is 100% horny ', color=randomcolour)
            
            else:
                embed2 = disnake.Embed(title='Horny rating machine', description=f'{member.name} is {simprate}% horny ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def boomerrate(self, ctx, member : disnake.Member=None):
        """Are you a boomer 🤔"""

        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Boomer rating machine', description='You are 0% boomer ', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Boomer rating machine', description=f'You are {simprate}% boomer ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            if ctx.author.id == 374622847672254466:
                embed1 = disnake.Embed(title='Boomer rating machine', description='You are 0% boomer ', color=randomcolour)

            else:
                embed1 = disnake.Embed(title='Boomer rating machine', description=f'You are {simprate}% boomer ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        else:
            if member.id == 374622847672254466:
                embed2 = disnake.Embed(title='Boomer rating machine', description=f'{member.name} is 0% boomer ', color=randomcolour)

            else:	
                embed2 = disnake.Embed(title='Boomer rating machine', description=f'{member.name} is {simprate}% boomer ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Ask a question and i shall give you an answer."""

        responses = [
                    "it is certain",
                    "it is undoubtedly so",
                    "without a doubt!! x3",
                    "yes - definitely!! ",
                    "you may rely on it",
                    "as I see it, yes",
                    "most likely",
                    "outlook good",
                    "yes!!",
                    "signs point to ye.",
                    "reply hazy, try again",
                    "ask again later",
                    "better not tell you now",
                    "cannot predict now",
                    "concentrate and ask again",
                    "don't count on it",
                    "my reply is no",
                    "my sources say no",
                    "outlook not so good",
                    "yery doubtful",
                    "definetly not",
                    "don't tell anyone, but definitely yes",
                    "no!!",
                    "daddy... sadly yes",
                    "it's a secret friend...",
                    "don't tell anyone but not a chance ^_^",
                    "xD yus dad!!",
                    "daddy... positive",
                    "hell yeah",
                    "maybe! :(",
                    "only for today.",
                    "ok, whatever yes",
                    ".-. no onee-san!!",
                    " heck off, you know that's a no",
                    " hell to the yes",
                    "only for today",
                    "when you grow a braincell, yes",
                    "negative",
                    " it's a secret senpai...",
                    "hell no! :(",
                    " honestly I don't care lol",
                    "master... no",
                    "yus",
                    "only for today! ;x",
                    "it's a secret",
                    "im an 8ball, not a deal with ur shit ball",
                    "sadly yes silly...",
                    "not a chance! c:",
                    "sadly yes!!",
                    "sir... nu",
                    "UwU hell yeah b-baka!!",
                    "don't tell anyone but never ._.",
                    "don't tell anyone but only for today ^_^",
                    "friend... negative",
                    "senpai... of course",
                    "of course",
                    "of course! ;c",
                    "don't tell anyone but sadly yes :)",
                    "not today!!",
                    "sadly no love...",
                    "sadly no! :(",
                    "only today daddy...",
                    "you bet.",
                    "negative master...",
                    "positive! :x",
                    "sadly no",
                    "don't tell anyone but you bet :)",
                    "^_^ of course ma'am!!",
                    "yes silly...",
                    "only today",
                    "no senpai...",
                    "yes! UwU",
                    "silly... yus",
                    "no.",
                    "no! c;",
                    "don't tell anyone but nu! :)",
                    "hell no" ,
                    "mom... yus",
                    "b-baka... sadly no",
                    "don't tell anyone but it's a secret! ;c",
                    "hell yeah!!",
                    "hell yeah! :(",
                    "don't tell anyone but yes ;c",
                    "only today.",
                    "don't tell anyone but no ( ͡° ͜ʖ ͡°)",
                    ";-; not a chance b-baka!!",
                    "UwU it's a secret love!!",
                    "honey... sadly yes",
                    "nii-san... nu",
                    "c: hell no mom!!",
                    "yus love...",
                    ":x sadly no onee-san!!",
                    "hell yeah! :x",
                    "don't tell anyone but nu :x",
                    "i can tell you certainly, no",
                    "don't tell anyone but only for today .-.",
                    "positive! ;x",
                    "don't tell anyone but only for today >///<",
                    " im not sure but ur def stupid",
                    "ma'am... of course",
                    "no???",
                    "no, you dingleberry",
                    "don't tell anyone but positive ^_^",
                    "sure, why not!",
                    "don't tell anyone but yus ;-;",
                    "sure, I literally couldn't care less",
                    "yes, idiot",
                    "^_^ sadly yes silly!!",
                    "don't tell anyone but no >///<",
                    "nu!!",
                    "lol literally no",
                    "don't tell anyone but nu xD",
                    ".-. only today friend!!",
                    "dad... sadly yes",
                    "dont sass me bitch",
                    " not a chance.",
                    "sadly yes! ._.",
                    "never",
                    "no!!!!",
                    "nii-san... hell no",
                    "you bet!!",
                    "don't tell anyone but never ;x",
                    "yus.",
                    "yus friend...",
                    "only today!!",
                    "hell no! UwU",
                    "hell yeah love...",
                    "sadly yes! .-.",
                    "don't tell anyone but it's a secret :c",
                    "no sir...",
                    ";-; positive ma'am!!",
                    "maybe mom...",
                    "don't tell anyone but not today ^_^",
                    "don't tell anyone but never c;",
                    "dad... only today",
                    "not a chance! xD",
                    "._. never sir!!",
                    "OwO hell yeah mom!!",
                    "you bet! UwU",
                    "don't tell anyone but not today OwO",
                    "^_^ you bet love!!",
                    "only today! ._.",
                    "hell yeah nii-san...",
                    "it's secret love!!",
                    "onee-san... negative",
                    "don't tell anyone but never :)",
                    "yes dad...",
                    "maybe! OwO",
                    "positive",
                    "sadly no mom...",
                    "sir... positive",
                    "only today! ;c",
                    "OwO yes onee-san!!",
                    "silly... not a chance",
                    "honey... never",
                    "negative silly...",
                    "don't tell anyone but you bet >///<",
                    "don't tell anyone but maybe :)",
                    "friend... hell yeah",
                    ":) hell yeah master!!",
                    "hell yeah honey...",
                    "not today.",
                    "love... negative",
                    "c: only for today honey!!",
                    "positive!!",
                    "never! :(",
                    "nu friend...",
                    "dad... positive",
                    "nu b-baka...",
                    "xD no sir!!",
                    "hell yeah! c:",
                    "of course silly...",
                    "nii-san... no",
                    "xD yes mom!!",
                    "c; yus dad!!",
                    "._. sadly yes sir!!",
                    "no mommy...",
                    "^_^ only today honey!!",
                    "don't tell anyone but sadly no >///<",
                    "friend... yus",
                    "OwO only today onee-san!!",
                    "sadly no! OwO",
                    "don't tell anyone but hell yeah >///<",
                    "it's a secret nii-san...",
                    "don't tell anyone but negative .-.",
                    "honey... it's a secret",
                    "friend... only today",
                    "positive friend...",
                    "negative friend...",
                    " don't tell anyone but maybe ( ͡° ͜ʖ ͡°)",
                    " don't tell anyone but yes ( ͡° ͜ʖ ͡°)",
                    "c; of course b-baka!!",
                    "never! ;c",
                    "sadly no sir...",
                    "not a chance! ^_^",
                    "negative!!",
                    "positive nii-san...",
                    "nu",
                    "positive.",
                    "don't tell anyone but negative OwO",
                    "don't tell anyone but yus :c",
                    "don't tell anyone but hell no UwU",
                    "sadly no!!",
                    "don't tell anyone but only for today c;",
                    "no",
                    "yes",
                    "hell no! :x",
                    "don't tell anyone but no c:",
                    "hell yeah sir...",
                    "no! ( ͡° ͜ʖ ͡°)",
                    "yes! ( ͡° ͜ʖ ͡°)",
                    "no dad...",
                    "no! .-.",
                    "don't tell anyone but positive UwU",
                    "nii-san... of course",
                    ":c you bet ma'am!!",
                    "maybe",
                    "only for today mommy...",
                    "it's a secret.",
                    "not today c;",
                    "of course! >///<",
                    "nu.",
                    "maybe! xD",
                    "no! :)",
                    "maybe! UwU",
                    "only for today mom...",
                    "mom... negative",
                    "c; not today dad!!",
                    "only today! >///<",
                    "don't tell anyone but nu ;x",
                    "don't tell anyone but yus ;c",
                    "UwU positive mom!!",
                    "yus!!",
                    ";x only today dad!!",
                    "don't tell anyone but of course >///<"

                    ]
        await ctx.send(f':8ball:** | {ctx.author.name} asked:** {question}\n<:blank:788666214318735360>** | Answer:** {random.choice(responses)}')


    @commands.command()
    async def fight(self, ctx, p2: disnake.Member):
        """Have an interactive fight with someone."""

        if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
            return

        if p2 == ctx.author:
            return await ctx.reply('You cannot fight with yourself.')

        p1 = ctx.author
        view = self.bot.confirm_view(ctx, f"{p2.mention} Did not react in time.", p2)
        view.message = msg = await ctx.send(f"**{p1.display_name}** wants to have a fight with you, do you accept? {p2.mention}", view=view)
        await view.wait()
        if view.response is True:
            await msg.delete()
            players = [ctx.author, p2]
            random.shuffle(players)
            f = games.Fight(players[0], players[1], ctx)
            f.message = await ctx.send(f'You start: {players[0].mention}', view=f)
            return

        elif view.response is False:
            return await msg.edit(content=f"**{p2.display_name}** does not want to fight with you **{p1.display_name}**", view=view)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def vampify(self, ctx, *args):
        """Adds a <:vampy:773535195210973237> between each word of your text."""

        vampify = " <:vampy:773535195210973237> ".join(args)
        await ctx.send(vampify)
        await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def clapify(self, ctx, *args):
        """Adds a 👏 between each word of your text."""

        clapify = " 👏 ".join(args)
        await ctx.send(clapify)
        await ctx.message.delete()

    @commands.command()
    async def cat(self, ctx):
        """Get a random image of a cat ❤️"""

        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://aws.random.cat/meow") as r:
                data = await r.json()

            imgUrl = data['file']

            embed = disnake.Embed(title="Cat", url=imgUrl, color=color.orange, timestamp=ctx.message.created_at.replace(tzinfo=None))
            embed.set_image(url=imgUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❤️")
            await msg.add_reaction("😸")

    @commands.command()
    async def dog(self, ctx): 
        """Sends a random image of a dog ❤️"""

        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://random.dog/woof.json") as r:
                data = await r.json()

            embed = disnake.Embed(title="Dog", url=data['url'], color=color.orange, timestamp=ctx.message.created_at.replace(tzinfo=None))
            embed.set_image(url=data['url'])
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❤️")
            await msg.add_reaction("🐶")

    @commands.command()
    async def meme(self, ctx):
        """Get a random meme"""
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/random/.json') as r:
                res = await r.json()
                imgUrl = res[0]['data']['children'] [0]['data']
                linkUrl = imgUrl['url']
                titleUrl = imgUrl['title']
                
                embed = disnake.Embed(color=color.orange, title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at.replace(tzinfo=None))
                embed.set_image(url=linkUrl)
                embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)

                await ctx.send(embed=embed)

    @commands.command(name='tic-tac-toe', aliases=['ttt'])
    async def _tictactoe(self, ctx, member: disnake.Member = None):
        """Play a game of tictactoe against someone."""

        if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
            return

        if member is None:
            return await ctx.send(f"You must mention the person you wish to have a tic-tac-toe game with. {ctx.author.mention}")
        elif member is ctx.author:
            return await ctx.send(f"You cannot play with yourself. {ctx.author.mention}")

        user = await self.db.find_one({'_id': ctx.author.id})
        opponent = await self.db.find_one({'_id': member.id})
        
        if user is None:
            await ctx.send(f"{ctx.author.mention} You must first register. To do that type `!register`")
            return		
        if opponent is None:
            await ctx.send(f"**{member.display_name}** is not registered. {ctx.author.mention}")
            return
        
        if user['wallet'] < 10000:
            await ctx.send(f"You must have `10,000` <:carrots:822122757654577183> in your wallet to play. {ctx.author.mention}")
            return
        if opponent['wallet'] < 10000:
            await ctx.send(f"**{member.display_name}** does not have `10,000` <:carrots:822122757654577183> in their wallet. Cannot play. {ctx.author.mention}")
            return

        view = self.bot.confirm_view(ctx, f"{member.mention} Did not react in time.", member)
        view.message = msg = await ctx.send(f"**{ctx.author.mention}** Wants to play tic-tac-toe with you {member.mention}. Do you accept?\nWinner gets **10,000** <:carrots:822122757654577183>\nLoser loses **10,000** <:carrots:822122757654577183>", view=view)
        await view.wait()
        if view.response is True:
            await msg.delete()
            players = [ctx.author, member]
            random.shuffle(players)
            ttt_view = games.TicTacToe(players[0], players[1], ctx)
            ttt_view.message = await ctx.send(f'You start: {players[0].mention}', view=ttt_view)
            return
            
        elif view.response is False:
            e = f"**{member.mention}** does not want to play tic-tac-toe with you."
            return await msg.edit(content=e, view=view)

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """Reverses the text."""

        await ctx.send(f'> {text[::-1]}')

    @commands.command()
    async def uwu(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
        """Converts the text to its uwu equivalent."""

        conversion_func = functools.partial(replace_many, replacements=UWU_WORDS, ignore_case=True, match_case=True)
        converted_text = conversion_func(text)
        converted_text = suppress_links(converted_text)
        await ctx.send(f'> {converted_text}')

    @commands.command()
    async def invert(self, ctx, member: disnake.Member = None):
        """Inverts the colors of the member's pfp."""

        member = member or ctx.author
        pfp = await invert_pfp(member)
        em = disnake.Embed(color=color.lightpink, title='Here\'s your inverted avatar image:')
        em.set_image(url=f'attachment://{member.display_name}_inverted_avatar.png')
        em.set_footer(text=f"Requested by: {ctx.author}", icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em, file=pfp)
    
    @commands.command(name='akinator', aliases=['aki'])
    async def _akinator(self, ctx):
        """Play a game with akinator."""

        if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
            return

        aki_em = disnake.Embed(title='Akinator', description='Starting game...')
        msg = await ctx.send(embed=aki_em)
        aki = akinator.Akinator()
        q = aki.start_game()
        
        while aki.progression <= 90:
            view = AkinatorView(ctx)
            aki_em.description = q
            await msg.edit(embed=aki_em, view=view)
            await view.wait()
            if view.response == None:
                for item in view.children:
                    item.disabled = True
                    item.style = disnake.ButtonStyle.grey
                aki_em.description = 'Ran out of time.'
                return await msg.edit(embed=aki_em, view=view)
            elif view.response == 'quit':
                for item in view.children:
                    item.disabled = True
                    if item.label == 'quit':
                        item.style = disnake.ButtonStyle.blurple
                    else:
                        item.style = disnake.ButtonStyle.grey
                aki_em.description = 'Quit the game.'
                return await msg.edit(embed=aki_em, view=view)
            elif view.response == 'back':
                try:
                    q = aki.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                q = aki.answer(view.response)
        aki.win()
        em = disnake.Embed(title='Akinator', description=f'**{aki.first_guess["name"]}**\n{aki.first_guess["description"]}')
        em.set_image(url=aki.first_guess['absolute_picture_path'])
        view = self.bot.confirm_view(ctx)
        view.message = await msg.edit(embed=em, view=view)
        await view.wait()
        if view.response == True:
            em.colour = disnake.Color.green()
            em.set_footer(text='It seems like I win :D')
            await msg.edit(embed=em, view=view)
        elif view.response == False:
            em = disnake.Embed(color=disnake.Color.red(), title='Akinator', description='Oof. It seems like this was too hard for me to guess.')
            await msg.edit(embed=em, view=view)

    @commands.command()
    async def bagels(self, ctx):
        """Play a game of bagels."""

        if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
            return

        em = disnake.Embed(color=color.light_blue, title='Bagels, a deductive logic game', description='I am thinking of a 3-digit number with no repeated digits.')
        em.add_field(name='When I say', value='Pico\nFermi\nBagels')
        em.add_field(name='That means', value='One digit is correct but in the wrong position.\nOne digit is correct and in the right position.\nNo digit is correct.')
        em.add_field(name='Example', value='If the secret number was 248 and your guess was 843, the clues would be Fermi Pico.', inline=False)
        em.set_footer(text='You can quit the game by typing ``quit``')
        view = BagelsView(ctx)
        msg = await ctx.send(embed=em, view=view)
        await view.wait()
        if view.response is None:
            em = disnake.Embed(description='Ran out of time.', color=color.light_blue)
            return await msg.edit(embed=em, view=view)
        elif view.response == 'cancel':
            em = disnake.Embed(description='Canceled.', color=color.light_blue)
            return await msg.edit(embed=em, view=view)
        else:
            await msg.edit(view=view)
            def check(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            guesses = 10
            digits = 3
            letters = random.sample('0123456789', digits)
            if letters[0] == '0':
                letters.reverse()
            number = ''.join(letters)
            counter = 1
            while True:
                await ctx.send(f'Input your guess #{counter}:')
                try:
                    ans = await self.bot.wait_for('message', check=check, timeout=180.0)
                    guess = ans.content
                    if guess in ('quit', 'q', '!cancel', 'exit'):
                        return await ans.reply('Quit the game.')
                except asyncio.TimeoutError:
                    return await ctx.reply('Took too much to give an answer.')
                else:
                    if len(guess) != digits:
                        await ctx.send('Wrong number of digits. Try again!')
                        continue
                    
                    clues = []
                    for index in range(digits):
                        if guess[index] == number[index]:
                            clues.append('Fermi')
                        elif guess[index] in number:
                            clues.append('Pico')
                    random.shuffle(clues)

                    if len(clues) == 0:
                        await ctx.send('Bagels')
                    else:
                        await ctx.send(' '.join(clues))
                    counter += 1

                    if guess == number:
                        return await ctx.send(f'You got it! The number was `{guess}`\nHere\'s your 🥯')
                    if counter > guesses:
                        return await ctx.send(f'You ran out of guesses. The answer was `{number}`')

    @vampify.error
    async def vampify_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"You're on cooldown, try again in {time_phaser(error.retry_after)}.")
        elif isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            await self.bot.reraise(ctx, error)
        else:
            await self.bot.reraise(ctx, error)

    @clapify.error
    async def clapify_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"You're on cooldown, try again in {time_phaser(error.retry_after)}.")
        elif isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            await self.bot.reraise(ctx, error)
        else:
            await self.bot.reraise(ctx, error)
        
    @fight.error
    async def fight_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(error.original)
        else:
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Fun(bot))