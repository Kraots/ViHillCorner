import discord
from discord.ext import commands
import utils.colors as color
import os
from discord import Member
from discord.ext.commands import Greedy

huggles = os.environ.get("HUGGLES")
grouphug = os.environ.get("GROUPHUG")
eat = os.environ.get("EAT")
chew = os.environ.get("CHEW")
sip = os.environ.get("SIP")
clap = os.environ.get("CLAP")
cry = os.environ.get("CRY")
rofl = os.environ.get("ROFL")
lol = os.environ.get("LOL")
kill = os.environ.get("KILL")
pat = os.environ.get("PAT")
rub = os.environ.get("RUB")
nom = os.environ.get("NOM")
catpat = os.environ.get("CATPAT")
hug = os.environ.get("HUG")
pillow = os.environ.get("PILLOW")
spray = os.environ.get("SPRAY")
hype = os.environ.get("HYPE")
specialkiss = os.environ.get("SPECIALKISS")
kiss = os.environ.get("KISS")
ily = os.environ.get("ILY")
nocry = os.environ.get("NOCRY")
shrug = os.environ.get("SHRUG")
smug = os.environ.get("SMUG")
bearhugg = os.environ.get("BEARHUG")
moann = os.environ.get("MOAN")


class actions(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = ";"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.command(hidden=True)
    async def rape(self, ctx):

        await ctx.send('https://cdn.discordapp.com/attachments/745298904832278530/782729248623427614/video0-1_1.mp4')

    @commands.command(hidden=True)
    async def huggles(self, ctx, members : Greedy[Member] = None):
        version = discord.Embed(color=color.red)
        version.set_image(url=huggles)
        mention_list = []

        if members == None:
            msg = await ctx.send(embed=version)

        else:
            for member in members:
                a = member.mention
        
                mention_list.append(a)
                mentions = f" ".join(mention_list)
            
            msg = await ctx.send(mentions, embed=version)
        await msg.add_reaction('<:hug:750751796317913218>')

    @commands.command(hidden=True)
    async def grouphug(self, ctx, members : Greedy[Member] = None):
        version = discord.Embed(color=color.red)
        version.set_image(url=grouphug)
        mention_list = []

        if members == None:
            msg = await ctx.send(embed=version)

        else:
            for member in members:
                a = member.mention
        
                mention_list.append(a)
                mentions = f" ".join(mention_list)
            
            msg = await ctx.send(mentions, embed=version)
        await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def eat(self, ctx, members : Greedy[Member] = None):

            version = discord.Embed(color=color.red)
            version.set_image(url=eat)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def chew(self, ctx, members : Greedy[Member] = None):

            version = discord.Embed(color=color.red)
            version.set_image(url=chew)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def sip(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=sip)

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def clap(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=clap)

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def cry(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=cry)
            mention_list = []

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def rofl(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=rofl)
            mention_list = []

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def lol(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=lol)
            mention_list = []

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def kill(self, ctx, members : Greedy[Member] = None):
            
            version = discord.Embed(color=color.red)
            version.set_image(url=kill)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def pat(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=pat)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('<:kanna_pat:750757139001245806>')

    @commands.command(hidden=True)
    async def rub(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=rub)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def nom(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=nom)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def catpat(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=catpat)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def hug(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=hug)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def pillow(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=pillow)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def spray(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=spray)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def hype(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=hype)
            mention_list = []

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    @commands.has_role('Staff')
    async def specialkiss(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=specialkiss)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    async def kiss(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=kiss)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def ily(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=ily)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def nocry(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            version.set_image(url=nocry)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def shrug(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=shrug)

            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def smug(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=smug)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def bearhug(self, ctx, members : Greedy[Member] = None):
            version = discord.Embed(color=color.red)
            bearhug.set_image(url=bearhugg)
            mention_list = []

            if members == None:
                msg = await ctx.send(embed=version)

            else:
                for member in members:
                    a = member.mention
            
                    mention_list.append(a)
                    mentions = f" ".join(mention_list)
                
                msg = await ctx.send(mentions, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command()
    async def moan(self, ctx):
        
        moan = discord.Embed(color=color.red)
        moan.set_image(url=moann)

        msg = await ctx.channel.send(embed=moan)
        await msg.add_reaction('🗑️')




def setup (client):
    client.add_cog(actions(client))

