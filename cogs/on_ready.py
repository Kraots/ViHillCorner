import disnake
from disnake.ext import commands

class on_ready(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connected_once = False

    @commands.Cog.listener()
    async def on_connect(self):
        if self.connected_once:
            return
        self.connected_once = True
        self.bot._owner = await self.bot.fetch_user(self.bot.owner_id)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot succsesfully went online')
        print('Owner: ' + str(self.bot._owner))
        print('Servers connected to:')
        for guild in self.bot.guilds:
                print(f"Name: {guild.name} | ID: {guild.id} | Members: {guild.member_count}")


def setup(bot):
    bot.add_cog(on_ready(bot))
