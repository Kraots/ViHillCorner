import discord
from discord.ext import commands
import random
import aiohttp

class Memes(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def meme(self, ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            imgUrl = res['data']['children'] [random.randint(0, 24)]['data']
            linkUrl = imgUrl['url']
            titleUrl = imgUrl['title']
            
            embed = discord.Embed(color=0xe97115, description=f'[{titleUrl}]({linkUrl})', timestamp=ctx.message.created_at)
            embed.set_image(url=linkUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

def setup (client):
  client.add_cog(Memes(client))