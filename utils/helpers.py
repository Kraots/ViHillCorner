import discord
import asyncio
import random
import utils.colors as color
from typing import Union
from utils import time, formats
import os, datetime
from discord.ext.buttons import Paginator
from PIL import Image, ImageFont, ImageDraw
import numpy as np

import typing
import pkg_resources

GRAY = (48, 48, 48)
ORANGE = (255, 128, 0)
TRANSPARENT = (0, 0, 0, 0)
BLUE = (22, 160, 245)
BLACK = (0, 0, 0)

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

def get_font(text, image):
	fontsize = 1
	font = ImageFont.truetype("arial.ttf", fontsize)
	while font.getsize(text)[0] < image.size[0]:
		fontsize += 1
		font = ImageFont.truetype("arial.ttf", fontsize)
	while font.getsize(text)[1] > image.size[1]:
		fontsize -= 1
		font = ImageFont.truetype("arial.ttf", fontsize)
	fontsize -= 1
	font = ImageFont.truetype("arial.ttf", fontsize)
	return font

async def rank_card(user, level: int, rank: int, members_count: int, current_xp: int, needed_xp: int, percentage: float):
	max_lvl = False
	if level == 500:
		max_lvl = True
	
	img = Image.new("RGBA", (1000, 350), GRAY)
	await user.avatar_url_as(format='jpg').save(fp='avatar.png')
	
	av = Image.open('avatar.png')
	h, w = av.size
	npImage = np.array(av)
	new_img = Image.new('L', av.size, 0)
	draw = ImageDraw.Draw(new_img)
	draw.pieslice([0, 0, h, w], 0, 360, fill=255)
	np_new = np.array(new_img)
	npImage = np.dstack((npImage, np_new))
	final_img = Image.fromarray(npImage)
	final_img.thumbnail((250, 250))
	final_img.save('avatar.png')
	av = Image.open('avatar.png')

	orange_line = Image.new("RGBA", (500, 10), ORANGE)
	
	_user = Image.new("RGBA", (500, 50), TRANSPARENT)
	draw = ImageDraw.Draw(_user)
	txt = str(user.display_name) + '#' + str(user.discriminator)
	font = get_font(txt, _user)
	draw.text((0, 0), txt, font=font)

	has_xp = Image.new("RGBA", (200, 40), TRANSPARENT)
	draw = ImageDraw.Draw(has_xp)
	font = ImageFont.truetype('arial.ttf', 35)
	draw.text((0, 0), f"{current_xp:,}xp", font=font, fill=BLACK)

	percent = Image.new("RGBA", (130, 40), TRANSPARENT)
	draw = ImageDraw.Draw(percent)
	font = ImageFont.truetype('arial.ttf', 35)
	if max_lvl != True:
		draw.text((10, 0), f"{percentage}%", font=font, fill=BLACK)
	else:
		draw.text((10, 0), f"MAX", font=font, fill=BLACK)

	next_xp = Image.new("RGBA", (200, 40), TRANSPARENT)
	draw = ImageDraw.Draw(next_xp)
	font = ImageFont.truetype('arial.ttf', 35)
	if len(str(needed_xp)) == 3:
		z = f"    {needed_xp:,}xp"
	else:
		z = f"{needed_xp:,}xp"
	draw.text((0, 0), z, font=font, fill=BLACK)

	progressbar = Image.new("RGBA", (750, 50), (0, 0, 0, 0))
	d = ImageDraw.Draw(progressbar)
	d = drawProgressBar(d, 0, 0, 650, 45, percentage/100, fg=BLUE)

	_rank = Image.new("RGBA", (235, 100))
	draw = ImageDraw.Draw(_rank)
	font = ImageFont.truetype('arial.ttf', 35)
	draw.text((0, 0), f"     Rank:\n        {rank}/{members_count}", font=font)

	_level = Image.new("RGBA", (235, 100))
	draw = ImageDraw.Draw(_level)
	font = ImageFont.truetype('arial.ttf', 35)
	if max_lvl != True:
		draw.text((0, 0), f"     Level:\n       {level}", font=font)
	else:
		draw.text((0, 0), f"     Level:\n       500(Max)", font=font)

	img.paste(im=av, mask=av, box=(10, 50))
	img.paste(im=orange_line, box=(350, 100))
	img.paste(im=_user, mask=_user, box=(350, 50))
	img.paste(im=progressbar, mask=progressbar, box=(275, 250))
	if max_lvl != True:
		img.paste(im=has_xp, mask=has_xp, box=(285, 255))
		img.paste(im=next_xp, mask=next_xp, box=(820, 255))
	img.paste(im=percent, mask=percent, box=(552, 255))
	img.paste(im=_rank, mask=_rank, box=(325, 125))
	img.paste(im=_level, mask=_level, box=(600, 125))
	img.save('rank_card.png')
	
	f = discord.File(fp='rank_card.png', filename='rank_card.png')
	
	return f