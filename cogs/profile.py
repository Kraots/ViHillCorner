import asyncio
import discord
from discord.ext import commands
import typing

def get_user_image(user: discord.User):
    if str(user.avatar_url_as(static_format='png'))[54:].startswith('a_'):
        image = str(user.avatar_url).rsplit("?", 1)[0]
    else:
        image = user.avatar_url_as(static_format='png')
    return image

def get_member_role(member: discord.Member):
    role = member.top_role.name
    if role == "@everyone":
        role = "N/A"
    return role

def get_member_voice(member: discord.Member):
    return "Not in VC" if not member.voice else member.voice.channel

def create_embed(ctx, user):
    em = discord.Embed(timestamp=ctx.message.created_at, colour=0x2F3136)
    em.add_field(name='User ID', value=user.id, inline=True)
    if isinstance(user, discord.Member):
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Status', value=user.status, inline=True)
        em.add_field(name='In Voice', value=get_member_voice(user), inline=True)
        em.add_field(name='Game', value=user.activity, inline=True)
        em.add_field(name='Highest Role', value=get_member_role(user), inline=True)
        em.add_field(name='Join Date', value=user.joined_at.strftime('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name="\u2800", value=f'[Avatar]({get_user_image(user)})')
    em.add_field(name='Account Created', value=user.created_at.strftime('%A, %d. %B %Y @ %H:%M:%S'))
    em.set_thumbnail(url=get_user_image(user))
    em.set_author(name=user, icon_url=user.avatar_url)
    em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url) 
    return em

class Userinfo(commands.Cog):
    """ Get info for user"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def profile(self, ctx, *, user: typing.Optional[discord.Member]):
        if ctx.invoked_subcommand is None:
            if not user:
                user = ctx.message.author
            em = create_embed(ctx,user)
            await ctx.send(embed=em)
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Userinfo(bot))
