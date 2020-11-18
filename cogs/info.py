import discord
from discord.ext import commands

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
        
        # SFW

    @commands.command()
    @commands.has_any_role('Mod', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+')
    async def sfw(self, ctx, *, mention=None):
        sfw = discord.Embed(title="NSFW Warning", description="Please keep the chat appropiate and sfw.", color=0xe64343)

        msg = await ctx.send(mention, embed=sfw)
        await msg.add_reaction('🗑️')

    @commands.command()
    @commands.has_any_role('Mod', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+')
    async def lvl(self, ctx, *, mention=None):
        lvl = discord.Embed(title="How to lvl up", description="You can level up in this server by chatting in any channel. Spamming or `XP farming` would result in level reset. \n\nTo check your rank, send `^rank` in <#750160851822182486>.", color=0xe64343)

        msg = await ctx.send(mention, embed=lvl)
        await msg.add_reaction('🗑️')

    @commands.command()
    @commands.has_any_role('Mod', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+')
    async def rank(self, ctx, *, mention=None):
        rank = discord.Embed(title="How to check your rank", description="Send `^rank` in <#750160851822182486> to check your rank.", color=0xe64343)

        msg = await ctx.send(mention, embed=rank)
        await msg.add_reaction('🗑️')































def setup (client):
    client.add_cog(info(client))
