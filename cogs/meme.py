import discord
from discord.ext import commands
import aiohttp
import utils.colors as color

class Memes(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.prefix = "!"
  async def cog_check(self, ctx):
        return ctx.prefix == self.prefix




  @commands.command()
  async def meme(self, ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/random/.json') as r:
            res = await r.json()
            imgUrl = res[0]['data']['children'] [0]['data']
            linkUrl = imgUrl['url']
            titleUrl = imgUrl['title']
            
            embed = discord.Embed(color=color.orange, title=titleUrl, url=linkUrl, timestamp=ctx.message.created_at)
            embed.set_image(url=linkUrl)
            embed.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

def setup (bot):
  bot.add_cog(Memes(bot))