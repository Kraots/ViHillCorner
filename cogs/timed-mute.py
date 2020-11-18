import discord
import asyncio
import re
from discord.ext import commands
import sys
import traceback


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

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, member:discord.Member, *, time:TimeConverter = None):
        """Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
        &mute @Someone 1d"""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        unban = discord.Embed(description= f'{member.mention} has been muted for **{time} seconds**.' , color=0xe64343)
        
        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️') 
        if time:
            await asyncio.sleep(time)
            await member.remove_roles(role)

    

def setup(bot):
    bot.add_cog(MuteCog(bot))