import discord
from discord.ext import commands
import time
import utils.colors as color
from utils import time as t

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
            msg = await ctx.send(embed=botinfo)
            end = time.time() * 1000
            botinfo = discord.Embed(title="Pong!", description=f"Websocket Latency: `{(round(self.client.latency * 1000, 2))}ms`\nBot Latency: `{int(round(end-start, 0))}ms`\nResponse Time: `{(msg.created_at - ctx.message.created_at).total_seconds()/1000}` ms", color=color.lightpink)
            botinfo.set_footer(text=f"Online for {t.human_timedelta(dt=self.client.uptime, suffix=False)}")
            await msg.edit(embed=botinfo)

    @commands.command(hidden=True)
    async def uptime(self, ctx):
        uptime = discord.Embed(description=f"Bot has been online for: `{t.human_timedelta(dt=self.client.uptime, suffix=False)}`", color=color.lightpink)
        uptime.set_footer(text=f'Bot made by: Kraots#0001', icon_url=self.client.user.avatar_url)
        await ctx.send(embed=uptime)



def setup (client):
    client.add_cog(Ping(client))