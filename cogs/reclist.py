import discord
from discord.ext import commands
from utils.paginator_v2 import WrappedPaginator, PaginatorEmbedInterface
import pymongo
from pymongo import MongoClient
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Reclist"]

class Reclist(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra = False)
	async def reclist(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		all_users = []
		resultss = collection.find()
		for result in resultss:
			all_users.append(result['_id'])

		user = member
		if user.id in all_users:
			results = collection.find({"_id": user.id})

			for data in results:
				alist = data['reclist']

			for line in alist.splitlines():
				final = alist.replace("\n", "\n`###`\u2800")

			if len(final) > 1:
				paginator = WrappedPaginator(prefix=f"**`{member.name}`'𝘀 𝗔𝗻𝗶𝗺𝗲 𝗥𝗲𝗰𝗼𝗺𝗺𝗲𝗻𝗱𝗮𝘁𝗶𝗼𝗻𝘀:**\n", suffix='', max_size = 500)
				paginator.add_line(final)
				interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author)
				await interface.send_to(ctx)

		else:
			if ctx.author.id == user.id:
				await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")
				return

			else:
				await ctx.send("User does not have a reclist!")



	@reclist.command()
	async def set(self, ctx, *, args):
		user = ctx.author
		try:
			post = {"_id": user.id, "reclist": f"`###`\u2800{args}"}
			collection.insert_one(post)
		except pymongo.errors.DuplicateKeyError:
			collection.update_one({"_id": user.id}, {"$set":{"reclist": f"`###`\u2800{args}"}})
		await ctx.message.delete()
		await ctx.send(f"Reclist set! {user.mention}")



	@reclist.command()
	async def add(self, ctx, *, args):

		user = ctx.author

		all_users = []
		resultss = collection.find()
		for result in resultss:
			all_users.append(result['_id'])
		
		if not user.id in all_users:
			post = {"_id": user.id, "reclist": f"`###`\u2800{args}"}
			collection.insert_one(post)

		else:
			result = collection.find({"_id": user.id})
			for data in result:
				rec = data['reclist']
			collection.update_one({"_id": user.id}, {"$set":{"reclist": f"{rec}\n{args}"}})
		
		await ctx.message.delete()
		await ctx.send("Succesfully added to your reclist! {}".format(user.mention))



	@reclist.command()
	async def raw(self, ctx):

		all_users = []
		resultss = collection.find()
		for result in resultss:
			all_users.append(result['_id'])
		
		if ctx.author.id in all_users:
			results = collection.find({"_id": ctx.author.id})
			for data in results:
				user_list = data['reclist']

			final = user_list[6:]

			paginator = WrappedPaginator(prefix='```CSS', suffix='```', max_size = 375)
			paginator.add_line(final)
			interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author)
			await interface.send_to(ctx)

		else:
			await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")



	@reclist.command()
	async def delete(self, ctx):

		all_users = []
		resultss = collection.find()
		for result in resultss:
			all_users.append(result['_id'])
		
		if ctx.author.id in all_users:
			collection.delete_one({"_id": ctx.author.id})
		
		else:
			await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")





	@reclist.command()
	@commands.is_owner()
	async def remove(self, ctx, user : discord.Member):

		all_users = []
		resultss = collection.find()
		for result in resultss:
			all_users.append(result['_id'])
		
		if user.id in all_users:
			collection.delete_one({"_id": user.id})
			await ctx.send("Succesfully deleted `{}`'s reclist!".format(user.display_name))
		
		else:
			await ctx.send("User does not have a reclist!")


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection.delete_one({"_id": member.id})








	@reclist.error
	async def reclist_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("User does not have any reclist!")
		elif isinstance(error, commands.TooManyArguments):
			return











def setup(client):
	client.add_cog(Reclist(client))