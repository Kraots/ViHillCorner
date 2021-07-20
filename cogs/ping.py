import discord
from discord.ext import commands
import time
import utils.colors as color
from utils import time as t

class Ping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command()
	async def ping(self, ctx):
		"""See the bot's ping data."""
		ping = discord.Embed(title="Pong!", description="_Pinging..._", color=color.lightpink)
		start = time.time() * 1000
		msg = await ctx.send(embed=ping)
		end = time.time() * 1000
		ping = discord.Embed(title="Pong!", description=f"Websocket Latency: `{(round(self.bot.latency * 1000, 2))}ms`\nBot Latency: `{int(round(end-start, 0))}ms`\nResponse Time: `{(msg.created_at - ctx.message.created_at).total_seconds()/1000}` ms", color=color.lightpink)
		ping.set_footer(text=f"Online for {t.human_timedelta(dt=self.bot.uptime, suffix=False)}")
		await msg.edit(embed=ping)

	@commands.command()
	async def uptime(self, ctx):
		"""See how long the bot has been online for."""

		uptime = discord.Embed(description=f"Bot has been online for: `{t.human_timedelta(dt=self.bot.uptime, suffix=False)}`", color=color.lightpink)
		uptime.set_footer(text=f'Bot made by: Kraots#0001', icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=uptime)



def setup(bot):
	bot.add_cog(Ping(bot))