import discord
import asyncio
import random
import utils.colors as color
from typing import Union
from utils import time, formats
import os, datetime
from discord.ext.buttons import Paginator
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

import typing
import pkg_resources


class Pag(Paginator):
	async def teardown(self):
		try:
			await self.page.clear_reactions()
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

def time_phaserr(seconds):
	output = ""
	print(seconds)
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
	"""
	Returns package version as a string, or None if it couldn't be found.
	"""

	try:
		return pkg_resources.get_distribution(package_name).version
	except (pkg_resources.DistributionNotFound, AttributeError):
		return None

def drawProgressBar(d, x, y, w, h, progress, bg="white", fg="black"):
	# draw background
	d.ellipse((x+w, y, x+h+w, y+h), fill=bg)
	d.ellipse((x, y, x+h, y+h), fill=bg)
	d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)

	# draw progress bar
	w *= progress
	if w != 0.0:
		d.ellipse((x+w, y, x+h+w, y+h),fill=fg)
		d.ellipse((x, y, x+h, y+h),fill=fg)
		d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=fg)

	return d
