import discord
from discord.ext import commands
import random
from utils import embedlinks
import utils.colors as color


class Waifu(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.prefix = "!"
  async def cog_check(self, ctx):
    return ctx.prefix == self.prefix


  @commands.command()
  async def waifu(self, ctx):
    chosen_image = random.choice(embedlinks.waifuLinks)
    embed = discord.Embed(color=color.lightpink)
    embed.set_image(url=chosen_image)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


def setup (client):
  client.add_cog(Waifu(client))