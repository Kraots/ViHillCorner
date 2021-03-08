from discord.ext import commands

class Nicks(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.prefix = "!"
  async def cog_check(self, ctx):
    return ctx.prefix == self.prefix


  @commands.group(invoke_without_command=True, case_insensitive=True)
  @commands.has_any_role('Mod', 'lvl 3+', 'lvl 5+', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 55+', 'lvl 50+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
  async def nick(self, ctx, *, nick):
            await ctx.author.edit(nick=nick)
            await ctx.send(f'I have changed your nickname to `{nick}`')

  @nick.command(aliases=['reset', "remove"])
  async def off(self, ctx):
      await ctx.author.edit(nick=None)
      await ctx.send("Nickname succesfully removed!")

  @nick.error
  async def nick_error(self, ctx, error):
      if isinstance(error, commands.errors.CommandInvokeError):
          if ctx.author.id == 374622847672254466:
              await ctx.send("Bots **do not** have permission to change guild owner's nickname!")
          else:
              await ctx.send("The nickname is too long. Please choose a nickname that's 32 characters or less!")


  @off.error
  async def nick_remove_error(self, ctx, error):
      if isinstance(error, commands.errors.CommandInvokeError):
          if ctx.author.id == 374622847672254466:
              await ctx.send("Bots **do not** have permission to change guild owner's nickname!")

			  
def setup (client):
    client.add_cog(Nicks(client))