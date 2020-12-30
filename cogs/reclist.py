import discord
from discord.ext import commands
import json

class Birthdays(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def reclist(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		await open_arec(member)
		user = member
		users = await get_arec_data()

		alist = users[str(user.id)]["reclist"]

		for line in alist.splitlines():
			final = alist.replace("\n", "\n`###`\u2800")

		em = discord.Embed(color=member.color, title=f"{member.name}'s Anime Recommendations:", description = f"`###`\u2800{final}")
		em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)




	@reclist.command()
	async def set(self, ctx, *, args):
		await open_arec(ctx.author)

		user = ctx.author

		users = await get_arec_data()

		users[str(user.id)] = {}
		users[str(user.id)]['reclist'] = args

		with open("AnimeList.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.message.delete()
		await ctx.send(f"Reclist set! {user.mention}")



	@reclist.command()
	async def add(self, ctx, *, args):
		await open_arec(ctx.author)

		user = ctx.author

		thechange = f"\n{args}"

		await update_arec(user, thechange)
		await ctx.message.delete()
		await ctx.send("Succesfully added to your reclist! {}".format(user.mention))






	@reclist.command(aliases=['remove'])
	async def delete(self, ctx):
		await open_arec(ctx.author)

		users = await get_arec_data()

		del users[str(ctx.author.id)]

		with open("AnimeList.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Succesfully deleted your reclist! {}".format(ctx.author.mention))



	@reclist.error
	async def reclist_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("User does not have any reclist!")














async def open_arec(user):

	users = await get_arec_data()

	if str(user.id) in users:
		return False


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
	client.add_cog(Birthdays(client))