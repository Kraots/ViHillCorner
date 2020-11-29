import discord
from discord.ext import commands
import psutil
import humanize
import time
from utils.helpers import time_phaser
import utils.colors as color

up = time.time()

class Metrics(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["!metrics"])
    @commands.is_owner()
    async def asdasdasdasdadsmetrics(self, ctx):
        kraots = self.client.get_user(374622847672254466)
        proc = psutil.Process()
        mem = proc.memory_full_info()
        guilds = len(list(self.client.guilds))
        metrics = discord.Embed(color=color.inviscolor)
        start = time.time() * 1000
        msg = await ctx.message.channel.send(embed=metrics)
        end = time.time() * 1000
        metrics = discord.Embed(title="Metrics", color=color.pink)
        metrics.add_field(name="Ping:", value=f"Avg. Latency: `{(round(self.client.latency * 1000, 2))}ms`\nRest: `{int(round(end-start, 0))}ms`", inline=False)
        metrics.add_field(name="Memory Usage:", value=f" \n{humanize.naturalsize(mem.rss)} physical memory \n{humanize.naturalsize(mem.vms)} virtual memory \n{humanize.naturalsize(mem.uss)} of which unique to this process", inline=False)
        metrics.add_field(name="Guilds:", value=guilds, inline=False)
        metrics.add_field(name="Commands loaded:", value=f"{len([x.name for x in self.client.commands])}", inline=False)
        metrics.add_field(name="Uptime:", value=str(time_phaser(int(time.time()-up))))
        metrics.set_footer(text=f"Bot made by: {kraots}", icon_url="https://cdn.discordapp.com/avatars/751724369683677275/0ad4d3b39956b6431c7167ef82c30d30.webp?size=1024")
        await msg.edit(embed=metrics)

def setup (client):
  client.add_cog(Metrics(client))