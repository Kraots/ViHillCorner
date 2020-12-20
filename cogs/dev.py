import discord
from discord.ext import commands
import asyncio
import utils.colors as color
from discord.ext.commands import Greedy
from discord import Member
import os
import sys
    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

class developer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = ";;"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx):
        em = discord.Embed(color=color.lightpink, title="ViHill Corner Rerver Rules", description="We have a small but strict set of rules on our server. Please read over them and take them on board. If you don't understand anything or need some clarification, feel free to ask any staff member!")
        em.add_field(name="Rule 1", value="Follow the [Discord Community Guidelines](https://discord.com/guidelines) and [Terms Of Service](https://discord.com/terms).", inline=False)
        em.add_field(name="Rule 2", value="Follow the [ViHill Corner Code Of Conduct](https://medium.com/vihill-corner/vihill-corner-code-of-conduct-7f187ab0c56).", inline=False)
        em.add_field(name="Rule 3", value="Listen to and respect staff members and their instructions.", inline=False)
        em.add_field(name="Rule 4", value="This is an English-speaking server, so please speak English to the best of your ability", inline=False)
        em.add_field(name="Rule 5", value="No advertising of any kind, including in a server member’s DM.", inline=False)

        await ctx.send(embed=em)


    @commands.command()
    @commands.is_owner()
    async def mail(self, ctx, members : Greedy[Member]=None, *, args=None):
      if members is None:
        await ctx.channel.send("You must provide a user!")
        return

      if args is None:
        await ctx.channel.send("You must provide args!")
        return

      for member in members:
            await member.send(f'{args}')
            await ctx.message.add_reaction('✅')


    @commands.command()
    @commands.is_owner()
    async def modmute(self, ctx, members: Greedy[Member]):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        
        for member in members:
            await member.add_roles(mute)
            await member.remove_roles(staff)
            await member.remove_roles(mod)

            modmute = discord.Embed(color=color.red, description=f'Mod {member.mention} has been muted!')
            await ctx.channel.send(embed=modmute)


    @commands.command()
    @commands.is_owner()
    async def modunmute(self, ctx, members: Greedy[Member]):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        
        for member in members: 
            await member.add_roles(staff)
            await member.add_roles(mod)
            await member.remove_roles(mute)
        
            modunmute = discord.Embed(color=color.red, description=f'Mod {member.mention} has been unmuted!')
            await ctx.channel.send(embed=modunmute)

    @commands.command()
    @commands.is_owner()
    async def makemod(self, ctx, members: Greedy[Member]):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")

        for member in members:
            await member.add_roles(staff)
            await member.add_roles(mod)
        
            modunmute = discord.Embed(color=color.red, description=f'{member.mention} is now a mod!')
            await ctx.channel.send(embed=modunmute)

    @commands.command()
    @commands.is_owner()
    async def removemod(self, ctx, members: Greedy[Member]):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")
        
        for member in members:
            await member.remove_roles(staff)
            await member.remove_roles(mod)
        
            modunmute = discord.Embed(color=color.red, description=f'{member.mention} is no longer a mod!')
            await ctx.channel.send(embed=modunmute)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.message.add_reaction('✅')
        await self.client.close()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("*Restarting...*")
        restart_program()
    
    
    
    
    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def status(self, ctx):
      statuses = discord.Embed(title="Statuses:", color=color.lightpink)
      statuses.add_field(name="Online:", value=";;status online\n   ;;status online playing [custom status]\n   ;;status online listening [custom status]\n   ;;status online watching [custom status]", inline=False)
      statuses.add_field(name="Idle:", value=";;status idle\n   ;;status idle playing [custom status]\n   ;;status idle listening [custom status]\n   ;;status idle watching [custom status]", inline=False)
      statuses.add_field(name="Dnd:", value=";;status dnd\n   ;;status dnd playing [custom status]\n   ;;status dnd listening [custom status]\n   ;;status dnd watching [custom status]", inline=False)
      statuses.add_field(name="Offline:", value=";;status offline", inline=False)
      await ctx.channel.send(embed=statuses, delete_after=5)
      await asyncio.sleep(4)
      await ctx.message.delete()
      
      

   
   
   
   
   

   
   
    @status.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def online(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.online)
      await ctx.channel.send("**[ONLINE]** Status succesfully changed.", delete_after=5)



    @online.command(aliases=["playing"])
    @commands.is_owner()
    async def online_playing(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.playing, name=f"{args}")
        await self.client.change_presence(status=discord.Status.online, activity=listening)
        await ctx.channel.send("**[ONLINE] [PLAYING]** Status succesfully changed.", delete_after=5)

    @online.command(aliases=["listening"])
    @commands.is_owner()
    async def online_listening(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.listening, name=f"{args}")
        await self.client.change_presence(status=discord.Status.online, activity=listening)
        await ctx.channel.send("**[ONLINE] [LISTENING]** Status succesfully changed.", delete_after=5)

    @online.command(aliases=["watching"])
    @commands.is_owner()
    async def online_watching(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.watching, name=f"{args}")
        await self.client.change_presence(status=discord.Status.online, activity=listening)
        await ctx.channel.send("**[ONLINE] [WATCHING]** Status succesfully changed.", delete_after=5)


















    @status.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def idle(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.idle)
      await ctx.channel.send("**[IDLE]** Status succesfully changed.", delete_after=5)



    @idle.command(aliases=["playing"])
    @commands.is_owner()
    async def idle_playing(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.playing, name=f"{args}")
        await self.client.change_presence(status=discord.Status.idle, activity=listening)
        await ctx.channel.send("**[IDLE] [PLAYING]** Status succesfully changed.", delete_after=5)

    @idle.command(aliases=["listening"])
    @commands.is_owner()
    async def idle_listening(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)

      else:

        listening= discord.Activity(type=discord.ActivityType.listening, name=f"{args}")
        await self.client.change_presence(status=discord.Status.idle, activity=listening)
        await ctx.channel.send("**[IDLE] [LISTENING]** Status succesfully changed.", delete_after=5)

    @idle.command(aliases=["watching"])
    @commands.is_owner()
    async def idle_watching(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.watching, name=f"{args}")
        await self.client.change_presence(status=discord.Status.idle, activity=listening)
        await ctx.channel.send("**[IDLE] [WATCHING]** Status succesfully changed.", delete_after=5)


















    @status.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def dnd(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.do_not_disturb)
      await ctx.channel.send("**[DND]** Status succesfully changed.", delete_after=5)



    @dnd.command(aliases=["playing"])
    @commands.is_owner()
    async def dnd_playing(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.playing, name=f"{args}")
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=listening)
        await ctx.channel.send("**[DND] [PLAYING]** Status succesfully changed.", delete_after=5)

    @dnd.command(aliases=["listening"])
    @commands.is_owner()
    async def dnd_listening(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.listening, name=f"{args}")
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=listening)
        await ctx.channel.send("**[DND] [LISTENING]** Status succesfully changed.", delete_after=5)

    @dnd.command(aliases=["watching"])
    @commands.is_owner()
    async def dnd_watching(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.watching, name=f"{args}")
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=listening)
        await ctx.channel.send("**[DND] [WATCHING]** Status succesfully changed.", delete_after=5)
















    @status.command()
    @commands.is_owner()
    async def offline(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.offline)
      await ctx.channel.send("**[OFFLINE]** Status succesfully changed.", delete_after=5)






def setup (client):
    client.add_cog(developer(client))
