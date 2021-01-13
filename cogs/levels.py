import discord
from discord.ext import commands

import os

import utils.colors as color

from pymongo import MongoClient

DBKEY = os.getenv("MONGODBLVLKEY")
cluster = MongoClient(DBKEY)
db = cluster['ViHillCornerDB']
collection = db['Levels']


bot_channel = [750160851822182486, 750160851822182487, 752164200222163016]
no_talk_channels = 750160852006469807

level = [758278459645755392, 750160850290999330, 750160850290999331, 750160850290999332, 750160850290999333, 750160850290999334, 750160850290999335, 750160850295324744, 750160850295324745, 750160850295324746, 750160850295324747, 750160850295324748, 750160850295324749, 750160850295324750, 788127504710762497, 788127526278791240, 788127540459208725, 788127547606827028, 788127552686129265, 788127561283928115, 788127569198579764, 788127574663495720, 788127580330655744, 788127589092818994, 788127593386868758]
lvlnum = [3, 5, 10, 15, 20, 25, 30, 40, 45, 50, 55, 60, 65, 69, 75, 80, 85, 90, 95, 100, 105, 110, 120, 130, 150]


class LevelSystem(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.channel.id != no_talk_channels:
			if not message.author.bot:
				guild = self.client.get_guild(750160850077089853)
				stats = collection.find_one({"_id": message.author.id})
				if stats is None:
					newuser = {"_id": message.author.id, "xp": 0}
					collection.insert_one(newuser)
				else:
					xp = stats['xp'] + 5
					collection.update_one({"_id": message.author.id}, {"$set":{"xp": xp}})
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
					elif xp == 0:
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
			stats = collection.find_one({"_id": member.id})
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
				for data in rankings:
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
				em.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}")
				em.add_field(name="Level", value=lvl)
				em.add_field(name="Rank", value=f"{rank}/{all_guild_members}", inline=False)
				em.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
				em.set_thumbnail(url=member.avatar_url)

				await ctx.send(embed=em)



	@rank.command()
	async def set(self, ctx, lvl: int,  member: discord.Member = None):
		if member is None:
			member = ctx.author

		xp = ((50*((lvl-1)**2))+(50*(lvl-1))) - 5
		collection.update_one({"_id": member.id}, {"$set":{"xp": xp}})
		await ctx.send("Set level `{}` for **{}**.".format(lvl, member.display_name))



	@rank.command(aliases=['lb', 'top'])
	async def leaderboard(self, ctx):
		if ctx.channel.id in bot_channel:
			results = collection.find().sort([('xp', -1)]).limit(10)
			index = 0
			em = discord.Embed(color=color.lightpink, title="Top 10 highest level people\n _ _")
			for result in results:
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
				em.add_field(name=f"`#{index}` **-->** {user.display_name}", value=f"Level: `{lvl}`\nTotal XP: `{result['xp']}`", inline=False)
			
			await ctx.send(embed=em)


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		collection.delete_one({"_id": member.id})


def setup(client):
	client.add_cog(LevelSystem(client))