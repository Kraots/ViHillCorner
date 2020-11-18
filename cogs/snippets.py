import discord
from discord.ext import commands


class snippets(commands.Cog):

    def __init__(self, client):
        self.client = client





    @commands.command(hidden=True)
    async def creepy(self, ctx):

            creepy = discord.Embed(color=0xe64343)
            creepy.set_image(url="https://cdn.discordapp.com/attachments/751162510454816786/763031145059057704/unknown.png")

            msg = await ctx.send(embed=creepy)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def kraots(self, ctx):

            version = discord.Embed(color=0xe64343)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024894/752549480347205682/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    async def welcome(self, ctx):

            version = discord.Embed(color=0xe64343)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160851822182482/751095873772978249/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def fuyu(self, ctx):

            version = discord.Embed(color=0xe64343)
            version.set_image(url='https://cdn.discordapp.com/attachments/751162510454816786/751479743962021939/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def ViHillCorner(self, ctx):

            version = discord.Embed(color=0xe64343)
            version.set_image(url='https://cdn.discordapp.com/attachments/751162510454816786/765546029474250812/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('😐')

    @commands.command(hidden=True)
    async def S(self, ctx):

            version = discord.Embed(color=0xe64343)
            version.set_image(url='https://cdn.discordapp.com/attachments/752148605753884792/753937672019640350/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def thefourhorsemanofsus(self, ctx):

            version = discord.Embed(color=0xe64343)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/754262819846881372/unknown.png')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')


def setup (client):
    client.add_cog(snippets(client))