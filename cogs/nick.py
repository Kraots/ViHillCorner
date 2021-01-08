from discord.ext import commands

class Nicks(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.prefix = "!"
  async def cog_check(self, ctx):
    return ctx.prefix == self.prefix


  @commands.group(invoke_without_command=True, case_insensitive=True)
  @commands.has_any_role('Mod', 'lvl 3+', 'lvl 5+', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+')
  async def nick(self, ctx, *, nick):
            await ctx.author.edit(nick=nick)
            await ctx.reply(f'I have changed your nickname to `{nick}`')

  @nick.command(aliases=['reset', "remove"])
  async def off(self, ctx, nick=None):
      if nick is None:
          nick = ctx.author.name
      await ctx.author.edit(nick=ctx.author.name)
      await ctx.reply("Nickname succesfully removed!")

  @nick.error
  async def nick_error(self, ctx, error):
      if isinstance(error, commands.errors.CommandInvokeError):
          if ctx.author.id == 374622847672254466:
              await ctx.reply("Bots **do not** have permission to change guild owner's nickname!")
          else:
              await ctx.reply("The nickname is too long. Please choose a nickname that's 32 characters or less!")


def setup (client):
    client.add_cog(Nicks(client))