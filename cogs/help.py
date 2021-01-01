import discord
from discord.ext import commands
import utils.colors as color


class Help(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix



	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra=False)
	async def help(self, ctx):
		helpEm = discord.Embed(description="", color=color.lightpink)
		helpEm.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
		helpEm.set_thumbnail(url=self.client.user.avatar_url)
		helpEm.add_field(name="Commands", value="`ee`, `nick`, `profile`, `created`, `joined`, `av`, `waifu`, `invite`, `suggest`, `spotify`, `meme`, `cat`, `dog`, `snipe`, `nsfw`, `topic`, `gayrate`, `straightrate` , `simprate`, `hornyrate`, `boomerrate`, `8ball`, `fight`, `birthday`, `intro`, `whois`, `reclist`, `dev-portal`, `perm-calc`, `cr`, `vampify`, `clapify`, `define`, `search`, `calculator`, `marry`, `marriedwho`, `divorce`, `scrs`, `tag`, `snippets`")
		helpEm.add_field(name="Economy", value="`balance`, `deposit`, `withdraw`, `steal`, `slots`, `beg`, `give`, `work`, `crime`, `guess`, `race`", inline=False)
		helpEm.add_field(name="Info", value="`untill-partner`, `membercount`, `level`, `rank`, `sfw`, `spam`, `english`, `botinfo`, `uptime`, `ping`, `serverad`, `rawad`, `serverinfo`, `vote`", inline=False)
		if "Staff" in [role.name for role in ctx.message.author.roles]:
			helpEm.add_field(name="Moderator Commands", value="`clear`, `mute`, `tempmute`, `unmute`, `kick`, `ban`, `opban`, `unban`, `opunban`, `nsfw`, `slowmode`, `snippet`", inline=False)
		
		if ctx.author.id == 374622847672254466:
			helpEm.add_field(name="Dev Commands", value="`load`, `unload`, `reload`, `reload all`, `unload all`, `load all`, `modmute`, `modunmute`, `makemod`, `removemod`, `shutdown`, `restart`, `jsk`, `statuses`, `metrics`, `mail`", inline=False)

		await ctx.message.channel.send(embed=helpEm)
	
	@help.command(aliases=['tags'])
	async def tag(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!tag <tag_name>```")
		em.add_field(name="***Commands:***", value="\n• **create**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• make\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!tag create <tag_name>`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Create a new tag!\n\u2800\u2800***Warning:***\n\u2800\u2800\u2800• They cannot contain any of the banned words (in case it does you will be banned without a second thought, so be careful!)\n\u2800\u2800\u2800• They cannot contain attachments!\n\n• **delete**\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!tag delete <tag_name>`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete a tag that you made.\n\n• **info**\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!tag info <tag_name>`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• See info about a tag!\n\n• **all**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• list\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!tag all`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get paginated list with all tags.", inline=False)
		
		if ctx.author.id == 374622847672254466:
			em.add_field(name="_ _ \n***Owner Only:***", value="_ _ \n\u2800***Usage***: \n\u2800\u2800`!tag remove <tag_name>`\n\u2800***Info:***\n\u2800\u2800• Remove a tag from the database.\n _ _")

		em.add_field(name="***Info:***", value="\u2800• Allows you to tag text for later retrieval.", inline=False)
		await ctx.send(embed=em)

	@help.command(aliases=['ss'])
	async def scrs(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!scrs <domain>```")
		em.add_field(name="***Aliases:***", value="• ss", inline=False)
		em.add_field(name="***Info:***", value="\u2800• Take a scren shot of a domain.\n• It will **not** work if the site you try to screen shot has captcha verification.", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def marry(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!marry <user>```")
		em.add_field(name="***Info:***", value="\u2800• Marry to someone <:SheepLove:787370467438362694>")
		await ctx.send(embed=em)

	@help.command()
	async def divorce(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!divorce```")
		em.add_field(name="***Info:***", value="\u2800• Divorce with the person you are married to. :cry:")
		await ctx.send(embed=em)

	@help.command()
	async def marriedwho(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!marriedwho <user>```")
		em.add_field(name="***Info:***", value="\u2800• See who the user is married to.")
		await ctx.send(embed=em)

	@help.command()
	async def opban(self, ctx):
		em = discord.Embed(color=color.lightpink, title="**Usage:**", description="```\n!opban <user>```")
		em.add_field(name="***Info:***", value="\u2800• Bans a user that is **not** in the server.")
		await ctx.send(embed=em)


	@help.command()
	async def opunban(self, ctx):
		em = discord.Embed(color=color.lightpink, title="**Usage:**", description="```\n!opunban <user>```")
		em.add_field(name="***Info:***", value="\u2800• Unbans a user that is **not** in the ban appeal server or the server itself.")
		await ctx.send(embed=em)

	@help.command()
	async def search(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!define <query>```")
		em.add_field(name="***Info:***", value="\u2800• Search for a query.")
		await ctx.send(embed=em)

	@help.command()
	async def define(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!define <word>```")
		em.add_field(name="***Info:***", value="\u2800• Search the definition of a word.")
		await ctx.send(embed=em)

	@help.command(aliases=['snippets'])
	async def snippet(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!snippets```")
		em.add_field(name="***Commands:***", value="• **create**\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!snippet create <snippet_name>`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Create a new snippet.\n\u2800\u2800***Requirements:***\n\u2800\u2800\u2800• Level 55+\n\n• **delete**\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!snippet delete <snippet_name>`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete a snippet you own.\n\u2800\u2800***Requirements:***\n\u2800\u2800\u2800• Level 55+", inline=False)

		if ctx.author.id == 374622847672254466:
			em.add_field(name="_ _ \n***Owner Only:***", value="_ _ \n\u2800***Usage***: \n\u2800\u2800`!snippet remove <snippet_name>`\n\u2800***Info:***\n\u2800\u2800• Remove a snippet from the database.\n _ _")

		em.add_field(name="***Info:***", value="\u2800• Send paginated list of all snippets.", inline=False)

		await ctx.send(embed=em)

	@help.command()
	async def vampify(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!vampify <text>```")
		embed.add_field(name="***Info:***", value="\u2800• Vampify your text!")
		await ctx.send(embed=embed)

	@help.command()
	async def clapify(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!clapify <text>```")
		embed.add_field(name="***Info:***", value="\u2800• Clapify your text!")
		await ctx.send(embed=embed)

	@help.command()
	async def cr(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!cr create | delete```")
		em.add_field(name="***Info:***", value="\u2800• Create your custom role or delete it if you have one already.", inline=False)
		em.add_field(name="***Requirements:***", value="• Level 40 +", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def reclist(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!reclist [user] | set <text> | add <text> | delete```")
		em.add_field(name="***Info:***", value="\u2800• Check your/someone else's reclist\n• Set your reclist\n• Add recs to ur reclist\n• Delete your reclist!\n• Reclist stands for recommendations list, please recommend anime only!")
		await ctx.send(embed=em)

	@help.command()
	async def race(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!race```")
		em.add_field(name="***Info:***", value="\u2800• Get into a race and win or lose some money depending on your luck.")
		await ctx.send(embed=em)

	@help.command()
	async def intro(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!intro | delete```")
		em.add_field(name="***Info:***", value="\u2800• Set your intro | Delete your intro")
		await ctx.send(embed=em)

	@help.command(aliases=['wi'])
	async def whois(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!whois [user]```")
		em.add_field(name="***Aliases:***", value="• wi", inline=False)
		em.add_field(name="***Info:***", value="\u2800• Check someone's intro!", inline=False)
		await ctx.send(embed=em)

	@help.command(aliases=['b-day', 'bday'])
	async def birthday(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!birthday [user] | set [birthday] | remove```")
		embed.add_field(name="***Aliases:***", value="• b-day\n• bday", inline=False)
		embed.add_field(name="***Info:***", value="\u2800• See when's someone's birthday | Set your birthday | Remove your birthday")
		await ctx.send(embed=embed)

	@help.command()
	async def crime(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!crime```")
		embed.add_field(name="***Info:***", value="\u2800• Commit crimes that range between `small-medium-big`, and depending on which one you get, the more money you get, but be careful! You can lose the money as well.")
		await ctx.send(embed=embed)

	@help.command(aliases=['guess'])
	async def gtn(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!guess```")
		embed.add_field(name="***Aliases:***", value="• gtn", inline=False)
		embed.add_field(name="***Info:***", value="\u2800• Play guess the number and if you win you'll get some money as prize, but if you lose it then some money will be taken from your wallet.", inline=False)
		await ctx.send(embed=embed)


	@help.command()
	async def work(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!work```")
		embed.add_field(name="***Info:***", value="\u2800• Work and get `5000` coins each hour!")
		await ctx.send(embed=embed)

	@help.command()
	async def fight(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!fight <user>```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• Fight someone, the outcome is always random!")
		await ctx.send(embed=embed)

	@help.command(aliases=['8ball'])
	async def _8ball(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!8ball <question>```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• Ask the 8ball a question and get an answer.")
		await ctx.send(embed=embed)

	@help.command()
	async def boomerrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!boomerrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• See how boomer someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def hornyrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!hornyrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• See how horny someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def gayrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!gayrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• See how gay someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def straightrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!straightrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• See how straight someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def simprate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```!simprate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• See how simp someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def ee(self, ctx):
		ee = discord.Embed(title="***Usage:***", description="```\n!ee <emote>```", color=color.lightpink)
		ee.add_field(name="***Info:***", value="\u2800• Enlarges the chosen emote.")
		await ctx.message.channel.send(embed=ee)

	@help.command()
	async def nick(self, ctx):
		nick = discord.Embed(title="***Usage:***", description="```\n!nick <newnickname> | remove```", color=color.lightpink)
		nick.add_field(name="***Info:***", value="\u2800• Change your nickname | Remove your nickname", inline=False)
		nick.add_field(name="***Requirements:***", value="• Level 3 +", inline=False)
		await ctx.message.channel.send(embed=nick)

	@help.command()
	async def profile(self, ctx):
		profile = discord.Embed(title="***Usage:***", description="```\n!profile [user]```", color=color.lightpink)
		profile.add_field(name="***Info:***", value="\u2800• Get a user's profile info.")
		await ctx.channel.send(embed=profile)

	@help.command()
	async def created(self, ctx):
		created = discord.Embed(title="***Usage:***", description="```\n!created [user]```", color=color.lightpink)
		created.add_field(name="***Info:***", value="\u2800• See when a user joined discord / created their account.")
		await ctx.channel.send(embed=created)

	@help.command()
	async def joined(self, ctx):
		joined = discord.Embed(title="***Usage:***", description="```\n!joined [user]```", color=color.lightpink)
		joined.add_field(name="***Info:***", value="\u2800• See when a user joined the server.")
		await ctx.channel.send(embed=joined)

	@help.command(aliases=["avatar"])
	async def av(self, ctx):
		av = discord.Embed(title="***Usage:***", description="```\n!avatar [user]```", color=color.lightpink)
		av.add_field(name="***Aliases:***", value="• av", inline=False)
		av.add_field(name="***Info:***", value="\u2800• See user's avatar.", inline=False)
		await ctx.channel.send(embed=av)

	@help.command(aliases=["server", "si", "sinfo"])
	async def serverinfo(self, ctx):
		serverinfo = discord.Embed(title="***Usage:***", description="```\n!serverinfo```", color=color.lightpink)
		serverinfo.add_field(name="***Aliases:***", value="• server \n• sinfo \n• si", inline=False)
		serverinfo.add_field(name="***Info:***", value="\u2800• Get some info about the server.", inline=False)
		await ctx.channel.send(embed=serverinfo)

	@help.command()
	async def actions(self, ctx):
		actions = discord.Embed(title="***Usage:***", description="```\n!actions```", color=color.lightpink)
		actions.add_field(name="***Info:***", value="\u2800• See a list of all existing actions.")
		await ctx.channel.send(embed=actions)

	@help.command()
	async def waifu(self, ctx):
		waifu = discord.Embed(title="***Usage:***", description="```\n!waifu```", color=color.lightpink)
		waifu.add_field(name="***Info:***", value="\u2800• Get a random waifu pic.")
		await ctx.channel.send(embed=waifu)

	@help.command(aliases=["inv"])
	async def invite(self, ctx):
		invite = discord.Embed(title="***Usage:***", description="```\n!invite```", color=color.lightpink)
		invite.add_field(name="***Aliases:***", value="• inv", inline=False)
		invite.add_field(name="***Info:***", value="\u2800• Get the invite to the server.", inline=False)
		await ctx.channel.send(embed=invite)

	@help.command()
	async def serverad(self, ctx):
		ad = discord.Embed(title="***Usage:***", description="```\n!serverad```", color=color.lightpink)
		ad.add_field(name="***Info:***", value="\u2800• Get the server's advertising text.", inline=False)
		await ctx.channel.send(embed=ad)

	@help.command()
	async def rawad(self, ctx):
		rawad = discord.Embed(title="***Usage:***", description="```\n!rawad```", color=color.lightpink)
		rawad.add_field(name="***Info:***", value="\u2800• Get the server's advertising text in raw format.", inline=False)
		await ctx.channel.send(embed=rawad)

	@help.command(aliases=["untill-partner"])
	async  def up(self, ctx):
		up = discord.Embed(title="***Usage:***", description="```\n!untill-partner```", color=color.lightpink)
		up.add_field(name="***Info:***", value="\u2800• See how many members the server needs untill it's eligible for applying for the discord partnership program.", inline=False)
		await ctx.channel.send(embed=up)

	@help.command()
	async def level(self, ctx):
		level = discord.Embed(title="***Usage:***", description="```\n!level [user]```", color=color.lightpink)
		level.add_field(name="***Info:***", value="\u2800• See how to check your current level.", inline=False)
		await ctx.channel.send(embed=level)

	@help.command()
	async def rank(self, ctx):
		level = discord.Embed(title="***Usage:***", description="```\n!rank [user]```", color=color.lightpink)
		level.add_field(name="***Info:***", value="\u2800• See how to check your current rank.", inline=False)
		await ctx.channel.send(embed=level)

	@help.command()
	async def sfw(self, ctx):
		sfw = discord.Embed(title="***Usage:***", description="```\n!sfw <user>```", color=color.lightpink)
		sfw.add_field(name="***Info:***", value="\u2800• Warn a user to keep the chat appropriate and sfw.", inline=False)
		await ctx.channel.send(embed=sfw)

	@help.command()
	async def botinfo(self, ctx):
		botinfo = discord.Embed(title="***Usage:***", description="```\n!botinfo```", color=color.lightpink)
		botinfo.add_field(name="***Info:***", value="\u2800• See info about <@!751724369683677275>.", inline=False)
		await ctx.channel.send(embed=botinfo)

	@help.command()
	async def uptime(self, ctx):
		uptime = discord.Embed(title="***Usage:***", description="```\n!uptime```", color=color.lightpink)
		uptime.add_field(name="***Info:***", value="\u2800• Check the bot's uptime.", inline=False)
		await ctx.channel.send(embed=uptime)

	@help.command()
	async def ping(self, ctx):
		ping = discord.Embed(title="***Usage:***", description="```\n!ping```", color=color.lightpink)
		ping.add_field(name="***Info:***", value="\u2800• Check the bot's ping.", inline=False)
		await ctx.channel.send(embed=ping)

	@help.command()
	@commands.has_role("Staff")
	async def clear(self, ctx):
		clear = discord.Embed(title="***Usage:***", description="```\n!clear <amount>```", color=color.lightpink)
		clear.add_field(name="***Info:***", value="\u2800• Clear's the chat of the amount of messages given..", inline=False)
		await ctx.channel.send(embed=clear)

	@help.command()
	@commands.has_role("Staff")
	async def tempmute(self, ctx):
		tempmute = discord.Embed(title="***Usage:***", description="```\n!tempmute <user> <time>```", color=color.lightpink)
		tempmute.add_field(name="***Example:***", value="!tempmute @BananaBoy69 1 s|m|h|d", inline=False)
		tempmute.add_field(name="***Info:***", value="\u2800• s - second\n• m - minute\n• h - hour\n• d - day\n\n• Tempmutes a user with the  given time.", inline=False)
		tempmute.add_field(name="***Warning:***", value="**DO NOT GO ABOVE 12H**", inline=False)
		await ctx.channel.send(embed=tempmute)

	@help.command()
	@commands.has_role("Staff")
	async def unban(self, ctx):
		unban = discord.Embed(title="***Usage:***", description="```\n!unban <user>```", color=color.lightpink)
		unban.add_field(name="***Info:***", value="\u2800• This command only works in the ban appeal server, if the user is in that server ;)).", inline=False)
		await ctx.channel.send(embed=unban)

	@help.command(aliases=['ps'])
	@commands.has_role("Staff")
	async def partnership(self, ctx):
		partnership = discord.Embed(title="***Usage:***", description="```\n!partnership <ad>```", color=color.lightpink)
		partnership.add_field(name="***Aliases:***", value="• ps", inline=False)
		partnership.add_field(name="***Info:***", value="\u2800• ad - the ad of the server that the partnership is made with.\n\n**USE IT ONLY IN <#750160851822182480>**", inline=False)
		await ctx.channel.send(embed=partnership)

	@help.command()
	async def suggest(self, ctx):
		suggest = discord.Embed(title="***Usage:***", description="```\n!suggest <suggestion>```", color=color.lightpink)
		suggest.add_field(name="***Info:***", value="\u2800• Make a suggestion in <#750160850593251454>\n• There is 1 minute cooldown between each suggestion per user.", inline=False)
		await ctx.channel.send(embed=suggest)

	@help.command()
	async def spotify(self, ctx):
		spotify = discord.Embed(title="***Usage:***", description="```\n!spotify [user]```", color=color.lightpink)
		spotify.add_field(name="***Info:***", value="\u2800• Show's what song you're listening to, the artist & the album.\n• You gotta have spotify as activity and no other custom activity in order for this command to work.", inline=False)
		await ctx.channel.send(embed=spotify)

	@help.command()
	async def membercount(self, ctx):
		membercount = discord.Embed(title="***Usage:***", description="```\n!membercount```", color=color.lightpink)
		membercount.add_field(name="***Info:***", value="\u2800• See how many members ViHill Corner has (**bots are not included**).", inline=False)
		await ctx.channel.send(embed=membercount)

	@help.command()
	async def meme(self, ctx):
		meme = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!meme```")
		meme.add_field(name="***Info:***", value="\u2800• Sends a random meme! ;3", inline=False)
		await ctx.channel.send(embed=meme)

	@help.command()
	async def cat(self, ctx):
		cat = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!cat```")
		cat.add_field(name="***Info:***", value="\u2800• Sends a random cat pic! ;3", inline=False)
		await ctx.channel.send(embed=cat)

	@help.command()
	async def dog(self, ctx):
		dog = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!dog``")
		dog.add_field(name="***Info:***", value="\u2800• Sends a random dog pic! ;3", inline=False)
		await ctx.channel.send(embed=dog)

	@help.command()
	async def snipe(self, ctx):
		em = discord.Embed(title='***Usage:***', description='```!snipe```', color=color.lightpink)
		em.add_field(name="***Info:***", value="\u2800• Snipe the last deleted message in the channel!", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def nsfw(self, ctx):
		if "Staff" in [role.name for role in ctx.message.author.roles]:

			em = discord.Embed(color=color.lightpink, title='***Usage:***', description='```!nsfw add <users> | remove <users>```')
			em.add_field(name="***Info:***", value="\u2800• Give the user perms to see the nsfw channel or remove them!", inline=False)
			await ctx.send(embed=em)

		else:

			em = discord.Embed(color=color.lightpink, title='***Usage:***', description='```!nsfw yuri | hentai | tentacle | real```')
			em.add_field(name="***Info:***", value="\u2800• Get a random `yuri | hentai | tentacle | real` pic!", inline=False)
			em.set_footer(text="USE ONLY IN THE NSFW CHANNEL", icon_url=ctx.author.avatar_url)
			await ctx.send(embed=em)

	@help.command(aliases=['calculate, calculator'])
	async def calc(self, ctx):
		embed = discord.Embed(color=color.lightpink, title='***Usage:***', description='```!calculator <operation>```')
		embed.add_field(name="***Aliases:***", value="• calculate\n• calc", inline=False)
		embed.add_field(name="***Info:***", value="\u2800• Basic calculator for basic operations!", inline=False)
		await ctx.channel.send(embed=embed)

	@help.command()
	@commands.has_role('Staff')
	async def slowmode(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```\n!slowmode <time>```")
		embed.add_field(name="***Info:***", value="\u2800• Change the slowmode of the current channel.", inline=False)
		await ctx.channel.send(embed=embed)

	@help.command()
	async def topic(self, ctx):
		embed = discord.Embed(color=color.lightpink, title='***Usage:***', description='```!topic```')
		embed.add_field(name="***Info:***", value="\u2800• Get a random question or a random topic to talk about.", inline=False)
		await ctx.send(embed=embed)

	@help.command(aliases=['balance'])
	async def bal(self, ctx):
		if ctx.author.id == 374622847672254466:
			embedd = discord.Embed(title="***Usage:***", description="```\n!bal```", color=color.lightpink)
			embedd.add_field(name="***Commands:***", value="• add-wallet\n\n\u2800\u2800\u2800***Usage:***\n\u2800\u2800`!bal add-wallet [amount] [user]`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Add money to an user's wallet.\n\n• add-bank\n\n\u2800\u2800***Usage:***\n\u2800\u2800`!bal add-bank [amount] [user]`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Add money to an user's bank.\n\n• set-wallet\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!bal set-walet [amount] [user]`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Set user's wallet money.\n\n• set-bank\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!bal set-bank [amount] [user]`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Set user's bank money.\n\n• reset\n\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800`!bal reset [user]`\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Reset user's balance.")
			embedd.add_field(name="***Info:***", value="\u2800• Check your or another user's balance!", inline=False)
			await ctx.send(embed=embedd)

		else:
			embed = discord.Embed(title="***Usage:***", description="```\n!bal [user]```", color=color.lightpink)
			embed.add_field(name="***Info:***", value="\u2800• Check your or another user's balance!", inline=False)
			await ctx.send(embed=embed)

	@help.command(aliases=['deposit'])
	async def dep(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```\n!deposit [amount]```", color=color.lightpink)
		embed.add_field(name="***Aliases:***", value="• dep", inline=False)
		embed.add_field(name="***Info:***", value="\u2800• Deposit the amount of money into your bank.", inline=False)
		await ctx.send(embed=embed)

	@help.command(aliases=['withdraw', "with"])
	async def _with(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```\n!withdraw [amount]```", color=color.lightpink)
		embed.add_field(name="***Aliases:***", value="• with", inline=False)
		embed.add_field(name="***Info:***", value="\u2800• Withdraw the amount of money from your bank.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def beg(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```\n!beg```", color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• Beg for some money, peasant.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def steal(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```\n!steal [user]```")
		embed.add_field(name="***Aliases:***", value="• rob", inline=False)
		embed.add_field(name="***Info:***", value="\u2800• Steal some money from someone's wallet.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def slots(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```\n!slots [amount]```", color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• Bet your money in the slots machine!", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def give(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```\n!give [user] [amount]```", color=color.lightpink)
		embed.add_field(name="***Info:***", value="\u2800• Be a kind person and give some of your money from ur bank to someone else's!", inline=False)
		await ctx.send(embed=embed)

	@help.error
	async def help_error(self, ctx, error):
		if isinstance(error, commands.TooManyArguments):
			return



















def setup(client):
	client.add_cog(Help(client))