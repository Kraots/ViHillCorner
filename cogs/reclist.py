import discord
from discord.ext import commands
from utils.paginator import CustomMenu
import motor.motor_asyncio
import os
import utils.colors as color
import asyncio

class ReclistPageEntry:
	def __init__(self, entry):

		self.name = entry

	def __str__(self):
		return f'\u2800{self.name}'

class ReclistPages(CustomMenu):
	def __init__(self, entries, *, per_page=12, title="", color=None):
		converted = [ReclistPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page, color=color, title=title)

DBKEY = os.getenv("MONGODBKEY")

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Reclist"]

class Reclist(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def reclist(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		results = await collection.find_one({"_id": member.id})

		user = member
		if results != None:
			entries = results['reclist']
			p = ReclistPages(entries=entries, per_page=10, title=f"Here's {ctx.author.display_name} reclist:", color=color.lightpink)
			await p.start(ctx)

		else:
			if ctx.author.id == user.id:
				await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")
				return

			else:
				await ctx.send("User does not have a reclist!")



	@reclist.command(aliases=['set'])
	async def _set(self, ctx, *, args: str):
		user = ctx.author
		results = await collection.find_one({"_id": user.id})
		reclist = list(filter(bool, args.splitlines()))
		if results == None:
			post = {"_id": user.id, "reclist": reclist}
			await collection.insert_one(post)
		else:
			await collection.update_one({"_id": user.id}, {"$set":{"reclist": reclist}})
		await ctx.message.delete()
		await ctx.send(f"Reclist set! {user.mention}")


	@reclist.command()
	async def add(self, ctx, *, args):
		user = ctx.author
		results = await collection.find_one({"_id": user.id})
		reclist = list(filter(bool, args.splitlines()))
		if results == None:
			post = {"_id": user.id, "reclist": reclist}
			await collection.insert_one(post)
		else:
			rec = results['reclist']
			await collection.update_one({"_id": user.id}, {"$set":{"reclist": rec + reclist}})
		await ctx.message.delete()
		await ctx.send("Succesfully added to your reclist! {}".format(user.mention))


	@reclist.command()
	async def delete(self, ctx, nr: int):
		results = await collection.find_one({'_id': ctx.author.id})
		if results == None:
			return await ctx.send("You do not have a reclist. %s" % (ctx.author.mention))
		n = nr - 1
		new_reclist = []
		rec = None
		
		for i in range(len(results['reclist'])):
			if i != n:
				new_reclist.append(results['reclist'][i])
			else:
				rec = results['reclist'][i]
		
		await collection.update_one({'_id': ctx.author.id}, {'$set':{'reclist': new_reclist}})
		if rec != None:
			return await ctx.send(f"Successfully removed **{rec}** from your reclist. {ctx.author.mention}")
		await ctx.send(f"No recommendation with that number found. {ctx.author.mention}")



	@reclist.command()
	async def clear(self, ctx):
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
			await ctx.send("Succesfully removed `{}`'s reclist from the database.".format(user.display_name))
		
		else:
			await ctx.send("User does not have a reclist!")


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await collection.delete_one({"_id": member.id})


def setup(client):
	client.add_cog(Reclist(client))