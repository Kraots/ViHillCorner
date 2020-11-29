import discord
import asyncio
import time
import random
import datetime
import utils.colors as color

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

def profile(ctx, user):
    em = discord.Embed(timestamp=ctx.message.created_at, colour=color.lightpink)
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

def time_phaser(seconds):
    output = ""
    print(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    mo, d = divmod(d, 30)
    if mo > 0:
        output = output + str(int(round(m, 0))) + " Months "
    if d > 0:
        output = output + str(int(round(d, 0))) + " Days "
    if h > 0:
        output = output + str(int(round(h, 0))) + " Hours "
    if m > 0:
        output = output + str(int(round(m, 0))) + " Minutes "
    if s > 0:
        output = output + str(int(round(s, 0))) + " Seconds "
    return output

def Developer(ctx):
    return ctx.author.id == 374622847672254466

def NSFW(ctx):
    return ctx.channel.id == 780374324598145055

def fuckmicroseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

def BotChannels(ctx):
    return ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016]