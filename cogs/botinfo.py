import discord
from discord.ext import commands
import utils.colors as color
import os
from utils.helpers import package_version
import sys
import motor.motor_asyncio

DBKEY = os.getenv('MONGODBKEY')

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']['Updates']

class BotInfo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(hidden=True)
	async def botinfo(self, ctx):
		update = await db.find_one({'_id': 374622847672254466})
		updatedMsg = update['update']
		major = sys.version_info.major
		minor = sys.version_info.minor
		micro = sys.version_info.micro
		py_version = "{}.{}.{}".format(major, minor, micro)
		kraots = self.bot.get_user(374622847672254466)
		cache_summary = f"**{len(self.bot.guilds)}** guild(s) and **{len(self.bot.users)}** user(s)"
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

def setup (bot):
	bot.add_cog(BotInfo(bot))