import discord
from discord.ext import commands
import time
import utils.colors as color

from utils.helpers import time_phaserr

up = time.time()


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.command(help="Check bot's ping", hidden=True)
    async def ping(self, ctx):
            botinfo = discord.Embed(title="Pong!", description="_Pinging..._", color=color.lightpink)
            start = time.time() * 1000
            msg = await ctx.reply(embed=botinfo)
            end = time.time() * 1000
            botinfo = discord.Embed(title="Pong!", description=f"Avg. Latency: `{(round(self.client.latency * 1000, 2))}ms`\nRest: `{int(round(end-start, 0))}ms`", color=color.lightpink)
            botinfo.set_footer(text="Online For: " + str(time_phaserr(int(time.time()-up))))
            await msg.edit(embed=botinfo)

    @commands.command(hidden=True)
    async def uptime(self, ctx):
        uptime = discord.Embed(description=f"Bot has been online for: `{time_phaserr(int(time.time()-up))}`", color=color.lightpink)
        uptime.set_footer(text=f'Bot made by: Kraots#0001', icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=uptime)



def setup (client):
    client.add_cog(Ping(client))