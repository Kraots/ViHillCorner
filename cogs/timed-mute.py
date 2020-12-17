import discord
import asyncio
import re
from discord.ext import commands
import utils.colors as color
from utils.helpers import time_phaserr

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.command()
    @commands.has_role("Staff")
    async def tempmute(self, ctx, member:discord.Member, *, time: TimeConverter = None):
        """Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
        &mute @Someone 1d"""
        guild = self.bot.get_guild(750160850077089853)
        log_channel = guild.get_channel(788377362739494943)

        if time is None:
            await ctx.send("You need to specify time.")
            return

        muted = guild.get_role(750465726069997658)
        await member.add_roles(muted)
        msg = ("You have been muted in `Anime Hangouts`")
        em = discord.Embed(description=f"Time: `{time_phaserr(time)}`", color=color.inviscolor)
        await member.send(msg, embed = em)


        unban = discord.Embed(description= f'{member.mention} has been muted for `{time_phaserr(time)}`' , color=color.red)
        
        await ctx.send(embed=unban)

        log = discord.Embed(color=color.reds, title="___Mute___", timestamp = ctx.message.created_at)
        log.add_field(name="Member", value=f"`{member}`", inline=False)
        log.add_field(name="Moderator", value=f"`{ctx.author}`", inline=False)
        log.add_field(name="Time", value=f"`{time_phaserr(time)}`", inline=False)
        await log_channel.send(embed=log)

        await asyncio.sleep(time)
        await member.remove_roles(muted)
        await member.send("You have been unmuted in `Anime Hangouts`.")
    

def setup(bot):
    bot.add_cog(MuteCog(bot))