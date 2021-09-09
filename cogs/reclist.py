import disnake
from disnake.ext import commands
from utils.paginator import CustomMenu
import utils.colors as color
import asyncio

class ReclistPageEntry:
	def __init__(self, entry):

		self.name = entry

	def __str__(self):
		return f'\u2800{self.name}'

class ReclistPages(CustomMenu):
	def __init__(self, ctx, entries, *, per_page=12, title="", color=None):
		converted = [ReclistPageEntry(entry) for entry in entries]
		super().__init__(ctx=ctx, entries=converted, per_page=per_page, color=color, title=title)

class Reclist(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Reclist']
		self.prefix = '!'
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def reclist(self, ctx, member: disnake.Member = None):
		"""See the member's anime recommendations list."""

		member = member or ctx.author

		results = await self.db.find_one({"_id": member.id})

		user = member
		if results != None:
			entries = results['reclist']
			p = ReclistPages(ctx=ctx, entries=entries, per_page=10, title=f"Here's `{member.display_name}` reclist:", color=color.reds)
			await p.start()

		else:
			if ctx.author.id == user.id:
				await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")
				return

			else:
				await ctx.send("User does not have a reclist!")



	@reclist.command(name='set')
	async def reclist_set(self, ctx, *, rec: str):
		"""Set your anime recommendations list."""

		args = rec
		user = ctx.author
		results = await self.db.find_one({"_id": user.id})
		reclist = list(filter(bool, args.splitlines()))
		if results == None:
			post = {"_id": user.id, "reclist": reclist}
			await self.db.insert_one(post)
		else:
			await self.db.update_one({"_id": user.id}, {"$set":{"reclist": reclist}})
		await ctx.message.delete()
		await ctx.send(f"Reclist set! {user.mention}")


	@reclist.command(name='add')
	async def reclist_add(self, ctx, *, rec: str):
		"""Add to your anime recommendations list."""

		args = rec
		user = ctx.author
		results = await self.db.find_one({"_id": user.id})
		reclist = list(filter(bool, args.splitlines()))
		if results == None:
			post = {"_id": user.id, "reclist": reclist}
			await self.db.insert_one(post)
		else:
			rec = results['reclist']
			await self.db.update_one({"_id": user.id}, {"$set":{"reclist": rec + reclist}})
		await ctx.message.delete()
		await ctx.send("Succesfully added to your reclist! {}".format(user.mention))


	@reclist.command(name='delete')
	async def reclist_delete(self, ctx, index: str):
		"""Delete the recommendation at the given index."""

		try:
			nr = int(index)
		except ValueError:
			return await ctx.send("Must be a number. %s" % (ctx.author.mention))
		results = await self.db.find_one({'_id': ctx.author.id})
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
		
		await self.db.update_one({'_id': ctx.author.id}, {'$set':{'reclist': new_reclist}})
		if rec != None:
			return await ctx.send(f"Successfully removed **{rec}** from your reclist. {ctx.author.mention}")
		await ctx.send(f"No recommendation with that number found. {ctx.author.mention}")



	@reclist.command(name='clear')
	async def reclist_clear(self, ctx):
		"""Delete your reclist, completely."""
		
		results = await self.db.find_one({"_id": ctx.author.id})
		
		if results != None:
			view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
			view.message = msg = await ctx.send("Are you sure you want to delete your reclist? %s" % (ctx.author.mention), view=view)
			await view.wait()
			if view.response is True:
				await self.db.delete_one({"_id": ctx.author.id})
				e = "Succesfully deleted your reclist! %s" % (ctx.author.mention)
				return await msg.edit(content=e, view=view)
			
			elif view.response is False:
				e = "Reclist has not been deleted. %s" % (ctx.author.mention)
				return await msg.edit(content=e, view=view)
		
		else:
			await ctx.send("You do not have a reclist! Type: `!reclist set <recommendations>` to set your reclist!")





	@reclist.command(name='remove')
	@commands.is_owner()
	async def reclist_remove(self, ctx, member: disnake.Member):
		"""Remove the member from the database."""

		results = await self.db.find_one({"_id": member.id})
		
		if results != None:
			await self.db.delete_one({"_id": member.id})
			await ctx.send("Succesfully removed `{}`'s reclist from the database.".format(member.display_name))
		
		else:
			await ctx.send("User does not have a reclist!")


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({"_id": member.id})


def setup(bot):
	bot.add_cog(Reclist(bot))
