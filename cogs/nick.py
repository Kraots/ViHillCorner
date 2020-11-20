import discord
from discord.ext import commands

class Nicks(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.group(invoke_without_command=True, case_insensitive=True)
  @commands.has_any_role('Mod', 'lvl 3+', 'lvl 5+', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+')
  async def nick(self, ctx, *, nick):
            await ctx.author.edit(nick=nick)
            await ctx.send(f'Nickname changed to **{nick}.**')

  @nick.command()
  async def off(self, ctx, nick=None):
      if nick is None:
          nick = ctx.author.name
      await ctx.author.edit(nick=ctx.author.name)
      await ctx.send("Nickname succesfully removed!")

  @nick.error
  async def nick_error(self, ctx, error):
      if isinstance(error, commands.errors.CommandInvokeError):
          await ctx.send("The nickname is too long. Please choose a nickname that's 32 characters or less!")


def setup (client):
    client.add_cog(Nicks(client))