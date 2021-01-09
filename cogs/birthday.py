import discord
from discord.ext import commands
import utils.colors as color
from pymongo import MongoClient
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Birthdays"]


class Birthdays(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bday', 'b-day'])
	async def birthday(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		user = member

		if user.id in all_users:

			get_data = collection.find({"_id": user.id})
			for data in get_data:
				birthday = data['birthdaydate']

			em = discord.Embed(color=color.blue, description = f"_ _ \n`{birthday}`")
			em.set_author(name=f"{member.name}'s birthday is on:", url=member.avatar_url, icon_url=member.avatar_url)
			await ctx.send(embed=em)
		
		else:
			if user.id == ctx.author.id:
				await ctx.send("You did not set your birthday! Type: `!birthday set <day | month>` to set your birthday.")
			else:
				await ctx.send("User did not set their birthday!")




	@birthday.command(aliases=['add'])
	async def set(self, ctx, *, args):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		user = ctx.author

		post = {"_id": user.id, "birthdaydate": args}
		collection.insert_one(post)

		await ctx.message.delete()
		await ctx.send(f"Birthday set to `{args}` {user.mention}")



	@birthday.command(aliases=['remove'])
	async def delete(self, ctx):
		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		if ctx.author.id in all_users:
			collection.delete_one({"_id": ctx.author.id})
			await ctx.send("Succesfully deleted your birthday from the list! {}".format(ctx.author.mention))

		else:
			await ctx.send("You did not set your birthday, therefore you don't have what to delete! Type: `!birthday set <day | month>` to set your birthday.")















def setup(client):
	client.add_cog(Birthdays(client))