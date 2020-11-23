import discord
from discord.ext import commands

class on_ready(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.playing, name='taking a break, nothing to worry')
        await self.client.change_presence(status=discord.Status.dnd, activity=activity)
        print('Bot succsesfully went online')
        print('Servers connected to:')
        for guild in self.client.guilds:
                print(guild.name)


def setup (client):
    client.add_cog(on_ready(client))
