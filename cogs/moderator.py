import discord
from discord.ext import commands
import asyncio
import utils.colors as color
from discord.ext.commands import Greedy
from discord import Member
import re
from utils.helpers import time_phaser

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # SLOWMODE
    @commands.command()
    @commands.has_role('Staff')
    async def slowmode(self, ctx, *, time : TimeConverter):
        await ctx.message.delete()
        if time:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.author.send(f'Set slowmode for <#{ctx.channel.id}> to {time_phaser(time)} !')
        else:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.author.send(f'Disabled slowmode for <#{ctx.channel.id}> !')

    # Say
    @commands.command()
    @commands.has_role('Staff')
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)
    
    # Kick
    @commands.command(help=".kick [user] <reason>")
    @commands.has_role('Staff')
    async def kick(self, ctx, member : discord.Member, *, reason="not specified"):
        await member.kick(reason=reason)
    
        kick = discord.Embed(description=f"The user has been kicked for the reason: **{reason}**" , color=color.red)
    
        await ctx.channel.send(embed=kick)

    # MASS KICK 
    @commands.command()
    @commands.has_role('Staff')
    async def masskick(self, ctx, members : Greedy[Member], *, reason="Toxicity & Insult"):
        for member in members:
            msg = "You have been kicked from **Anime Hangouts!**"
            reasonn = discord.Embed(description=f'**Reason:** [{reason}]({ctx.message.jump_url}).', color=color.inviscolor)
            await member.send(msg, embed=reasonn)
            await member.kick()
            kick = discord.Embed(description=f"{member.mention} has been kicked for the reason: [{reason}]({ctx.message.jump_url})" , color=color.red)
        
            await ctx.channel.send(embed=kick)

    # Ban
    @commands.command(help=".ban [user] <reason>")
    @commands.has_role('Staff')
    async def ban(self, ctx, member : discord.Member, *, reason="Toxicty & Insult"):
        reasonn = discord.Embed(description="**Unban appeal server** \n https://discord.gg/rD5z5Jp")
        reasonn.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
        msg="You have been banned from Anime Hangouts. If you think that this has been applied in error please submit a detailed appeal at the following link."
        await member.send(msg, embed=reasonn)

        await member.ban()
        ban = discord.Embed(description=f"{member.mention} has been banned from the server." , color=color.red)

        await ctx.send(embed=ban)


    # MASS BAN 
    @commands.command()
    @commands.has_role('Staff')
    async def massban(self, ctx, members : Greedy[Member]):
        
        reasonn = discord.Embed(description="**Unban appeal server** \n https://discord.gg/rD5z5Jp")
        reasonn.set_image(url="https://thumbs.gfycat.com/SardonicBareArawana-small.gif")
        msg="You have been banned from Anime Hangouts. If you think that this has been applied in error please submit a detailed appeal at the following link."
        
        for member in members:
            await member.send(msg, embed=reasonn)
          
            await member.ban()

            ban = discord.Embed(description=f"{member.mention} has been banned from the server." , color=color.red)

            await ctx.channel.send(embed=ban)




        

    # Unban
    @commands.command(help=".unban [user_ID]")
    @commands.has_role('Staff')
    async def unban(self, ctx, member: discord.Member):
        guild = self.client.get_guild(750160850077089853)
        await guild.unban(member)
        
        unban = discord.Embed(description= "The user has been unbanned from the server" , color=color.red)

        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️')
        msg="Congrats! You have been unbanned from Anime Hangouts. Come back: https://discord.gg/mFm5GrQ"
        await member.send(msg)
        await member.guild.kick(member)

    # MASS UNBAN
    @commands.command(help=".unban [user_ID]")
    @commands.has_role('Staff')
    async def massunban(self, ctx, members: Greedy[Member]):
        guild = self.client.get_guild(750160850077089853)
        for member in members:

            await guild.unban(member)
            
            unban = discord.Embed(description= "The user has been unbanned from the server" , color=color.red)

            msg = await ctx.send(embed=unban)
            await msg.add_reaction('🗑️')
            msg="Congrats! You have been unbanned from Anime Hangouts. Come back: https://discord.gg/mFm5GrQ"
            await member.send(msg)
            await member.guild.kick(member)





    # Clear/Purge
    @commands.command(help=".clear [amount]")
    @commands.has_role('Staff')
    async def clear(self, ctx, amount=0):
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)

    # Mute
    @commands.command(help=".mute [user] <reason>")
    @commands.has_role('Staff')
    async def mute(self, ctx, member : discord.Member, *, reason="Toxicity & Insult"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role)     
        unban = discord.Embed(description= f'{member.mention} has been muted for [{reason}]({ctx.message.jump_url}).' , color=color.red)
        
        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️') 
        reason = discord.Embed(description=f'**Reason:** [{reason}]({ctx.message.jump_url}).', color=color.inviscolor)
        msg="You were muted in Anime Hangouts"

        await member.send(msg, embed=reason)

    # MASS MUTE
    @commands.command(help=".mute [user] <reason>")
    @commands.has_role('Staff')
    async def massmute(self, ctx, members : Greedy[Member], *, reason="Toxicity & Insult"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        for member in members:
            await member.add_roles(role)     
            unban = discord.Embed(description= f'{member.mention} has been muted for [{reason}]({ctx.message.jump_url}).' , color=color.red)
            
            msg = await ctx.send(embed=unban)
            await msg.add_reaction('🗑️') 
            reasonn = discord.Embed(description=f'**Reason:** [{reason}]({ctx.message.jump_url}).', color=color.inviscolor)
            msg="You were muted in Anime Hangouts"

            await member.send(msg, embed=reasonn)




    # Unmute
    @commands.command(help=".unmute [user]")
    @commands.has_role('Staff')
    async def unmute(self, ctx, member : discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)     
        unban = discord.Embed(description= f'{member.mention} has been unmuted.' , color=color.red)
        
        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️')

        await member.send("You have been unmuted in Anime Hangouts")

    # MASS UNMUTE 
    @commands.command(help=".unmute [user]")
    @commands.has_role('Staff')
    async def massunmute(self, ctx, members : Greedy[Member]):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        for member in members:
            await member.remove_roles(role)     
            unban = discord.Embed(description= f'{member.mention} has been unmuted.' , color=color.red)
            
            msg = await ctx.send(embed=unban)
            await msg.add_reaction('🗑️')

            await member.send("You have been unmuted in Anime Hangouts")


    @commands.command(aliases=["ps"])
    @commands.has_role('Staff')
    async def partnership(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(title="NEW PARTNERSHIP", description=f'{arg}', color=color.red)
        embed.set_footer(text=f'Partnership by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
        await asyncio.sleep(1)
        await ctx.channel.send("<@&750160850077089861>")


        


def setup (client):
    client.add_cog(Moderation(client))