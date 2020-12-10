# IMPORTS
import discord
from discord.ext import commands
import os
import keep_alive
import random
import asyncio


token = os.environ.get('DISCORD_BOT_SECRET')

intents = discord.Intents.all()

# CLIENT
client = commands.Bot(command_prefix=('!', ';;'), case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=False))
client.remove_command("help")
client.load_extension("jishaku")


# COGS
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./outsidereloadcogs'):
  if filename.endswith('.py'):
    client.load_extension(f'outsidereloadcogs.{filename[:-3]}')


# TASK LOOP
async def ch_pr():
    await client.wait_until_ready()
    guild = client.get_guild(750160850077089853)

    status_list = ["carrots", f"{guild.member_count - 12} members"]

    while not client.is_closed():

        status = random.choice(status_list)

        activity = discord.Activity(type=discord.ActivityType.watching, name=status)

        await client.change_presence(status=discord.Status.dnd, activity=activity)

        await asyncio.sleep(60)



# RUN
client.loop.create_task(ch_pr())
keep_alive.keep_alive()
client.run(token)
