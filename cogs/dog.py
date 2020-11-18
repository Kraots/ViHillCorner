import discord
from discord.ext import commands
import aiohttp

class Dog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dog(self, ctx): 
        async with aiohttp.ClientSession() as cs:
          async with cs.get("http://random.dog/woof.json") as r:
            data = await r.json()

            embed = discord.Embed(description=f"[Dog]({data['url']})", color=0xe97115, timestamp=ctx.message.created_at)
            embed.set_image(url=data['url'])
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(Dog(client))