# IMPORTS
import discord
from discord.ext import commands
import os
import keep_alive

token = os.environ.get('DISCORD_BOT_SECRET')

intents = discord.Intents.all()

# CLIENT
client = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=False))
client.remove_command("help")
client.load_extension("jishaku")


# COGS
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./outsidereloadcogs'):
  if filename.endswith('.py'):
    client.load_extension(f'outsidereloadcogs.{filename[:-3]}')



# RUN
keep_alive.keep_alive()
client.run(token)
