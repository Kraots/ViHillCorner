import disnake
from disnake.ext import commands
from utils.paginator import CustomMenu
import utils.colors as color
from mal import Anime as AnimeSearchId
from mal import AnimeSearch
import textwrap

class AlistPageEntry:
	def __init__(self, entry):

		self.name = entry

	def __str__(self):
		return f'\u2800{self.name.title()}'

class AlistPages(CustomMenu):
	def __init__(self, ctx, entries, *, per_page=12, title="", color=None):
		converted = [AlistPageEntry(entry) for entry in entries]
		super().__init__(ctx=ctx, entries=converted, per_page=per_page, color=color, title=title)

class Anime(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Alist']
		self.prefix = '!'
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def alist(self, ctx, member: disnake.Member = None):
		"""See the member's anime list."""

		member = member or ctx.author

		results = await self.db.find_one({"_id": member.id})

		user = member
		if results != None:
			entries = results['alist']
			p = AlistPages(ctx=ctx, entries=entries, per_page=10, title=f"Here's `{member.display_name}`'s anime list:", color=color.reds)
			await p.start()

		else:
			if ctx.author.id == user.id:
				await ctx.send("You do not have an anime list! Type: `!alist set <recommendations>` to set your anime list!")
				return

			else:
				await ctx.send("User does not have an anime list!")



	@alist.command(name='set')
	async def alist_set(self, ctx, *, rec: str):
		"""Set your anime list."""

		args = rec
		user = ctx.author
		results = await self.db.find_one({"_id": user.id})
		alist = list(filter(bool, args.splitlines()))
		if results == None:
			post = {"_id": user.id, "alist": alist}
			await self.db.insert_one(post)
		else:
			await self.db.update_one({"_id": user.id}, {"$set":{"alist": alist}})
		await ctx.message.delete()
		await ctx.send(f"Anime list set! {user.mention}")


	@alist.command(name='add')
	async def alist_add(self, ctx, *, anime: str):
		"""Add to your anime list."""

		args = anime
		user = ctx.author
		results = await self.db.find_one({"_id": user.id})
		alist = list(filter(bool, args.splitlines()))
		if results == None:
			post = {"_id": user.id, "alist": alist}
			await self.db.insert_one(post)
		else:
			alst = results['alist']
			await self.db.update_one({"_id": user.id}, {"$set":{"alist": alst + alist}})
		await ctx.message.delete()
		await ctx.send("Succesfully added to your anime list! {}".format(user.mention))


	@alist.command(name='delete')
	async def alist_delete(self, ctx, index: str):
		"""Delete the recommendation at the given index."""

		try:
			nr = int(index)
		except ValueError:
			return await ctx.send("Must be a number. %s" % (ctx.author.mention))
		results = await self.db.find_one({'_id': ctx.author.id})
		if results == None:
			return await ctx.send("You do not have an anime list. %s" % (ctx.author.mention))
		n = nr - 1
		new_alist = []
		rec = None
		
		for i in range(len(results['alist'])):
			if i != n:
				new_alist.append(results['alist'][i])
			else:
				rec = results['alist'][i]
		
		await self.db.update_one({'_id': ctx.author.id}, {'$set':{'alist': new_alist}})
		if rec != None:
			return await ctx.send(f"Successfully removed **{rec}** from your anime list. {ctx.author.mention}")
		await ctx.send(f"No recommendation with that number found. {ctx.author.mention}")



	@alist.command(name='clear')
	async def alist_clear(self, ctx):
		"""Delete your whole anime list."""
		
		results = await self.db.find_one({"_id": ctx.author.id})
		
		if results != None:
			view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
			view.message = msg = await ctx.send("Are you sure you want to delete your anime list? %s" % (ctx.author.mention), view=view)
			await view.wait()
			if view.response is True:
				await self.db.delete_one({"_id": ctx.author.id})
				e = "Succesfully deleted your anime list! %s" % (ctx.author.mention)
				return await msg.edit(content=e, view=view)
			
			elif view.response is False:
				e = "Your anime list has not been deleted. %s" % (ctx.author.mention)
				return await msg.edit(content=e, view=view)
		
		else:
			await ctx.send("You do not have an anime list! Type: `!alist set <recommendations>` to set your anime list!")

	@alist.command(name='remove')
	@commands.is_owner()
	async def alist_remove(self, ctx, member: disnake.Member):
		"""Remove the member from the anime list database."""

		results = await self.db.find_one({"_id": member.id})
		
		if results != None:
			await self.db.delete_one({"_id": member.id})
			await ctx.send("Succesfully removed `{}`'s anime list from the database.".format(member.display_name))
		
		else:
			await ctx.send("User does not have an anime list!")

	def search_anime(self, query):
		anime = AnimeSearch(query)
		return anime.results[0]
	
	def search_anime_id(self, query):
		return AnimeSearchId(query)

	@commands.command(name='myanimelist', aliases=['mal', 'anime'])
	async def anime_mal(self, ctx, *, query):
		"""Search an anime and get an embed with it's info based on its name, it can also accept the anime's id from MyAnimeList."""

		try:
			query = int(query)
		except ValueError:
			query = str(query)
		if isinstance(query, str):
			anime_ = await self.bot.loop.run_in_executor(None, self.search_anime, query)
			anime: AnimeSearchId = await self.bot.loop.run_in_executor(None, self.search_anime_id, anime_.mal_id)
		elif isinstance(query, int):
			anime: AnimeSearchId = await self.bot.loop.run_in_executor(None, self.search_anime_id, query)
		else:
			return await ctx.reply('Not a valid query!')

		em = disnake.Embed(title=anime.title, url=anime.url, description=f'**Synopsis:** *{textwrap.shorten(text=anime.synopsis, width=700, placeholder=f" [[...]]({anime.url})")}*')
		em.set_thumbnail(url=anime.image_url)
		em.add_field(name='Episodes:', value=anime.episodes)
		em.add_field(name='Genres:', value=', '.join(anime.genres))
		em.add_field(name='Duration:', value=anime.duration)
		em.add_field(name='Status:', value=anime.status)
		em.add_field(name='Aired:', value=anime.aired)
		em.add_field(name='Premiered:' ,value=anime.premiered)
		em.add_field(name='Broadcast:', value=anime.broadcast)
		em.add_field(name='Score:', value=f'{anime.score} (by {anime.scored_by:,} users)')
		em.add_field(name='Rank:', value=f'#{anime.rank}')
		em.add_field(name='Popularity:', value=f'#{anime.popularity}')
		em.add_field(name='Studios:', value=', '.join(anime.studios))
		em.add_field(name='Rating:', value=anime.rating)
		em.add_field(name='Favorites:', value=f'{anime.favorites:,}')
		em.add_field(name='Producers:', value=', '.join(anime.producers))
		em.add_field(name='Source:', value=anime.source)
		em.set_footer(text=f'Requested by: {ctx.author} • ID: {anime.mal_id}')

		await ctx.reply(embed=em)


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({"_id": member.id})


def setup(bot):
	bot.add_cog(Anime(bot))