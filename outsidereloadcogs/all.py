import discord
from discord.ext import commands
import os

class All(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.prefix = ";;"
  async def cog_check(self, ctx):
    return ctx.prefix == self.prefix


  @commands.command(aliases=["reload-all"])
  @commands.is_owner()
  async def reloadall(self, ctx):


    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.unload_extension(f'cogs.{filename[:-3]}')
    
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.load_extension(f'cogs.{filename[:-3]}')

    await ctx.channel.send("All cogs have been reloaded!")


  @commands.command(aliases=["load-all"])
  @commands.is_owner()
  async def loadall(self, ctx):

    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.load_extension(f'cogs.{filename[:-3]}')

    await ctx.channel.send("All cogs have been loaded!")

  @commands.command(aliases=["unload-all"])
  @commands.is_owner()
  async def unloadall(self, ctx):
  
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        self.client.unload_extension(f'cogs.{filename[:-3]}')

    await ctx.channel.send("All cogs have been unloaded!")

  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, extension):
        self.client.load_extension(extension)
        await ctx.send(f":inbox_tray: `{extension}`")

  @commands.command()
  @commands.is_owner()
  async def reload(self, ctx, extension):
        self.client.unload_extension(extension)
        self.client.load_extension(extension)
        await ctx.send(f":repeat: `{extension}`")

  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, extension):
        self.client.unload_extension(extension)
        await ctx.send(f":outbox_tray: `{extension}`")



def setup (client):
    client.add_cog(All(client))