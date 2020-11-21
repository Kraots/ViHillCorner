import discord
from discord.ext import commands

snipes = {}

class Snipe(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        snipes[message.channel.id] = message

    
    @commands.command()
    async def snipe(self, ctx, *, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            msg = snipes[channel.id]
        except KeyError:
            return await ctx.send('Nothing to snipe!', delete_after=5)
        
        if msg.author.id == 374622847672254466:
            await ctx.send('Hah! You tried, but no ;))')
            return

        if msg.author.bot:
            await ctx.send(f'Cannot snipe messages sent by bots!\n_ _ _ _ Bot: {msg.author.mention}')
            return

        else:
            embed = discord.Embed(description= msg.content, color=msg.author.color, timestamp=msg.created_at)
            embed.set_author(name=msg.author, icon_url=msg.author.avatar_url)
            await ctx.send(embed=embed)


            

def setup (client):
    client.add_cog(Snipe(client))