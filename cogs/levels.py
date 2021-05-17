import discord
from discord.ext import commands

import os

import utils.colors as color

import motor.motor_asyncio

DBKEY = os.getenv("MONGODBLVLKEY")
cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']
collection = db['Levels']

bot_channel = [750160851822182486, 750160851822182487, 752164200222163016]
no_talk_channels = [750160852006469807, 780374324598145055]

level = [758278459645755392, 750160850290999330, 750160850290999331, 750160850290999332, 750160850290999333, 750160850290999334, 750160850290999335, 750160850295324744, 750160850295324745, 750160850295324746, 750160850295324747, 750160850295324748, 750160850295324749, 750160850295324750, 788127504710762497, 788127526278791240, 788127540459208725, 788127547606827028, 788127552686129265, 788127561283928115, 788127569198579764, 788127574663495720, 788127580330655744, 788127589092818994, 788127593386868758, 818562249349660713, 818562250252091413, 818562250477404173, 818562251644076072, 818562252185534465, 818562252360777749, 818562252906037259, 818562253501628507, 818562254043480075, 818562254495547462, 818562254680883241, 818562255188131924, 818562256101965844, 818562256546824192, 818562257033101372, 818562257653858304, 818562258119950367, 818562258551832657, 818562259587563523, 818562260254588988, 818562260686995486, 818562261844230215, 818562262360784977, 818562262520430654, 818562263169368076, 818562263850025031, 818562264030380033, 818562264554405899, 818562265422757898, 818562265779273749, 818562266475528242, 818562266760740926, 818562267410726964, 818562267837628456, 818562268044197889, 818562268966027294, 818562269029466124, 818562269835034625, 818562270119985163, 818562270375182357, 818562271100928020, 818562271269486623, 818562271978586132, 818562272791101500, 818562273202405396, 818562273215774776, 818562274318090260, 818562274502508555, 818562275539550239, 818562276490870857, 818562276939661343, 818562277514805258, 818562277619400765, 818562278521569282, 818562278832078939, 818562279725203508, 818562280009760889, 818562280765390909, 818562281410658344, 818562282019356733]
lvlnum = [3, 5, 10, 15, 20, 25, 30, 40, 45, 50, 55, 60, 65, 69, 75, 80, 85, 90, 95, 100, 105, 110, 120, 130, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 230, 240, 250, 255, 260, 265, 270, 275, 280, 285, 290, 300, 305, 310, 315, 320, 330, 340, 350, 355, 360, 365, 370, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 430, 440, 450, 455, 460, 465, 470, 475, 480, 485, 490, 495, 500]

class LevelSystem(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
			if not message.channel.id in no_talk_channels:
				if not message.author.bot:
					guild = self.client.get_guild(750160850077089853)
					stats = await collection.find_one({"_id": message.author.id})
					if stats is None:
						newuser = {"_id": message.author.id, "xp": 0, "messages_count": 0}
						await collection.insert_one(newuser)
					else:			
						
						kraotsDocument = await collection.find_one({'_id':374622847672254466})
						membersMultiplier = kraotsDocument['xp multiplier']
						boostersMultiplier = kraotsDocument['booster xp multiplier']
						modMultiplier = kraotsDocument['mod xp multiplier']
						kraotsMultiplier = kraotsDocument['kraots xp multiplier']

						await collection.update_one({"_id": message.author.id}, {"$inc": {"messages_count": 1}})
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
							server_booster = guild.get_role(759475712867565629)
							staff = guild.get_role(754676705741766757)
							if server_booster in message.author.roles:
								xp = stats['xp'] + (15 * boostersMultiplier)
							elif staff in message.author.roles:
								xp = stats['xp'] + (20 * modMultiplier)
							else:
								xp = stats['xp'] + (5 * membersMultiplier)
							
							if message.author.id == 374622847672254466:
								xp = stats['xp'] + (30 * kraotsMultiplier)

							await collection.update_one({"_id": message.author.id}, {"$set":{"xp": xp}})
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
								for i in range(len(level)):
									if lvl == lvlnum[i]:
										lvlrole = level[i]
										userroles = []
										for x in message.author.roles:
											if not x.id in level:
												userroles.append(x.id)
										userroles.append(lvlrole)
										newroles = []
										for role in userroles:
											newrole = guild.get_role(role)
											newroles.append(newrole)
										await message.author.edit(roles=newroles)



	@commands.group(invoke_without_command = True, case_insensitive = True, aliases=['lvl', 'level'])
	async def rank(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		if ctx.channel.id in bot_channel:
			stats = await collection.find_one({"_id": member.id})
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
				boxes = int((xp/(200*((1/2)*lvl)))*20)
				rankings = collection.find().sort('xp', -1)
				for data in await rankings.to_list(100000000):
					rank += 1
					if stats['_id'] == data['_id']:
						break
				
				if xp < 0:
					lvl = lvl - 1
					xp = stats['xp']
					xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
					boxes = int((xp/(200*((1/2)*lvl)))*20)

				guild = self.client.get_guild(750160850077089853)
				all_guild_members = len([m for m in guild.members if not m.bot])
				
				em = discord.Embed(title=f"{member.display_name}'s level stats", color=color.lightpink)
				em.add_field(name="Name", value=member.mention)
				


				if lvl == 500:
					lvl = "500(MAX)"
					em.add_field(name="XP", value="MAX")
					em.add_field(name="Level", value=lvl)
					em.add_field(name="Rank", value=f"{rank}/{all_guild_members}", inline=False)
					em.add_field(name="Progress Bar [lvl]", value=20 * ":blue_square:", inline=False)
				else:
					if str(xp).endswith(".0"):
						x = str(xp).replace(".0", "")
					else:
						x = xp

					em.add_field(name="XP", value=f"{x}/{int(200*((1/2)*lvl))}")
					em.add_field(name="Level", value=lvl)
					em.add_field(name="Rank", value=f"{rank}/{all_guild_members}", inline=False)
					em.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
				
				em.set_thumbnail(url=member.avatar_url)

				await ctx.send(embed=em)



	@rank.command()
	@commands.is_owner()
	async def set(self, ctx, lvl: int,  member: discord.Member = None):
		if member is None:
			member = ctx.author

		xp = ((50*((lvl-1)**2))+(50*(lvl-1)))
		await collection.update_one({"_id": member.id}, {"$set":{"xp": xp}})
		await ctx.send("Set level `{}` for **{}**.".format(lvl, member.display_name))



	@rank.command(aliases=['lb', 'top'])
	async def leaderboard(self, ctx):
		if ctx.channel.id in bot_channel:
			results = collection.find().sort([('xp', -1)])
			index = 0
			em = discord.Embed(color=color.lightpink, title="Top 10 highest level people\n _ _")
			for result in await results.to_list(10):
				xp = result['xp']
				user = result['_id']
				user = self.client.get_user(user)

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
				else:
					f = f
				

				em.add_field(name=f"`#{index}` **-->** {user.display_name}", value=f"Level: `{lvl}`\nTotal XP: `{f}`", inline=False)
			
			await ctx.send(embed=em)


	@commands.group(invoke_without_command = True, case_insensitive = True, aliases=['multipliers'])
	async def multiplier(self, ctx):
		kraotsDocument = await collection.find_one({'_id':374622847672254466})
		membersMultiplier = float(kraotsDocument['xp multiplier'])
		boostersMultiplier = float(kraotsDocument['booster xp multiplier'])
		modMultiplier = float(kraotsDocument['mod xp multiplier'])
		kraotsMultiplier = float(kraotsDocument['kraots xp multiplier'])

		em = discord.Embed(color=color.lightpink, title="**Current Multipliers:**")
		em.add_field(name="Mod/Staff", value="%sx (%s XP per message)" % (modMultiplier, 20 * modMultiplier), inline=False)
		em.add_field(name="Server Boosters", value="%sx (%s XP per message)" % (boostersMultiplier, 15 * boostersMultiplier), inline=False)
		em.add_field(name="Members", value="%sx (%s XP per message)" % (membersMultiplier, 5 * membersMultiplier), inline=False)
		em.add_field(name="Kraots", value="%sx (%s XP per message)" % (kraotsMultiplier, 30 * kraotsMultiplier), inline=False)
		em.set_footer(text="Requested By: %s" % (ctx.author), icon_url=ctx.author.avatar_url)

		await ctx.send(embed=em)

	@multiplier.command(aliases=['set'])
	@commands.is_owner()
	async def _set(self, ctx, group : str = None, multiplier : float = None):
		if group == None:
			await ctx.send("You must specify which group you want to set the multiplier for.\nGroups:\n\u2800 • **Mod/Staff**\n\u2800 • **Boosters**\n\u2800 • **Members**\n\u2800 **Kraots**")
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
			
			if group in ['mod', 'staff', 'mods']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': multiplier}})
				await ctx.send("Set the multiplier for Mods/Staff members to **%s**." % (x))
				return
			
			elif group in ['booster', 'boosters', 'serverbooster', 'serverboosters']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': multiplier}})
				await ctx.send("Set the multiplier for Server Boosters to **%s**." % (x))
				return
			
			elif group in ['member', 'members']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': multiplier}})
				await ctx.send("Set the multiplier for Members to **%s**." % (x))
				return
			
			elif group in ['kraots', 'kraot']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': multiplier}})
				await ctx.send("Set the multiplier for Kraots to **%s**." % (x))
				return

	@multiplier.command()
	@commands.is_owner()
	async def reset(self, ctx, group : str = None):
		if group == None:
			await ctx.send("You must specify which group you want to reset the multiplier for.\nGroups:\n\u2800 • **Mod/Staff**\n\u2800 • **Boosters**\n\u2800 • **Members**")
			return
		
		else:
			group = group.lower()
			
			if group in ['mod', 'staff', 'mods']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': 1}})
				await ctx.send("Set the multiplier for Mods/Staff members back to **1**.")
				return
			
			elif group in ['booster', 'boosters', 'serverbooster', 'serverboosters']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': 1}})
				await ctx.send("Set the multiplier for Server Boosters back to **1**.")
				return
			
			elif group in ['member', 'members']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': 1}})
				await ctx.send("Set the multiplier for Members back to **1**.")
				return
			
			elif group in ['kraots', 'kraot']:
				await collection.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': 1}})
				await ctx.send("Set the multiplier for Kraots to **1**.")
				return

			elif group == "all":
				await collection.update_one({'_id':374622847672254466}, {'$set':{'mod xp multiplier': 1}})
				await collection.update_one({'_id':374622847672254466}, {'$set':{'booster xp multiplier': 1}})
				await collection.update_one({'_id':374622847672254466}, {'$set':{'xp multiplier': 1}})
				await collection.update_one({'_id':374622847672254466}, {'$set':{'kraots xp multiplier': 1}})
				await ctx.send("Set the multiplier for every group back to **1**.")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await collection.delete_one({"_id": member.id})

def setup(client):
	client.add_cog(LevelSystem(client))