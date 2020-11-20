import discord
from discord.ext import commands

class BotInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def botinfo(self, ctx):
        kraots = self.client.get_user(374622847672254466)
        guilds = len(list(self.client.guilds))
        cache_summary = f"**{len(self.client.guilds)}** guild(s) and **{len(self.client.users)}** user(s)"
        botinfo = discord.Embed(title="", color=0x2F3136, timestamp=ctx.message.created_at)
        botinfo.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        botinfo.add_field(name="Bot Owner:", value=f"{kraots}", inline=False)
        botinfo.add_field(name="Created at:", value="05/09/2020", inline=False)
        botinfo.add_field(name="Info", value=f"This bot is not sharded and can see {cache_summary}")
        botinfo.add_field(name="Commands loaded", value=f"{len([x.name for x in self.client.commands])}", inline=False)
        botinfo.add_field(name="About:", value="*This bot is a private bot (meaning it is not open sourced) made only for Anime Hangouts, so do not ask to host it or to add it to your server!*", inline=True)
        botinfo.set_thumbnail(url="https://cdn.discordapp.com/avatars/751724369683677275/0ad4d3b39956b6431c7167ef82c30d30.webp?size=1024")
        await ctx.channel.send(embed=botinfo)

def setup (client):
    client.add_cog(BotInfo(client))