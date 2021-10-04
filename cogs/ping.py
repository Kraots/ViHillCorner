import disnake
from disnake.ext import commands
import time
import utils.colors as color
from utils import time as t
from utils.context import Context
from main import ViHillCorner


class Ping(commands.Cog):
    """Ping related commands."""
    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '❕'

    @commands.command()
    async def ping(self, ctx: Context):
        """See the bot's ping data."""
        ping = disnake.Embed(title="Pong!", description="_Pinging..._", color=color.lightpink)
        start = time.time() * 1000
        msg = await ctx.send(embed=ping)
        end = time.time() * 1000
        ping = disnake.Embed(
            title="Pong!",
            description=f"Websocket Latency: `{(round(self.bot.latency * 1000, 2))}ms`"
            f"\nBot Latency: `{int(round(end-start, 0))}ms`"
            f"\nResponse Time: `{(msg.created_at.replace(tzinfo=None) - ctx.message.created_at.replace(tzinfo=None)).total_seconds()/1000}` ms",
            color=color.lightpink
        )
        ping.set_footer(text=f"Online for {t.human_timedelta(dt=self.bot.uptime, suffix=False)}")
        await msg.edit(embed=ping)

    @commands.command()
    async def uptime(self, ctx: Context):
        """See how long the bot has been online for."""

        uptime = disnake.Embed(description=f"Bot has been online for: `{t.human_timedelta(dt=self.bot.uptime, suffix=False)}`", color=color.lightpink)
        uptime.set_footer(text=f'Bot made by: {self.bot._owner}', icon_url=self.bot.user.display_avatar)
        await ctx.send(embed=uptime)


def setup(bot):
    bot.add_cog(Ping(bot))
