import discord
from discord.ext import commands
import utils.colors as color

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

        
        # SFW

    @commands.command()
    async def sfw(self, ctx, *, mention=None):
        sfw = discord.Embed(title="NSFW Warning", description="Please keep the chat appropiate and sfw.", color=color.red)

        msg = await ctx.send(mention, embed=sfw)
        await msg.add_reaction('🗑️')

    @commands.command(aliases=['lvl'])
    async def level(self, ctx, *, mention=None):
        lvl = discord.Embed(title="How to lvl up", description="You can level up in this server by chatting in any channel. Spamming or `XP farming` would result in level reset. \n\nTo check your rank, send `^rank` in <#750160851822182486>.", color=color.red)

        msg = await ctx.send(mention, embed=lvl)
        await msg.add_reaction('🗑️')

    @commands.command()
    async def rank(self, ctx, *, mention=None):
        rank = discord.Embed(title="How to check your rank", description="Send `^rank` in <#750160851822182486> to check your rank.", color=color.red)

        msg = await ctx.send(mention, embed=rank)
        await msg.add_reaction('🗑️')































def setup (client):
    client.add_cog(info(client))
