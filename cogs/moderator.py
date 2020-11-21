import discord
from discord.ext import commands
import asyncio
import utils.colors as color

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

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
        unban = discord.Embed(description= f'{member.mention} has been muted for **{reason}**.' , color=color.red)
        
        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️') 
        reason = discord.Embed(description=f'**Reason:** [{reason}]({ctx.message.jump_url}).')
        msg="You were muted in Anime Hangouts"

        await member.send(msg, embed=reason)


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
