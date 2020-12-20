import discord
from discord.ext import commands
import utils.colors as color

class BotInfo(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(hidden=True)
	async def botinfo(self, ctx):
		kraots = self.client.get_user(374622847672254466)
		cache_summary = f"**{len(self.client.guilds)}** guild(s) and **{len(self.client.users)}** user(s)"
		botinfo = discord.Embed(title="", color=color.lightpink, timestamp=ctx.message.created_at)
		botinfo.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		botinfo.add_field(name="Name | ID", value=f"{self.client.user} | {self.client.user.id}", inline=False)
		botinfo.add_field(name="Bot Owner:", value=f"{kraots}", inline=False)
		botinfo.add_field(name="Created at:", value="05/09/2020", inline=False)
		botinfo.add_field(name="Info", value=f"This bot is not sharded and can see {cache_summary}")
		botinfo.add_field(name="Commands loaded", value=f"{len([x.name for x in self.client.commands])}", inline=False)
		botinfo.add_field(name="About:", value="*This bot is a private bot (meaning it is not open sourced) made only for ViHill Corner, so do not ask to host it or to add it to your server!*", inline=True)
		botinfo.add_field(name="Vote:", value="\n[Click Here](https://top.gg/servers/750160850077089853/vote)", inline=False)
		botinfo.set_thumbnail(url=self.client.user.avatar_url)
		await ctx.channel.send(embed=botinfo)

def setup (client):
	client.add_cog(BotInfo(client))