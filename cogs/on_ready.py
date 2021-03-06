from disnake.ext import commands

from main import ViHillCorner


class on_ready(commands.Cog):

    def __init__(self, bot: ViHillCorner):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot successfully went online')
        print('Servers connected to:')
        for guild in self.bot.guilds:
            print(f"Name: {guild.name} | ID: {guild.id} | Members: {guild.member_count}")


def setup(bot):
    bot.add_cog(on_ready(bot))
