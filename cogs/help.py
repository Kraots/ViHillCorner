import discord
from discord.ext import commands
from utils.helpers import Developer
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
		helpEm.set_thumbnail(url="https://cdn.discordapp.com/attachments/752148605753884792/772510591565824000/00795f0d4b6710316662326aedb9d502.png")
		helpEm.add_field(name="Commands", value="`revive`, `ee`, `nick`, `profile`, `created`, `joined`, `av`, `waifu`, `invite`, `ad`, `suggest`, `spotify`, `meme`, `cat`, `dog`, `snipe`, `nsfw`, `calc`, `topic`, `gayrate`, `straightrate` , `simprate`, `hornyrate`, `boomerrate`, `8ball`, `fight`, `birthday`, `intro`, `whois`, `reclist`, `dev-portal`, `perm-calc`, `cr`")
		helpEm.add_field(name="Economy", value="`balance`, `deposit`, `withdraw`, `steal`, `slots`, `beg`, `give`, `work`, `crime`, `guess`, `ppsuck`", inline=False)
		helpEm.add_field(name="Info", value="`untill-partner`, `membercount`, `level`, `rank`, `sfw`, `botinfo`, `uptime`, `ping`, `serverad`, `rawad`, `snippets`, `actions`, `serverinfo`", inline=False)
		if "Staff" in [role.name for role in ctx.message.author.roles]:
			helpEm.add_field(name="Moderator Commands", value="`clear`, `mute`, `massmute`, `tempmute`, `unmute`, `massunmute`, `kick`, `masskick`, `ban`, `massban`, `unban`, `massunban`, `partnership`, `nsfw`, `slowmode`", inline=False)
		
		if ctx.author.id == 374622847672254466:
			helpEm.add_field(name="Dev Commands", value="`load`, `unload`, `reload`, `reload-all`, `unload-all`, `load-all`, `modmute`, `modunmute`, `makemod`, `removemod`, `shutdown`, `restart`, `jsk`, `statuses`, `metrics`, `mail`", inline=False)

		await ctx.message.channel.send(embed=helpEm)

	@help.command()
	async def cr(self, ctx):
		em = discord.Embed(color=color.lightpink, description="**Usage**:\n\nSimply type `!cr` to see the available commands, their name are pretty self-explanatory.\n\n*You need to be at least lvl 40+ to use this command c:*")
		await ctx.send(embed=em)

	@help.command()
	async def reclist(self, ctx):
		em = discord.Embed(color=color.lightpink, description="**Usage:**\n\n`!reclist [user]` - check your/someone else's reclist\n`!reclist set` - set your reclist\n`!reclist add` - add recs to ur reclist\n`!reclist remove/delete` - delete/remove ur reclist!\n\nReclist stands for recommendations list, please recommend anime only!")
		await ctx.send(embed=em)

	@help.command()
	async def ppsuck(self, ctx):
		em = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!ppsuck`\n\nSuck pp for some quick money.")
		await ctx.send(embed=em)

	@help.command()
	async def intro(self, ctx):
		em = discord.Embed(color=color.lightpink, description="**Usage:**\n\n \n\n`!intro` - set your intro\n`!intro remove/delete` - remove/delete your intro")
		await ctx.send(embed=em)

	@help.command(aliases=['wi'])
	async def whois(self, ctx):
		em = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!whois [user]`\n\nCheck someone's intro!")
		await ctx.send(embed=em)

	@help.command(aliases=['b-day', 'bday'])
	async def birthday(self, ctx):
		embed = discord.Embed(color=color.lightpink, description="**Usage:**\n\n \n`!birthday [user]` - see when's someone's birthday \n`!birthday set [birthday]` - set your birthday!\n`!birthday remove` - remove your birthday from the list! \n`!birthday delete` - delete your birthday from the list!\n\n***NOTE:***\n `!birthday remove` & `birthday delete` are and do the exact same thing!")
		await ctx.send(embed=embed)

	@help.command()
	async def crime(self, ctx):
		embed = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!work`\n\nCommit crimes that range between `small-medium-big`, and depending on which one you get, the more money you get, but be careful! You can lose the money as well.")
		await ctx.send(embed=embed)

	@help.command(aliases=['guess'])
	async def gtn(self, ctx):
		embed = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!gtn`\n\nPlay guess the number and if you win you'll get some money as prize, but if you lose it then some money will be taken from your wallet.")
		await ctx.send(embed=embed)


	@help.command()
	async def work(self, ctx):
		embed = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!work`\n\nWork and get `5000` coins each hour!")
		await ctx.send(embed=embed)

	@help.command()
	async def fight(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!fight <user>`\n\nFight someone, the outcome is always random!', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command(aliases=['8ball'])
	async def _8ball(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!8ball <question>`\n\nAsk the 8ball a question and get an answer', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def boomerrate(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!boomerrate [user]`', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def hornyrate(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!hornyrate [user]`', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def gayrate(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!gayrate [user]`', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def straightrate(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!straightrate [user]`', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def simprate(self, ctx):
		embed = discord.Embed(description='**Usage:**\n\n `!simprate [user]`', color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def revive(self, ctx):
		revive = discord.Embed(description="**Usage:**\n\n `!revive`!\n\nPings everyone with the chat revive role.\n*Cooldown of 2h after each use.*", color=color.lightpink)
		await ctx.message.channel.send(embed=revive)

	@help.command()
	async def ee(self, ctx):
		ee = discord.Embed(description="**Usage:**\n\n `!ee <emote>`\n\nEnlarges the chosen emote.", color=color.lightpink)
		await ctx.message.channel.send(embed=ee)

	@help.command()
	async def nick(self, ctx):
		nick = discord.Embed(description="**Usage:**\n\n `!nick <newnickname>`\n\nChanges your nickname.\n\nType `!nick off/remove` to remove your nickname!\n\n*Requires you to be at least level 3.*", color=color.lightpink)
		await ctx.message.channel.send(embed=nick)

	@help.command()
	async def snippets(self, ctx):
		snippets = discord.Embed(description="**Usage:**\n\n `!snippets`\n\nSee the list of all snippets.", color=color.lightpink)
		await ctx.message.channel.send(embed=snippets)

	@help.command()
	async def profile(self, ctx):
		profile = discord.Embed(description="**Usage:**\n\n `!profile <user>`\n\nGet a user's profile info.", color=color.lightpink)
		await ctx.channel.send(embed=profile)

	@help.command()
	async def created(self, ctx):
		created = discord.Embed(description="**Usage:**\n\n `!created <user>`\n\nSee when the user joined discord / created their account.", color=color.lightpink)
		await ctx.channel.send(embed=created)

	@help.command()
	async def joined(self, ctx):
		joined = discord.Embed(description="**Usage:**\n\n `!joined <user>`\n\nSee when the user joined the server.", color=color.lightpink)
		await ctx.channel.send(embed=joined)

	@help.command(aliases=["avatar"])
	async def av(self, ctx):
		av = discord.Embed(description="**Usage:**\n\n `!av <user>`\n\nSee a user's avatar.", color=color.lightpink)
		await ctx.channel.send(embed=av)

	@help.command(aliases=["server", "si", "sinfo"])
	async def serverinfo(self, ctx):
		serverinfo = discord.Embed(description="**Usage:**\n\n `!serverinfo`\nAliases: `server`, `sinfo`, `si`\n\nGet some info about the server.", color=color.lightpink)
		await ctx.channel.send(embed=serverinfo)

	@help.command()
	async def actions(self, ctx):
		actions = discord.Embed(description="**Usage:**\n\n `!actions`\n\nSee a list of all actions.", color=color.lightpink)
		await ctx.channel.send(embed=actions)

	@help.command()
	async def waifu(self, ctx):
		waifu = discord.Embed(description="**Usage:**\n\n `!waifu`\n\nGet a random waifu pic.", color=color.lightpink)
		await ctx.channel.send(embed=waifu)

	@help.command(aliases=["inv"])
	async def invite(self, ctx):
		invite = discord.Embed(description="**Usage:**\n\n `!invite`\n\nGet the server invite.", color=color.lightpink)
		await ctx.channel.send(embed=invite)

	@help.command()
	async def ad(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!ad {your ad}`\n\nAdvertise your server in the advertisement channel ;3\nUse only in <#750160851822182486> or <#750160851822182487>", color=color.lightpink)
		await ctx.channel.send(embed=embed)

	@help.command()
	async def serverad(self, ctx):
		ad = discord.Embed(description="**Usage:**\n\n `!serverad`\n\nGet the server's advertising text.", color=color.lightpink)
		await ctx.channel.send(embed=ad)

	@help.command()
	async def rawad(self, ctx):
		rawad = discord.Embed(description="**Usage:**\n\n `!rawad`\n\nGet the server's advertising text in raw format.", color=color.lightpink)
		await ctx.channel.send(embed=rawad)

	@help.command(aliases=["untill-partner"])
	async  def up(self, ctx):
		up = discord.Embed(description="**Usage:**\n\n `!untill-partner`\n\nSee how many members the server needs untill it's eligible for applying for the discord partnership program.", color=color.lightpink)
		await ctx.channel.send(embed=up)

	@help.command()
	async def level(self, ctx):
		level = discord.Embed(description="**Usage:**\n\n `!level <user>`\n\nSee how to check your current level.\n*This is not the command to check your level, it's just a help command to show u/others how to check your level.*\n*Requires at least level*   **10**  *in order to use the command.*", color=color.lightpink)
		await ctx.channel.send(embed=level)

	@help.command()
	async def rank(self, ctx):
		level = discord.Embed(description="**Usage:**\n\n `!rank <user>`\n\nSee how to check your current level.\n*This is not the command to check your level, it's just a help command to show u/others how to check your level.*\n*Requires at least level*  **10**  *in order to use the command.*", color=color.lightpink)
		await ctx.channel.send(embed=level)

	@help.command()
	async def sfw(self, ctx):
		sfw = discord.Embed(description="**Usage:**\n\n `!sfw <user>`\n\nWarn a user to keep the chat appropriate and sfw.\n\n*Requires at least level*  **10**  *in order to use the command.*", color=color.lightpink)
		await ctx.channel.send(embed=sfw)

	@help.command()
	async def botinfo(self, ctx):
		botinfo = discord.Embed(description="**Usage:**\n\n `!botinfo`\n\nSee info about <@!751724369683677275>.", color=color.lightpink)
		await ctx.channel.send(embed=botinfo)

	@help.command()
	async def uptime(self, ctx):
		uptime = discord.Embed(description="**Usage:**\n\n `!uptime`\n\nCheck the bot's uptime.", color=color.lightpink)
		await ctx.channel.send(embed=uptime)

	@help.command()
	async def ping(self, ctx):
		ping = discord.Embed(description="**Usage:**\n\n `!ping`\n\nCheck the bot's ping.", color=color.lightpink)
		await ctx.channel.send(embed=ping)

	@help.command()
	@commands.has_role("Staff")
	async def clear(self, ctx):
		clear = discord.Embed(description="**Usage:**\n\n `!clear <amount>`\n\nClear's the chat of the amount of messages given.", color=color.lightpink)
		await ctx.channel.send(embed=clear)

	@help.command()
	@commands.has_role("Staff")
	async def mute(self, ctx):
		mute = discord.Embed(description="**Usage:**\n\n `!mute <user> <reason>`\n\nThis command mutes the user permanently untill a moderator unmutes him.", color=color.lightpink)
		await ctx.channel.send(embed=mute)

	@help.command()
	@commands.has_role("Staff")
	async def massmute(self, ctx):
		mute = discord.Embed(description="**Usage:**\n\n `!mute {user1} {user2} {user3} {reason}`\n\nThis command mutes the users permanently untill a moderator unmutes him.", color=color.lightpink)
		await ctx.channel.send(embed=mute)

	@help.command()
	@commands.has_role("Staff")
	async def tempmute(self, ctx):
		tempmute = discord.Embed(description="**Usage:**\n\n `!tempmute <user> <time>`\n**!tempmute @BananaBoy69 1 s|m|h|d**\n s - second\n m - minute\n h - hour\n d - day\n\nTempmutes a user with the  given time.\n**DO NOT GO ABOVE 24H**", color=color.lightpink)
		await ctx.channel.send(embed=tempmute)

	@help.command()
	@commands.has_role("Staff")
	async def unmute(self, ctx):
		unmute = discord.Embed(description="**Usage:**\n\n `!unmute <user>`\n\nUnmutes the user.", color=color.lightpink)
		await ctx.channel.send(embed=unmute)

	@help.command()
	@commands.has_role("Staff")
	async def massunmute(self, ctx):
		unmute = discord.Embed(description="**Usage:**\n\n `!massunmute {user1} {user2} {user3}`\n\nUnmutes the users.", color=color.lightpink)
		await ctx.channel.send(embed=unmute)
	
	@help.command()
	@commands.has_role('Staff')
	async def kick(self, ctx):
		kick = discord.Embed(description="**Usage:**\n\n `!kick {user} {reason}`\n\nKicks an user from the server!", color=color.lightpink)
		await ctx.send(embed=kick)

	@help.command()
	@commands.has_role('Staff')
	async def masskick(self, ctx):
		kick = discord.Embed(description="**Usage:**\n\n `!masskick {user1} {user2} {user3} {reason}`\n\nKicks the users from the server!", color=color.lightpink)
		await ctx.send(embed=kick)

	@help.command()
	@commands.has_role("Staff")
	async def ban(self, ctx):
		ban = discord.Embed(description="**Usage:**\n\n `!ban <user>`\n\nBans a user.", color=color.lightpink)
		await ctx.channel.send(embed=ban)

	@help.command()
	@commands.has_role("Staff")
	async def massban(self, ctx):
		ban = discord.Embed(description="**Usage:**\n\n `!ban {user1} {user2} {user3}`\n\nBans the users.", color=color.lightpink)
		await ctx.channel.send(embed=ban)

	@help.command()
	@commands.has_role("Staff")
	async def unban(self, ctx):
		unban = discord.Embed(description="**Usage:**\n\n `!unban <user>`\n\nThis command only works in the ban appeal server, if the user is in that server ;)).", color=color.lightpink)
		await ctx.channel.send(embed=unban)

	@help.command()
	@commands.has_role("Staff")
	async def massunban(self, ctx):
		unban = discord.Embed(description="**Usage:**\n\n `!unban {user1} {user2} {user3}`\n\nThis command only works in the ban appeal server, if the users are in that server ;)).", color=color.lightpink)
		await ctx.channel.send(embed=unban)

	@help.command()
	@commands.has_role("Staff")
	async def partnership(self, ctx):
		partnership = discord.Embed(description="**Usage:**\n\n `!partenrship <ad>`\n ad - the ad of the server that the partnership is made with.\n\n**USE IT ONLY IN <#750160851822182480>**", color=color.lightpink)
		await ctx.channel.send(embed=partnership)

	@help.command()
	async def suggest(self, ctx):
		suggest = discord.Embed(description="**Usage:**\n\n `!suggest <suggestion>` in <#750160851822182486> or <#750160851822182487>\n\nMake a suggestion in <#750160850593251454>\n*There is 1 minute cooldown between each suggestion per user.*", color=color.lightpink)
		await ctx.channel.send(embed=suggest)

	@help.command()
	async def spotify(self, ctx):
		spotify = discord.Embed(description="**Usage:**\n\n `!spotify`\n\nShow's what song you're listening to, the artist & the album.\n*You gotta have spotify as activity and no other custom activity in order for this command to work*", color=color.lightpink)
		await ctx.channel.send(embed=spotify)

	@help.command()
	async def membercount(self, ctx):
		membercount = discord.Embed(description="**Usage:**\n\n `!membercount`\n\nSee how many members Anime Hangouts has (**bots are not included**)", color=color.lightpink)
		await ctx.channel.send(embed=membercount)

	@help.command(aliases=["status"])
	@commands.check(Developer)
	async def statuses(self, ctx):
		statuses = discord.Embed(title="Statuses:", color=color.lightpink)
		statuses.add_field(name="Online:", value=";;status online\n   ;;status online-playing [custom status]\n   ;;status online-listening [custom status]\n   ;;status online-watching [custom status]", inline=False)
		statuses.add_field(name="Idle:", value=";;status idle\n   ;;status idle-playing [custom status]\n   ;;status idle-listening [custom status]\n   ;;status idle-watching [custom status]", inline=False)
		statuses.add_field(name="Dnd:", value=";;status dnd\n   ;;status dnd-playing [custom status]\n   ;;status dnd-listening [custom status]\n   ;;status dnd-watching [custom status]", inline=False)
		statuses.add_field(name="Offline:", value=";;status offline", inline=False)

		await ctx.channel.send(embed=statuses)

	@help.command()
	async def meme(self, ctx):
		meme = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!meme`\n\nSends a random meme! ;3")
		await ctx.channel.send(embed=meme)

	@help.command()
	async def cat(self, ctx):
		meme = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!cat`\n\nSends a random cat pic/vid! ;3")
		await ctx.channel.send(embed=meme)

	@help.command()
	async def dog(self, ctx):
		meme = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!dog`\n\nSends a random dog pic/vid! ;3")
		await ctx.channel.send(embed=meme)

	@help.command()
	@commands.check(Developer)
	async def mail(self, ctx):
		em = discord.Embed(description='**Usage:**\n\n `;;mail {member} {args}`\n To get the member, copy the ID and then put it in between `<@!ID>` by replacing the "ID" with the ID of the member you want the bot to dm.\n\n***Note that this command works in dms as well. ;))***')
		await ctx.send(embed=em)

	@help.command()
	async def snipe(self, ctx):
		em = discord.Embed(description='**Usage:**\n\n `!snipe`\n\nSnipe the last deleted message in the channel!', color=color.lightpink)
		await ctx.send(embed=em)

	@help.command()
	async def nsfw(self, ctx):
		if "Staff" in [role.name for role in ctx.message.author.roles]:

			em = discord.Embed(color=color.lightpink, description='**Usage:**\n\n `!nsfw add {user}` \n `!nsfw remove {user}`\n\nGive the user perms to see the nsfw channel or remove them!')
			await ctx.send(embed=em)

		else:

			em = discord.Embed(color=color.lightpink, description='**Usage:**\n\n `!nsfw yuri | hentai | tentacle | real`\nGet a random `yuri | hentai | tentacle | real` pic! **USE ONLY IN <#780374324598145055>**')
			await ctx.send(embed=em)

	@help.command()
	async def calc(self, ctx):
		embed = discord.Embed(color=color.lightpink, description='**Usage:**\n\n`!calc add {a} {b}`\n`!calc subtract {a} {b}`\n`!calc multiply {a} {b}`\n`!calc divide {a} {b}`\n\n*WARNING: NUMBERS LIKE `2,3` OR `2.3` WILL NOT WORK! USE ONLY NUMBERS LIKE `2` OR `3`;;!*\n\nExample:\n\n`!calc divide 4 2` will result `2.0`\n`!calc divide 4.6 2.3` will result an error;;')
		await ctx.channel.send(embed=embed)

	@help.command()
	@commands.has_role('Staff')
	async def slowmode(self, ctx):
		embed = discord.Embed(color=color.lightpink, description="**Usage:**\n\n `!slowmode {time}`\n\nExample:\n\n`!slowmode 5h` => will set the slowmode to 5h\n`!slowmode 3s` => will change the slowmode to 3s\n`!slowmode off` => will disabled the slowmode\n\n*NOTE: ANY OTHER TIME THAT DOES NOT INCLUDE s |  h, or if it's a letter, then the slowmode will be disabled regardless*")
		await ctx.channel.send(embed=embed)

	@help.command()
	async def topic(self, ctx):
		embed = discord.Embed(color=color.lightpink, description='**Usage:**\n\n `!topic`\n\nGet a random topic to talk about, lolz.')
		await ctx.send(embed=embed)

	@help.command(aliases=['balance'])
	async def bal(self, ctx):
		if ctx.author.id == 374622847672254466:
			embedd = discord.Embed(description="\n\n**[MANAGE]**\n\n`!bal add-wallet [amount] [user]`\n`!bal add-bank [amount] [user]`\n`!bal set-wallet [amount][user]`\n`!bal set-bank [amount] [user]`\n`!bal reset [user]`\n\nAdd money to an user's bank/wallet.\nSet user's bank/wallet coins.\nReset a user's balance back to 0.", color=color.lightpink)
			await ctx.send(embed=embedd)

		else:
			embed = discord.Embed(description="**Usage:**\n\n `!bal`\n\nCheck your or another user's balance!", color=color.lightpink)
			await ctx.send(embed=embed)

	@help.command(aliases=['deposit'])
	async def dep(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!dep [amount]`\n\nDeposit the amount of money from your wallet into the bank!", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command(aliases=['withdraw', "with"])
	async def _with(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!with [amount]`\n\nWithdraw the amount of money from your bank into your wallet!", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def beg(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!beg`\n\nBeg to get some money, peasant!\n*You can only use this command each 5 seconds!*", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def steal(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!steal [user]`\n\nSteal some money from someone's wallet!", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def rob(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!rob [user]`\n\nRob from someone's wallet!", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def slots(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!slots [amount]`\n\nBet your money in the slots machine!", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.command()
	async def give(self, ctx):
		embed = discord.Embed(description="**Usage:**\n\n `!give [user] [amount]`\n\nBe a kind person and give some of your money from ur bank to someone else's!", color=color.lightpink)
		await ctx.send(embed=embed)

	@help.error
	async def help_error(self, ctx, error):
		if isinstance(error, commands.TooManyArguments):
			return



















def setup(client):
	client.add_cog(Help(client))