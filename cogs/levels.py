import disnake
from disnake.ext import commands
import utils.colors as color
from utils.pillow import rank_card
from utils.paginator import RoboPages, FieldPageSource

bot_channel = (750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061, 787357561116426258)
no_talk_channels = (750160852006469807, 780374324598145055)
botsChannels = (750160851822182486, 750160851822182487)

# LEVEL: LEVEL_ROLE_ID
levels = {3: 758278459645755392, 5: 750160850290999330, 10: 750160850290999331, 15: 750160850290999332, 20: 750160850290999333, 25: 750160850290999334, 30: 750160850290999335, 40: 750160850295324744, 45: 750160850295324745, 50: 750160850295324746, 55: 750160850295324747, 60: 750160850295324748, 65: 750160850295324749, 69: 750160850295324750, 75: 788127504710762497, 80: 788127526278791240, 85: 788127540459208725, 90: 788127547606827028, 95: 788127552686129265, 100: 788127561283928115, 105: 788127569198579764, 110: 788127574663495720, 120: 788127580330655744, 130: 788127589092818994, 150: 788127593386868758, 155: 818562249349660713, 160: 818562250252091413, 165: 818562250477404173, 170: 818562251644076072, 175: 818562252185534465, 180: 818562252360777749, 185: 818562252906037259, 190: 818562253501628507, 195: 818562254043480075, 200: 818562254495547462, 205: 818562254680883241, 210: 818562255188131924, 215: 818562256101965844, 220: 818562256546824192, 230: 818562257033101372, 240: 818562257653858304, 250: 818562258119950367, 255: 818562258551832657, 260: 818562259587563523, 265: 818562260254588988, 270: 818562260686995486, 275: 818562261844230215, 280: 818562262360784977, 285: 818562262520430654, 290: 818562263169368076, 300: 818562263850025031, 305: 818562264030380033, 310: 818562264554405899, 315: 818562265422757898, 320: 818562265779273749, 330: 818562266475528242, 340: 818562266760740926, 350: 818562267410726964, 355: 818562267837628456, 360: 818562268044197889, 365: 818562268966027294, 370: 818562269029466124, 375: 818562269835034625, 380: 818562270119985163, 385: 818562270375182357, 390: 818562271100928020, 395: 818562271269486623, 400: 818562271978586132, 405: 818562272791101500, 410: 818562273202405396, 415: 818562273215774776, 420: 818562274318090260, 430: 818562274502508555, 440: 818562275539550239, 450: 818562276490870857, 455: 818562276939661343, 460: 818562277514805258, 465: 818562277619400765, 470: 818562278521569282, 475: 818562278832078939, 480: 818562279725203508, 485: 818562280009760889, 490: 818562280765390909, 495: 818562281410658344, 500: 818562282019356733}

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db2['Levels']
        self.prefix = "!"
    def cog_check(self, ctx):
        return ctx.prefix == self.prefix
    

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.guild:
            ch_id = message.channel.id
            if not ch_id in no_talk_channels:
                if not message.author.bot:
                    guild = self.bot.get_guild(750160850077089853)
                    stats = await self.db.find_one({"_id": message.author.id})
                    if stats is None:
                        newuser = {"_id": message.author.id, "xp": 0, "messages_count": 0, "weekly_messages_count": 0}
                        await self.db.insert_one(newuser)
                        return
                        
                    kraotsDocument = await self.db.find_one({'_id': 374622847672254466})
                    membersMultiplier = kraotsDocument['xp multiplier']
                    boostersMultiplier = kraotsDocument['booster xp multiplier']
                    modMultiplier = kraotsDocument['mod xp multiplier']
                    kraotsMultiplier = kraotsDocument['kraots xp multiplier']
                    
                    if not ch_id in botsChannels:
                        await self.db.update_one({"_id": message.author.id}, {"$inc": {"weekly_messages_count": 1}})
                    xp = stats['xp']
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp < 0:
                        lvl = lvl - 1
                        xp = stats['xp']
                        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if lvl >= 500:
                        return
                    
                    else:
                        if message.author.id == 374622847672254466:
                            xp = stats['xp'] + (30 * kraotsMultiplier)
                        elif 754676705741766757 in (role.id for role in message.author.roles):
                            xp = stats['xp'] + (20 * modMultiplier)
                        elif 759475712867565629 in (role.id for role in message.author.roles):
                            xp = stats['xp'] + (15 * boostersMultiplier)
                        else:
                            xp = stats['xp'] + (5 * membersMultiplier)

                        await self.db.update_one({"_id": message.author.id}, {"$set":{"xp": xp}})
                        lvl = 0
                        while True:
                            if xp < ((50*(lvl**2))+ (50*(lvl-1))):
                                break
                            lvl += 1
                        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                        if xp < 0:
                            lvl = lvl - 1
                            xp = stats['xp']
                            xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                        elif xp >= 0:
                            if message.guild.id == 750160850077089853:
                                try:
                                    role_id = levels[lvl]
                                    roles_id = [role.id for role in message.author.roles if not role.id in (levels[k] for k in levels)] + [role_id]
                                    newroles = []
                                    for role in roles_id:
                                        newrole = guild.get_role(role)
                                        newroles.append(newrole)
                                    await message.author.edit(roles=newroles)
                                except KeyError:
                                    role_id = 0
                                    for k in levels:
                                        if k < lvl:
                                            role_id = levels[k]
                                        else:
                                            break
                                    roles_id = [role.id for role in message.author.roles if not role.id in (levels[k] for k in levels)] + [role_id]
                                    newroles = []
                                    for role in roles_id:
                                        newrole = guild.get_role(role)
                                        newroles.append(newrole)
                                    await message.author.edit(roles=newroles)



    @commands.group(invoke_without_command = True, case_insensitive = True, aliases=['lvl', 'level'])
    async def rank(self, ctx, member: disnake.Member = None):
        """
        Check the member's level.
        This will send you a image with their data.
        """
        member = member or ctx.author

        if ctx.channel.id in bot_channel:
            stats = await self.db.find_one({"_id": member.id})
            if stats is None:
                if member.id == ctx.author.id:
                    await ctx.send("You haven't sent any messages, therefore you don't have a level.")
                    return
                elif member.bot:
                    await ctx.send("Bots do not have levels.")
                    return
                else:
                    await ctx.send(f"`{member.display_name}` did not send any messages, therefore they do not have any level.")
                    return
            else:
                xp = stats['xp']
                lvl = 0
                rank = 0
                while True:
                        if xp < ((50*(lvl**2))+ (50*(lvl-1))):
                            break
                        lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                rankings = await self.db.find().sort('xp', -1).to_list(100000)
                for data in rankings:
                    rank += 1
                    if stats['_id'] == data['_id']:
                        break
                
                if xp < 0:
                    lvl = lvl - 1
                    xp = stats['xp']
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))

                guild = self.bot.get_guild(750160850077089853)
                members_count = len([m for m in guild.members if not m.bot])
                
                if str(xp).endswith(".0"):
                    x = str(xp).replace(".0", "")
                    x = int(x)
                else:
                    x = int(xp)

                current_xp = x
                needed_xp = int(200*((1/2)*lvl))
                percent = round(float(current_xp * 100 / needed_xp), 2)

                f = await rank_card(member, lvl, rank, members_count, current_xp, needed_xp, percent)
                await ctx.send(file=f)


    @rank.command(name='set')
    @commands.is_owner()
    async def rank_set(self, ctx, lvl: int,  member: disnake.Member = None):
        """Set the rank for the member."""

        member = member or ctx.author

        xp = ((50*((lvl-1)**2))+(50*(lvl-1)))
        await self.db.update_one({"_id": member.id}, {"$set":{"xp": xp}})
        await ctx.send("Set level `{}` for **{}**.".format(lvl, member.display_name))



    @rank.command(name='leaderboard', aliases=['lb', 'top'])
    async def rank_leaderboard(self, ctx):
        """Leaderboard for levels."""

        if ctx.channel.id in bot_channel:
            top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
            data = []
            results = await self.db.find().sort([('xp', -1)]).to_list(100000)
            index = 0
            for result in results:
                xp = result['xp']
                user = result['_id']
                user = self.bot.get_user(user)

                lvl = 0
                while True:
                        if xp < ((50*(lvl**2))+ (50*(lvl-1))):
                            break
                        lvl += 1
                
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                
                if xp < 0:
                    lvl = lvl - 1
                    xp = result['xp']
                
                index += 1
                f = result['xp']
                if lvl == 500:
                    lvl = "500(MAX)"
                
                if str(f).endswith(".0"):
                    f = str(f).replace(".0", "")
                    f = int(f)
                else:
                    f = int(f)
                
                if index in (1, 2, 3):
                    place = top_3_emojis[index]
                else:
                    place = f'`#{index:,}`'
                if user == ctx.author:
                    to_append = (f"**{place} {user.name} (YOU)**", f"Level: `{lvl}`\nTotal XP: `{f:,}`")
                    data.append(to_append)
                else:
                    to_append = (f"{place} {user.name}", f"Level: `{lvl}`\nTotal XP: `{f:,}`")
                    data.append(to_append)
            
            source = FieldPageSource(data, per_page=10)
            source.embed.title = 'Rank top'
            pages = RoboPages(source, ctx=ctx)
            await pages.start()


    @commands.group(invoke_without_command = True, case_insensitive = True, aliases=['multipliers'])
    async def multiplier(self, ctx):
        """See the multipliers."""

        kraotsDocument = await self.db.find_one({'_id':374622847672254466})
        membersMultiplier = float(kraotsDocument['xp multiplier'])
        boostersMultiplier = float(kraotsDocument['booster xp multiplier'])
        modMultiplier = float(kraotsDocument['mod xp multiplier'])
        kraotsMultiplier = float(kraotsDocument['kraots xp multiplier'])

        em = disnake.Embed(color=color.lightpink, title="**Current Multipliers:**")
        em.add_field(name="Mod/Staff", value="%sx (%s XP per message)" % (modMultiplier, 20 * modMultiplier), inline=False)
        em.add_field(name="Server Boosters", value="%sx (%s XP per message)" % (boostersMultiplier, 15 * boostersMultiplier), inline=False)
        em.add_field(name="Members", value="%sx (%s XP per message)" % (membersMultiplier, 5 * membersMultiplier), inline=False)
        em.add_field(name="Kraots", value="%sx (%s XP per message)" % (kraotsMultiplier, 30 * kraotsMultiplier), inline=False)
        em.set_footer(text="Requested By: %s" % (ctx.author), icon_url=ctx.author.display_avatar)

        await ctx.send(embed=em)

    @multiplier.command(name='set')
    @commands.is_owner()
    async def multiplier_set(self, ctx, group : str = None, multiplier : float = None):
        """Set the multiplier for a group."""

        if group == None:
            await ctx.send("You must specify which group you want to set the multiplier for.\nGroups:\n\u2800 • **Mod/Staff**\n\u2800 • **Boosters**\n\u2800 • **Members**\n\u2800 • **Kraots**\n\u2800 • **all**")
            return
        
        elif multiplier == None:
            await ctx.send("You must give the number that you want to multiply the XP with.")
            return

        elif multiplier > 1000000:
            await ctx.send("You can't set the multiplier more than `1,000,000`, or else it will break the bot.")
            return

        else:
            group = group.lower()

            if str(multiplier).endswith(".0"):
                x = str(multiplier).replace(".0", "")
            else:
                x = multiplier
            
            if group in ('mod', 'staff', 'mods'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': multiplier}})
                await ctx.send("Set the multiplier for Mods/Staff members to **%s**." % (x))
                return
            
            elif group in ('booster', 'boosters', 'serverbooster', 'serverboosters'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': multiplier}})
                await ctx.send("Set the multiplier for Server Boosters to **%s**." % (x))
                return
            
            elif group in ('member', 'members'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': multiplier}})
                await ctx.send("Set the multiplier for Members to **%s**." % (x))
                return
            
            elif group in ('kraots', 'kraot'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': multiplier}})
                await ctx.send("Set the multiplier for Kraots to **%s**." % (x))
                return
            
            elif group == "all":
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': multiplier}})
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': multiplier}})
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': multiplier}})
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': multiplier}})
                await ctx.send("Set the multiplier for every group to **%s**." % (x))

    @multiplier.command()
    @commands.is_owner()
    async def multiplier_reset(self, ctx, group : str = None):
        """Reset the multipliers of a group."""

        if group == None:
            await ctx.send("You must specify which group you want to reset the multiplier for.\nGroups:\n\u2800 • **Mod/Staff**\n\u2800 • **Boosters**\n\u2800 • **Members**\n\u2800 • **Kraots**\n\u2800 • **all**")
            return
        
        else:
            group = group.lower()
            
            if group in ('mod', 'staff', 'mods'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': 1}})
                await ctx.send("Set the multiplier for Mods/Staff members back to **1**.")
                return
            
            elif group in ('booster', 'boosters', 'serverbooster', 'serverboosters'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': 1}})
                await ctx.send("Set the multiplier for Server Boosters back to **1**.")
                return
            
            elif group in ('member', 'members'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': 1}})
                await ctx.send("Set the multiplier for Members back to **1**.")
                return
            
            elif group in ('kraots', 'kraot'):
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': 1}})
                await ctx.send("Set the multiplier for Kraots to **1**.")
                return

            elif group == "all":
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': 1}})
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': 1}})
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': 1}})
                await self.db.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': 1}})
                await ctx.send("Set the multiplier for every group back to **1**.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.id == 374622847672254466:
            return
        await self.db.delete_one({"_id": member.id})

def setup(bot):
    bot.add_cog(Levels(bot))