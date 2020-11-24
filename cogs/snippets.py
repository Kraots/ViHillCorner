import discord
from discord.ext import commands
import utils.colors as color
import os

creepy = os.environ.get('CREEPY')
kraots1 = os.environ.get('KRAOTS1')
kraots2 = os.environ.get('KRAOTS2')
kraots3 = os.environ.get('KRAOTS3')
welcome = os.environ.get('WELCOME')
fuyu = os.environ.get('FUYU')
vihillcorner = os.environ.get('VIHILLCORNER')
s = os.environ.get('S')
thefourhorsemanofsus = os.environ.get('THEFOURHORSEMANOFSUS')
nikki = os.environ.get('NIKKI')
mina = os.environ.get('MINA')
pandie1 = os.environ.get('PANDIE1')
pandie2 = os.environ.get('PANDIE2')

class snippets(commands.Cog):

    def __init__(self, client):
        self.client = client





    @commands.command(hidden=True)
    async def creepy(self, ctx):

            creepy = discord.Embed(color=color.red)
            creepy.set_image(url=creepy)

            msg = await ctx.send(embed=creepy)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True, aliases=['carrots'])
    async def kraots(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=kraots3)

            
            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    async def welcome(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=welcome)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def fuyu(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=fuyu)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def ViHillCorner(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=vihillcorner)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('😐')

    @commands.command(hidden=True)
    async def S(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=s)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def thefourhorsemanofsus(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url=thefourhorsemanofsus)


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command()
    async def nikki(self, ctx):

        nikki = discord.Embed(color=color.red)
        nikki.set_image(url=nikki)

        msg = await ctx.send(embed=nikki)
        await msg.add_reaction('🗑️')

    @commands.command()
    async def mina(self, ctx):

        mina = discord.Embed(color=color.red)
        mina.set_image(url=mina)

        msg = await ctx.send(embed=mina)
        await msg.add_reaction('🗑️')

    @commands.command()
    async def pandie(self, ctx):

        pandie = discord.Embed(color=color.red)
        pandie.set_image(url=pandie2) 


        msg = await ctx.send(embed=pandie)
        await msg.add_reaction('🗑️')

def setup (client):
    client.add_cog(snippets(client))