import discord
from discord.ext import commands
from utils.paginator_v2 import WrappedPaginator, PaginatorEmbedInterface
import motor.motor_asyncio
import os
import asyncio

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Reclist"]

class Reclist(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra = False)
	async def reclist(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})

		user = member
		if results != None:
			alist = results['reclist']

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
		results = await collection.find_one({"_id": user.id})
		if results == None:
			post = {"_id": user.id, "reclist": f"`###`\u2800{args}"}
			await collection.insert_one(post)
		else:
			await collection.update_one({"_id": user.id}, {"$set":{"reclist": f"`###`\u2800{args}"}})
		await ctx.message.delete()
		await ctx.send(f"Reclist set! {user.mention}")



	@reclist.command()
	async def add(self, ctx, *, args):

		user = ctx.author

		results = await collection.find_one({"_id": user.id})
		
		if results == None:
			post = {"_id": user.id, "reclist": f"`###`\u2800{args}"}
			await collection.insert_one(post)

		else:
			rec = results['reclist']
			await collection.update_one({"_id": user.id}, {"$set":{"reclist": f"{rec}\n{args}"}})
		
		await ctx.message.delete()
		await ctx.send("Succesfully added to your reclist! {}".format(user.mention))



	@reclist.command()
	async def raw(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})
		
		if results != None:
			user_list = results['reclist']

			final = user_list[6:]

			paginator = WrappedPaginator(prefix='```CSS', suffix='```', max_size = 375)
			paginator.add_line(final)
			interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author)
			await interface.send_to(ctx)

		else:
			await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")



	@reclist.command()
	async def delete(self, ctx):
		results = await collection.find_one({"_id": ctx.author.id})
		
		if results != None:
			def check(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
			msg = await ctx.send("Are you sure you want to delete your reclist? %s" % (ctx.author.mention))
			await msg.add_reaction('<:agree:797537027469082627>')
			await msg.add_reaction('<:disagree:797537030980239411>')
			
			try:
				reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)

			except asyncio.TimeoutError:
				new_msg = f"{ctx.author.mention} Did not react in time."
				await msg.edit(content=new_msg)
				await msg.clear_reactions()
				return
			
			else:
				if str(reaction.emoji) == '<:agree:797537027469082627>':
					await collection.delete_one({"_id": ctx.author.id})
					e = "Succesfully deleted your reclist! %s" % (ctx.author.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return
				
				elif str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = "Reclist has not been deleted. %s" % (ctx.author.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return
		
		else:
			await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")





	@reclist.command()
	@commands.is_owner()
	async def remove(self, ctx, user : discord.Member):

		results = await collection.find_one({"_id": user.id})
		
		if results != None:
			await collection.delete_one({"_id": user.id})
			await ctx.send("Succesfully deleted `{}`'s reclist!".format(user.display_name))
		
		else:
			await ctx.send("User does not have a reclist!")


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await collection.delete_one({"_id": member.id})








	@reclist.error
	async def reclist_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("User does not have any reclist!")
		elif isinstance(error, commands.TooManyArguments):
			return











def setup(client):
	client.add_cog(Reclist(client))