from discord.ext import commands
import asyncio
import discord
import re
import zlib
import io
import os
from utils import fuzzy

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

class RTFMCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

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

	@commands.group(aliases=['rtfd'], invoke_without_command=True)
	async def rtfm(self, ctx, *, obj: str = None):
		key = self.transform_rtfm_language_key(ctx, 'latest')
		await self.do_rtfm(ctx, key, obj)

	@rtfm.command(name='python', aliases=['py'])
	async def rtfm_python(self, ctx, *, obj: str = None):
		key = self.transform_rtfm_language_key(ctx, 'python')
		await self.do_rtfm(ctx, key, obj)

	@rtfm.command(name='master', aliases=['2.0'])
	async def rtfm_master(self, ctx, *, obj: str = None):
		await self.do_rtfm(ctx, 'master', obj)



def setup(bot):
	bot.add_cog(RTFMCommand(bot))