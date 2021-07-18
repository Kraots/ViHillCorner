import discord
from discord.ext import commands
import psutil
import os
import utils.colors as color
from utils import time
from typing import Union
import datetime
import random
import sys
import urllib.request
import urllib.parse
import inspect

ss_key = os.getenv("SS_KEY")

async def generate_screenshot_api_url(customer_key,  options):
	api_url = 'https://api.screenshotmachine.com/?key=' + customer_key
	api_url = api_url + '&' + urllib.parse.urlencode(options)
	return api_url

async def take_ss(url):
	options = {
				'url': str(url),
				'dimension': '1920x1080',
				'format': 'png',
				'hide': '.cookie-banner',
				'click': '.button-close',
				'delay': '600',
				'cacheLimit': '0.041666'
				}
	api_url = await generate_screenshot_api_url(ss_key, options)
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', '-')]
	urllib.request.install_opener(opener)
	output = 'ss.png'
	urllib.request.urlretrieve(api_url, output)
	

addd = """
୨୧ VIHILL CORNER ୨୧
♥︎ Your chance to meet and chat with awesome people ♥︎

♡︎ What we offer ♡︎:
╭・Exclusive bots
﹕・Lots of fun channels
﹕・Lots of emotes
﹕・Intros (Instead of reaction roles :D)
﹕・Not that active unless there's someone to start the convo, then there's a 80% chance it'll be active
╰・Horny Peeps (mostly 1 but ok)

♥︎ server link: https://discord.gg/Uf2kA8q ♥︎
° . · . ✧ °  .  ₊˚ˑ˚₊ . ° ✧ . · .°
"""

nono_list = ["pornhub.com", "hentaiheaven.com", "nhentai.net", "hanime.tv", "xvideos.com", "hentai.com", "hentai.net"]

class command(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.process = psutil.Process(os.getpid())
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(aliases=["ss"])
	async def scrs(self, ctx, site):
		if ctx.author.id != 374622847672254466:
			if str(site) in nono_list:
				await ctx.send("( ͡° ͜ʖ ͡°)")
				return
		
		else:
			ss = await take_ss(site)
			f = discord.File(fp='ss.png', filename='ss.png')
			em = discord.Embed(color=color.lightpink, title="Here's your screen shot of `{}`".format(site))
			em.set_image(url='attachment://ss.png')
			em.set_footer(text="Requested by: {}".format(ctx.author), icon_url=ctx.author.avatar_url)
			await ctx.send(embed=em, file=f)

	@commands.command()
	async def vote(self, ctx):
		em = discord.Embed(title="Click Here", url="https://top.gg/servers/750160850077089853/vote", color=color.lightpink)
		
		await ctx.send(embed=em)

	@commands.command(aliases=["perm-calc"])
	async def perm_calc(self, ctx):
		em = discord.Embed(color=color.lightpink, title= " Here's the link to the permission calculator for bots. ", description = "https://discordapi.com/permissions.html#2147483647")
		await ctx.send(embed=em)


	@commands.command(aliases=["dev-portal"])
	async def dev_portal(self, ctx):
		em = discord.Embed(color=color.lightpink, title = " Here's the link to dev portal. ", description="https://discord.com/developers/applications")
		await ctx.send(embed=em)

	@commands.command()
	async def joined(self, ctx, user: Union[discord.Member, discord.User]=None):
		if user is None:
			user = ctx.author

		def format_date(dt):
			if dt is None:
				return 'N/A'
			return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

		if user.id == 374622847672254466:
			x = "2020-09-01 01:11"
			kraots_joined = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
			embed = discord.Embed(color=color.lightpink)
			embed.add_field(name='Join Date:', value=f"{user} **--->** {format_date(kraots_joined)}")
			await ctx.send(embed=embed)
		
		elif user.id == 747329236695777340:
			x = "2020-09-30 12:12"
			twil_joined = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
			embed = discord.Embed(color=color.lightpink)
			embed.add_field(name='Join Date:', value=f"{user} **--->** {format_date(twil_joined)}")
			await ctx.send(embed=embed)

		else:
			embed = discord.Embed(color=color.lightpink)
			embed.add_field(name='Join Date:', value=f"{user} **--->** {format_date(getattr(user, 'joined_at', None))}")
			await ctx.send(embed=embed)

	@commands.command()
	async def created(self, ctx, user: Union[discord.Member, discord.User]=None):
		if user is None:
			user = ctx.author

		def format_date(dt):
			if dt is None:
				return 'N/A'
			return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'
		
		embed = discord.Embed(color=color.lightpink)
		embed.add_field(name='Create Date:', value=f"{user} **--->** {format_date(user.created_at)}")
		await ctx.send(embed=embed)

	@commands.command(help="Get a list of all snippets", aliases=["inv", "invite"])
	async def _invite(self, ctx):

			version = discord.Embed(title="https://discord.gg/Uf2kA8q", color=color.lightpink)
			version.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=version)

	@commands.command(hidden=True)
	async def membercount(self, ctx):
			guild = self.bot.get_guild(750160850077089853)
			member_count = len([m for m in guild.members if not m.bot])
			await ctx.send(f'`{member_count}` members.') 

	@commands.command(hidden=True, aliases=["av", "avatar"])
	async def _av(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
			
		avatar = discord.Embed(title=f"Here's {member.display_name}'s avatar", url=member.avatar_url, color=color.blue)
		avatar.set_image(url=member.avatar_url)
		avatar.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.send(embed=avatar, reference=ctx.replied_reference)

	@commands.command()
	async def ee(self, ctx, emoji: discord.PartialEmoji):
		await ctx.message.delete()

		embed = discord.Embed(color=color.lightpink)
		embed.set_image(url=emoji.url)
		embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

		await ctx.send(embed=embed)

	@commands.command(aliases=['ad'])
	async def serverad(self, ctx):
		await ctx.message.delete()
		ad = discord.Embed(color=color.lightpink, title="Here's the ad to the server:", description=addd)
		ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.send(embed=ad)

	@commands.command(aliases=["ra"])
	async def rawad(self, ctx):
		await ctx.message.delete()
		ad = discord.Embed(color=color.lightpink, title="Here's the raw ad version of the server:", description="```%s```" % (addd))
		ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.send(embed=ad)

	@commands.command(aliases=["untill-partner"])
	async def up(self, ctx):
		guild = self.bot.get_guild(750160850077089853)
		member_count = len([m for m in guild.members if not m.bot])
		await ctx.send(f'Members left untill the server can apply for the *discord partnership program:* \n\n`{500 - member_count}`')

	@commands.command(aliases=['randomnr', 'randomnumber', 'random', 'rn'])
	async def number(self, ctx, num1: int = None, num2: int = None, num3: int = None):
		if num1 == None and num2 == None:
			number = random.randint(0, sys.maxsize)
			await ctx.send("Random number between `0` and the largest positive integer supported by the machine is: \n`%s`" % (number))
			return

		elif num2 == None:
			number = random.randint(0, num1)
			await ctx.send("Random number from `0` to `%s`: \n`%s`" % (num1,number))
			return
		
		elif num3 == None:
			number = random.randint(num1,num2)
			await ctx.send("Random number between `%s` and `%s`: \n`%s`" % (num1,num2,number))
			return
		
		else:
			while True:
				number = random.randint(num1,num2)
				if number != num3:
					await ctx.send("Random number between `%s` and `%s` that is not `%s`: \n`%s`" % (num1,num2,num3,number))
					return
				else:
					pass

	@commands.command()
	async def source(self, ctx, *, command: str = None):
		source_url = 'https://github.com/Kraots/ViHillCorner'
		branch = 'master'
		if command is None:
			return await ctx.send(source_url)
		if command.lower() in ['jsk', 'jishaku']:
			return await ctx.send("That is an extension's command, code unavailable.")

		obj = self.bot.get_command(command.replace('.', ' '))
		if obj is None:
			return await ctx.send('Could not find command.')

		src = obj.callback.__code__
		filename = src.co_filename

		lines, firstlineno = inspect.getsourcelines(src)
		
		location = os.path.relpath(filename).replace('\\', '/')

		final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
		
		await ctx.send(final_url)

def setup(bot):
	bot.add_cog(command(bot))
