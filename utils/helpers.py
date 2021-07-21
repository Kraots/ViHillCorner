import discord
import asyncio
import random
import utils.colors as color
from typing import Union
from utils import time, formats
import os, datetime
from discord.ext.buttons import Paginator

import typing
import pkg_resources

class Pag(Paginator):
	def __init__(self, *, title: str = '', length: int = 10, entries: list = None,
				extra_pages: list = None, prefix: str = '', suffix: str = '', format: str = '',
				colour: Union[int, discord.Colour] = discord.Embed.Empty,
				color: Union[int, discord.Colour] = discord.Embed.Empty, use_defaults: bool = True, embed: bool = True,
				joiner: str = '\n', timeout: int = 180, thumbnail: str = None, ctx):
		super().__init__(title=title, length=length, entries=entries, extra_pages=extra_pages, prefix=prefix, suffix=suffix, format=format, colour=colour, color=color, use_defaults=use_defaults, embed=embed, joiner=joiner, timeout=timeout, thumbnail=thumbnail)
		self.ctx = ctx

	async def teardown(self):
		try:
			await self.ctx.message.delete()
			await self.page.delete()
		except discord.HTTPException:
			pass

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
	
	def format_date(dt):
		if dt is None:
			return 'N/A'
		return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

	em = discord.Embed(timestamp=ctx.message.created_at, colour=color.lightpink)
	em.add_field(name='User ID', value=user.id, inline=False)
	if isinstance(user, discord.Member):
		em.add_field(name='Nick', value=user.nick, inline=False)
		em.add_field(name='Status', value=user.status, inline=False)
		voice = getattr(user, 'voice', None)
		if voice is not None:
			vc = voice.channel
			other_people = len(vc.members) - 1
			voice = f'`{vc.name}` with {other_people} others' if other_people else f'`{vc.name}` by themselves'
			em.add_field(name='In Voice', value=voice, inline=False)
		em.add_field(name='Game', value=user.activity, inline=False)
		em.add_field(name='Highest Role', value=get_member_role(user), inline=False)
		em.add_field(name='Join Date', value=format_date(getattr(user, 'joined_at', None)), inline=False)
		em.add_field(name="Avatar", value=f'[Click Here]({get_user_image(user)})', inline=False)
	em.add_field(name='Account Created', value=format_date(user.created_at), inline=False)
	em.set_thumbnail(url=get_user_image(user))
	em.set_author(name=user, icon_url=user.avatar_url)
	em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url) 
	return em

def time_phaser(seconds):
	output = ""
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	mo, d = divmod(d, 30)
	if mo > 0:
		output = output + str(int(round(m, 0))) + " months "
	if d > 0:
		output = output + str(int(round(d, 0))) + " days "
	if h > 0:
		output = output + str(int(round(h, 0))) + " hours "
	if m > 0:
		output = output + str(int(round(m, 0))) + " minutes "
	if s > 0:
		output = output + str(int(round(s, 0))) + " seconds "
	return output

def Developer(ctx):
	return ctx.author.id == 374622847672254466

def NSFW(ctx):
	return ctx.channel.id == 780374324598145055

def BotChannels(ctx):
	return ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016]

def clean_code(content):
	if content.startswith("```") and content.endswith("```"):
		return "\n".join(content.split("\n")[1:])[:-3]
	else:
		return content

def package_version(package_name: str) -> typing.Optional[str]:
	try:
		return pkg_resources.get_distribution(package_name).version
	except (pkg_resources.DistributionNotFound, AttributeError):
		return None

def format_balance(balance):
    cBalance = "{:,}".format(balance)
    sBalance = cBalance.split(",")
    if len(sBalance) == 1:
        return str(balance)
    elif len(sBalance) == 2:
        sign = "K"
    elif len(sBalance) == 3:
        sign = "M"
    elif len(sBalance) == 4:
        sign = "B"
    elif len(sBalance) == 5:
        sign = "T"
    elif len(sBalance) >= 6:
        sign = "Q"
    fBalance = sBalance[0] + "." + sBalance[1][0:2] + sign
    return fBalance