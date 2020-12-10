import discord
from discord.ext import commands

class on_ready(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot succsesfully went online')
        print('Servers connected to:')
        for guild in self.client.guilds:
                print(f"Name: {guild.name} | ID: {guild.id} | Members: {guild.member_count}")


def setup (client):
    client.add_cog(on_ready(client))
