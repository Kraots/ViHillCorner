import discord
from discord.ext import commands
import time
import utils.colors as color

from pythonping import ping
from utils.helpers import time_phaser

up = time.time()


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def plping(self, ctx):
        global up
        pongEmbed = discord.Embed(title="Pong!", description="_Pinging..._", color=color.inviscolor)
        start = time.time() * 1000
        msg = await ctx.message.channel.send(embed=pongEmbed)
        end = time.time() * 1000
        response_list = ping('gateway.discord.gg', size=56, count=5)
        gateway_ping = response_list.rtt_avg_ms
        pongEmbed = discord.Embed(title="Pong!", description="Gateway: `%sms`\nRest: `%sms`" % (str(gateway_ping), str(int(round(end-start, 0)))), color=color.inviscolor)
        pongEmbed.set_footer(text="Online For: " + str(time_phaser(int(time.time()-up))))
        await msg.edit(embed=pongEmbed)
        await msg.add_reaction('🗑️')


    @commands.command(help="Check bot's ping", hidden=True)
    async def ping(self, ctx):
            botinfo = discord.Embed(title="Pong!", description="_Pinging..._", color=color.inviscolor)
            start = time.time() * 1000
            msg = await ctx.message.channel.send(embed=botinfo)
            end = time.time() * 1000
            botinfo = discord.Embed(title="Pong!", description=f"Avg. Latency: `{(round(self.client.latency * 1000, 2))}ms`\nRest: `{int(round(end-start, 0))}ms`", color=color.inviscolor)
            botinfo.set_footer(text="Online For: " + str(time_phaser(int(time.time()-up))))
            await msg.edit(embed=botinfo)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def uptime(self, ctx):
        uptime = discord.Embed(description=f"Bot has been online for: " + str(time_phaser(int(time.time()-up))), color=color.inviscolor)
        uptime.set_footer(text=f'Bot made by: Kraots#0001', icon_url="https://cdn.discordapp.com/avatars/751724369683677275/0ad4d3b39956b6431c7167ef82c30d30.webp?size=1024")
        msg = await ctx.channel.send(embed=uptime)
        await msg.add_reaction('🗑️')



def setup (client):
    client.add_cog(Ping(client))

    