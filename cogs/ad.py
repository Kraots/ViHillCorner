import discord
from discord.ext import commands
from utils.helpers import time_phaser, BotChannels
import utils.colors as color

class AdvertisementCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.command()
    @commands.check(BotChannels)
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def ad(self, ctx, *, args):
        guild = self.client.get_guild(750160850077089853)
        adchannel = guild.get_channel(780333682866913320)
        embed = discord.Embed(title="New Advertisement", description=args, color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await adchannel.send(embed=embed)
        await ctx.message.delete()
        succes = discord.Embed(color=color.inviscolor, description=f'[Succesfully posted your advertisement!]({msg.jump_url})\n\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800{ctx.author.mention}')
        await ctx.channel.send(embed=succes)

    @ad.error
    async def ad_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.message.delete()
            msg = f"To use this command go to <#750160851822182486> or <#750160851822182487>.\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _{ctx.author.mention}"
            await ctx.channel.send(msg, delete_after=6)

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            msg = f'Your already advertised today, please try again in **{time_phaser(error.retry_after)}**.'
            await ctx.channel.send(msg, delete_after=6)
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            msg = "You have to add your ad, try again in **12 hours**."
            await ctx.channel.send(msg, delete_after=3)




def setup (client):
    client.add_cog(AdvertisementCommand(client))    