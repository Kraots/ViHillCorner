import discord
from discord.ext import commands
import aiohttp

class Cat(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
          async with cs.get("http://aws.random.cat/meow") as r:
            data = await r.json()

          imgUrl = data['file']

          embed = discord.Embed(description=f"[Cat]({imgUrl})", color=0xe97115, timestamp=ctx.message.created_at)
          embed.set_image(url=imgUrl)
          embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
          await ctx.channel.send(embed=embed)



def setup(client):
    client.add_cog(Cat(client))