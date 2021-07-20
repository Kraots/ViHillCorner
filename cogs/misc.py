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
from datetime import datetime
from dateutil.relativedelta import relativedelta

snipes = {}

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
			diff = relativedelta(datetime.utcnow(), member.activities[0].created_at)
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
			diff = relativedelta(datetime.utcnow(), member.activities[1].created_at)
			
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
			snipes[message.channel.id] = message

	
	@commands.command()
	async def snipe(self, ctx, *, channel: discord.TextChannel = None):
		"""Get the last deleted message from the channel, if any."""
		
		channel = channel or ctx.channel
		try:
			msg = snipes[channel.id]
		except KeyError:
			return await ctx.send('Nothing to snipe!')

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
		"""Reset your nickname."""

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

	@nick.error
	async def nick_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			if ctx.author.id == ctx.guild.owner.id:
				await ctx.send("Bots **do not** have permission to change guild owner's nickname!")
			else:
				await ctx.send("The nickname is too long. Please choose a nickname that's 32 characters or less!")
	
	@nick_remove.error
	async def off_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			if ctx.author.id == ctx.guild.owner.id:
				await ctx.send("Bots **do not** have permission to change guild owner's nickname!")

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You must be at least `level 3+` in order to use this command! %s" % (ctx.author.mention))


def setup(bot):
	bot.add_cog(Misc(bot))