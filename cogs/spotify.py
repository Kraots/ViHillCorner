import discord
from discord.ext import commands
import utils.colors as color
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
        
            if isinstance(member.activities[0],discord.activity.Spotify):
                m =discord.Embed(title=f"{member.name} activity:")
                m.add_field(name="Listening to :",value=member.activities[0].title, inline=False)
                m.add_field(name="By:",value=member.activities[0].artist, inline=False)
                m.add_field(name="On:",value =member.activities[0].album, inline=False)
                m1, s1 = divmod(int(member.activities[0].duration.seconds), 60)
                song_length = f'{m1}:{s1}'
                m.add_field(name="Total Duration:",value =song_length, inline=False)
                m.add_field(name='Link to song:', value=f"[Click Here](https://open.spotify.com/track/{member.activities[0].track_id}?si=xrjyVAxhS1y5rNHLM_WRww)", inline=False)
                m.set_thumbnail(url=member.activities[0].album_cover_url)
                m.color = color.inviscolor 
                await ctx.send(embed=m)
            else:
                await ctx.message.delete()
                await ctx.send("No spotify activity detected. Check if you're using a custom status, in case you do, you gotta get rid of it in order for the command to work!", delete_after=10)



def setup (client):
    client.add_cog(Spotify(client))