import discord
from discord.ext import commands
import json
from utils.paginator_v2 import WrappedPaginator, PaginatorEmbedInterface

class Reclist(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra = False)
	async def reclist(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		user = member
		users = await get_arec_data()

		alist = users[str(user.id)]["reclist"]

		for line in alist.splitlines():
			final = alist.replace("\n", "\n`###`\u2800")

		if len(final) > 1:
			paginator = WrappedPaginator(prefix=f"**`{member.name}`'𝘀 𝗔𝗻𝗶𝗺𝗲 𝗥𝗲𝗰𝗼𝗺𝗺𝗲𝗻𝗱𝗮𝘁𝗶𝗼𝗻𝘀:**\n", suffix='', max_size = 500)
			paginator.add_line(final)
			interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author)
			await interface.send_to(ctx)




	@reclist.command()
	async def set(self, ctx, *, args):

		user = ctx.author

		users = await get_arec_data()

		users[str(user.id)] = {}
		users[str(user.id)]['reclist'] = f"`###`\u2800{args}"

		with open("AnimeList.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.message.delete()
		await ctx.send(f"Reclist set! {user.mention}")



	@reclist.command()
	async def add(self, ctx, *, args):

		user = ctx.author

		users = await get_arec_data()
		
		if not str(user.id) in users:
			users[str(user.id)] = {}
			users[str(user.id)]["reclist"] = f"`###`\u2800{args}"

			with open("AnimeList.json", "w", encoding='utf-8') as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)

		else:
			thechange = f"\n{args}"

			await update_arec(user, thechange)
		
		await ctx.message.delete()
		await ctx.send("Succesfully added to your reclist! {}".format(user.mention))



	@reclist.command()
	async def raw(self, ctx):

		users = await get_arec_data()

		user_list = users[str(ctx.author.id)]["reclist"]

		final = user_list[6:]

		paginator = WrappedPaginator(prefix='```CSS', suffix='```', max_size = 375)
		paginator.add_line(final)
		interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author)
		await interface.send_to(ctx)


	@reclist.command()
	async def delete(self, ctx):

		users = await get_arec_data()

		del users[str(ctx.author.id)]

		with open("AnimeList.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Succesfully deleted your reclist! {}".format(ctx.author.mention))
		return





	@reclist.command()
	@commands.is_owner()
	async def remove(self, ctx, user : discord.Member):

		users = await get_arec_data()

		del users[str(user.id)]

		with open("AnimeList.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Succesfully deleted `{}`'s reclist!".format(user.display_name))


	@commands.Cog.listener()
	async def on_member_remove(self, member):

		users = await get_arec_data()
		try:
			del users[str(member.id)]

			with open("AnimeList.json", "w", encoding="utf-8") as f:
				json.dump(users, f, ensure_ascii = False, indent = 4)
		except KeyError:
			pass








	@reclist.error
	async def reclist_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("User does not have any reclist!")
		elif isinstance(error, commands.TooManyArguments):
			return










async def get_arec_data():
	with open("AnimeList.json", "r") as f:
		users = json.load(f)

	return users

async def update_arec(user, change = "\n", mode = "reclist"):
	users = await get_arec_data()
	users[str(user.id)][mode] += change
	
	with open("AnimeList.json", "w", encoding="utf-8") as f:
		json.dump(users, f, ensure_ascii = False, indent = 4)

	areclist = users[str(user.id)]["reclist"]
	return areclist


def setup(client):
	client.add_cog(Reclist(client))