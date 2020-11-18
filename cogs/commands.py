import typing
import discord
from discord.ext import commands
import time
import random
from random import randint
import asyncio
from discord.ext.commands.cooldowns import BucketType
import psutil
import os

from datetime import time


class command(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())
    
    @commands.command(help="Get a list of all actions")
    async def actions(self, context):

            version = discord.Embed(title="Here's the list of all actions", description="`.ily`\n`.huggle` \n`.grouphug`\n`.bearhug`\n`.nocry` \n`.chew` \n`.eat` \n`.spray` \n`.sip` \n`.hype` \n`.clap` \n`.cry` \n`.lol` \n`.rofl` \n`.kill` \n`.pat` \n`.nom` \n`.rub` \n`.hug` \n`.catpat` \n`.pillow` \n`.kiss`\n`.shrug`\n`.smug` ", color=0x2F3136)
            version.set_footer(text=f'Requested by: {context.author}', icon_url=context.author.avatar_url)
            await context.message.channel.send(embed=version)

    @commands.command(help="Get a list of all snippets")
    async def snippets(self, context):

            version = discord.Embed(title="Here's the list of all snippets", description="`.fuyu`\n`.welcome`\n`.kraots`\n`.vihillcorner`\n`.s`\n`.thefourhorsemanofsus`\n`.creepy` ", color=0x2F3136)
            version.set_footer(text=f'Requested by: {context.author}', icon_url=context.author.avatar_url)
            await context.message.channel.send(embed=version)

    @commands.command(help="Change your nickname")
    @commands.has_any_role('Mod', 'lvl 3+', 'lvl 5+', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+')
    async def nick(self, ctx, *, nick):
            await ctx.author.edit(nick=nick)
            await ctx.send(f'Nickname changed to **{nick}.**')

    @commands.command()
    async def created(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(color=0x2F3136)
        embed.add_field(name=f"{member.name}'s account was made on:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def joined(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(color=0x2F3136)
        embed.add_field(name=f"{member.name} joined on:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        await ctx.channel.send(embed=embed)

    @commands.command(help="Get a list of all snippets", aliases=["inv", "invite"])
    async def _invite(self, context):

            version = discord.Embed(title="Here's the invite:", description="[Anime Hangouts](https://discord.gg/Uf2kA8q)", color=0x2F3136)
            version.set_footer(text=f'Requested by: {context.author}', icon_url=context.author.avatar_url)

            await context.message.channel.send(embed=version)

    @commands.command(hidden=True)
    async def botinfo(self, ctx):
        guilds = len(list(self.client.guilds))
        cache_summary = f"**{len(self.client.guilds)}** guild(s) and **{len(self.client.users)}** user(s)"
        botinfo = discord.Embed(title="", color=0x2F3136, timestamp=ctx.message.created_at)
        botinfo.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        botinfo.add_field(name="Bot Owner:", value="Kraots#0001", inline=False)
        botinfo.add_field(name="Created at:", value="05/09/2020", inline=False)
        botinfo.add_field(name="Info", value=f"This bot is not sharded and can see {cache_summary}")
        botinfo.add_field(name="Commands loaded", value=f"{len([x.name for x in self.client.commands])}", inline=False)
        botinfo.add_field(name="About:", value="*This bot is a private bot (meaning it is not open sourced) made only for Anime Hangouts, so do not ask to host it or to add it to your server!*", inline=True)
        botinfo.set_thumbnail(url="https://cdn.discordapp.com/avatars/751724369683677275/0ad4d3b39956b6431c7167ef82c30d30.webp?size=1024")
        await ctx.channel.send(embed=botinfo)

    @commands.command(hidden=True)
    async def membercount(self, ctx):
            guild = self.client.get_guild(750160850077089853)
            await ctx.channel.send(f'`{guild.member_count - 12}` members.') 

    @commands.command(hidden=True, aliases=["av", "avatar"])
    async def _av(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if member is None:
            member = ctx.author

        avatar = discord.Embed(description=f'[{member.name}]({member.avatar_url})', color=0x708DD0)
        avatar.set_image(url=member.avatar_url)
        avatar.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=avatar)


    @commands.group(aliases=['server', 'sinfo', 'si'], pass_context=True, invoke_without_command=True)
    async def serverinfo(self, ctx, *, msg=""):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            if msg:
                server = None
                try:
                    float(msg)
                    server = self.client.get_guild(int(msg))
                    if not server:
                        return await ctx.send(
                                              self.client.client_prefix + 'Server not found.')
                except:
                    for i in self.client.guilds:
                        if i.name.lower() == msg.lower():
                            server = i
                            break
                    if not server:
                        return await ctx.send(self.client.client_prefix + 'Could not find server. Note: You must be a member of the server you are trying to search.')
            else:
                server = ctx.message.guild

            online = 0
            for i in server.members:
                if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    online += 1
            all_users = []
            for user in server.members:
                all_users.append('{}#{}'.format(user.name, user.discriminator))
            all_users.sort()
            

            channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

            role_count = len(server.roles)
            emoji_count = len(server.emojis)

            em = discord.Embed(color=0x2F3136)
            em.add_field(name='Name', value=server.name)
            em.add_field(name='Owner', value=server.owner, inline=False)
            em.add_field(name='Members', value=server.member_count)
            em.add_field(name='Currently Online', value=online)
            em.add_field(name='Text Channels', value=str(channel_count))
            em.add_field(name='Region', value=server.region)
            em.add_field(name='Verification Level', value=str(server.verification_level))
            em.add_field(name='Highest role', value="Staff")
            em.add_field(name='Number of roles', value=str(role_count))
            em.add_field(name='Number of emotes', value=str(emoji_count))
            em.add_field(name='Created At', value=server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
            em.set_thumbnail(url=server.icon_url)
            em.set_author(name='Server Info')
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
           
            await ctx.send(embed=em)

    @commands.command()
    async def ee(self, ctx, emoji: discord.PartialEmoji):
        await ctx.message.delete()

        embed = discord.Embed(color=0x2F3136)
        embed.set_image(url=emoji.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def ad(self, ctx):
        await ctx.message.delete()
        ad = discord.Embed(color=0x2F3136, title="Here's the ad to the server:", description="**__Anime Hangouts__**\nAnime Hangouts is mainly for anime & talking & meeting new people & generally chatting!\n\n**WHAT WE HAVE TO OFFER**\n★ Awesome Private Bot\n★ Fun Channels\n★ Active Users\n★ Lots Of Emotes\n★ Reaction Roles\n\nConvinced?\n\nhttps://discord.gg/Uf2kA8q")
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=ad)

    @commands.command(aliases=["ra"])
    async def rawad(self, ctx):
        await ctx.message.delete()
        ad = discord.Embed(color=0x2F3136, title="Here's the raw ad version of the server:", description="```**__Anime Hangouts__**\nAnime Hangouts is mainly for anime & talking & meeting new people & generally chatting!\n\n**WHAT WE HAVE TO OFFER**\n★ Awesome Private Bot\n★ Fun Channels\n★ Active Users\n★ Lots Of Emotes\n★ Reaction Roles\n\nConvinced?\n\nhttps://discord.gg/Uf2kA8q```")
        ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=ad)

    @commands.command(aliases=['chat revive', 'revive', 'revive chat'])
    @commands.cooldown(1, 7200, commands.BucketType.guild)
    async def _asdjknasdjkn(self, ctx):
        await ctx.message.delete()
        msg = '<@&750160850236604537>'
        revive = self.client.get_channel(761652915450413106)
        await revive.send(msg)

    @commands.command(aliases=["untill-partner", "up"])
    async def _sdlajkndasjkdn(self, ctx):
        guild = self.client.get_guild(750160850077089853)
        await ctx.channel.send(f'Members left untill the server can apply for the *discord partership program:* \n\n`{500 - guild.member_count + 12}`')




def setup (client):
    client.add_cog(command(client))
