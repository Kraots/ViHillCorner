import discord
from discord.ext import commands
import random
from random import randint
import utils.colors as color
import asyncio

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.command()
    async def gayrate(self, ctx, member : discord.Member=None):
        gayrate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            embed1 = discord.Embed(title='Gay rating machine', description=f'You are {gayrate}% gay :gay_pride_flag:', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            embed1 = discord.Embed(title='Gay rating machine', description=f'You are {gayrate}% gay :gay_pride_flag:', color=randomcolour)

            await ctx.send(embed=embed1)

        else:
            embed2 = discord.Embed(title='Gay rating machine', description=f'{member.name} is {gayrate}% gay :gay_pride_flag:', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def simprate(self, ctx, member : discord.Member=None):
        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            embed1 = discord.Embed(title='Simp rating machine', description=f'You are {simprate}% simp ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            embed1 = discord.Embed(title='Simp rating machine', description=f'You are {simprate}% simp ', color=randomcolour)

            await ctx.send(embed=embed1)

        else:
            embed2 = discord.Embed(title='Simp rating machine', description=f'{member.name} is {simprate}% simp ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def straightrate(self, ctx, member : discord.Member=None):
        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            embed1 = discord.Embed(title='Straight rating machine', description=f'You are {simprate}% straight ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            embed1 = discord.Embed(title='Straight rating machine', description=f'You are {simprate}% straight ', color=randomcolour)

            await ctx.send(embed=embed1)

        else:
            embed2 = discord.Embed(title='Straight rating machine', description=f'{member.name} is {simprate}% straight ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def hornyrate(self, ctx, member : discord.Member=None):
        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            embed1 = discord.Embed(title='Horny rating machine', description=f'You are {simprate}% horny ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            embed1 = discord.Embed(title='Horny rating machine', description=f'You are {simprate}% horny ', color=randomcolour)

            await ctx.send(embed=embed1)

        else:
            embed2 = discord.Embed(title='Horny rating machine', description=f'{member.name} is {simprate}% horny ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command()
    async def boomerrate(self, ctx, member : discord.Member=None):
        simprate = randint(1, 100)
        randomcolour = randint(0, 0xffffff)

        if member is None:
            embed1 = discord.Embed(title='Boomer rating machine', description=f'You are {simprate}% boomer ', color=randomcolour)
            
            await ctx.send(embed=embed1)

        elif member is ctx.author:
            embed1 = discord.Embed(title='Boomer rating machine', description=f'You are {simprate}% boomer ', color=randomcolour)

            await ctx.send(embed=embed1)

        else:
            embed2 = discord.Embed(title='Boomer rating machine', description=f'{member.name} is {simprate}% boomer ', color=randomcolour)
            await ctx.send(embed=embed2)

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
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
                    "only today!!"
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
    async def fight(self, ctx):
            message = ctx.message
            args = message.content.split()
            loss = 0
            rounds = 1
            init = message.author.mention
            target = " ".join(args[1:])
            fight = "%s has challenged %s to a fight!" % (init, target) + "\n"
            fightEm = discord.Embed(description=fight, colour=color.reds)
            fightEm.set_author(name="Fight")
            fMessage = await message.channel.send(embed=fightEm)
            while not (loss == 1) and not (rounds > 7):
                fight = fight + random.choice(["%s threw a chair at %s" % (init, target), "%s whacked %s with a stick" % (init, target), "%s slapped %s to the floor" % (init, target), "%s threw %s through a wall" % (init, target), "%s bitch slapped %s" % (init, target), "%s used dark magic against %s" % (init, target), "%s used the infinity gauntlet" % (init), "%s used fake news on %s" % (init, target), "%s ran %s over with a truck" % (init, target), "%s ate %s and threw them up again" % (init, target), "%s savagely roasted %s for sunday lunch" % (init, target), "%s forced %s to watch anime" % (init, target), "%s slapped %s with a Macbook" % (init, target), "%s used TUNNELBEAR! THE FREE EASY TO USE VPN..." % (init), "%s performed a windows update on %s" % (init, target), "%s used the might of Zeus" % (init), "%s trapped %s in Flex Tape" % (init, target), "%s built a wall!" % (init)])+"\n"
                fightEm = discord.Embed(title="Fight!", description=fight, colour=color.reds)
                await fMessage.edit(embed=fightEm)
                await asyncio.sleep(2)
                loss = random.randint(1, 4)
                if loss == 1:
                    fight = fight + "%s accepts defeat! %s has won the fight!" % (target, init)
                elif rounds == 7:
                    fight = fight + "The fight has ended in a draw!"
                else:
                    fight = fight +"%s does not giveup and continues the fight!" % (target) + "\n"
                fightEm = discord.Embed(description=fight, colour=color.reds)
                fightEm.set_author(name="Fight")
                await fMessage.edit(embed=fightEm)
                temp = target
                target = init
                init = temp
                rounds = rounds + 1
                await asyncio.sleep(4)






def setup (client):
    client.add_cog(Fun(client))
