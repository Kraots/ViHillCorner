import discord
from discord.ext import commands
import utils.colors as color
from utils import time

class ServerInfo(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix


	@commands.command(aliases=['server', 'sinfo', 'si'])
	async def serverinfo(self, ctx):
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

def setup (bot):
	bot.add_cog(ServerInfo(bot))