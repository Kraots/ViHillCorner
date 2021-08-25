from discord.ext import commands
import discord
import sys
import async_tio
import async_cse as cse
import utils.colors as color
from utils.helpers import package_version, profile
import os
import re
import zlib
import io
import os
from utils import fuzzy, time, embedlinks, topicslist
import random
import datetime
from dateutil.relativedelta import relativedelta
from utils.paginator import SimplePages, RoboPages, CustomMenu
import pymongo
from discord.ext.commands import Greedy
from discord import Member
import asyncio
from discord.ext import menus

class UrbanDictionaryPageSource(menus.ListPageSource):
	BRACKETED = re.compile(r'(\[(.+?)\])')
	def __init__(self, data):
		super().__init__(entries=data, per_page=1)

	def cleanup_definition(self, definition, *, regex=BRACKETED):
		def repl(m):
			word = m.group(2)
			return f'[{word}](http://{word.replace(" ", "-")}.urbanup.com)'

		ret = regex.sub(repl, definition)
		if len(ret) >= 2048:
			return ret[0:2000] + ' [...]'
		return ret

	async def format_page(self, menu, entry):
		maximum = self.get_max_pages()
		title = f'{entry["word"]}: {menu.current_page + 1} out of {maximum}' if maximum else entry['word']
		embed = discord.Embed(title=title, colour=color.lightpink, url=entry['permalink'])
		embed.set_footer(text=f'by {entry["author"]}')
		embed.description = self.cleanup_definition(entry['definition'])

		try:
			up, down = entry['thumbs_up'], entry['thumbs_down']
		except KeyError:
			pass
		else:
			embed.add_field(name='Votes', value=f'\N{THUMBS UP SIGN} {up} \N{THUMBS DOWN SIGN} {down}', inline=False)

		try:
			date = discord.utils.parse_time(entry['written_on'][0:-1])
		except (ValueError, KeyError):
			pass
		else:
			embed.timestamp = date

		return embed

class SnipesPageEntry:
	def __init__(self, entry):

		self.message = entry['message']
		self.author = entry['author']

	def __str__(self):
		return f'*{self.message}* **-** ___{self.author}___'

class SnipesPages(CustomMenu):
	def __init__(self, entries, *, per_page=12):
		converted = [SnipesPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page, color=color.lightpink)

class SuggestPageEntry:
	def __init__(self, entry):

		self.id = entry['_id']

	def __str__(self):
		return f'<@!{self.id}>\u2800•\u2800(`UserID:` {self.id})'

class SuggestionPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [SuggestPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)

GoogleKey1 = os.getenv("GOOGLE_API_KEY_A")
GoogleKey2 = os.getenv("GOOGLE_API_KEY_B")
GoogleKey3 = os.getenv("GOOGLE_API_KEY_C")

class SphinxObjectFileReader:
	# Inspired by Sphinx's InventoryFileReader
	BUFSIZE = 16 * 1024

	def __init__(self, buffer):
		self.stream = io.BytesIO(buffer)

	def readline(self):
		return self.stream.readline().decode('utf-8')

	def skipline(self):
		self.stream.readline()

	def read_compressed_chunks(self):
		decompressor = zlib.decompressobj()
		while True:
			chunk = self.stream.read(self.BUFSIZE)
			if len(chunk) == 0:
				break
			yield decompressor.decompress(chunk)
		yield decompressor.flush()

	def read_compressed_lines(self):
		buf = b''
		for chunk in self.read_compressed_chunks():
			buf += chunk
			pos = buf.find(b'\n')
			while pos != -1:
				yield buf[:pos].decode('utf-8')
				buf = buf[pos + 1:]
				pos = buf.find(b'\n')

class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Updates']
		self.db2 = bot.db2['Suggestion blocks']
		self.prefix = '!'
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	def parse_object_inv(self, stream, url):
		result = {}

		inv_version = stream.readline().rstrip()

		if inv_version != '# Sphinx inventory version 2':
			raise RuntimeError('Invalid objects.inv file version.')

		projname = stream.readline().rstrip()[11:]
		version = stream.readline().rstrip()[11:]

		line = stream.readline()
		if 'zlib' not in line:
			raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

		entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
		for line in stream.read_compressed_lines():
			match = entry_regex.match(line.rstrip())
			if not match:
				continue

			name, directive, prio, location, dispname = match.groups()
			domain, _, subdirective = directive.partition(':')
			if directive == 'py:module' and name in result:
				continue

			# Most documentation pages have a label
			if directive == 'std:doc':
				subdirective = 'label'

			if location.endswith('$'):
				location = location[:-1] + name

			key = name if dispname == '-' else dispname
			prefix = f'{subdirective}:' if domain == 'std' else ''

			if projname == 'discord.py':
				key = key.replace('discord.ext.commands.', '').replace('discord.', '')

			result[f'{prefix}{key}'] = os.path.join(url, location)

		return result

	async def build_rtfm_lookup_table(self, page_types):
		cache = {}
		for key, page in page_types.items():
			sub = cache[key] = {}
			async with self.bot.session.get(page + '/objects.inv') as resp:
				if resp.status != 200:
					raise RuntimeError('Cannot build rtfm lookup table, try again later.')

				stream = SphinxObjectFileReader(await resp.read())
				cache[key] = self.parse_object_inv(stream, page)

		self._rtfm_cache = cache

	async def do_rtfm(self, ctx, key, obj):
		page_types = {
			'latest': 'https://discordpy.readthedocs.io/en/latest',
			'python': 'https://docs.python.org/3',
			'master': 'https://discordpy.readthedocs.io/en/master',
		}

		if obj is None:
			await ctx.send(page_types[key])
			return

		if not hasattr(self, '_rtfm_cache'):
			await ctx.trigger_typing()
			await self.build_rtfm_lookup_table(page_types)

		obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

		if key.startswith('latest'):
			q = obj.lower()
			for name in dir(discord.abc.Messageable):
				if name[0] == '_':
					continue
				if q == name:
					obj = f'abc.Messageable.{name}'
					break

		cache = list(self._rtfm_cache[key].items())
		def transform(tup):
			return tup[0]

		matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

		e = discord.Embed(colour=discord.Colour.blurple())
		if len(matches) == 0:
			return await ctx.send('Could not find anything. Sorry.')

		e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
		await ctx.send(embed=e, reference=ctx.replied_reference)

	def transform_rtfm_language_key(self, ctx, prefix):
		return prefix

	@commands.command()
	async def botinfo(self, ctx):
		"""Get some info of the bot"""

		update = await self.db.find_one({'_id': 374622847672254466})
		updatedMsg = update['update']
		major = sys.version_info.major
		minor = sys.version_info.minor
		micro = sys.version_info.micro
		py_version = "{}.{}.{}".format(major, minor, micro)
		kraots = self.bot.get_user(374622847672254466)
		botinfo = discord.Embed(title="", color=color.lightpink, timestamp=ctx.message.created_at)
		botinfo.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		botinfo.add_field(name="Name | ID :", value=f"{self.bot.user} | {self.bot.user.id}", inline=False)
		botinfo.add_field(name="Bot Owner:", value=f"{kraots}", inline=False)
		botinfo.add_field(name="Created at:", value="05/09/2020", inline=False)
		botinfo.add_field(name="Python Versions:", value=f"`{py_version}`", inline=False)
		botinfo.add_field(name="Wrapper Version:", value=f"`discord.py {package_version('discord.py')}`", inline=False)
		botinfo.add_field(name="Commands loaded:", value=f"{len([x.name for x in self.bot.commands])}", inline=False)
		botinfo.add_field(name="About:", value="*This bot is a private bot made only for ViHill Corner, so do not ask to host it or to add it to your server!*", inline=True)
		botinfo.add_field(name="Last Update:", value=updatedMsg, inline=False)
		botinfo.add_field(name="Bot's Source of Code:", value="[Click Here](https://github.com/Kraots/ViHillCorner)")
		botinfo.add_field(name="Vote For Server:", value="\n[Click Here](https://top.gg/servers/750160850077089853/vote)", inline=False)
		botinfo.set_thumbnail(url=self.bot.user.avatar_url)
		await ctx.send(embed=botinfo)

	@commands.command(aliases=['calculator', 'calculate'])
	async def calc(self, ctx, *, operation:str):
		"""Do some basic mathematics operations."""
		
		args = operation
		if '^' in args:
			args = args.replace('^', '**')
	
		tio = await async_tio.Tio()
		result = await tio.execute(f"print({args})", language="python3")
		await tio.close()
		exit_status_ = result.exit_status
		if int(exit_status_) == 1:
			return await ctx.reply("Are you sure you're using this command for a valid operation?")

		try:
			em = discord.Embed()
			em.set_author(name=f"Here's your result `{ctx.author.display_name}`:", icon_url=ctx.author.avatar_url)
			em.add_field(name="Operation:", value=f"`{args}`", inline=False)
			em.add_field(name="Result:", value=f"`{result.stdout}`")
			em.color = color.lightpink
			await ctx.send(embed=em, reference=ctx.replied_reference)
		except discord.HTTPException:
			em = discord.Embed()
			em.set_author(name=f"Here's your result `{ctx.author.display_name}`:", icon_url=ctx.author.avatar_url)
			em.add_field(name="Operation:", value="`Operation too long`", inline=False)
			em.add_field(name="Result:", value=f"`{result.stdout}`")
			em.color = color.lightpink
			await ctx.send(embed=em, reference=ctx.replied_reference)

	@commands.command()
	async def google(self, ctx, *, query):
		"""Search for something on google and get a short description and a link if you want to read more."""

		GoogleClient = cse.Search([GoogleKey1, GoogleKey2, GoogleKey3])
		query = str(query)
		results = await GoogleClient.search(query, safesearch=False)
		result = results[0]
		em = discord.Embed(title=result.title, url=result.url, description=result.description)
		if str(result.image_url) != "https://image.flaticon.com/teams/slug/google.jpg":
			em.set_image(url=result.image_url)
		await ctx.send(embed=em)
		await GoogleClient.close()

	@commands.group(aliases=['rtfd'], invoke_without_command=True)
	async def rtfm(self, ctx, *, obj: str = None):
		"""Gives you a documentation link for a discord.py entity."""

		key = self.transform_rtfm_language_key(ctx, 'latest')
		await self.do_rtfm(ctx, key, obj)

	@rtfm.command(name='python', aliases=['py'])
	async def rtfm_python(self, ctx, *, obj: str = None):
		"""Gives you a documentation link for a python entity."""

		key = self.transform_rtfm_language_key(ctx, 'python')
		await self.do_rtfm(ctx, key, obj)

	@rtfm.command(name='master', aliases=['2.0'])
	async def rtfm_master(self, ctx, *, obj: str = None):
		"""Gives you a documentation link for a discord.py master entity."""

		await self.do_rtfm(ctx, 'master', obj)

	@commands.command(aliases=['server', 'sinfo', 'si'])
	async def serverinfo(self, ctx):
		"""Gives some info about the server."""

		await ctx.message.delete()
		guild = self.bot.get_guild(750160850077089853)
		online = 0
		for i in guild.members:
			if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
				online += 1
		all_users = []
		for user in guild.members:
			all_users.append('{0.name}#{0.discriminator}'.format(user))
		all_users.sort()

		channel_count = len([x for x in guild.channels if type(x) == discord.channel.TextChannel])

		role_count = len(guild.roles)
		emoji_count = len(guild.emojis)

		def format_date(dt):
			if dt is None:
				return 'N/A'
			return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

		em = discord.Embed(color=color.lightpink)
		em.add_field(name='Name | ID', value=f"{guild.name}  |  {guild.id}")
		em.add_field(name='Owner', value=guild.owner, inline=False)
		em.add_field(name='Users', value=f"{len([m for m in guild.members if not m.bot])} members | {len([m for m in guild.members if m.bot])} bots")
		em.add_field(name='Currently Online', value=online)
		em.add_field(name='Text Channels', value=str(channel_count))
		em.add_field(name='Region', value=guild.region)
		em.add_field(name='Verification Level', value=str(guild.verification_level))
		em.add_field(name='Highest role', value="Staff")
		em.add_field(name='Number of roles', value=str(role_count))
		em.add_field(name='Number of emotes', value=str(emoji_count))
		em.add_field(name='Created At', value=format_date(guild.created_at))
		em.set_thumbnail(url=guild.icon_url)
		em.set_author(name='Server Info')
		em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=em, reference=ctx.replied_reference)

	@commands.command()
	async def waifu(self, ctx):
		"""Get a random waifu image."""

		chosen_image = random.choice(embedlinks.waifuLinks)
		embed = discord.Embed(color=color.lightpink)
		embed.set_image(url=chosen_image)
		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

		await ctx.send(embed=embed)

	@commands.command(aliases=['user'])
	async def profile(self, ctx, member: discord.Member = None):
		"""Get info about the member."""

		if member is None:
			member = ctx.author
		
		em = profile(ctx, member)
		await ctx.send(embed=em)
		await ctx.message.delete()

	@commands.command()
	async def topic(self, ctx):
		"""Get a random topic."""

		await ctx.message.delete()
		topics = random.choice(topicslist.topicsList)
		await ctx.send(topics)

	@commands.command()
	async def spotify(self, ctx, member: discord.Member=None):
		"""See info about the member's spotify activity."""
			
		if member is None:
			member = ctx.author

		if member.bot:
			await ctx.message.delete()
			await ctx.send("Cannot check for spotify activity for bots! Use on members only!", delete_after=10)
			return

		if isinstance(member.activities[0],discord.activity.Spotify):
			diff = relativedelta(datetime.datetime.utcnow(), member.activities[0].created_at)
			m =discord.Embed(title=f"{member.name} activity:")
			m.add_field(name="Listening to :",value=member.activities[0].title, inline=False)
			m.add_field(name="By:",value=member.activities[0].artist, inline=False)
			m.add_field(name="On:",value =member.activities[0].album, inline=False)
			m1, s1 = divmod(int(member.activities[0].duration.seconds), 60)
			song_length = '{:02}:{:02}'.format(m1, s1)
			playingfor = '{:02}:{:02}'.format(diff.minutes, diff.seconds)
			m.add_field(name="Duration:", value=f"{playingfor} - {song_length}")
			m.add_field(name="Total Duration:",value =song_length, inline=False)
			m.add_field(name='Link to song:', value=f"[Click Here](https://open.spotify.com/track/{member.activities[0].track_id}?si=xrjyVAxhS1y5rNHLM_WRww)", inline=False)
			m.set_thumbnail(url=member.activities[0].album_cover_url)
			m.color = discord.Color.green()
			await ctx.send(embed=m)
		
		elif isinstance(member.activities[1], discord.activity.Spotify):
			diff = relativedelta(datetime.datetime.utcnow(), member.activities[1].created_at)
			
			m =discord.Embed(title=f"{member.name} activity:")
			m.add_field(name="Listening to :",value=member.activities[1].title, inline=False)
			m.add_field(name="By:",value=member.activities[1].artist, inline=False)
			m.add_field(name="On:",value =member.activities[1].album, inline=False)
			m2, s2 = divmod(int(member.activities[1].duration.seconds), 60)
			song_length = '{:02}:{:02}'.format(m2, s2)
			playingfor = '{:02}:{:02}'.format(diff.minutes, diff.seconds)
			m.add_field(name="Duration:", value=f"{playingfor} - {song_length}")
			m.add_field(name="Total Duration:",value =song_length, inline=False)
			m.add_field(name='Link to song:', value=f"[Click Here](https://open.spotify.com/track/{member.activities[1].track_id}?si=xrjyVAxhS1y5rNHLM_WRww)", inline=False)
			m.set_thumbnail(url=member.activities[1].album_cover_url)
			m.color = discord.Color.green() 
			await ctx.send(embed=m)
			return

		else:
			await ctx.send("No spotify activity detected!")

	@commands.Cog.listener()
	async def on_message_delete(self, message: discord.Message):
		if message.author.id == 374622847672254466:
			return
		elif message.author.bot:
			return
		else:
			try:
				curr_snipes = self.bot.snipes[message.channel.id]
			except KeyError:
				self.bot.snipes[message.channel.id] = [message]
			else:
				if len(curr_snipes) == 500:
					curr_snipes.pop(0)
				curr_snipes.append(message)
				self.bot.snipes[message.channel.id] = curr_snipes
	
	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def snipe(self, ctx, *, channel: discord.TextChannel = None):
		"""Get the last deleted message from the channel, if any."""
		
		channel = channel or ctx.channel
		try:
			msg = self.bot.snipes[channel.id][-1]
		except KeyError:
			return await ctx.send('Nothing to snipe!')

		embed = discord.Embed(description= msg.content, color=msg.author.color, timestamp=msg.created_at)
		embed.set_author(name=msg.author, icon_url=msg.author.avatar_url)
		embed.set_footer(text="Deleted in `{}`".format(msg.channel))
		if msg.attachments:
			embed.set_image(url=msg.attachments[0].proxy_url)
		await ctx.send(embed=embed)

	@snipe.command(name='list')
	async def snipe_list(self, ctx, *, channel: discord.TextChannel = None):
		"""See a list of all available snipes indexed with a brief view of their content."""

		channel = channel or ctx.channel
		try:
			curr_snipes = self.bot.snipes[channel.id]
		except KeyError:
			return await ctx.send('That channel has no snipes!')
		else:
			snipes = []
			for snipe in curr_snipes:
				if len(snipe.content) > 50:
					content = snipe.content[0:50] + '[...]'
				else:
					content = snipe.content

				snipes.append({'message': content, 'author': snipe.author})

			m = SnipesPages(entries=snipes, per_page=10)
			await m.start(ctx)

	@snipe.command(name='index')
	async def snipe_index(self, ctx, index: int):
		"""Just like the usual `!snipe` but instead of giving the latest deleted message it returns the full content of the deleted message at the given index."""

		index += 1
		try:
			msg = self.bot.snipes[ctx.channel.id][index]
		except KeyError:
			return await ctx.send('This channel has no deleted messages.')
		except IndexError:
			return await ctx.send('There is no index with that number. For a list of all available indexes please use `!snipe list`')

		embed = discord.Embed(description= msg.content, color=msg.author.color, timestamp=msg.created_at)
		embed.set_author(name=msg.author, icon_url=msg.author.avatar_url)
		embed.set_footer(text="Deleted in `{}`".format(msg.channel))
		if msg.attachments:
			embed.set_image(url=msg.attachments[0].proxy_url)
		await ctx.send(embed=embed)

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.has_any_role('Mod', 'lvl 3+', 'lvl 5+', 'lvl 10+', 'lvl 15+', 'lvl 20+', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 55+', 'lvl 50+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def nick(self, ctx, *, nick):
		"""Change your nickname."""

		await ctx.author.edit(nick=nick)
		await ctx.send(f'I have changed your nickname to `{nick}`')

	@nick.command(name='remove', aliases=['reset'])
	async def nick_remove(self, ctx):
		"""Remove your nickname."""

		await ctx.author.edit(nick=None)
		await ctx.send("Nickname succesfully removed!")

	@commands.group(invoke_without_command = True, case_insensitive = True, aliases=['updates'])
	async def update(self, ctx):
		"""See what the latest update was."""

		update = await self.db.find_one({'_id': 374622847672254466})
		updatedMsg = update['update']
		updatedDate = time.human_timedelta(dt=update['date'], accuracy=3, brief=False, suffix=True)
		em = discord.Embed(title="Here's what's new to the bot:", description=f"{updatedMsg}\n\n*{updatedDate}*", color=color.red)
		em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em, reference=ctx.replied_reference)
	
	@update.command(name='set')
	@commands.is_owner()
	async def update_set(self, ctx, *, args: str):
		"""Set the update."""

		args = args.replace('```py', '')
		args = args.replace('```', '')
		await self.db.update_one({'_id': ctx.author.id}, {'$set':{'update': args, 'date': datetime.datetime.utcnow()}})
		await ctx.reply('Operation successful.')

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def suggest(self, ctx, *, args):
		"""Make a suggestion in <#750160850593251454>."""

		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		result = await self.db2.find_one({'_id': ctx.author.id})
		if result != None:
			await ctx.send("You are blocked from using this command. %s" % (ctx.author.mention))
			ctx.command.reset_cooldown(ctx)
			return

		await ctx.message.delete()
		em1 = discord.Embed(color=color.lightpink, title="Are you ready to post your suggestion?", description="**`%s`**" %(args))
		em1.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
		msg1 = await ctx.send(embed=em1)
		await msg1.add_reaction('<:agree:797537027469082627>')
		await msg1.add_reaction('<:disagree:797537030980239411>')

		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
		
		try:
			reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)
		
		except asyncio.TimeoutError:
			new_msg = f"{ctx.author.mention} Did not react in time."
			await msg1.edit(content=new_msg, embed=None)
			await msg1.clear_reactions()
			return
		
		else:
			if str(reaction.emoji) == '<:agree:797537027469082627>':
				suggest = discord.Embed(color=color.inviscolor, title="", description=f"{args}", timestamp=ctx.message.created_at)
				suggest.set_author(name=f'{ctx.author.name} suggested:', icon_url=ctx.author.avatar_url)
				suggestions = self.bot.get_channel(750160850593251454)
				msg = await suggestions.send(embed=suggest)
				await msg.add_reaction('<:agree:797537027469082627>')
				await msg.add_reaction('<:disagree:797537030980239411>')
				em = discord.Embed(color=color.inviscolor, title="Suggestion successfully added!", url=msg.jump_url)
				await msg1.edit(embed=em)
				await msg1.clear_reactions()
				return

			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = "Suggestion aborted. %s" % (ctx.author.mention)
				await msg1.edit(content=e, embed=None)
				await msg1.clear_reactions()
				return
	
	@suggest.command(name='block')
	@commands.is_owner()
	async def suggest_block(self, ctx, members: Greedy[Member]):
		"""Block the members from using the suggest command."""

		blocked_list = []
		if len(members) < 1:
			await ctx.send("You have not given any member to block.")
			return
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			blocked_list.append(a)
			post = {'_id': member.id}
			try:
				await self.db2.insert_one(post)
			except pymongo.errors.DuplicateKeyError:
				pass
			await member.send("You are not able to use the command `!suggest` anymore, you have been blocked from using it due to abuse or innapropriate use.")
		blocked_users = " | ".join(blocked_list)
		await ctx.send("`%s` have been blocked from using the command **!suggest**." % (blocked_users))

	@suggest.command(name='unblock')
	@commands.is_owner()
	async def suggest_unblock(self, ctx, members: Greedy[Member]):
		"""Unblock the members from using the suggest command."""

		unblocked_list = []
		if len(members) < 1:
			await ctx.send("You have not given any member to block.")
			return
		for member in members:
			a = f"{member.name}#{member.discriminator}"
			unblocked_list.append(a)
			post = {'_id': member.id}
			await self.db2.delete_one(post)
			await member.send("You are able to use the command `!suggest` again. Do **not** abuse it and do **not** use it for innapropriate things that will result in your access being taken away again.")
		unblocked_users = " | ".join(unblocked_list)
		await ctx.send("`%s` have been allowed to use the command **!suggest** again." % (unblocked_users))

	@suggest.command(name='blocks')
	@commands.is_owner()
	async def suggest_blocks(self, ctx):
		"""Get a list with all the members who have been blocked from using the command suggest."""

		try:
			entries = await self.db2.find().to_list(100000)
			p = SuggestionPages(entries = entries, per_page = 7)
			await p.start(ctx)
		except:
			await ctx.send("There are no members whose access has been restricted.")

	@commands.command()
	async def urban(self, ctx, *, word):
		"""Searches the urban dictionary for the word."""

		url = 'http://api.urbandictionary.com/v0/define'
		async with ctx.session.get(url, params={'term': word}) as resp:
			if resp.status != 200:
				kraots = self.bot.get_user(self.bot.owner_id)
				await kraots.send(embed=discord.Embed(description=f"[`{ctx.command}`]({ctx.message.jump_url}) gave an error:\n\nWord: **{word}**\nStatus: **{resp.status}**\nReason: **{resp.reason}**"))
				return await ctx.send(f'An error occurred. Please try again later.')

			js = await resp.json()
			data = js.get('list', [])
			if not data:
				return await ctx.send('No results found.')

		pages = RoboPages(UrbanDictionaryPageSource(data))
		try:
			await pages.start(ctx)
		except Exception as error:
			await self.bot.reraise(ctx, error)

	@suggest.error
	async def suggest_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.message.delete()
			msg = f"To use this command go to <#750160851822182486> or <#750160851822182487>.\n{ctx.author.mention}"
			ctx.command.reset_cooldown(ctx)
			await ctx.send(msg, delete_after=6)

		elif isinstance(error, commands.CommandOnCooldown):
				await ctx.message.delete()
				msg = 'Your on cooldown, please try again in **{:.2f}**s.'.format(error.retry_after)
				await ctx.send(msg, delete_after=3)

		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.message.delete()
			msg = "You have to add your suggestion."
			ctx.command.reset_cooldown(ctx)
			await ctx.send(msg, delete_after=3)

		else:
			await self.bot.reraise(ctx, error)

	@nick.error
	async def nick_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			if ctx.author.id == ctx.guild.owner.id:
				await ctx.send("Bots **do not** have permission to change guild owner's nickname!")
			else:
				await ctx.send("The nickname is too long. Please choose a nickname that's 32 characters or less!")
		else:
			await self.bot.reraise(ctx, error)

	@nick_remove.error
	async def off_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			if ctx.author.id == ctx.guild.owner.id:
				await ctx.send("Bots **do not** have permission to change guild owner's nickname!")
		else:
			await self.bot.reraise(ctx, error) 

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You must be at least `level 3+` in order to use this command! %s" % (ctx.author.mention))
		else:
			if hasattr(ctx.command, 'on_error'):
				return
			await self.bot.reraise(ctx, error)

def setup(bot):
	bot.add_cog(Misc(bot))