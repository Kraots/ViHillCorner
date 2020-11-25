import discord
from discord.ext import commands
import utils.colors as color
import os

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

    @commands.command(hidden=True)
    async def huggles(self, ctx, *, mention=None,):

            version = discord.Embed(color=color.red)
            version.set_image(url=huggles)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('<:hug:750751796317913218>')

    @commands.command(hidden=True)
    async def grouphug(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=grouphug)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def eat(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=eat)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def chew(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=chew)


            msg = await ctx.send(mention, embed=version)
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


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def rofl(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=rofl)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def lol(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=lol)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def kill(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=kill)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def pat(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=pat)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('<:kanna_pat:750757139001245806>')

    @commands.command(hidden=True)
    async def rub(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=rub)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def nom(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=nom)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def catpat(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=catpat)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def hug(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=hug)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def pillow(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=pillow)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def spray(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=spray)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def hype(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=hype)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    @commands.has_role('Staff')
    async def specialkiss(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=specialkiss)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    async def kiss(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=kiss)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def ily(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=ily)


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def nocry(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url=nocry)


            msg = await ctx.send(mention, embed=version)
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
    async def bearhug(self, ctx, *, mention=None):

            bearhug = discord.Embed(color=color.red)
            bearhug.set_image(url=bearhugg)
            
            msg = await ctx.send(mention, embed=bearhug)
            await msg.add_reaction('🗑️')

    @commands.command()
    async def moan(self, ctx):
        
        moan = discord.Embed(color=color.red)
        moan.set_image(url=moann)

        msg = await ctx.channel.send(embed=moan)
        await msg.add_reaction('🗑️')




def setup (client):
    client.add_cog(actions(client))

