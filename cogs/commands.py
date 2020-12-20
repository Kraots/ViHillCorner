import discord
from discord.ext import commands
import psutil
import os
import utils.colors as color
from utils import time
from typing import Union

class command(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.process = psutil.Process(os.getpid())
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
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
		
		embed = discord.Embed(color=color.lightpink)
		embed.add_field(name='Create Date:', value=f"{user} **--->** {format_date(getattr(user, 'joined_at', None))}")
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
	async def _invite(self, context):

			version = discord.Embed(title="Here's your invite", description="[ViHill Corner](https://discord.gg/Uf2kA8q)", color=color.lightpink)
			version.set_footer(text=f"Requested by: {context.author}", icon_url=context.author.avatar_url)

			await context.message.channel.send(embed=version)

	@commands.command(hidden=True)
	async def membercount(self, ctx):
			guild = self.client.get_guild(750160850077089853)
			member_count = len([m for m in guild.members if not m.bot])
			await ctx.channel.send(f'`{member_count}` members.') 

	@commands.command(hidden=True, aliases=["av", "avatar"])
	async def _av(self, ctx, member: discord.Member = None):
		await ctx.message.delete()
		if member is None:
			member = ctx.author

		avatar = discord.Embed(title=f"{member.name}", url=f"{member.avatar_url}", color=color.blue)
		avatar.set_image(url=member.avatar_url)
		avatar.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.channel.send(embed=avatar)

	@commands.command()
	async def ee(self, ctx, emoji: discord.PartialEmoji):
		await ctx.message.delete()

		embed = discord.Embed(color=color.lightpink)
		embed.set_image(url=emoji.url)
		embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

		await ctx.channel.send(embed=embed)

	@commands.command()
	async def serverad(self, ctx):
		await ctx.message.delete()
		ad = discord.Embed(color=color.lightpink, title="Here's the ad to the server:", description="**__ViHill Corner__**\nViHill Corner is mainly for talking & meeting new people & generally chatting!\n\n**WHAT WE HAVE TO OFFER**\n★ Awesome Private Bot\n★ Fun Channels\n★ Active Users\n★ Lots Of Emotes\n★ Reaction Roles\n\n\nhttps://discord.gg/Uf2kA8q")
		ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.channel.send(embed=ad)

	@commands.command(aliases=["ra"])
	async def rawad(self, ctx):
		await ctx.message.delete()
		ad = discord.Embed(color=color.lightpink, title="Here's the raw ad version of the server:", description="```**__ViHill Corner__**\nViHill Corner is mainly for talking & meeting new people & generally chatting!\n\n**WHAT WE HAVE TO OFFER**\n★ Awesome Private Bot\n★ Fun Channels\n★ Active Users\n★ Lots Of Emotes\n★ Reaction Roles\n\n\nhttps://discord.gg/Uf2kA8q```")
		ad.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)

		await ctx.channel.send(embed=ad)

	@commands.command(aliases=["untill-partner", "up"])
	async def _sdlajkndasjkdn(self, ctx):
		guild = self.client.get_guild(750160850077089853)
		member_count = len([m for m in guild.members if not m.bot])
		await ctx.channel.send(f'Members left untill the server can apply for the *discord partership program:* \n\n`{500 - member_count}`')



def setup (client):
	client.add_cog(command(client))
