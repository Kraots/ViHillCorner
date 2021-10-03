import disnake
from disnake.ext import commands
import psutil
import time
from utils import time as t
import utils.colors as color
from utils.context import Context


class Metrics(commands.Cog):
    """Metrics command."""

    def __init__(self, bot):
        self.bot = bot
        self.prefix = "!"
        self.process = psutil.Process()

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '⚒️'

    @commands.command()
    @commands.is_owner()
    async def metrics(self, ctx: Context):
        """A lot of useful system information."""

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        guilds = len(list(self.bot.guilds))
        metrics = disnake.Embed(description="_ _", color=color.inviscolor)
        start = time.time() * 1000
        msg = await ctx.send(embed=metrics)
        end = time.time() * 1000
        metrics = disnake.Embed(title="Metrics", description="_ _", color=color.inviscolor)
        metrics.add_field(
            name="Ping:",
            value=f"Websocket Latency: `{(round(self.bot.latency * 1000, 2))}ms`\n"
            f"Bot Latency: `{int(round(end-start, 0))}ms`\n"
            f"Response Time: `{(msg.created_at.replace(tzinfo=None) - ctx.message.created_at.replace(tzinfo=None)).total_seconds()/1000}` ms",
            inline=False)
        metrics.add_field(
            name="Memory Usage:",
            value=f" \n{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU",
            inline=False
        )
        metrics.add_field(
            name="Guilds:",
            value=guilds,
            inline=False
        )
        metrics.add_field(
            name="Commands loaded:",
            value=f"{len([x.name for x in self.bot.commands])}",
            inline=False)
        metrics.add_field(
            name="Uptime:",
            value=t.human_timedelta(dt=self.bot.uptime, accuracy=3, brief=False, suffix=False)
        )
        metrics.set_footer(
            text=f"Bot made by: {self.bot._owner}",
            icon_url=self.bot.user.display_avatar
        )
        await msg.edit(embed=metrics)


def setup(bot):
    bot.add_cog(Metrics(bot))
