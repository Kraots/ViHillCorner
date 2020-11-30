import discord
from discord.ext import commands
import os

class All(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=["!reload-all"])
  @commands.is_owner()
  async def reloadall(self, ctx):


    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.unload_extension(f'cogs.{filename[:-3]}')
    
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.load_extension(f'cogs.{filename[:-3]}')

    await ctx.channel.send("All cogs have been reloaded!")


  @commands.command(aliases=["!load-all"])
  @commands.is_owner()
  async def loadall(self, ctx):

    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.load_extension(f'cogs.{filename[:-3]}')

    await ctx.channel.send("All cogs have been loaded!")

  @commands.command(aliases=["!unload-all"])
  @commands.is_owner()
  async def unloadall(self, ctx):
  
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.unload_extension(f'cogs.{filename[:-3]}')

    await ctx.channel.send("All cogs have been unloaded!")

  @commands.command(help="Load's the carg", aliases=['!load'])
  @commands.is_owner()
  async def asdloasdasdasdasfasfafad(self, ctx, extension):
        self.client.load_extension(extension)
        await ctx.send(f":inbox_tray: `{extension}`")

  @commands.command(help="Reload's the carg", aliases=['!reload'])
  @commands.is_owner()
  async def relasdffasfasfsfbhashuasgfbasfusaefoad(self, ctx, extension):
        self.client.unload_extension(extension)
        self.client.load_extension(extension)
        await ctx.send(f":repeat: `{extension}`")

  @commands.command(help="Unload's the carg", aliases=['!unload'])
  @commands.is_owner()
  async def dasdjkhnasduiashdishadkjaskdaskdadkasdmnunload(self, ctx, extension):
        self.client.unload_extension(extension)
        await ctx.send(f":outbox_tray: `{extension}`")



def setup (client):
    client.add_cog(All(client))