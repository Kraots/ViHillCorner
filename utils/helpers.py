import disnake
import asyncio
import random
import utils.colors as color
from typing import Union
from utils import time, formats
import os, datetime
from disnake.ext import commands
from traceback import format_exception
import re
import string
from .pag import Paginator

import typing
import pkg_resources

class Pag(Paginator):
	def __init__(self, *, title: str = '', length: int = 10, entries: list = None,
				extra_pages: list = None, prefix: str = '', suffix: str = '', format: str = '',
				colour: Union[int, disnake.Colour] = disnake.Embed.Empty,
				color: Union[int, disnake.Colour] = disnake.Embed.Empty, use_defaults: bool = True, embed: bool = True,
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
		except disnake.HTTPException:
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

		if isinstance(self._pages[self._index], disnake.Embed):
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
				embed = disnake.Embed(title=self.title, description=self.joiner.join(chunk), colour=self.colour)

				if self.thumbnail:
					embed.set_thumbnail(url=self.thumbnail)
				if self.footer:
					embed.set_footer(text=self.footer)

				self._pages.append(embed)

		self._pages = self._pages + self.extra_pages

		if isinstance(self._pages[0], disnake.Embed):
			self.page = await ctx.send(embed=self._pages[0])
		else:
			self.page = await ctx.send(self._pages[0])

		self._session_task = ctx.bot.loop.create_task(self._session(ctx))

def get_user_image(user: disnake.User):
	if str(user.avatar.url_as(static_format='png'))[54:].startswith('a_'):
		image = str(user.avatar.url).rsplit("?", 1)[0]
	else:
		image = user.avatar.url_as(static_format='png')
	return image

def get_member_role(member: disnake.Member):
	role = member.top_role.name
	if role == "@everyone":
		role = "N/A"
	return role

def get_member_voice(member: disnake.Member):
	return "Not in VC" if not member.voice else member.voice.channel

def profile(ctx, user):
	
	def format_date(dt):
		if dt is None:
			return 'N/A'
		return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

	em = disnake.Embed(timestamp=ctx.message.created_at.replace(tzinfo=None), colour=color.lightpink)
	em.add_field(name='User ID', value=user.id, inline=False)
	if isinstance(user, disnake.Member):
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
		em.add_field(name='Join Date', value=format_date(user.joined_at.replace(tzinfo=None)), inline=False)
		em.add_field(name="Avatar", value=f'[Click Here]({get_user_image(user)})', inline=False)
	em.add_field(name='Account Created', value=format_date(user.created_at.replace(tzinfo=None)), inline=False)
	em.set_thumbnail(url=get_user_image(user))
	em.set_author(name=user, icon_url=user.avatar.url)
	em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar.url) 
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
		output = output + str(int(round(s, 0))) + " seconds"
	return output

def Developer(ctx):
	return ctx.author.id == 374622847672254466

def NSFW(ctx):
	return ctx.channel.id == 780374324598145055

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
		return str(balance).replace('.0', '')
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

async def reraise(ctx, error):
	if isinstance(error, commands.NotOwner):
		error = disnake.Embed(title="ERROR", description="Command Error: You do not own this bot!")
		
		await ctx.send(embed=error, delete_after=8)
		await asyncio.sleep(7.5)
		await ctx.message.delete()
		
	elif isinstance(error, commands.errors.CommandNotFound):
		return
	
	elif isinstance(error, commands.CommandOnCooldown):
		return await ctx.send(f'This command is on cooldown!\n**{time_phaser(error.retry_after)}** remaining.')

	elif isinstance(error, commands.errors.MissingRequiredArgument):
		return await ctx.send(f"You are missing an argument! See `!help {ctx.command}` if you do not know how to use this.")

	elif isinstance(error, commands.errors.MemberNotFound):
		await ctx.send("Could not find member.")
		ctx.command.reset_cooldown(ctx)
		return

	elif isinstance(error, commands.errors.UserNotFound):
		await ctx.send("Could not find user.")
		ctx.command.reset_cooldown(ctx)
		return

	elif isinstance(error, commands.errors.CheckFailure):
		ctx.command.reset_cooldown(ctx)
		return

	else:
		get_error = "".join(format_exception(error, error, error.__traceback__))
		em = disnake.Embed(description=f'```py\n{get_error}\n```')
		if ctx.guild.id == 750160850077089853:
			await ctx.bot._owner.send(content=f"**An error occured with the command `{ctx.command}`, here is the error:**", embed=em)
			em = disnake.Embed(title='Oops... An error has occured.', description='An error has occured while invoking this command and has been sent to my master to fix it.', color=color.red)
			await ctx.send(embed=em)
		else:
			await ctx.send(embed=em)

def replace_many(
	sentence: str, replacements: dict, *, ignore_case: bool = False, match_case: bool = False
) -> str:
	"""
	Replaces multiple substrings in a string given a mapping of strings.
	By default replaces long strings before short strings, and lowercase before uppercase.
	Example:
		var = replace_many("This is a sentence", {"is": "was", "This": "That"})
		assert var == "That was a sentence"
	If `ignore_case` is given, does a case insensitive match.
	Example:
		var = replace_many("THIS is a sentence", {"IS": "was", "tHiS": "That"}, ignore_case=True)
		assert var == "That was a sentence"
	If `match_case` is given, matches the case of the replacement with the replaced word.
	Example:
		var = replace_many(
			"This IS a sentence", {"is": "was", "this": "that"}, ignore_case=True, match_case=True
		)
		assert var == "That WAS a sentence"
	"""
	if ignore_case:
		replacements = dict(
			(word.lower(), replacement) for word, replacement in replacements.items()
		)

	words_to_replace = sorted(replacements, key=lambda s: (-len(s), s))

	# Join and compile words to replace into a regex
	pattern = "|".join(re.escape(word) for word in words_to_replace)
	regex = re.compile(pattern, re.I if ignore_case else 0)

	def _repl(match: re.Match) -> str:
		"""Returns replacement depending on `ignore_case` and `match_case`."""
		word = match.group(0)
		replacement = replacements[word.lower() if ignore_case else word]

		if not match_case:
			return replacement

		# Clean punctuation from word so string methods work
		cleaned_word = word.translate(str.maketrans("", "", string.punctuation))
		if cleaned_word.isupper():
			return replacement.upper()
		elif cleaned_word[0].isupper():
			return replacement.capitalize()
		else:
			return replacement.lower()

	return regex.sub(_repl, sentence)

def suppress_links(message: str) -> str:
    """Accepts a message that may contain links, suppresses them, and returns them."""
    for link in set(re.findall(r"https?://[^\s]+", message, re.IGNORECASE)):
        message = message.replace(link, f"<{link}>")
    return message

class ConfirmView(disnake.ui.View):
	"""
	This class is a view with yes and no buttons, this checks which button the user has pressed and returns True via the self.response if the button they clicked was Yes else  False if the button they clicked is No
	"""

	def __init__(self, ctx, *, timeout = 180.0):
		super().__init__(timeout=timeout)
		self.ctx = ctx
		self.response = None

	async def interaction_check(self, interaction: disnake.MessageInteraction):
		return self.ctx.author.id == interaction.author.id
	
	async def on_error(self, error: Exception, item, interaction):
		return await self.ctx.bot.reraise(self.ctx, error)

	@disnake.ui.button(label='Yes', style=disnake.ButtonStyle.green)
	async def yes_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
		self.response = True
		for item in self.children:
			item.disabled = True
			item.style = disnake.ButtonStyle.grey
			if item.label == button.label:
				item.style = disnake.ButtonStyle.blurple
		self.stop()
	
	@disnake.ui.button(label='No', style=disnake.ButtonStyle.red)
	async def no_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
		self.response = False
		for item in self.children:
			item.disabled = True
			item.style = disnake.ButtonStyle.grey
			if item.label == button.label:
				item.style = disnake.ButtonStyle.blurple

		self.stop()