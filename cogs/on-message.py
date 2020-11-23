import discord
from discord.ext import commands
import asyncio
import utils.colors as color

class on_message(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, message):

        if message.author.bot:
            return

        if message.author.id == 374622847672254466:
                return

        else:

                
                embed = discord.Embed(color=color.red, description=f'Message deleted in <#{message.channel.id}> \n\n**Content:** \n```{message.content}```', timestamp=message.created_at)
                embed.set_author(name=f'{message.author}', icon_url=f'{message.author.avatar_url}')
                embed.set_footer(text=f'User ID: {message.author.id}')

        message_logging = self.client.get_channel(750432155179679815)
        await message_logging.send(embed=embed)

    @commands.Cog.listener('on_message_edit')
    async def on_message_edit(self, before, after):

        if before.author.bot:
                return
        if before.author.id == 374622847672254466:
                return
        else:
                after_logging = self.client.get_channel(750432155179679815)
                embed = discord.Embed(title="Getting timestamp...", color=color.red)
                msg = await after_logging.send(embed=embed)
                embed = discord.Embed(color=color.yellow, description=f'Message edited in <#{before.channel.id}>\n\n**Before:**\n```{before.content}```\n\n**After:**\n```{after.content}```', timestamp=msg.created_at)
                embed.set_author(name=f'{before.author}', icon_url=f'{before.author.avatar_url}')
                embed.set_footer(text=f'User ID: {before.author.id}')

                await asyncio.sleep(0.5)
                await msg.edit(embed=embed)



    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == 750160850593251449:
            await message.add_reaction("<:hug:750751796317913218>")
            await message.add_reaction("<:bloblove:758378159015723049>")
            await message.add_reaction("<:LoveHeart:777868133087707157>")

        if message.guild is None and not message.author.bot:
            kraots = self.client.get_user(374622847672254466)
            em = discord.Embed(title=f'{message.author}:', description=f'{message.content}', color=color.inviscolor, timestamp=message.created_at)
            em.set_footer(text=f'User ID: {message.author.id}')

            if message.author is kraots:
              return
            
            else:                        
              await kraots.send(embed=em)

        if message.content.startswith('!rank'):
            if message.channel.id in [750160851822182486, 750160851822182487]:
                await message.channel.send("It's `^rank`, noob!")
                return
            
            else:
                await message.channel.send("It's `^rank` in <#750160851822182486> or <#750160851822182487>, NOOB!")
                return
        
        elif message.content.startswith('!help'):
            await message.channel.send("It's `.help`, noob!")
            return





def setup (client):
    client.add_cog(on_message(client))