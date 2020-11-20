import asyncio
import discord
from discord.ext import commands
import typing
from utils.helpers import profile

class Userinfo(commands.Cog):
    """ Get info for user"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def profile(self, ctx, *, user: typing.Optional[discord.Member]):
        if ctx.invoked_subcommand is None:
            if not user:
                user = ctx.message.author
            em = profile(ctx,user)
            await ctx.send(embed=em)
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Userinfo(bot))
