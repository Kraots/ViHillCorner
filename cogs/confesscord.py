import discord
from discord.ext import commands

class Confesscord(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        guild = self.client.get_guild(750160850077089853)
        confessions = guild.get_channel(783304066691235850)
        confessionLogs = guild.get_channel(783306308270817311)
        if message.channel.id == 783304085079588894:
            await message.delete()
            embed = discord.Embed(title='***___New Confession:___***', description=f'`{message.content}`', color=message.author.color)
            await confessions.send(embed = embed)
            logs = discord.Embed(title='***___NEW CONFESSION:___***', description=f'`{message.content}`', color=message.author.color)
            logs.set_footer(text=f'By: {message.author}', icon_url=message.author.avatar_url)
            await confessionLogs.send(embed=logs)

def setup (client):
    client.add_cog(Confesscord(client))