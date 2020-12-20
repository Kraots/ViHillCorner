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
		self.prefix = ";;"
		self.process = psutil.Process()
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command()
	@commands.is_owner()
	async def metrics(self, ctx):
		kraots = self.client.get_user(374622847672254466)
		memory_usage = self.process.memory_full_info().uss / 1024**2
		cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
		guilds = len(list(self.client.guilds))
		metrics = discord.Embed(color=color.inviscolor)
		start = time.time() * 1000
		msg = await ctx.message.channel.send(embed=metrics)
		end = time.time() * 1000
		metrics = discord.Embed(title="Metrics", color=color.inviscolor)
		metrics.add_field(name="Ping:", value=f"Avg. Latency: `{(round(self.client.latency * 1000, 2))}ms`\nRest: `{int(round(end-start, 0))}ms`", inline=False)
		metrics.add_field(name="Memory Usage:", value=f" \n{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU", inline=False)
		metrics.add_field(name="Guilds:", value=guilds, inline=False)
		metrics.add_field(name="Commands loaded:", value=f"{len([x.name for x in self.client.commands])}", inline=False)
		metrics.add_field(name="Uptime:", value=str(time_phaser(int(time.time()-up))))
		metrics.set_footer(text=f"Bot made by: {kraots}", icon_url=self.client.user.avatar_url)
		await msg.edit(embed=metrics)

def setup (client):
	client.add_cog(Metrics(client))