import discord
import asyncio
import random
import utils.colors as color
from typing import Union
from utils import time, formats
import os, datetime
from discord.ext.buttons import Paginator
from discord.ext import commands

import typing
import pkg_resources

class Pag(Paginator):
	def __init__(self, *, title: str = '', length: int = 10, entries: list = None,
				extra_pages: list = None, prefix: str = '', suffix: str = '', format: str = '',
				colour: Union[int, discord.Colour] = discord.Embed.Empty,
				color: Union[int, discord.Colour] = discord.Embed.Empty, use_defaults: bool = True, embed: bool = True,
				joiner: str = '\n', timeout: int = 180, thumbnail: str = None, ctx, footer: str = ''):
		super().__init__(title=title, length=length, entries=entries, extra_pages=extra_pages, prefix=prefix, suffix=suffix, format=format, colour=colour, color=color, use_defaults=use_defaults, embed=embed, joiner=joiner, timeout=timeout, thumbnail=thumbnail)
		self.ctx = ctx
		self.footer = footer

	async def cancel(self):
		self._cancelled = True
		self._session_task.cancel()
		await self.page.clear_reactions()

	async def teardown(self):
		self._cancelled = True
		
		try:
			await self.page.delete()
			await self.ctx.message.delete()
		except discord.HTTPException:
			pass
		
		self._session_task.cancel()

	async def _default_indexer(self, control, ctx, member):
		previous = self._index

		if control == 'stop':
			return await self.teardown()

		if control == 'end':
			self._index = len(self._pages) - 1
		elif control == 'start':
			self._index = 0
		else:
			self._index += control

		if self._index > len(self._pages) - 1 or self._index < 0:
			self._index = previous

		if self._index == previous:
			return

		if isinstance(self._pages[self._index], discord.Embed):
			await self.page.edit(embed=self._pages[self._index])
		else:
			await self.page.edit(content=self._pages[self._index])

	async def _paginate(self, ctx: commands.Context):
		if not self.entries and not self.extra_pages:
			raise AttributeError('You must provide atleast one entry or page for pagination.')  # ^^

		if self.entries:
			self.entries = [self.formatting(entry) for entry in self.entries]
			entries = list(self.chunker())
		else:
			entries = []

		for chunk in entries:
			if not self.use_embed:
				self._pages.append(self.joiner.join(chunk))
			else:
				embed = discord.Embed(title=self.title, description=self.joiner.join(chunk), colour=self.colour)

				if self.thumbnail:
					embed.set_thumbnail(url=self.thumbnail)
				if self.footer:
					embed.set_footer(text=self.footer)

				self._pages.append(embed)

		self._pages = self._pages + self.extra_pages

		if isinstance(self._pages[0], discord.Embed):
			self.page = await ctx.send(embed=self._pages[0])
		else:
			self.page = await ctx.send(self._pages[0])

		self._session_task = ctx.bot.loop.create_task(self._session(ctx))

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