import discord
from discord.ext import commands
import psutil
import os
import utils.colors as color
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from random import randint

class command(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix
    
    @commands.command(help="Get a list of all actions")
    async def actions(self, context):

            version = discord.Embed(title="Here's the list of all actions", description="`!ily`\n`!huggle` \n`!grouphug`\n`!bearhug`\n`!nocry` \n`!chew` \n`!eat` \n`!spray` \n`!sip` \n`!hype` \n`!clap` \n`!cry` \n`!lol` \n`!rofl` \n`!kill` \n`!pat` \n`!nom` \n`!rub` \n`!hug` \n`!catpat` \n`!pillow` \n`!kiss`\n`!shrug`\n`!smug` ", color=color.lightpink)
            version.set_footer(text=f'Requested by: {context.author}', icon_url=context.author.avatar_url)
            await context.message.channel.send(embed=version)

    @commands.command(help="Get a list of all snippets")
    async def snippets(self, context):

            version = discord.Embed(title="Here's the list of all snippets", description="`!fuyu`\n`!welcome`\n`!kraots`\n`!vihillcorner`\n`!s`\n`!thefourhorsemanofsus`\n`!creepy`\n`!nikki`\n`!mina`\n`!pandie`\n`!teis`\n`!galactus`\n`!le-pole-dancer`\n`!kewi`\n`!twilight`\n`!onii` ", color=color.lightpink)
            version.set_footer(text=f'Requested by: {context.author}', icon_url=context.author.avatar_url)
            await context.message.channel.send(embed=version)

    @commands.command()
    async def created(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        diff = relativedelta(datetime.utcnow(), member.created_at)
        
        embed = discord.Embed(color=color.lightpink)
        embed.add_field(name='Create Date:', value=f"{member.name}'s account was made **{diff.years}** years, **{diff.months}** months, **{diff.weeks}** weeks, **{diff.days}** days , **{diff.hours}** hours, **{diff.minutes}** minutes and **{diff.seconds}** seconds ago.")
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def joined(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        diff = relativedelta(datetime.utcnow(), member.joined_at)

        embed = discord.Embed(color=color.lightpink)
        embed.add_field(name="Join Date:", value=f"{member.name} joined **{diff.months}** months, **{diff.weeks}** weeks, **{diff.days}** days, **{diff.hours}** hours, **{diff.minutes}** minutes and **{diff.seconds}** seconds ago.")
        await ctx.channel.send(embed=embed)

    @commands.command(help="Get a list of all snippets", aliases=["inv", "invite"])
    async def _invite(self, context):

            version = discord.Embed(title="Here's the invite:", description="[Anime Hangouts](https://discord.gg/Uf2kA8q)", color=color.lightpink)
            version.set_footer(text=f'Requested by: {context.author}', icon_url=context.author.avatar_url)

            await context.message.channel.send(embed=version)

    @commands.command(hidden=True)
    async def membercount(self, ctx):
            guild = self.client.get_guild(750160850077089853)
            await ctx.channel.send(f'`{guild.member_count - 11}` members.') 

    @commands.command(hidden=True, aliases=["av", "avatar"])
    async def _av(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if member is None:
            member = ctx.author

        avatar = discord.Embed(description=f'[{member.name}]({member.avatar_url})', color=color.blue)
        avatar.set_image(url=member.avatar_url)
        avatar.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=avatar)

    @commands.command()
    async def ee(self, ctx, emoji: discord.PartialEmoji):
        await ctx.message.delete()

        embed = discord.Embed(color=color.lightpink)
        embed.set_image(url=emoji.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def serverad(self, ctx):
        await ctx.message.delete()
        ad = discord.Embed(color=color.lightpink, title="Here's the ad to the server:", description="**__Anime Hangouts__**\nAnime Hangouts is mainly for anime & talking & meeting new people & generally chatting!\n\n**WHAT WE HAVE TO OFFER**\n★ Awesome Private Bot\n★ Fun Channels\n★ Active Users\n★ Lots Of Emotes\n★ Reaction Roles\n\n\nhttps://discord.gg/Uf2kA8q")
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=ad)

    @commands.command(aliases=["ra"])
    async def rawad(self, ctx):
        await ctx.message.delete()
        ad = discord.Embed(color=color.lightpink, title="Here's the raw ad version of the server:", description="```**__Anime Hangouts__**\nAnime Hangouts is mainly for anime & talking & meeting new people & generally chatting!\n\n**WHAT WE HAVE TO OFFER**\n★ Awesome Private Bot\n★ Fun Channels\n★ Active Users\n★ Lots Of Emotes\n★ Reaction Roles\n\n\nhttps://discord.gg/Uf2kA8q```")
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=ad)

    @commands.command(aliases=['chat revive', 'revive', 'revive chat'])
    @commands.cooldown(1, 7200, commands.BucketType.guild)
    async def _asdjknasdjkn(self, ctx):
        await ctx.message.delete()
        msg = '<@&750160850236604537>'
        revive = self.client.get_channel(761652915450413106)
        await revive.send(msg)

    @commands.command(aliases=["untill-partner", "up"])
    async def _sdlajkndasjkdn(self, ctx):
        guild = self.client.get_guild(750160850077089853)
        await ctx.channel.send(f'Members left untill the server can apply for the *discord partership program:* \n\n`{500 - guild.member_count + 11}`')



def setup (client):
    client.add_cog(command(client))
