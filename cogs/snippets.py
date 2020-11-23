import discord
from discord.ext import commands
import utils.colors as color

class snippets(commands.Cog):

    def __init__(self, client):
        self.client = client





    @commands.command(hidden=True)
    async def creepy(self, ctx):

            creepy = discord.Embed(color=color.red)
            creepy.set_image(url="https://cdn.discordapp.com/attachments/751162510454816786/763031145059057704/unknown.png")

            msg = await ctx.send(embed=creepy)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True, aliases=['carrots'])
    async def kraots(self, ctx):

            version = discord.Embed(color=color.red, description='<:hug:750751796317913218> Taking a break! Nothing to worry about! <:hug:750751796317913218>')
#            version.set_image(url='https://cdn.discordapp.com/attachments/750160851822182482/779839054782005248/Screenshot_20201116_020704.jpg')
# https://cdn.discordapp.com/attachments/750160852380024894/752549480347205682/unknown.png
            
            
            await ctx.send(embed=version)
           # msg = await ctx.send(embed=version)
           # await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    async def welcome(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160851822182482/751095873772978249/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def fuyu(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/751162510454816786/751479743962021939/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def ViHillCorner(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/751162510454816786/765546029474250812/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('😐')

    @commands.command(hidden=True)
    async def S(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/752148605753884792/753937672019640350/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def thefourhorsemanofsus(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/754262819846881372/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command()
    async def nikki(self, ctx):

        nikki = discord.Embed(color=color.red)
        nikki.set_image(url='https://cdn.discordapp.com/attachments/750160851822182482/779835701079834674/IMG_20201122_002834.png')

        msg = await ctx.send(embed=nikki)
        await msg.add_reaction('🗑️')

    @commands.command()
    async def mina(self, ctx):

        mina = discord.Embed(color=color.red)
        mina.set_image(url='https://cdn.discordapp.com/attachments/750160851822182482/779838737927634964/Screenshot_20201119_013203.jpg')

        msg = await ctx.send(embed=mina)
        await msg.add_reaction('🗑️')

    @commands.command()
    async def pandie(self, ctx):

        pandie = discord.Embed(color=color.red)
        pandie.set_image(url='https://cdn.discordapp.com/attachments/757857924168024064/780144695090348052/unknown.png')

        msg = await ctx.send(embed=pandie)
        await msg.add_reaction('🗑️')

def setup (client):
    client.add_cog(snippets(client))