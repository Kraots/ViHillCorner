import discord
from discord.ext import commands
import utils.colors as color

class on_join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="👋┃welcome")

        welcome = discord.Embed(description='\n\n***Go get roles from*** <#779276428045975573>\n***Go get a color from*** <#779388444304211991>\n***Go get read the rules and see the punishment if u break them at*** <#750160850303582236>\n***Go introduce yourself at*** <#750160850593251449>\n\nEnjoy your stay\n\n', color=color.pastel)
        welcome.set_thumbnail(url=f'{member.avatar_url}')
        guild = self.client.get_guild(750160850077089853)
        msg = f'Hey {member.mention}, welcome to **Anime Hangouts!** \nYou are our **{guild.member_count - 11}** member.\n\n\n<@&750160850077089856>'
        await channel.send(msg, embed=welcome)
        role1 = discord.utils.get(member.guild.roles, name="Member")        
        await member.add_roles(role1)
        role2 = discord.utils.get(member.guild.roles, name="≻─────── ⋆ Epic Roles ⋆ ───────≺")
        await member.add_roles(role2)
        role3 = discord.utils.get(member.guild.roles, name="≻──────── ⋆ Pings  ⋆ ────────≺")
        await member.add_roles(role3)


def setup (client):
    client.add_cog(on_join(client))
