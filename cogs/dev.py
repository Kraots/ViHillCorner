import discord
from discord.ext import commands
import typing
import asyncio

class developer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['.modmute'])
    @commands.is_owner()
    async def modmutsdjkgnskjkdshgjklshfvuedhfhnkswvvfe(self, ctx, member: discord.Member):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(staff)
        await member.remove_roles(mod)
        await member.add_roles(mute)

        modmute = discord.Embed(color=0xe64343, description=f'Mod {member.mention} has been muted!')
        await ctx.channel.send(embed=modmute)

    @commands.command(aliases=['.modunmute'])
    @commands.is_owner()
    async def modunmasoduhasidhdhjiashdahidasdute(self, ctx, member: discord.Member):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(staff)
        await member.add_roles(mod)
        await member.remove_roles(mute)
        
        modunmute = discord.Embed(color=0xe64343, description=f'Mod {member.mention} has been unmuted!')
        await ctx.channel.send(embed=modunmute)

    @commands.command(aliases=['.makemod'])
    @commands.is_owner()
    async def makemasdljknasdkjbaskdhaskdajksdakdhnod(self, ctx, member: discord.Member):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")

        await member.add_roles(staff)
        await member.add_roles(mod)
        
        modunmute = discord.Embed(color=0xe64343, description=f'{member.mention} is now a mod!')
        await ctx.channel.send(embed=modunmute)

    @commands.command(aliases=['.removemod'])
    @commands.is_owner()
    async def askjdhajidasdaihdjisahdjiadihasdremovemod(self, ctx, member: discord.Member):
        staff = discord.utils.get(ctx.guild.roles, name="Staff")
        mod = discord.utils.get(ctx.guild.roles, name="Mod")
        
        await member.remove_roles(staff)
        await member.remove_roles(mod)
        
        modunmute = discord.Embed(color=0xe64343, description=f'{member.mention} is no longer a mod!')
        await ctx.channel.send(embed=modunmute)

    @commands.command(aliases=['.shutdown'])
    @commands.is_owner()
    async def asdjklnasdjskdhnajkshdjkashdjkhaskdhajdhasjd(self, ctx):
        await ctx.message.add_reaction('✅')
        await self.client.close()

    
    
    
    
    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=[".status"])
    @commands.is_owner()
    async def stasdasdasdhbashdgasihdsukahdisuahdaatus(self, ctx):
      statuses = discord.Embed(title="Statuses:", color=0x2F3136)
      statuses.add_field(name="Online:", value="..status online\n   ..status online-playing [custom status]\n   ..status online-listening [custom status]\n   ..status online-watching [custom status]", inline=False)
      statuses.add_field(name="Idle:", value="..status idle\n   ..status idle-playing [custom status]\n   ..status idle-listening [custom status]\n   ..status idle-watching [custom status]", inline=False)
      statuses.add_field(name="Dnd:", value="..status dnd\n   ..status dnd-playing [custom status]\n   ..status dnd-listening [custom status]\n   ..status dnd-watching [custom status]", inline=False)
      statuses.add_field(name="Offline:", value="..status offline", inline=False)
      await ctx.channel.send(embed=statuses, delete_after=5)
      await asyncio.sleep(4)
      await ctx.message.delete()
      
      

   
   
   
   
   

   
   
    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command()
    @commands.is_owner()
    async def online(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.online)
      await ctx.channel.send("**[ONLINE]** Status succesfully changed.", delete_after=5)



    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["online-playing"])
    @commands.is_owner()
    async def onlinegame(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.playing, name=f"{args}")
        await self.client.change_presence(status=discord.Status.online, activity=listening)
        await ctx.channel.send("**[ONLINE] [PLAYING]** Status succesfully changed.", delete_after=5)

    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["online-listening"])
    @commands.is_owner()
    async def onlinelistening(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.listening, name=f"{args}")
        await self.client.change_presence(status=discord.Status.online, activity=listening)
        await ctx.channel.send("**[ONLINE] [LISTENING]** Status succesfully changed.", delete_after=5)

    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["online-watching"])
    @commands.is_owner()
    async def onlinewatching(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.watching, name=f"{args}")
        await self.client.change_presence(status=discord.Status.online, activity=listening)
        await ctx.channel.send("**[ONLINE] [WATCHING]** Status succesfully changed.", delete_after=5)


















    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command()
    @commands.is_owner()
    async def idle(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.idle)
      await ctx.channel.send("**[IDLE]** Status succesfully changed.", delete_after=5)



    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["idle-playing"])
    @commands.is_owner()
    async def idleplaying(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.playing, name=f"{args}")
        await self.client.change_presence(status=discord.Status.idle, activity=listening)
        await ctx.channel.send("**[IDLE] [PLAYING]** Status succesfully changed.", delete_after=5)

    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["idle-listening"])
    @commands.is_owner()
    async def idlelistening(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)

      else:

        listening= discord.Activity(type=discord.ActivityType.listening, name=f"{args}")
        await self.client.change_presence(status=discord.Status.idle, activity=listening)
        await ctx.channel.send("**[IDLE] [LISTENING]** Status succesfully changed.", delete_after=5)

    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["idle-watching"])
    @commands.is_owner()
    async def idlewatching(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.watching, name=f"{args}")
        await self.client.change_presence(status=discord.Status.idle, activity=listening)
        await ctx.channel.send("**[IDLE] [WATCHING]** Status succesfully changed.", delete_after=5)


















    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command()
    @commands.is_owner()
    async def dnd(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.do_not_disturb)
      await ctx.channel.send("**[DND]** Status succesfully changed.", delete_after=5)



    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["dnd-playing"])
    @commands.is_owner()
    async def dndplaying(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.playing, name=f"{args}")
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=listening)
        await ctx.channel.send("**[DND] [PLAYING]** Status succesfully changed.", delete_after=5)

    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["dnd-listening"])
    @commands.is_owner()
    async def dndlistening(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.listening, name=f"{args}")
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=listening)
        await ctx.channel.send("**[DND] [LISTENING]** Status succesfully changed.", delete_after=5)

    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command(aliases=["dnd-watching"])
    @commands.is_owner()
    async def dndwatching(self, ctx, *, args=None):
      await ctx.message.delete()
      
      if args is None:
        await ctx.channel.send("You must provide args!", delete_after=5)
      
      else:

        listening= discord.Activity(type=discord.ActivityType.watching, name=f"{args}")
        await self.client.change_presence(status=discord.Status.do_not_disturb, activity=listening)
        await ctx.channel.send("**[DND] [WATCHING]** Status succesfully changed.", delete_after=5)
















    @stasdasdasdhbashdgasihdsukahdisuahdaatus.command()
    @commands.is_owner()
    async def offline(self, ctx):
      await ctx.message.delete()
      await self.client.change_presence(status=discord.Status.offline)
      await ctx.channel.send("**[OFFLINE]** Status succesfully changed.", delete_after=5)









def setup (client):
    client.add_cog(developer(client))
