import discord
from discord.ext import commands
import utils.colors as color
from utils.paginator import HelpmMenu
import asyncio

reactions = {
			'<:SakataNom:787370388250034186>': 'help featured',
			'<:CutieUmwha:787370264165482537>': 'help economy',
			'<:vampy1:859050561184989204>': 'help utility',
			'<:epik:818803400154153002>': 'help fun',
			'<:pepecry:859050982507675699>': 'help miscellaneous',
			'<:pepe_hang1:859050982402687026>': 'help info',
			'<:creepy_bird1:859050982382108693>': 'help warns',
			'<:verifiedbotdev:859064715715018782>': 'help developer',
			'<:banhammer:859065173352644628>': 'help moderator'
			}

categs = """
<:SakataNom:787370388250034186> -> **Featured**	
<:CutieUmwha:787370264165482537> -> **Economy**
<:vampy1:859050561184989204> -> **Utility**
<:epik:818803400154153002> -> **Fun**
<:pepecry:859050982507675699> -> **Miscellaneous**
<:pepe_hang1:859050982402687026> -> **Info**
<:creepy_bird1:859050982382108693> -> **Warns**
		"""

class HelpPageEntry:
	def __init__(self, entry):

		self.name = entry['name']
		self.help = entry['help']

	def __str__(self):
		return f'```\n{self.name}```{self.help}\n'

class HelpPages(HelpmMenu):
	def __init__(self, entries, *, per_page=12, title="", color=None):
		converted = [HelpPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page, color=color, title=title)


class Help(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"

		self.ecoCommands = [
				{'_name': ['register'], 'name': '!register', 'help': 'Register yourself to be able to use the economy commands.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['unregister'], 'name': '!unregister', 'help': 'Unregister yourself, you won\'t be able to use the economy commands anymore.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['balance', 'bal', 'bank'], 'name': '![balance|bal] [user]', 'help': 'Check your or another user\'s balance.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['deposit', 'dep'], 'name': '![deposit|dep] <amount>', 'help': 'Deposit the amount of money into your bank.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['withdraw', 'with'], 'name': '![withdraw|with] <amount>', 'help': 'Withdraw the amount of money from your bank.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['steal', 'rob'], 'name': '![steal|rob] <user>', 'help': 'Steal some money from someone\'s wallet.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['slots'], 'name': '!slots <amount>', 'help': 'Bet your money in the slots machine.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['beg'], 'name': '!beg', 'help': 'Beg for some money. This is the easiest way of getting some money in the beginning.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['give', 'gift'], 'name': '![give|gift] <user> <amount>', 'help': 'Be a kind person and give some of your money from your **bank** to someone else\'s.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['work'], 'name': '!work', 'help': 'Work and get `5000` coins each hour.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['crime'], 'name': '!crime', 'help': 'Commit crimes that range between `small-medium-big`, and depending on which one you get, the more money you get, but be careful! You can lose the money as well.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['guess', 'gtn'], 'name': '![guess|gtn]', 'help': 'Play guess the number and if you win you\'ll get some money as prize, but if you lose it then some money will be taken from your wallet.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['race'], 'name': '!race', 'help': 'Get into a race and win or lose some money depending on your luck.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['ppsuck'], 'name': '!ppsuck', 'help': 'Suck pp for some quick money.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}
				]
		
		self.funCommands = [
				{'_name': ['meme'], 'name': '!meme', 'help': 'Sends a random meme! ;3', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['cat'], 'name': '!cat', 'help': 'Sends a random cat pic! ;3', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['dog'], 'name': '!dog', 'help': 'Sends a random dog pic! ;3', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['topic'], 'name': '!topic', 'help': 'Get a random question or a random topic to talk about.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['gayrate', 'gay'], 'name': '!gayrate [user]', 'help': 'See how gay someone is.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['straightrate', 'straight'], 'name': '!straightrate [user]', 'help': 'See how straight someone is.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['simprate', 'simp'], 'name': '!simprate [user]', 'help': 'See how simp someone is.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['hornyrate', 'horny'], 'name': '!hornyrate [user]', 'help': 'See how horny someone is.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['boomerrate', 'boomer'], 'name': '!boomerrate [user]', 'help': 'See how boomer someone is.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['8ball', 'ball'], 'name': '!8ball <question>', 'help': 'Ask the 8ball a question and get an answer.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['fight'], 'name': '!fight <user>', 'help': 'Challenge someone to a fight.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['ppsize', 'pp'], 'name': '!ppsize [user]', 'help': 'See how large your or someone else\'s dick is.', 'hasChild': False, 'devOnly': False, 'staffOnly': False},
				{'_name': ['trivia'], 'name': '!trivia', 'help': '', 'help1': 'Play a game of trivia, you can get points and see who can get the most points. These points have no actual use rather than just simply giving a competitive vibe to the game.', 'help2':'Play a game of trivia, you can get points and see who can get the most points. These points have no actual use rather than just simply giving a *competitive* vibe to the game.\n\u2800**Difficulties:**\n\u2800\u2800 - Easy -> 5 points\n\u2800\u2800 - Medium -> 10 points\n\u2800\u2800 - Hard -> 15 points\n\u2800**Modes:**\n\u2800\u2800 - Solo\n\u2800\u2800\u2800\u2800\u2800Play a normal game of trivia.\n\u2800\u2800 - Competitive\n\u2800\u2800\u2800\u2800\u2800Pick a bet and a player that you will have to do a trivia 1v1 with. The winner gets the bet amount as prize while the loser loses the bet amount of points.', 'hasChild': True, 'devOnly': False, 'staffOnly': False},
				{'_name': ['rock-paper-scissors', 'rps'], 'name': '![rock-paper-scissors|rps]', 'help': 'Play a game of rock-paper-scissors with the bot and earn money.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['tic-tac-toe', 'ttt', 'tictactoe'], 'name': '![tic-tac-toe|ttt] <user>', 'help': 'Play a tic-tac-toe game with someone. Both users must have `10,000` <:carrots:822122757654577183> in your wallet in order to play.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}
				]

		self.warnCommands = [
				{'_name': ['sfw'], 'name': ';sfw [user]', 'help': 'Warn someone about keeping the chat non-nsfw.', 'hasChild': False, 'devOnly': False, 'staffOnly': False},
				{'_name': ['spam'], 'name': ';spam [user]', 'help': 'Warn someone to not spam the chat.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['english', 'eng', 'en'], 'name': ';english [user]', 'help': 'Warn and/or tell someone that the server is english only.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}
				]
		
		self.infoCommands = [
				{'_name': ['lvlinfo', 'howtolvl'], 'name': ';[lvlinfo|howtolvl] [user]', 'help': 'See info about how to level up.', 'hasChild': False, 'devOnly': False, 'staffOnly': False},
				{'_name': ['rankinfo'], 'name': ';rankinfo [user]', 'help': 'See info about how to check your rank.', 'hasChild': False, 'devOnly': False, 'staffOnly': False},
				{'_name': ['cam', 'camera'], 'name': ';cam [user]', 'help': 'See info about what level you need to be in order to use the camera.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['vc', 'voicechat'], 'name': ';vc [user]', 'help': 'See info about what level you need to be in order to speak in a voice chat.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['img', 'images'], 'name': ';images [user]', 'help': 'See info about what level you need to be in order to send images/videos/gifs in general and other channels.', 'hasChild': False, 'devOnly': False, 'staffOnly': False},
				{'_name': ['untill-partner', 'up'], 'name': '![untill-partner|up]', 'help': 'See how many members the server needs untill it\'s eligible for applying for the discord partnership program.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['membercount'], 'name': '!membercount', 'help': 'See how many members ViHill Corner has (`bots are not included`).', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['botinfo'], 'name': '!botinfo', 'help': 'See info about <@!751724369683677275>.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['uptime'], 'name': '!uptime', 'help': 'Check the bot\'s uptime.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['ping'], 'name': '!ping', 'help': 'Check the bot\'s ping.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['serverad', 'ad'], 'name': '![serverad|ad]', 'help': 'Get the server\'s advertising text.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['rawad', 'ra'], 'name': '![rawad|ra]', 'help': 'Get the server\'s advertising text in raw format.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['serverinfo', 'si'], 'name': '![serverinfo|si]', 'help': 'Get some info about the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['vote'], 'name': '!vote', 'help': 'Vote for the server on top.gg', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['update', 'updates'], 'name': '!update', 'help': 'Shows the latest update and what new features have been brought to the bot.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}
				]
		
		self.utilityCommands = [
				{'_name': ['ee', 'enlargeemoji', 'emoji'], 'name': '!ee', 'help': 'Enlarges the chosen emote.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['nick', 'nickname'], 'name': '!nick <newnickname>', 'help': 'Change your nickname.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['profile', 'user'], 'name': '!profile [user]', 'help': 'Get a user\'s discord profile info.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['avatar', 'av'], 'name': '![avatar|av] [user]', 'help': 'See user\'s avatar.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['invite', 'inv'], 'name': '![invite|inv]', 'help': 'Get the invite link for the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['suggest', 'suggests'], 'name': '!suggest <suggestion>', 'help': 'Make a suggestion in <#858997857968193596>', 'hasChild': False, 'devOnly': False, 'staffOnly': False},
				{'_name': ['snipe'], 'name': '!snipe [channel]', 'help': 'Snipe the last deleted message in the channel.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['nsfw'], 'name': '!nsfw <category>', 'help': 'For nsfw categories type **!nsfw** in the nsfw channel. For more info about how to get access to the nsfw channel please type **!help nsfw**', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['google'], 'name': '!google <query>', 'help': 'Search for something on google.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['calculate', 'calc'], 'name': '![calculate|calc] <operation>', 'help': 'Basic calculator for basic operations.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['scrs', 'ss'], 'name': '![scrs|ss] <website>', 'help': 'Take a scren shot of a domain.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['rank', 'lvl'], 'name': '![rank|lvl] [user]', 'help': 'Check user\'s current level.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['rtfd', 'rtfm'], 'name': '![rtfd|rtfm] <obj>', 'help': 'Gives you a documentation link for a discord.py entity.', 'hasChild': True, 'devOnly': False, 'staffOnly': False},
				{'_name': ['source'], 'name': '!source <command>', 'help': 'Displays my full source code or for a specific command.\n\nTo display the source code of a subcommand you can separate it by periods, e.g. tag.create for the create subcommand of the tag command or by spaces.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}
				]
		
		self.miscCommands = [
				{'_name': ['created'], 'name': '!created [user]', 'help': 'See when a user created their account.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['joined'], 'name': '!joined [user]', 'help': 'See when a user joined the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['waifu'], 'name': '!waifu', 'help': 'Get a random waifu pic.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['spotify'], 'name': '!spotify [user]', 'help': 'Shows what song the user is listening to, the artist & the album.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['dev-portal', 'dev', 'portal'], 'name': '!dev-portal', 'help': 'Get the link to dev-portal website.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['perm-calc', 'perm'], 'name': '!perm-calc', 'help': 'Get the link to bots perm-calc website.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['vampify'], 'name': '!vampify <text>', 'help': 'Vampify your text.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['clapify'], 'name': '!clapify <text>', 'help': 'Clapify your text.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['role-id', 'roleid'], 'name': '!role-id <role_name>', 'help': 'Get the ID of the given role.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['reminder', 'remind'], 'name': '![reminder|remind] <when> [what]', 'help': 'Set a reminder.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['msg-top', 'top'], 'name': '![msg-top|top]', 'help': 'See top 15 most active members.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['randomnumber', 'rn'], 'name': '![randomnumber|rn] <nr1> <nr2> <nr3>', 'help': '', 'help1': 'Get a random number depending on the amount of numbers you give. For more info please type **!help randomnumber**', 'help2': 'If you don\'t provide any number, the bot will give a random number between `0` and the `largest positive integer supported by the machine`.\n\nIf you provide only one number, then the bot will give a random number between `0` and `your chosen number (num1)`.\n\nIf you provide two numbers only, then the bot will give you a random number between `your first number (num1)` and `your second number (num2)`.\n\nIf you provide all three numbers, then the bot will give a random number between `your first number (num1)` and `your second number (num2)`, that is not `your third number (num3)`, this can be used if you want a random number between 2 numbers that is not a specific one, here\'s some examples:\n• `10 15 13 - will give a number between 10 and 15 that is not 13`\n• `0 10 5 - will give a number between 0 and 10 that is not 5`\n• `20 100 50 - will give a number between 20 and 100 that is not 50`\n• `10 20 15 - will give a number between 10 and 20 that is not 15`', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['multiplier'], 'name': '!multiplier', 'help': 'Shows the multipliers for the next groups: **Staff/Mods**, **Server Boosters**, **Members**.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}
				]
		
		self.featuredCommands = [
				{'_name': ['birthday', 'bday'], 'name': '!birthday [user]', 'help': 'See when someone\'s birthday is if they have it set.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['intro'], 'name': '!intro', 'help': 'Create or edit your intro.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['whois', 'wi'], 'name': '!whois [user]', 'help': 'Check user\'s intro.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['reclist'], 'name': '!reclist [user]', 'help': 'Check user\'s recommendations list.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['cr'], 'name': '!cr', 'help': 'For more information about this command please see **!help cr**', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['marry', 'marriedwho', 'divorce'], 'name': '!marry <user>', 'help': 'Marry the mentioned user.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['scrs', 'ss'], 'name': '![scrs|ss] <website>', 'help': 'Take a screenshot of a website.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['tag', 'tags'], 'name': '!tag <tag_name>', 'help': 'Get the content of the tag.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['snippets', 'snippet'], 'name': '![snippet|snippets]', 'help': 'Get a list with all the snippets.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['bdsm'], 'name': '!bdsm', 'help': 'For more information please type **!help bdsm**', 'hasChild': True, 'devOnly': False, 'staffOnly': False},
				{'_name': ['todo'], 'name': '!todo <todo>', 'help': 'Add to your todo list.', 'hasChild': True, 'devOnly': False, 'staffOnly': False}
				]
		
		self.moderatorCommands = [
				{'_name': ['ban'], 'name': '!ban', 'help': 'Ban an user from the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['unban'], 'name': '!unban', 'help': 'Unban an user.\n*Only works in the ban appeal server.*', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['idban'], 'name': '!idban <id>', 'help': 'Ban someone that is not in the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['idunban'], 'name': '!idunban <id>', 'help': 'Unban someone that is not in the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': True},
				{'_name': ['kick'], 'name': '!kick', 'help': 'Kick an user from the server.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['mute'], 'name': '!mute', 'help': 'Mutes an user.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['unmute'], 'name': '!unmute', 'help': 'Unmutes an user.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['tempmute'], 'name': '!tempmute <user> <time>', 'help': 'Mute an user temporarily.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['clear'], 'name': '!clear <amount>', 'help': 'Delete the amount of messages in the channel you are in.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}, 
				{'_name': ['slowmode'], 'name': '!slowmode <how_much>', 'help': 'Set the slowmode for the channel you are in.', 'hasChild': False, 'devOnly': False, 'staffOnly': True}
				]
		
		self.developerCommands = [
				{'_name': ['eval', 'e'], 'name': '!eval <code>', 'help': 'Evaluate some code.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['load'], 'name': '!load cogs.<cog_name>', 'help': 'Loads the cog.', 'hasChild': True, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['unload'], 'name': '!unload cogs.<cog_name>', 'help': 'Unloads the cog.', 'hasChild': True, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['reload'], 'name': '!reload cogs.<cog_name>', 'help': 'Reloads the cog.', 'hasChild': True, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['modmute'], 'name': '!modmute <mod_user>', 'help': 'Mutes a mod.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['modunmute'], 'name': '!modunmute <mod_user>', 'help': 'Unmutes a mod.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['makemod'], 'name': '!makemod <user>', 'help': 'Make someone a mod.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['removemod'], 'name': '!removemod <mod_user>', 'help': 'Remove a mod.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['shutdown'], 'name': '!shutdown', 'help': 'Shut the bot down.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['restart'], 'name': '!restart', 'help': 'Restart the bot.', 'hasChild': False, 'devOnly': False, 'staffOnly': False}, 
				{'_name': ['status', 'statuses'], 'name': '!status', 'help': 'Shows what kind of different statuses you can apply to the bot.', 'hasChild': True, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['metrics'], 'name': '!metrics', 'help': 'Get info about the metrics.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}, 
				{'_name': ['mail'], 'name': '!mail <user> <message>', 'help': 'Dm the user the given message.', 'hasChild': False, 'devOnly': True, 'staffOnly': False}
				]

		self.childCommands = [
				{'Parent': 'balance', 'name': '!bal add-wallet <amount> [user]', 'help': 'Add money to an user\'s wallet.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'balance', 'name': '!bal add-bank <amount> [user]', 'help': 'Add money to an user\'s bank.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'balance', 'name': '!bal set-wallet <amount> [user]', 'help': 'Set user\'s wallet money.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'balance', 'name': '!bal set-bank <amount> [user]', 'help': 'Set user\'s bank money.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'balance', 'name': '!bal reset [user]', 'help': 'Reset user\'s balance.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'trivia', 'name': '!trivia points <user>', 'help': 'See how many points you, or someone else has.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'trivia', 'name': '!trivia points gift <amount> <user>', 'help': 'Gift some of your points to someone.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'trivia', 'name': '!trivia leaderboard', 'help': 'check the leaderboard and see the top **10** users that have the most points.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'trivia', 'name': '!trivia points set <amount> [user]', 'help': 'Set the amount of trivia points for an user.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'trivia', 'name': '!trivia points add <amount> [user]', 'help': 'Add trivia points to an user.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'trivia', 'name': '!trivia points reset <user>', 'help': 'Reset the trivia points of an user.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'nick', 'name': '!nick [remove|reset]', 'help': 'Remove your nickname.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'nsfw', 'name': '!nsfw me add', 'help': 'Add yourself the permission to view the nsfw channel.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'nsfw', 'name': '!nsfw me remove', 'help': 'Remove your permissions of viewing the nsfw channel.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'nsfw', 'name': '!nsfw block <user>', 'help': 'Block the user from using the nsfw channel.', 'devOnly': False, 'staffOnly': True}, 
				{'Parent': 'nsfw', 'name': '!nsfw unblock <user>', 'help': 'Unblock the user from using the nsfw channnel and let them use it again.', 'devOnly': False, 'staffOnly': True}, 
				{'Parent': 'nsfw', 'name': '!nsfw blocks', 'help': 'See all the nsfw blocked users that do not have access in the nsfw channel.', 'devOnly': False, 'staffOnly': True}, 
				{'Parent': 'rank', 'name': '!rank [leaderboard|top]', 'help': 'See top `10` highest level members.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'rank', 'name': '!rank set <lvl> [user]', 'help': 'Set the level for the user.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'rtfm', 'name': '!rtfm [master|2.0]', 'help': 'Gives you a documentation link for a discord.py master entity.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'rtfm', 'name': '!rtfm [py|python]', 'help': 'Gives you a documentation link for a python entity.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'remind', 'name': '!reminder list', 'help': 'Get a list of your 10 upcoming reminders.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'remind', 'name': '!reminder [cancel|remove|delete] <remindID>', 'help': 'Delete your reminder by its ID.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'remind', 'name': '!reminder clear', 'help': 'Clear all your reminders.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'top', 'name': '!msg-top rewards', 'help': 'See the rewards for the weekly top.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'top', 'name': '!msg-top reset <user>', 'help': 'Reset a user\'s weekly messages count', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'multiplier', 'name': '!multiplier set <group> <multiplier>', 'help': 'Groups:\n\u2800\u2800\u2800\u2800 • **Mod/Staff**\n\u2800\u2800\u2800\u2800 • **Boosters**\n\u2800\u2800\u2800\u2800 • **Members**\n\u2800\u2800\u2800\u2800 • **Kraots**\n\u2800\u2800\u2800\u2800 • **all** - to set for every group', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'multiplier', 'name': '!multiplier reset <group>', 'help': 'Groups:\n\u2800\u2800\u2800\u2800 • **Mod/Staff**\n\u2800\u2800\u2800\u2800 • **Boosters**\n\u2800\u2800\u2800\u2800 • **Members**\n\u2800\u2800\u2800\u2800 • **Kraots**\n\u2800\u2800\u2800\u2800 • **all** - to set for every group', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'birthday', 'name': '!birthday set <month/day>', 'help': 'Set up your birthday.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'birthday', 'name': '!birthday [delete|remove]', 'help': 'Delete your birthday.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'birthday', 'name': '!birthday [upcoming|top]', 'help': 'Get the next `5` upcoming birthdays.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'intro', 'name': '!intro [remove|delete]', 'help': 'Delete your intro.', 'devOnly': False, 'staffOnly': False},  
				{'Parent': 'reclist', 'name': '!reclist set <recommendations>', 'help': 'Set up your reclist.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'reclist', 'name': '!reclist add <recommendations>', 'help': 'Add recommendations up your reclist.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'reclist', 'name': '!reclist delete <index>', 'help': 'Delete the recommendation at the given index.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'reclist', 'name': '!reclist clear', 'help': 'Clear all your reclist, thus deleting it.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'reclist', 'name': '!reclist remove <user>', 'help': 'Remove a user\'s reclist from the database.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr create', 'help': 'Create your cr.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr delete', 'help': 'Delete your cr.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr edit color <new_color>', 'help': 'Edit your cr\'s color', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr edit name <new_name>', 'help': 'Edit your cr\'s name.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr share <user>', 'help': 'Get some info about a cr.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr info <cr_id>', 'help': 'Share your cr with someone.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr unrole <cr_id>', 'help': 'Remove a cr from your profile. To get the cr\'s ID type: `!role-id <role_name>`', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'cr', 'name': '!cr clean', 'help': 'Remove all cr\'s that you don\'t own from your profile.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag [create|make|add] <tag_name>', 'help': 'Create a new tag!', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag delete <tag_name>', 'help': 'Delete a tag that you made.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag alias <tag_name>', 'help': 'See all the aliases a tag has.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag alias create <tag_name>', 'help': 'Create an alias for a tag that you own.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag alias delete <tag_name>', 'help': 'Delete an alias from a tag that you own.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag info <tag_name>', 'help': 'See info about a tag.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag all', 'help': 'Get paginated list with all tags.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag list [user]', 'help': 'Get paginated list with all tags that a user owns.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag search <query>', 'help': 'Search for tags with the given query.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag [leaderboard|lb]', 'help': 'See top `10` most used tags!', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'tag', 'name': '!tag remove <tag_name>', 'help': 'Remove a tag from the database.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'snippets', 'name': '!snippet [create|make|add] <snippet_name>', 'help': 'Create a new snippet.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'snippets', 'name': '!snippet delete <snippet_name>', 'help': 'Delete a snippet you own.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'snippets', 'name': '!snippet list [user]', 'help': 'Get a paginated list of snippets that a user owns.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'snippets', 'name': '!snippet search <query>', 'help': 'Search for snippets containing the given query.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'snippets', 'name': '!snippet leaderboard', 'help': 'See top `10` most used snippets!', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'snippets', 'name': '!snippet remove <snippet_name>', 'help': 'Remove a snippet from the database.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'bdsm', 'name': '!bdsm set', 'help': 'Set your bdsm result by sending the screenshot of your results.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'bdsm', 'name': '!bdsm results [member]', 'help': 'Send the bdsm results of the specified member.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'bdsm', 'name': '!bdsm remove', 'help': 'Remove your bdsm results.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'bdsm', 'name': '!bdsm test', 'help': 'Get a link to the bdsm test webpage.', 'devOnly': False, 'staffOnly': False}, 
				{'Parent': 'load', 'name': '!load all', 'help': 'Loads all the cogs.', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'unload', 'name': '!unload all', 'help': 'Unloads all the cogs', 'devOnly': True, 'staffOnly': False}, 
				{'Parent': 'reload', 'name': '!reload all', 'help': 'Reloads all the cogs.', 'devOnly': True, 'staffOnly': False},
				{'Parent': 'marry', 'name': '!marriedwho [user]', 'help': 'See who the user is married with.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'marry', 'name': '!divorce', 'help': 'Divorce the person you\'re married with.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'update', 'name': '!update set <args>', 'help': 'Set the new update.', 'devOnly': True, 'staffOnly': False},
				{'Parent': 'todo', 'name': '!todo add <todo>', 'help': 'Same as `!todo <todo>`, adds to your todo list.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'todo', 'name': '!todo list', 'help': 'See your todo list. Each index is a hyperlink meaning that if you click on it you will be taken to the message where you have added that todo in your list.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'todo', 'name': '!todo [delete|remove] <index>', 'help': 'Delete|Remove a todo from your list using the index.', 'devOnly': False, 'staffOnly': False},
				{'Parent': 'todo', 'name': '!todo clear', 'help': 'Delete your todo list.', 'devOnly': False, 'staffOnly': False}
				]

		self.allCommands = self.featuredCommands + self.ecoCommands + self.funCommands + self.warnCommands + self.infoCommands + self.utilityCommands + self.miscCommands + self.moderatorCommands + self.developerCommands

	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def help(self, ctx, get_command : str = None):
		if get_command is None:
				# General help
			_categs = categs
			if "Staff" in [role.name for role in ctx.author.roles] or ctx.author.id == 374622847672254466:
				_categs = f"<:banhammer:859065173352644628> -> **Moderator**{categs}"
			if ctx.author.id == 374622847672254466:
				_categs = f"<:verifiedbotdev:859064715715018782> -> **Developer**\n<:banhammer:859065173352644628> -> **Moderator**{categs}"
			em = discord.Embed(color=color.lightpink, title="Here's the help.", description="```diff\n- [] = optional argument\n- <> = required argument\n- do NOT type these when using commands!\n+ Type !help [command|category] for more help on a command or a category!```")
			em.set_thumbnail(url=self.bot.user.avatar_url)
			em.add_field(name="React with the reactions specific to the category you wish to see.", 
			value=_categs)
			msg = await ctx.send(embed=em)
			
			if ctx.author.id == 374622847672254466:
				await msg.add_reaction("<:verifiedbotdev:859064715715018782>")
				await msg.add_reaction("<:banhammer:859065173352644628>")
			elif "Staff" in [role.name for role in ctx.author.roles]:
				await msg.add_reaction("<:banhammer:859065173352644628>")
			await msg.add_reaction("<:SakataNom:787370388250034186>")
			await msg.add_reaction("<:CutieUmwha:787370264165482537>")
			await msg.add_reaction("<:vampy1:859050561184989204>")
			await msg.add_reaction("<:epik:818803400154153002>")
			await msg.add_reaction("<:pepecry:859050982507675699>")
			await msg.add_reaction("<:pepe_hang1:859050982402687026>")
			await msg.add_reaction("<:creepy_bird1:859050982382108693>")

			def check(reaction, user):
				if ctx.author.id == 374622847672254466:
					return str(reaction.emoji) in ['<:verifiedbotdev:859064715715018782>' ,'<:banhammer:859065173352644628>', '<:SakataNom:787370388250034186>', '<:CutieUmwha:787370264165482537>', '<:vampy1:859050561184989204>', '<:epik:818803400154153002>', '<:pepecry:859050982507675699>', '<:pepe_hang1:859050982402687026>', '<:creepy_bird1:859050982382108693>'] and user.id == ctx.author.id
				elif "Staff" in [role.name for role in ctx.author.roles]:
					return str(reaction.emoji) in ['<:banhammer:859065173352644628>, <:SakataNom:787370388250034186>', '<:CutieUmwha:787370264165482537>', '<:vampy1:859050561184989204>', '<:epik:818803400154153002>', '<:pepecry:859050982507675699>', '<:pepe_hang1:859050982402687026>', '<:creepy_bird1:859050982382108693>'] and user.id == ctx.author.id
				else:
					return str(reaction.emoji) in ['<:SakataNom:787370388250034186>', '<:CutieUmwha:787370264165482537>', '<:vampy1:859050561184989204>', '<:epik:818803400154153002>', '<:pepecry:859050982507675699>', '<:pepe_hang1:859050982402687026>', '<:creepy_bird1:859050982382108693>'] and user.id == ctx.author.id

			try:
				reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=35)
			except asyncio.TimeoutError:
				await msg.clear_reactions()
				return
			else:
				try:
					get_command = reactions[str(reaction.emoji)]
					command = self.bot.get_command(get_command)
					await ctx.invoke(command)
					await msg.delete()
				except Exception as e:
					await ctx.send(e)

			return
		
			# Help for a command

		command = get_command.lower()
		found = False
		for i in range(len(self.allCommands)):
			if command in self.allCommands[i]['_name']:
				found = True
				if self.allCommands[i]['hasChild'] == True:
					childList = []
					for e in range(len(self.childCommands)):
						if self.childCommands[e]['Parent'] in self.allCommands[i]['_name']:
							if self.childCommands[e]['staffOnly'] == True:
								if "Staff" in [role.name for role in ctx.author.roles]:
									childList.append(self.childCommands[e])
							elif self.childCommands[e]['devOnly'] == True:
								if ctx.author.id == 374622847672254466:
									childList.append(self.childCommands[e])
							else:
								childList.append(self.childCommands[e])
					try:
						self.allCommands[i]['help'] = f"{self.allCommands[i]['help1']}{self.allCommands[i]['help2']}"
					except KeyError:
						pass
					entries = [self.allCommands[i]] + childList
					p = HelpPages(entries=entries, per_page=3, title=f"Here's help for command `{self.allCommands[i]['_name'][0]}`:", color=color.lightpink)
					await p.start(ctx)
					return
				
				if self.allCommands[i]['staffOnly'] == True:
					if not "Staff" in [role.name for role in ctx.author.roles]:
							return
				elif self.allCommands[i]['devOnly'] == True:
					if ctx.author.id != 374622847672254466:
						return
				try:
					self.allCommands[i]['help'] = f"{self.allCommands[i]['help1']}{self.allCommands[i]['help2']}"
				except KeyError:
					pass
				entries = [self.allCommands[i]]
				p = HelpPages(entries=entries, per_page=3, title=f"Here's help for command `{self.allCommands[i]['_name'][0]}`:", color=color.lightpink)
				await p.start(ctx)
				return
		
		if found == False:
			return await ctx.reply("Command not found! Type `!help` for a list of commands.")

	@help.command(aliases=['eco'])
	async def economy(self, ctx):
		for i in range(len(self.ecoCommands)):
			try:
				self.ecoCommands[i]['help'] = self.ecoCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.ecoCommands, per_page=5, color=color.lightpink, title="Here are all the `Economy` commands:")
		await p.start(ctx)
	
	@help.command()
	async def fun(self, ctx):
		for i in range(len(self.funCommands)):
			try:
				self.funCommands[i]['help'] = self.funCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.funCommands, per_page=5, color=color.lightpink, title="Here are all the `Fun` commands:")
		await p.start(ctx)
	
	@help.command(aliases=['warnings', 'warns'])
	async def warn(self, ctx):
		for i in range(len(self.warnCommands)):
			try:
				self.warnCommands[i]['help'] = self.warnCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.warnCommands, per_page=3, color=color.lightpink, title="Here are all the `Warn` commands:")
		await p.start(ctx)

	@help.command(aliases=['information', 'informative'])
	async def info(self, ctx):
		for i in range(len(self.infoCommands)):
			try:
				self.infoCommands[i]['help'] = self.infoCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.infoCommands, per_page=4, color=color.lightpink, title="Here are all the `Infomative` commands:")
		await p.start(ctx)
	
	@help.command(aliases=['utilities', 'util', 'utils'])
	async def utility(self, ctx):
		for i in range(len(self.utilityCommands)):
			try:
				self.utilityCommands[i]['help'] = self.utilityCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.utilityCommands, per_page=5, color=color.lightpink, title="Here are all the `Utility` commands:")
		await p.start(ctx)
	
	@help.command(aliases=['miscellaneous'])
	async def misc(self, ctx):
		for i in range(len(self.miscCommands)):
			try:
				self.miscCommands[i]['help'] = self.ecoCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.miscCommands, per_page=5, color=color.lightpink, title="Here are all the `Miscellaneous` commands:")
		await p.start(ctx)
	
	@help.command(aliases=['feature', 'features'])
	async def featured(self, ctx):
		for i in range(len(self.featuredCommands)):
			try:
				self.featuredCommands[i]['help'] = self.featuredCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.featuredCommands, per_page=5, color=color.lightpink, title="Here are all the `Featured` commands:")
		await p.start(ctx)
	
	@help.command(aliases=['dev'])
	@commands.is_owner()
	async def developer(self, ctx):
		for i in range(len(self.developerCommands)):
			try:
				self.developerCommands[i]['help'] = self.developerCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.developerCommands, per_page=4, color=color.lightpink, title="Here are all the `Developer` commands:")
		await p.start(ctx)
	
	@help.command(aliases=['mod', 'admin'])
	@commands.has_role('Staff')
	async def moderator(self, ctx):
		for i in range(len(self.moderatorCommands)):
			try:
				self.moderatorCommands[i]['help'] = self.moderatorCommands[i]['help1']
			except KeyError:
				pass
		p = HelpPages(entries=self.moderatorCommands, per_page=5, color=color.lightpink, title="Here are all the `Moderator` commands:")
		await p.start(ctx)
		


def setup(bot):
	bot.add_cog(Help(bot))