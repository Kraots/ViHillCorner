import discord
from discord.ext import commands
import random
from random import randint
from utils import embedlinks


class Waifu(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def waifu(self, ctx):
    chosen_image = random.choice(embedlinks.waifuLinks)
    embed = discord.Embed(color=0xf1a3d8)
    embed.set_image(url=chosen_image)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed=embed)


def setup (client):
  client.add_cog(Waifu(client))