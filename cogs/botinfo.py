import discord
from discord.ext import commands
import utils.colors as color
from github import Github
import os
from utils.helpers import package_version
import sys

git_user = os.getenv("github_user")
git_pass = os.getenv("github_pass") 

class BotInfo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(hidden=True)
	async def botinfo(self, ctx):
		g = Github(git_user, git_pass)
		repo = g.get_repo("Kraots/ViHillCorner")
		master = repo.get_branch("master")
		sha_com = master.commit
		sha_com = str(sha_com).split('Commit(sha="')
		sha_com = sha_com[1].split('")')
		sha_com = sha_com[0]
		commit = repo.get_commit(sha_com)
		commit = commit.commit.message
		major = sys.version_info.major
		minor = sys.version_info.minor
		micro = sys.version_info.micro
		py_version = "{}.{}.{}".format(major, minor, micro)
		kraots = self.client.get_user(374622847672254466)
		cache_summary = f"**{len(self.client.guilds)}** guild(s) and **{len(self.client.users)}** user(s)"
		botinfo = discord.Embed(title="", color=color.lightpink, timestamp=ctx.message.created_at)
		botinfo.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		botinfo.add_field(name="Name | ID :", value=f"{self.client.user} | {self.client.user.id}", inline=False)
		botinfo.add_field(name="Bot Owner:", value=f"{kraots}", inline=False)
		botinfo.add_field(name="Created at:", value="05/09/2020", inline=False)
		botinfo.add_field(name="Python Versions:", value=f"`{py_version}`", inline=False)
		botinfo.add_field(name="Wrapper Version:", value=f"`discord.py {package_version('discord.py')}`", inline=False)
		botinfo.add_field(name="Commands loaded:", value=f"{len([x.name for x in self.client.commands])}", inline=False)
		botinfo.add_field(name="About:", value="*This bot is a private bot (meaning it is not open sourced) made only for ViHill Corner, so do not ask to host it or to add it to your server!*", inline=True)
		botinfo.add_field(name="Last Update:", value=commit, inline=False)
		botinfo.add_field(name="Bot's Source of Code:", value="[Click Here](https://github.com/Kraots/ViHillCorner)")
		botinfo.add_field(name="Vote For Server:", value="\n[Click Here](https://top.gg/servers/750160850077089853/vote)", inline=False)
		botinfo.set_thumbnail(url=self.client.user.avatar_url)
		await ctx.send(embed=botinfo)

def setup (client):
	client.add_cog(BotInfo(client))