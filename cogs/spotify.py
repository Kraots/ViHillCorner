import discord
from discord.ext import commands
import datetime
import typing
from utils.helpers import fuckmicroseconds




class Spotify(commands.Cog):
   
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spotify(self, ctx):
        
        if isinstance(ctx.author.activities[0],discord.activity.Spotify):
            m =discord.Embed(title=f"{ctx.author.name} activity:")
            m.add_field(name="Listening to :",value=ctx.author.activities[0].title, inline=False)
            m.add_field(name="By:",value=ctx.author.activities[0].artist, inline=False)
            m.add_field(name="On:",value =ctx.author.activities[0].album, inline=False)
            m.add_field(name="Total Duration:",value =fuckmicroseconds(ctx.author.activities[0].duration), inline=False)
            m.set_thumbnail(url=ctx.author.activities[0].album_cover_url)
            m.color = 0x2F3136 
            await ctx.send(embed=m)
        else:
            await ctx.message.delete()
            await ctx.send("No spotify activity detected. Check if you're using a custom status, in case you do, you gotta get rid of it in order for the command to work!", delete_after=10)



def setup (client):
    client.add_cog(Spotify(client))