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
		helpEm = discord.Embed(description="To get help for a certain command type `!help <command_name>`", color=color.lightpink)
		helpEm.set_footer(text='To get help for a certain command type `!help <command_name>`\n', icon_url=ctx.author.avatar_url)
		helpEm.set_thumbnail(url=self.client.user.avatar_url)
		helpEm.add_field(name="Commands", value="`ee`, `nick`, `profile`, `created`, `joined`, `av`, `waifu`, `invite`, `suggest`, `spotify`, `meme`, `cat`, `dog`, `snipe`, `nsfw`, `topic`, `gayrate`, `straightrate` , `simprate`, `hornyrate`, `boomerrate`, `8ball`, `fight`, `ppsize`, `birthday`, `intro`, `whois`, `reclist`, `dev-portal`, `perm-calc`, `cr`, `vampify`, `clapify`, `define`, `search`, `calculator`, `marry`, `marriedwho`, `divorce`, `scrs`, `tag`, `snippets`, `role-id`, `rank`, `remind`, `top`, `bdsm`, `randomnumber`")
		helpEm.add_field(name="Economy", value="`register`, `unregister` ,`balance`, `deposit`, `withdraw`, `steal`, `slots`, `beg`, `give`, `work`, `crime`, `guess`, `race`, `ppsuck`, `daily`", inline=False)
		helpEm.add_field(name="Info", value="`untill-partner`, `membercount`, `sfw`, `spam`, `english`, `botinfo`, `uptime`, `ping`, `serverad`, `rawad`, `serverinfo`, `vote`", inline=False)
		if "Staff" in [role.name for role in ctx.message.author.roles]:
			helpEm.add_field(name="Moderator Commands", value="`clear`, `mute`, `tempmute`, `unmute`, `kick`, `ban`, `opban`, `unban`, `opunban`, `nsfw`, `slowmode`", inline=False)
		
		if ctx.author.id == 374622847672254466:
			helpEm.add_field(name="Dev Commands", value="`eval`, `load`, `unload`, `reload`, `reload all`, `unload all`, `load all`, `modmute`, `modunmute`, `makemod`, `removemod`, `shutdown`, `restart`, `jsk`, `statuses`, `metrics`, `mail`", inline=False)

		await ctx.send(embed=helpEm)
	
	@help.command(aliases=['number', 'random', 'rn', 'randomnr'])
	async def randomnumber(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!randomnumber [num1] [num2] [num3]```")
		em.add_field(name="***Aliases:***", value="• **number**\n• **random**\n• **rn**\n• **randomnr**", inline=False)
		em.add_field(name="***Info:***", value="If you don't provide any number, the bot will give a random number between `0` and the `largest positive integer supported by the machine`.\n\nIf you provide only one number, then the bot will give a random number between `0` and `your chosen number (num1)`.\n\nIf you provide two numbers only, then the bot will give you a random number between `your first number (num1)` and `your second number (num2)`.\n\nIf you provide all three numbers, then the bot will give a random number between `your first number (num1)` and `your second number (num2)`, that is not `your third number (num3)`, this can be used if you want a random number between 2 numbers that is not a specific one, here's some examples:\n• `10 15 13 - will give a number between 10 and 15 that is not 13`\n• `0 10 5 - will give a number between 0 and 10 that is not 5`\n• `20 100 50 - will give a number between 20 and 100 that is not 50`\n• `10 20 15 - will give a number between 10 and 20 that is not 15`", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def bdsm(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!bdsm set\n!bdsm results [member]\n!bdsm remove\n!bdsm test```")
		em.add_field(name="***Info:***", value="`!bdsm results <member>` - send the bdsm results of the specified member. \n`!bdsm set` - set your bdsm result by sending the screenshot of your results. \n`!bdsm remove` - remove your bdsm results. \n`!bdsm test` - take the test, duh.", inline=False)
		
		await ctx.send(embed=em)

	@help.command(aliases=['msg-top', 'top-msg'])
	async def top(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!top```")
		em.add_field(name="***Aliases:***", value="• **msg-top**\n• **top-msg**", inline=False)
		em.add_field(name="***Info:***", value="See top ~`15` most active members.", inline=False)
		
		await ctx.send(embed=em)

	@help.command(aliases=['reminder'])
	async def remind(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!reminder <when> [what]\n!remind list\n!remind cancel <remind ID>\n!remind clear```")
		em.add_field(name="***Commands:***", value="\n• **list**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get a list of your `10` upcoming reminders!\n\n• **cancel**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **remove**\n\u2800\u2800\u2800• **delete**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete your reminder by it's ID.\n\n• **clear**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Clear all your reminders!", inline = False)
		em.add_field(name="***Info:***", value="• Set a reminder.", inline = False)

		await ctx.send(embed=em)


	@help.command(aliases=['level', 'lvl'])
	async def rank(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!rank [member]\n!rank leaderboard```")
		em.add_field(name="***Commands:***", value="\n• **leaderboard**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **lb**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• See top `10` highest level members!", inline = False)
		em.add_field(name="***Aliases:***", value="• **level**\n• **lvl**", inline = False)
		
		if ctx.author.id == 374622847672254466:
			em.add_field(name="_ _ \n***Dev Only:***", value="_ _ \n\u2800***Usage***: \n\u2800\u2800`!rank set <lvl> <user>`\n\u2800***Info:***\n\u2800\u2800• Set a user's level.\n _ _")
		
		em.add_field(name="***Info:***", value="• Check your current level.", inline = False)
		
		await ctx.send(embed=em)

	@help.command(aliases=['role-id'])
	async def _role_id(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!role-id <role_name>```")
		em.add_field(name="***Info:***", value="• Get the ID of the given role.")

		await ctx.send(embed=em)

	@help.command()
	async def ppsuck(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!ppsuck```")
		em.add_field(name="***Info:***", value="• Suck pp for some quick money.")

		await ctx.send(embed=em)

	@help.command(aliases=['tags'])
	async def tag(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!tag <tag_name>\n!tag create <tag_name>\n!tag delete <tag_name>\n!tag info <tag_name>\n!tag all\n!tag list\n!tag leaderboard```")
		em.add_field(name="***Commands:***", value="\n• **create**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **make**\n\u2800\u2800\u2800• **add**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Create a new tag!\n\u2800\u2800***Warning:***\n\u2800\u2800\u2800• They cannot contain any of the banned words (in case it does you will be banned without a second thought, so be careful!)\n\u2800\u2800\u2800• They cannot contain attachments!\n\n• **delete**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete a tag that you made.\n\n• **info**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• See info about a tag!\n\n• **all**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get paginated list with all tags.\n\n• **list**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get paginated list with all tags that a user owns.\n\n• **leaderboard**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **lb**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• See top `10` most used tags!", inline=False)
		
		if ctx.author.id == 374622847672254466:
			em.add_field(name="_ _ \n***Dev Only:***", value="_ _ \n\u2800***Usage***: \n\u2800\u2800`!tag remove <tag_name>`\n\u2800***Info:***\n\u2800\u2800• Remove a tag from the database.\n _ _")

		em.add_field(name="***Info:***", value="• Allows you to tag text for later retrieval.", inline=False)
		await ctx.send(embed=em)

	@help.command(aliases=['ss'])
	async def scrs(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!scrs <domain>```")
		em.add_field(name="***Aliases:***", value="• ss", inline=False)
		em.add_field(name="***Info:***", value="• Take a scren shot of a domain.\n• It will **not** work if the site you try to screen shot has captcha verification.", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def marry(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!marry <user>```")
		em.add_field(name="***Info:***", value="• Marry to someone <:SheepLove:787370467438362694>")
		await ctx.send(embed=em)

	@help.command()
	async def divorce(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!divorce```")
		em.add_field(name="***Info:***", value="• Divorce with the person you are married to. :cry:")
		await ctx.send(embed=em)

	@help.command()
	async def marriedwho(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!marriedwho <user>```")
		em.add_field(name="***Info:***", value="• See who the user is married to.")
		await ctx.send(embed=em)

	@help.command()
	async def opban(self, ctx):
		em = discord.Embed(color=color.lightpink, title="**Usage:**", description="```CSS\n!opban <user>```")
		em.add_field(name="***Info:***", value="• Bans a user that is **not** in the server.")
		await ctx.send(embed=em)


	@help.command()
	async def opunban(self, ctx):
		em = discord.Embed(color=color.lightpink, title="**Usage:**", description="```CSS\n!opunban <user>```")
		em.add_field(name="***Info:***", value="• Unbans a user that is **not** in the ban appeal server or the server itself.")
		await ctx.send(embed=em)

	@help.command()
	async def search(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!define <query>```")
		em.add_field(name="***Info:***", value="• Search for a query.")
		await ctx.send(embed=em)

	@help.command()
	async def define(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!define <word>```")
		em.add_field(name="***Info:***", value="• Search the definition of a word.")
		await ctx.send(embed=em)

	@help.command(aliases=['snippets'])
	async def snippet(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!snippets\n!snippet create <snippet_name>\n!snippet delete <snippet_name>\n!snippet list [user]\n!snippet leaderboard```")
		em.add_field(name="***Commands:***", value="• **create**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **make**\n\u2800\u2800\u2800• **add**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Create a new snippet.\n\u2800\u2800***Requirements:***\n\u2800\u2800\u2800• Level 55+\n\n• **delete**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete a snippet you own.\n\u2800\u2800***Requirements:***\n\u2800\u2800\u2800• Level 55+\n\n• **list**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get a paginated list of snippets that a user owns.\n\n• **leaderboard**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **lb**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• See top `10` most used snippets!", inline=False)

		if ctx.author.id == 374622847672254466:
			em.add_field(name="_ _ \n***Dev Only:***", value="_ _ \n\u2800***Usage***: \n\u2800\u2800`!snippet remove <snippet_name>`\n\u2800***Info:***\n\u2800\u2800• Remove a snippet from the database.\n _ _")

		em.add_field(name="***Info:***", value="• Send paginated list of all snippets.", inline=False)

		await ctx.send(embed=em)

	@help.command()
	async def vampify(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!vampify <text>```")
		embed.add_field(name="***Info:***", value="• Vampify your text!")
		await ctx.send(embed=embed)

	@help.command()
	async def clapify(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!clapify <text>```")
		embed.add_field(name="***Info:***", value="• Clapify your text!")
		await ctx.send(embed=embed)

	@help.command()
	async def cr(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!cr create\n!cr delete\n!cr edit color <new_color>\n!cr name <new_name>\n!cr share <user>\n!cr unrole <cr_id>\n!cr clean```")
		em.add_field(name="***Commands:***", value="• **create**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Create your cr.\n\n• **delete**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete your cr.\n\n• **edit color**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Edit your cr's color.\n\n• **edit name**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Edit your cr's name.\n\n• **share**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Share your cr with someone.\n\n• **unrole**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Remove a cr from your profile. To get the cr's ID type: `!role-id <role_name>`.\n\n• **clean**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Remove all cr's that you don't own from your profile.")
		em.add_field(name="***Requirements:***", value="• Level 40 +", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def reclist(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!reclist [user]\n!reclist set <recommendations>\n!reclist add <recommendations>\n!reclist delete```")
		em.add_field(name="***Commands:***", value="• **set**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Set up your reclist.\n\n • **add**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Add reccomendations up your reclist.\n\n• **delete**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete your reclist.\n\n• **raw**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get a raw version of your reclist!\n*• This is used so you can copy paste your old reclist, and then remove what you want to remove from it so you don't have to type your reclist over and over again.*", inline=False)
		
		if ctx.author.id == 374622847672254466:
			em.add_field(name="_ _ \n***Dev Only:***", value="_ _ \n\u2800***Usage***: \n\u2800\u2800`!reclist remove <user>`\n\u2800***Info:***\n\u2800\u2800• Remove a user's reclist from the database.\n _ _")

		em.add_field(name="Info", value="• Check your or someone else's reclist\n• Reclist stands for recommendations list, please recommend anime only!", inline=False)

		await ctx.send(embed=em)

	@help.command()
	async def race(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!race```")
		em.add_field(name="***Info:***", value="• Get into a race and win or lose some money depending on your luck.")
		await ctx.send(embed=em)

	@help.command()
	async def intro(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!intro | delete```")
		em.add_field(name="***Info:***", value="• Set your intro | Delete your intro")
		await ctx.send(embed=em)

	@help.command(aliases=['wi'])
	async def whois(self, ctx):
		em = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!whois [user]```")
		em.add_field(name="***Aliases:***", value="• wi", inline=False)
		em.add_field(name="***Info:***", value="• Check someone's intro!", inline=False)
		await ctx.send(embed=em)

	@help.command(aliases=['b-day', 'bday'])
	async def birthday(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!birthday [user]\n!birthday set month/day\n!birthday remove\n!birthday upcoming```")
		embed.add_field(name="***Aliases:***", value="• b-day\n• bday", inline=False)
		embed.add_field(name="***Commands:***", value="• **set**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Set up your birthday.\n**Example:**\n\u2800`!birthday set 04/27`\n\u2800`!birthday set 01/09`\n\u2800`!birthday set 04/24`\n\u2800`!birthday set 12/01`\n\n • **delete**\n\n\u2800\u2800***Aliases:***\n\n\u2800\u2800\u2800• **remove**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Delete your birthday from the database.\n\n • **upcoming**\n\n\u2800\u2800***Aliases:***\n\n\u2800\u2800\u2800• **top**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Get the next `5` upcoming birthdays.", inline=False)
		embed.add_field(name="***Info:***", value="• See when someone's birthday is.")
		await ctx.send(embed=embed)

	@help.command()
	async def crime(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!crime```")
		embed.add_field(name="***Info:***", value="• Commit crimes that range between `small-medium-big`, and depending on which one you get, the more money you get, but be careful! You can lose the money as well.")
		await ctx.send(embed=embed)

	@help.command(aliases=['guess'])
	async def gtn(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!guess```")
		embed.add_field(name="***Aliases:***", value="• gtn", inline=False)
		embed.add_field(name="***Info:***", value="• Play guess the number and if you win you'll get some money as prize, but if you lose it then some money will be taken from your wallet.", inline=False)
		await ctx.send(embed=embed)


	@help.command()
	async def work(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!work```")
		embed.add_field(name="***Info:***", value="• Work and get `5000` coins each hour!")
		await ctx.send(embed=embed)

	@help.command()
	async def fight(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!fight <user>```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• Fight someone, the outcome is always random!")
		await ctx.send(embed=embed)

	@help.command(aliases=['8ball'])
	async def _8ball(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!8ball <question>```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• Ask the 8ball a question and get an answer.")
		await ctx.send(embed=embed)

	@help.command()
	async def boomerrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!boomerrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• See how boomer someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def hornyrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!hornyrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• See how horny someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def gayrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!gayrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• See how gay someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def straightrate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!straightrate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• See how straight someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def simprate(self, ctx):
		embed = discord.Embed(title='***Usage:***', description='```CSS\n!simprate [user]```', color=color.lightpink)
		embed.add_field(name="***Info:***", value="• See how simp someone is.")
		await ctx.send(embed=embed)

	@help.command()
	async def ee(self, ctx):
		ee = discord.Embed(title="***Usage:***", description="```CSS\n!ee <emote>```", color=color.lightpink)
		ee.add_field(name="***Info:***", value="• Enlarges the chosen emote.")
		await ctx.send(embed=ee)

	@help.command()
	async def nick(self, ctx):
		nick = discord.Embed(title="***Usage:***", description="```CSS\n!nick <newnickname>\n!nick remove```", color=color.lightpink)
		nick.add_field(name="***Commands:***", value="• **remove**\n\n\u2800\u2800***Aliases:***\n\u2800\u2800\u2800• **reset**\n\u2800\u2800\u2800• **off**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Remove your nickname.")
		nick.add_field(name="***Info:***", value="• Change your nickname", inline=False)
		nick.add_field(name="***Requirements:***", value="• Level 3 +", inline=False)
		await ctx.send(embed=nick)

	@help.command()
	async def profile(self, ctx):
		profile = discord.Embed(title="***Usage:***", description="```CSS\n!profile [user]```", color=color.lightpink)
		profile.add_field(name="***Info:***", value="• Get a user's profile info.")
		await ctx.send(embed=profile)

	@help.command()
	async def created(self, ctx):
		created = discord.Embed(title="***Usage:***", description="```CSS\n!created [user]```", color=color.lightpink)
		created.add_field(name="***Info:***", value="• See when a user joined discord / created their account.")
		await ctx.send(embed=created)

	@help.command()
	async def joined(self, ctx):
		joined = discord.Embed(title="***Usage:***", description="```CSS\n!joined [user]```", color=color.lightpink)
		joined.add_field(name="***Info:***", value="• See when a user joined the server.")
		await ctx.send(embed=joined)

	@help.command(aliases=["avatar"])
	async def av(self, ctx):
		av = discord.Embed(title="***Usage:***", description="```CSS\n!avatar [user]```", color=color.lightpink)
		av.add_field(name="***Aliases:***", value="• av", inline=False)
		av.add_field(name="***Info:***", value="• See user's avatar.", inline=False)
		await ctx.send(embed=av)

	@help.command(aliases=["server", "si", "sinfo"])
	async def serverinfo(self, ctx):
		serverinfo = discord.Embed(title="***Usage:***", description="```CSS\n!serverinfo```", color=color.lightpink)
		serverinfo.add_field(name="***Aliases:***", value="• server \n• sinfo \n• si", inline=False)
		serverinfo.add_field(name="***Info:***", value="• Get some info about the server.", inline=False)
		await ctx.send(embed=serverinfo)

	@help.command()
	async def actions(self, ctx):
		actions = discord.Embed(title="***Usage:***", description="```CSS\n!actions```", color=color.lightpink)
		actions.add_field(name="***Info:***", value="• See a list of all existing actions.")
		await ctx.send(embed=actions)

	@help.command()
	async def waifu(self, ctx):
		waifu = discord.Embed(title="***Usage:***", description="```CSS\n!waifu```", color=color.lightpink)
		waifu.add_field(name="***Info:***", value="• Get a random waifu pic.")
		await ctx.send(embed=waifu)

	@help.command(aliases=["inv"])
	async def invite(self, ctx):
		invite = discord.Embed(title="***Usage:***", description="```CSS\n!invite```", color=color.lightpink)
		invite.add_field(name="***Aliases:***", value="• inv", inline=False)
		invite.add_field(name="***Info:***", value="• Get the invite to the server.", inline=False)
		await ctx.send(embed=invite)

	@help.command()
	async def serverad(self, ctx):
		ad = discord.Embed(title="***Usage:***", description="```CSS\n!serverad```", color=color.lightpink)
		ad.add_field(name="***Info:***", value="• Get the server's advertising text.", inline=False)
		await ctx.send(embed=ad)

	@help.command()
	async def rawad(self, ctx):
		rawad = discord.Embed(title="***Usage:***", description="```CSS\n!rawad```", color=color.lightpink)
		rawad.add_field(name="***Info:***", value="• Get the server's advertising text in raw format.", inline=False)
		await ctx.send(embed=rawad)

	@help.command(aliases=["untill-partner"])
	async  def up(self, ctx):
		up = discord.Embed(title="***Usage:***", description="```CSS\n!untill-partner```", color=color.lightpink)
		up.add_field(name="***Info:***", value="• See how many members the server needs untill it's eligible for applying for the discord partnership program.", inline=False)
		await ctx.send(embed=up)

	@help.command()
	async def botinfo(self, ctx):
		botinfo = discord.Embed(title="***Usage:***", description="```CSS\n!botinfo```", color=color.lightpink)
		botinfo.add_field(name="***Info:***", value="• See info about <@!751724369683677275>.", inline=False)
		await ctx.send(embed=botinfo)

	@help.command()
	async def uptime(self, ctx):
		uptime = discord.Embed(title="***Usage:***", description="```CSS\n!uptime```", color=color.lightpink)
		uptime.add_field(name="***Info:***", value="• Check the bot's uptime.", inline=False)
		await ctx.send(embed=uptime)

	@help.command()
	async def ping(self, ctx):
		ping = discord.Embed(title="***Usage:***", description="```CSS\n!ping```", color=color.lightpink)
		ping.add_field(name="***Info:***", value="• Check the bot's ping.", inline=False)
		await ctx.send(embed=ping)

	@help.command()
	@commands.has_role("Staff")
	async def clear(self, ctx):
		clear = discord.Embed(title="***Usage:***", description="```CSS\n!clear <amount>```", color=color.lightpink)
		clear.add_field(name="***Info:***", value="• Clear's the chat of the amount of messages given..", inline=False)
		await ctx.send(embed=clear)

	@help.command()
	@commands.has_role("Staff")
	async def tempmute(self, ctx):
		tempmute = discord.Embed(title="***Usage:***", description="```CSS\n!tempmute <user> <time>```", color=color.lightpink)
		tempmute.add_field(name="***Example:***", value="!tempmute @BananaBoy69 1 s|m|h|d", inline=False)
		tempmute.add_field(name="***Info:***", value="• s - second\n• m - minute\n• h - hour\n• d - day\n\n• Mutes a user with the  given time.", inline=False)
		await ctx.send(embed=tempmute)

	@help.command()
	@commands.has_role("Staff")
	async def unban(self, ctx):
		unban = discord.Embed(title="***Usage:***", description="```CSS\n!unban <user>```", color=color.lightpink)
		unban.add_field(name="***Info:***", value="• This command only works in the ban appeal server, if the user is in that server ;)).", inline=False)
		await ctx.send(embed=unban)

	@help.command(aliases=['ps'])
	@commands.has_role("Staff")
	async def partnership(self, ctx):
		partnership = discord.Embed(title="***Usage:***", description="```CSS\n!partnership <ad>```", color=color.lightpink)
		partnership.add_field(name="***Aliases:***", value="• ps", inline=False)
		partnership.add_field(name="***Info:***", value="• ad - the ad of the server that the partnership is made with.\n\n**USE IT ONLY IN <#750160851822182480>**", inline=False)
		await ctx.send(embed=partnership)

	@help.command()
	async def suggest(self, ctx):
		suggest = discord.Embed(title="***Usage:***", description="```CSS\n!suggest <suggestion>```", color=color.lightpink)
		suggest.add_field(name="***Info:***", value="• Make a suggestion in <#750160850593251454>\n• There is 1 minute cooldown between each suggestion per user.", inline=False)
		await ctx.send(embed=suggest)

	@help.command()
	async def spotify(self, ctx):
		spotify = discord.Embed(title="***Usage:***", description="```CSS\n!spotify [user]```", color=color.lightpink)
		spotify.add_field(name="***Info:***", value="• Show's what song you're listening to, the artist & the album.\n• You gotta have spotify as activity and no other custom activity in order for this command to work.", inline=False)
		await ctx.send(embed=spotify)

	@help.command()
	async def membercount(self, ctx):
		membercount = discord.Embed(title="***Usage:***", description="```CSS\n!membercount```", color=color.lightpink)
		membercount.add_field(name="***Info:***", value="• See how many members ViHill Corner has (**bots are not included**).", inline=False)
		await ctx.send(embed=membercount)

	@help.command()
	async def meme(self, ctx):
		meme = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!meme```")
		meme.add_field(name="***Info:***", value="• Sends a random meme! ;3", inline=False)
		await ctx.send(embed=meme)

	@help.command()
	async def cat(self, ctx):
		cat = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!cat```")
		cat.add_field(name="***Info:***", value="• Sends a random cat pic! ;3", inline=False)
		await ctx.send(embed=cat)

	@help.command()
	async def dog(self, ctx):
		dog = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!dog```")
		dog.add_field(name="***Info:***", value="• Sends a random dog pic! ;3", inline=False)
		await ctx.send(embed=dog)

	@help.command()
	async def snipe(self, ctx):
		em = discord.Embed(title='***Usage:***', description='```CSS\n!snipe```', color=color.lightpink)
		em.add_field(name="***Info:***", value="• Snipe the last deleted message in the channel!", inline=False)
		await ctx.send(embed=em)

	@help.command()
	async def nsfw(self, ctx):
		if "Staff" in [role.name for role in ctx.message.author.roles]:

			em = discord.Embed(color=color.lightpink, title='***Usage:***', description='```CSS\n!nsfw block <users>\n!nsfw unblock <users>\n!nsfw blocks```')
			em.add_field(name="***Info:***", value="• Block / Unblock people from using the `!nsfw me add` command & seeing the nsfw channel, or get paginated list of all blocked users.", inline=False)
			await ctx.send(embed=em)

		else:

			em = discord.Embed(color=color.lightpink, title='***Usage:***', description='```CSS\n!nsfw <category>```')
			em.add_field(name="***Categories:***", value="• **`yuri`**\n• **`hentai`**\n• **`tentacle`**\n• **`real`**\n• **`yiff`**", inline=False)
			em.add_field(name="***Commands:***", value="• **me**\n\u2800\u2800***Usage:***\n\u2800\u2800\u2800• `!nsfw me add`\n\u2800\u2800\u2800• `!nsfw me remove`\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Toggle wether you see the nsfw channel or not.\n _ _ ")
			em.set_footer(text="USE ONLY IN THE NSFW CHANNEL", icon_url=ctx.author.avatar_url)
			await ctx.send(embed=em)

	@help.command(aliases=['calculate, calculator'])
	async def calc(self, ctx):
		embed = discord.Embed(color=color.lightpink, title='***Usage:***', description='```CSS\n!calculator <operation>```')
		embed.add_field(name="***Aliases:***", value="• calculate\n• calc", inline=False)
		embed.add_field(name="***Info:***", value="• Basic calculator for basic operations!", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	@commands.has_role('Staff')
	async def slowmode(self, ctx):
		embed = discord.Embed(color=color.lightpink, title="***Usage:***", description="```CSS\n!slowmode <time>```")
		embed.add_field(name="***Info:***", value="• Change the slowmode of the current channel.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def topic(self, ctx):
		embed = discord.Embed(color=color.lightpink, title='***Usage:***', description='```CSS\n!topic```')
		embed.add_field(name="***Info:***", value="• Get a random question or a random topic to talk about.", inline=False)
		await ctx.send(embed=embed)

	@help.command(aliases=['balance'])
	async def bal(self, ctx):
		if ctx.author.id == 374622847672254466:
			embedd = discord.Embed(title="***Usage:***", description="```CSS\n!bal\n!bal add-wallet <amount> [user]\n!bal add-bank <amount> [user]\n!bal set-wallet <amount> [user]\n!bal set-bank <amount> [user]\n!bal reset [user]```", color=color.lightpink)
			embedd.add_field(name="***Commands:***", value="• **add-wallet**\n\n\u2800\u2800\u2800***Info:***\n\u2800\u2800\u2800• Add money to an user's wallet.\n\n• **add-bank**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Add money to an user's bank.\n\n• **set-wallet**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Set user's wallet money.\n\n• **set-bank**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Set user's bank money.\n\n• **reset**\n\n\u2800\u2800***Info:***\n\u2800\u2800\u2800• Reset user's balance.")
			embedd.add_field(name="***Info:***", value="• Check your or another user's balance!", inline=False)
			await ctx.send(embed=embedd)

		else:
			embed = discord.Embed(title="***Usage:***", description="```CSS\n!bal [user]```", color=color.lightpink)
			embed.add_field(name="***Info:***", value="• Check your or another user's balance!", inline=False)
			await ctx.send(embed=embed)

	@help.command(aliases=['deposit'])
	async def dep(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```CSS\n!deposit [amount]```", color=color.lightpink)
		embed.add_field(name="***Aliases:***", value="• dep", inline=False)
		embed.add_field(name="***Info:***", value="• Deposit the amount of money into your bank.", inline=False)
		await ctx.send(embed=embed)

	@help.command(aliases=['withdraw', "with"])
	async def _with(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```CSS\n!withdraw [amount]```", color=color.lightpink)
		embed.add_field(name="***Aliases:***", value="• with", inline=False)
		embed.add_field(name="***Info:***", value="• Withdraw the amount of money from your bank.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def beg(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```CSS\n!beg```", color=color.lightpink)
		embed.add_field(name="***Info:***", value="• Beg for some money, peasant.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def steal(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```CSS\n!steal [user]```")
		embed.add_field(name="***Aliases:***", value="• rob", inline=False)
		embed.add_field(name="***Info:***", value="• Steal some money from someone's wallet.", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def slots(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```CSS\n!slots [amount]```", color=color.lightpink)
		embed.add_field(name="***Info:***", value="• Bet your money in the slots machine!", inline=False)
		await ctx.send(embed=embed)

	@help.command()
	async def give(self, ctx):
		embed = discord.Embed(title="***Usage:***", description="```CSS\n!give [user] [amount]```", color=color.lightpink)
		embed.add_field(name="***Info:***", value="• Be a kind person and give some of your money from ur bank to someone else's!", inline=False)
		await ctx.send(embed=embed)

	@help.error
	async def help_error(self, ctx, error):
		if isinstance(error, commands.TooManyArguments):
			return



















def setup(client):
	client.add_cog(Help(client))