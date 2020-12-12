import discord
from discord.ext import commands
import aiohttp
import utils.colors as color
from utils.helpers import NSFW
from discord.ext.commands import Greedy
from discord import Member

class NSFW(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.check(NSFW)
    async def nsfw(self, ctx):
        await ctx.send('`!nsfw hentai` | `!nsfw yuri` | `!nsfw tentacle` | `!nsfw real`')

    @nsfw.command()
    @commands.check(NSFW)
    async def hentai(self, ctx):
        async with aiohttp.ClientSession() as cs:
          async with cs.get("https://www.reddit.com/r/hentai/random/.json") as r:
            res = await r.json()
            EntryPoint = res[0]['data']['children'] [0]['data']           
            imgUrl = EntryPoint['url']
            Title = EntryPoint['title']

            embed = discord.Embed(title=Title, url=imgUrl, timestamp=ctx.message.created_at, color=color.pastel)
            embed.set_image(url=imgUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @nsfw.command()
    @commands.check(NSFW)
    async def yuri(self, ctx):
        async with aiohttp.ClientSession() as cs:
          async with cs.get("https://www.reddit.com/r/yuri/random/.json") as r:
            res = await r.json()
            imgUrl = res[0]['data']['children'] [0]['data']
            linkUrl = imgUrl['url']
            titleUrl = imgUrl['title']

            embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
            embed.set_image(url=linkUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @nsfw.command(aliases=['tentacles'])
    @commands.check(NSFW)
    async def tentacle(self, ctx):
        async with aiohttp.ClientSession() as cs:
          async with cs.get("https://www.reddit.com/r/Tentai/random/.json") as r:
            res = await r.json()
            imgUrl = res[0]['data']['children'] [0]['data']
            linkUrl = imgUrl['url']
            titleUrl = imgUrl['title']

            embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
            embed.set_image(url=linkUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @nsfw.command()
    @commands.check(NSFW)
    async def real(self, ctx):
        async with aiohttp.ClientSession() as cs:
          async with cs.get("https://www.reddit.com/r/pornpics/random/.json") as r:
            res = await r.json()
            imgUrl = res[0]['data']['children'] [0]['data']
            linkUrl = imgUrl['url']
            titleUrl = imgUrl['title']

            embed = discord.Embed(title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at, color=color.pastel)
            embed.set_image(url=linkUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @nsfw.command()
    @commands.has_role('Staff')
    async def add(self, ctx, members: Greedy[Member]):
        guild = self.client.get_guild(750160850077089853)
        NSFW = guild.get_role(780370679425925141)
        
        for member in members:
            await member.add_roles(NSFW)
            await ctx.send(f'{member.mention} can now see the nsfw channel!')
            await member.send('You can now see the nsfw channel! <#780374324598145055> <:peepo_yay:773535977624698890>')

    @nsfw.command()
    @commands.has_role('Staff')
    async def remove(self, ctx, members: Greedy[Member]):
        guild = self.client.get_guild(750160850077089853)
        NSFW = guild.get_role(780370679425925141)
        
        for member in members:
            await member.remove_roles(NSFW)
            await ctx.send(f'{member.mention} cannot see the nsfw channel anymore!')
            await member.send('You cannot see the nsfw channel anymore <:weird:773538796087803934>')




    @nsfw.error
    async def nsfw_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            if "Staff" in [role.name for role in ctx.message.author.roles]:
                await ctx.send('Invalid format!\nUse: `!nsfw add {user}` or `!nsfw remove {user}`!')
            else:

                msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
                await ctx.channel.send(msg)

    @hentai.error
    async def hentai_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
            await ctx.channel.send(msg)

    @yuri.error
    async def yuri_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
            await ctx.channel.send(msg)

    @tentacle.error
    async def tentacle_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            msg = f"This command is only usable in a nsfw marked channel!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ {ctx.author.mention}"
            await ctx.channel.send(msg)


















# https://www.reddit.com/r/hentai/random/.json
def setup (client):
    client.add_cog(NSFW(client))