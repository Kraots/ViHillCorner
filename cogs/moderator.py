import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_role('Staff')
    async def region(self, ctx, *, args):
        embed= discord.Embed(title= "***___Where are you from?___***", description= f'\u2800\n{args}', color= 0x2F3136)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        await msg.add_reaction('4️⃣')
        await msg.add_reaction('5️⃣')
        await msg.add_reaction('6️⃣')
        await msg.add_reaction('7️⃣')

    @commands.command()
    @commands.has_role('Staff')
    async def dms(self, ctx, *, args):
        embed = discord.Embed(title="***___Dm's?___***", description=f'\u2800\n{args}', color= 0x2F3136)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('<:vampy_yay:774677177282068501>')
        await msg.add_reaction('<:vampy_cry:750755087986458805>')
        await msg.add_reaction('<:weird:773538796087803934>')

    @commands.command()
    @commands.has_role('Staff')
    async def color(self, ctx, *, args):
        embed = discord.Embed(title="***___React to get the color you like ;))___***", description=f'\u2800\n{args}', color= 0x2F3136)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        await msg.add_reaction('4️⃣')
        await msg.add_reaction('5️⃣')
        await msg.add_reaction('6️⃣')
        await msg.add_reaction('7️⃣')
        await msg.add_reaction("\U00000038\U0000fe0f\U000020e3")
        await msg.add_reaction('\U00000039\U0000fe0f\U000020e3')

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
    
        kick = discord.Embed(description=f"The user has been kicked for the reason: **{reason}**" , color=0xe64343)
    
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

        ban = discord.Embed(description=f"{member.mention} has been banned from the server." , color=0xe64343)

        await ctx.channel.send(embed=ban)



        

    # Unban
    @commands.command(help=".unban [user_ID]")
    @commands.has_role('Staff')
    async def unban(self, ctx, member: discord.Member):
        guild = self.client.get_guild(750160850077089853)
        await guild.unban(member)
        unban = discord.Embed(description= "The user has been unbanned from the server" , color=0xe64343)
        
        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️')
        msg="Congrats! You have been unbanned from Anime Hangouts. Come back: https://discord.gg/mFm5GrQ"
        await member.send(msg)
        await member.guild.kick(member)



    # Clear/Purge
    @commands.command(help=".clear [amount]")
    @commands.has_role('Staff')
    async def clear(self, ctx, amount=0):
            await ctx.channel.purge(limit=amount + 1)

    # Mute
    @commands.command(help=".mute [user] <reason>")
    @commands.has_role('Staff')
    async def mute(self, ctx, member : discord.Member, *, reason="Toxicity & Insult"):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role)     
        unban = discord.Embed(description= f'{member.mention} has been muted for **{reason}**.' , color=0xe64343)
        
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
        unban = discord.Embed(description= f'{member.mention} has been unmuted.' , color=0xe64343)
        
        msg = await ctx.send(embed=unban)
        await msg.add_reaction('🗑️')

        await member.send("You have been unmuted in Anime Hangouts")


    @commands.command(aliases=["ps"])
    @commands.has_role('Staff')
    async def partnership(self, ctx, *, arg):
        await ctx.message.delete()
        embed = discord.Embed(title="NEW PARTNERSHIP", description=f'{arg}', color=0xe64343)
        embed.set_footer(text=f'Partnership by: {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)
        await asyncio.sleep(1)
        await ctx.channel.send("<@&750160850077089861>")


        


def setup (client):
    client.add_cog(Moderation(client))
