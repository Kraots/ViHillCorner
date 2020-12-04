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
        helpEm.add_field(name="Commands", value="`revive`, `ee`, `nick`, `profile`, `created`, `joined`, `av`, `waifu`, `invite`, `ad`, `suggest`, `spotify`, `meme`, `cat`, `dog`, `snipe`, `nsfw`, `calc`, `topic`, `gayrate`, `straightrate` , `simprate`")
        helpEm.add_field(name="Info Commands", value="`untill-partner`, `membercount`, `level`, `rank`, `sfw`, `botinfo`, `uptime`, `ping`, `serverad`, `rawad`, `snippets`, `actions`, `serverinfo`", inline=False)
        if "Staff" in [role.name for role in ctx.message.author.roles]:
            helpEm.add_field(name="Moderator Commands", value="`clear`, `mute`, `massmute`, `tempmute`, `unmute`, `massunmute`, `kick`, `masskick`, `ban`, `massban`, `unban`, `massunban`, `partnership`, `nsfw`, `slowmode`", inline=False)
        
        if ctx.author.id == 374622847672254466:
            helpEm.add_field(name="Dev Commands", value="`load`, `unload`, `reload`, `reload-all`, `unload-all`, `load-all`, `modmute`, `modunmute`, `makemod`, `removemod`, `shutdown`, `restart`, `jsk`, `statuses`, `metrics`, `mail`", inline=False)

        await ctx.message.channel.send(embed=helpEm)

    @help.command()
    async def gayrate(self, ctx):
        embed = discord.Embed(description='Usage: `!gayrate [user]`', color=color.lightpink)
        await ctx.send(embed=embed)

    @help.command()
    async def straightrate(self, ctx):
        embed = discord.Embed(description='Usage: `!straightrate [user]`', color=color.lightpink)
        await ctx.send(embed=embed)

    @help.command()
    async def simprate(self, ctx):
        embed = discord.Embed(description='Usage: `!simprate [user]`', color=color.lightpink)
        await ctx.send(embed=embed)

    @help.command()
    async def revive(self, ctx):
        revive = discord.Embed(description="Usage: `!revive`!\n\nPings everyone with the chat revive role.\n*Cooldown of 2h after each use.*", color=color.lightpink)
        await ctx.message.channel.send(embed=revive)

    @help.command()
    async def ee(self, ctx):
        ee = discord.Embed(description="Usage: `!ee <emote>`\n\nEnlarges the chosen emote.", color=color.lightpink)
        await ctx.message.channel.send(embed=ee)

    @help.command()
    async def nick(self, ctx):
        nick = discord.Embed(description="Usage: `!nick <newnickname>`\n\nChanges your nickanme.\nType `!nick off/remove` to remove your nickname!\n\n*Requires you to be at least level 3.*", color=color.lightpink)
        await ctx.message.channel.send(embed=nick)

    @help.command()
    async def snippets(self, ctx):
        snippets = discord.Embed(description="Usage: `!snippets`\n\nSee the list of all snippets.", color=color.lightpink)
        await ctx.message.channel.send(embed=snippets)

    @help.command()
    async def profile(self, ctx):
        profile = discord.Embed(description="Usage: `!profile <user>`\n\nGet a user's profile info.", color=color.lightpink)
        await ctx.channel.send(embed=profile)

    @help.command()
    async def created(self, ctx):
        created = discord.Embed(description="Usage: `!created <user>`\n\nSee when the user joined discord / created their account.", color=color.lightpink)
        await ctx.channel.send(embed=created)

    @help.command()
    async def joined(self, ctx):
        joined = discord.Embed(description="Usage: `!joined <user>`\n\nSee when the user joined the server.", color=color.lightpink)
        await ctx.channel.send(embed=joined)

    @help.command(aliases=["avatar"])
    async def av(self, ctx):
        av = discord.Embed(description="Usage: `!av <user>`\n\nSee a user's avatar.", color=color.lightpink)
        await ctx.channel.send(embed=av)

    @help.command(aliases=["server", "si", "sinfo"])
    async def serverinfo(self, ctx):
        serverinfo = discord.Embed(description="Usage: `!serverinfo`\nAliases: `server`, `sinfo`, `si`\n\nGet some info about the server.", color=color.lightpink)
        await ctx.channel.send(embed=serverinfo)

    @help.command()
    async def actions(self, ctx):
        actions = discord.Embed(description="Usage: `!actions`\n\nSee a list of all actions.", color=color.lightpink)
        await ctx.channel.send(embed=actions)

    @help.command()
    async def waifu(self, ctx):
        waifu = discord.Embed(description="Usage: `!waifu`\n\nGet a random waifu pic.", color=color.lightpink)
        await ctx.channel.send(embed=waifu)

    @help.command(aliases=["inv"])
    async def invite(self, ctx):
        invite = discord.Embed(description="Usage: `!invite`\n\nGet the server invite.", color=color.lightpink)
        await ctx.channel.send(embed=invite)

    @help.command()
    async def ad(self, ctx):
        embed = discord.Embed(description="Usage: `!ad {your ad}`\n\nAdvertise your server in the advertisement channel ;3\nUse only in <#750160851822182486> or <#750160851822182487>", color=color.lightpink)
        await ctx.channel.send(embed=embed)

    @help.command()
    async def serverad(self, ctx):
        ad = discord.Embed(description="Usage: `!serverad`\n\nGet the server's advertising text.", color=color.lightpink)
        await ctx.channel.send(embed=ad)

    @help.command()
    async def rawad(self, ctx):
        rawad = discord.Embed(description="Usage: `!rawad`\n\nGet the server's advertising text in raw format.", color=color.lightpink)
        await ctx.channel.send(embed=rawad)

    @help.command(aliases=["untill-partner"])
    async  def up(self, ctx):
        up = discord.Embed(description="Usage: `!untill-partner`\n\nSee how many members the server needs untill it's eligible for applying for the discord partnership program.", color=color.lightpink)
        await ctx.channel.send(embed=up)

    @help.command()
    async def level(self, ctx):
        level = discord.Embed(description="Usage: `!level <user>`\n\nSee how to check your current level.\n*This is not the command to check your level, it's just a help command to show u/others how to check your level.*\n*Requires at least level*   **10**  *in order to use the command.*", color=color.lightpink)
        await ctx.channel.send(embed=level)

    @help.command()
    async def rank(self, ctx):
        level = discord.Embed(description="Usage: `!rank <user>`\n\nSee how to check your current level.\n*This is not the command to check your level, it's just a help command to show u/others how to check your level.*\n*Requires at least level*  **10**  *in order to use the command.*", color=color.lightpink)
        await ctx.channel.send(embed=level)

    @help.command()
    async def sfw(self, ctx):
        sfw = discord.Embed(description="Usage: `!sfw <user>`\n\nWarn a user to keep the chat appropriate and sfw.\n\n*Requires at least level*  **10**  *in order to use the command.*", color=color.lightpink)
        await ctx.channel.send(embed=sfw)

    @help.command()
    async def botinfo(self, ctx):
        botinfo = discord.Embed(description="Usage: `!botinfo`\n\nSee info about <@!751724369683677275>.", color=color.lightpink)
        await ctx.channel.send(embed=botinfo)

    @help.command()
    async def uptime(self, ctx):
        uptime = discord.Embed(description="Usage: `!uptime`\n\nCheck the bot's uptime.", color=color.lightpink)
        await ctx.channel.send(embed=uptime)

    @help.command()
    async def ping(self, ctx):
        ping = discord.Embed(description="Usage: `!ping`\n\nCheck the bot's ping.", color=color.lightpink)
        await ctx.channel.send(embed=ping)

    @help.command()
    @commands.has_role("Staff")
    async def clear(self, ctx):
        clear = discord.Embed(description="Usage: `!clear <amount>`\n\nClear's the chat of the amount of messages given.", color=color.lightpink)
        await ctx.channel.send(embed=clear)

    @help.command()
    @commands.has_role("Staff")
    async def mute(self, ctx):
        mute = discord.Embed(description="Usage: `!mute <user> <reason>`\n\nThis command mutes the user permanently untill a moderator unmutes him.", color=color.lightpink)
        await ctx.channel.send(embed=mute)

    @help.command()
    @commands.has_role("Staff")
    async def massmute(self, ctx):
        mute = discord.Embed(description="Usage: `!mute {user1} {user2} {user3} {reason}`\n\nThis command mutes the users permanently untill a moderator unmutes him.", color=color.lightpink)
        await ctx.channel.send(embed=mute)

    @help.command()
    @commands.has_role("Staff")
    async def tempmute(self, ctx):
        tempmute = discord.Embed(description="Usage: `!tempmute <user> <time>`\n**.tempmute @BananaBoy69 1 s|m|h|d**\n s - second\n m - minute\n h - hour\n d - day\n\nTempmutes a user with the  given time.\n**DO NOT GO ABOVE 24H**", color=color.lightpink)
        await ctx.channel.send(embed=tempmute)

    @help.command()
    @commands.has_role("Staff")
    async def unmute(self, ctx):
        unmute = discord.Embed(description="Usage: `!unmute <user>`\n\nUnmutes the user.", color=color.lightpink)
        await ctx.channel.send(embed=unmute)

    @help.command()
    @commands.has_role("Staff")
    async def massunmute(self, ctx):
        unmute = discord.Embed(description="Usage: `!massunmute {user1} {user2} {user3}`\n\nUnmutes the users.", color=color.lightpink)
        await ctx.channel.send(embed=unmute)
    
    @help.command()
    @commands.has_role('Staff')
    async def kick(self, ctx):
        kick = discord.Embed(description="Usage: `!kick {user} {reason}`\n\nKicks an user from the server!", color=color.lightpink)
        await ctx.send(embed=kick)

    @help.command()
    @commands.has_role('Staff')
    async def masskick(self, ctx):
        kick = discord.Embed(description="Usage: `!masskick {user1} {user2} {user3} {reason}`\n\nKicks the users from the server!", color=color.lightpink)
        await ctx.send(embed=kick)

    @help.command()
    @commands.has_role("Staff")
    async def ban(self, ctx):
        ban = discord.Embed(description="Usage: `!ban <user>`\n\nBans a user.", color=color.lightpink)
        await ctx.channel.send(embed=ban)

    @help.command()
    @commands.has_role("Staff")
    async def massban(self, ctx):
        ban = discord.Embed(description="Usage: `!ban {user1} {user2} {user3}`\n\nBans the users.", color=color.lightpink)
        await ctx.channel.send(embed=ban)

    @help.command()
    @commands.has_role("Staff")
    async def unban(self, ctx):
        unban = discord.Embed(description="Usage: `!unban <user>`\n\nThis command only works in the ban appeal server, if the user is in that server ;)).", color=color.lightpink)
        await ctx.channel.send(embed=unban)

    @help.command()
    @commands.has_role("Staff")
    async def massunban(self, ctx):
        unban = discord.Embed(description="Usage: `!unban {user1} {user2} {user3}`\n\nThis command only works in the ban appeal server, if the users are in that server ;)).", color=color.lightpink)
        await ctx.channel.send(embed=unban)

    @help.command()
    @commands.has_role("Staff")
    async def partnership(self, ctx):
        partnership = discord.Embed(description="Usage: `!partenrship <ad>`\n ad - the ad of the server that the partnership is made with.\n\n**USE IT ONLY IN <#750160851822182480>**", color=color.lightpink)
        await ctx.channel.send(embed=partnership)

    @help.command()
    async def suggest(self, ctx):
        suggest = discord.Embed(description="Usage: `!suggest <suggestion>` in <#750160851822182486> or <#750160851822182487>\n\nMake a suggestion in <#750160850593251454>\n*There is 1 minute cooldown between each suggestion per user.*", color=color.lightpink)
        await ctx.channel.send(embed=suggest)

    @help.command()
    async def spotify(self, ctx):
        spotify = discord.Embed(description="Usage: `!spotify`\n\nShow's what song you're listening to, the artist & the album.\n*You gotta have spotify as activity and no other custom activity in order for this command to work*", color=color.lightpink)
        await ctx.channel.send(embed=spotify)

    @help.command()
    async def membercount(self, ctx):
        membercount = discord.Embed(description="Usage: `!membercount`\n\nSee how many members Anime Hangouts has (**bots are not included**)", color=color.lightpink)
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
      meme = discord.Embed(color=color.lightpink, description="Usage: `!meme`\n\nSends a random meme! ;3")
      await ctx.channel.send(embed=meme)

    @help.command()
    async def cat(self, ctx):
      meme = discord.Embed(color=color.lightpink, description="Usage: `!cat`\n\nSends a random cat pic/vid! ;3")
      await ctx.channel.send(embed=meme)

    @help.command()
    async def dog(self, ctx):
      meme = discord.Embed(color=color.lightpink, description="Usage: `!dog`\n\nSends a random dog pic/vid! ;3")
      await ctx.channel.send(embed=meme)

    @help.command()
    @commands.check(Developer)
    async def mail(self, ctx):
      em = discord.Embed(description='Usage: `;;mail {member} {args}`\n To get the member, copy the ID and then put it in between `<@!ID>` by replacing the "ID" with the ID of the member you want the bot to dm.\n\n***Note that this command works in dms as well. ;))***')
      await ctx.send(embed=em)

    @help.command()
    async def snipe(self, ctx):
        em = discord.Embed(description='Usage: `!snipe`\n\nSnipe the last deleted message in the channel!', color=color.lightpink)
        await ctx.send(embed=em)

    @help.command()
    async def nsfw(self, ctx):
        if "Staff" in [role.name for role in ctx.message.author.roles]:

            em = discord.Embed(color=color.lightpink, description='Usage:\n `!nsfw add {user}` \n `!nsfw remove {user}`\n\nGive the user perms to see the nsfw channel or remove them!')
            await ctx.send(embed=em)

        else:

            em = discord.Embed(color=color.lightpink, description='Usage: `!nsfw yuri | hentai | tentacle`\nGet a random `yuri | hentai | tentacle` pic! **USE ONLY IN <#780374324598145055>**')
            await ctx.send(embed=em)

    @help.command()
    async def calc(self, ctx):
        embed = discord.Embed(color=color.lightpink, description='Usage:\n\n`!calc add {a} {b}`\n`!calc substract {a} {b}`\n`!calc multiply {a} {b}`\n`!calc divide {a} {b}`\n\n*WARNING: NUMBERS LIKE `2,3` OR `2.3` WILL NOT WORK! USE ONLY NUMBERS LIKE `2` OR `3`;;!*\n\nExample:\n\n`!calc divide 4 2` will result `2.0`\n`!calc divide 4.6 2.3` will result an error;;')
        await ctx.channel.send(embed=embed)

    @help.command()
    @commands.has_role('Staff')
    async def slowmode(self, ctx):
        embed = discord.Embed(color=color.lightpink, description="Usage: `!slowmode {time}`\n\nExample:\n\n`!slowmode 5h` => will set the slowmode to 5h\n`!slowmode 3s` => will change the slowmode to 3s\n`!slowmode off` => will disabled the slowmode\n\n*NOTE: ANY OTHER TIME THAT DOES NOT INCLUDE s |  h, or if it's a letter, then the slowmode will be disabled regardless*")
        await ctx.channel.send(embed=embed)

    @help.command()
    async def topic(self, ctx):
        embed = discord.Embed(color=color.lightpink, description='Usage: `!topic`\n\nGet a random topic to talk about, lolz.')
        await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.TooManyArguments):
          return



















def setup(client):
	client.add_cog(Help(client))
