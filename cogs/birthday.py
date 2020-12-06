import discord
from discord.ext import commands
import json
import utils.colors as color

class Birthdays(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True)
	async def birthday(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		await open_birthday(member)
		user = member
		users = await get_birthday_data()

		birthday = users[str(user.id)]["birthdaydate"]

		em = discord.Embed(color=color.blue, title=f"{member.name}'s Birthay is on:", description = f"`{birthday}`")
		em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em)

	@birthday.command()
	async def set(self, ctx, *, args):
		await open_birthday(ctx.author)

		users = await get_birthday_data()

		del users[str(ctx.author.id)]["birthdaydate"]
		
		await update_birthday(ctx.author, args)
		await ctx.send(f"Succesfully set your birthday to `{args}`.")

	@birthday.command(aliases=['remove'])
	async def delete(self, ctx):
		await open_birthday(ctx.author)

		users = await get_birthday_data()

		del users[str(ctx.author.id)]["birthdaydate"]

		reseted = "Birthday not set!"

		await update_birthday(ctx.author, reseted)
		await ctx.send("Succesfully deleted your birthday from the list!")



	@set.error
	async def birthday_set_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("**Please specify your birthday!**")
			


















async def open_birthday(user):

	users = await get_birthday_data()

	if str(user.id) in users:
		return False

	else:
		users[str(user.id)] = {}
		users[str(user.id)]['birthdaydate'] = "Birthday not set!"

	with open("birthdaylist.json", "w") as f:
		json.dump(users, f)

	return True

async def get_birthday_data():
	with open("birthdaylist.json", "r") as f:
		users = json.load(f)

	return users

async def update_birthday(user, change = "Birthday not set!", mode = "birthdaydate"):
	users = await get_birthday_data()
	users[str(user.id)][mode] = change
	
	with open("birthdaylist.json", "w") as f:
		json.dump(users, f)

	bal = users[str(user.id)]["birthdaydate"]
	return bal


def setup(client):
	client.add_cog(Birthdays(client))