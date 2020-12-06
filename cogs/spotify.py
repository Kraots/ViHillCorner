import discord
from discord.ext import commands
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Spotify(commands.Cog):
   
    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.command()
    async def spotify(self, ctx, member: discord.Member=None):
            
            if member is None:
                member = ctx.author

            if member.bot:
                await ctx.message.delete()
                await ctx.send("Cannot check for spotify activity for bots! Use on members only!", delete_after=10)
                return
        
            if isinstance(member.activities[1], discord.activity.Spotify):
                diff = relativedelta(datetime.utcnow(), member.activities[1].created_at)
                
                m =discord.Embed(title=f"{member.name} activity:")
                m.add_field(name="Listening to :",value=member.activities[1].title, inline=False)
                m.add_field(name="By:",value=member.activities[1].artist, inline=False)
                m.add_field(name="On:",value =member.activities[1].album, inline=False)
                m2, s2 = divmod(int(member.activities[1].duration.seconds), 60)
                song_length = '{:02}:{:02}'.format(m2, s2)
                playingfor = '{:02}:{:02}'.format(diff.minutes, diff.seconds)
                m.add_field(name="Duration:", value=f"{playingfor} - {song_length}")
                m.add_field(name="Total Duration:",value =song_length, inline=False)
                m.add_field(name='Link to song:', value=f"[Click Here](https://open.spotify.com/track/{member.activities[1].track_id}?si=xrjyVAxhS1y5rNHLM_WRww)", inline=False)
                m.set_thumbnail(url=member.activities[1].album_cover_url)
                m.color = discord.Color.green() 
                await ctx.send(embed=m)
                return
            

    @spotify.error
    async def spotify_error(self, ctx, error, member : discord.Member = None):
        if member is None:
            member = ctx.author
        if isinstance(error, commands.errors.CommandInvokeError):
            if isinstance(member.activities[0],discord.activity.Spotify):
                diff = relativedelta(datetime.utcnow(), member.activities[0].created_at)
                m =discord.Embed(title=f"{member.name} activity:")
                m.add_field(name="Listening to :",value=member.activities[0].title, inline=False)
                m.add_field(name="By:",value=member.activities[0].artist, inline=False)
                m.add_field(name="On:",value =member.activities[0].album, inline=False)
                m1, s1 = divmod(int(member.activities[0].duration.seconds), 60)
                song_length = '{:02}:{:02}'.format(m1, s1)
                playingfor = '{:02}:{:02}'.format(diff.minutes, diff.seconds)
                m.add_field(name="Duration:", value=f"{playingfor} - {song_length}")
                m.add_field(name="Total Duration:",value =song_length, inline=False)
                m.add_field(name='Link to song:', value=f"[Click Here](https://open.spotify.com/track/{member.activities[0].track_id}?si=xrjyVAxhS1y5rNHLM_WRww)", inline=False)
                m.set_thumbnail(url=member.activities[0].album_cover_url)
                m.color = discord.Color.green()
                await ctx.send(embed=m)



def setup (client):
    client.add_cog(Spotify(client))