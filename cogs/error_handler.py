import disnake
from disnake.ext import commands

from utils.context import Context

from main import ViHillCorner


class GlobalErrorHandler(commands.Cog):
    def __init__(self, bot: ViHillCorner):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        await self.bot.reraise(ctx, error)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error):
        await self.bot.slash_reraise(inter, error)


def setup(bot):
    bot.add_cog(GlobalErrorHandler(bot))
