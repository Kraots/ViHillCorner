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

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bday', 'b-day'])
	async def birthday(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		await open_birthday(member)
		user = member
		users = await get_birthday_data()

		birthday = users[str(user.id)]["birthdaydate"]

		em = discord.Embed(color=color.blue, description = f"_ _ \n`{birthday}`")
		em.set_author(name=f"{member.name}'s birthday is on:", url=member.avatar_url, icon_url=member.avatar_url)
		await ctx.send(embed=em)




	@birthday.command(aliases=['add'])
	async def set(self, ctx, *, args):
		await open_birthday(ctx.author)

		user = ctx.author

		users = await get_birthday_data()

		users[str(user.id)] = {}
		users[str(user.id)]['birthdaydate'] = args

		with open("birthdaylist.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.message.delete()
		await ctx.send(f"Birthday set to `{args}` {user.mention}")



	@birthday.command(aliases=['remove'])
	async def delete(self, ctx):
		await open_birthday(ctx.author)

		users = await get_birthday_data()

		del users[str(ctx.author.id)]

		with open("birthdaylist.json", "w", encoding="utf-8") as f:
			json.dump(users, f, ensure_ascii = False, indent = 4)

		await ctx.send("Succesfully deleted your birthday from the list! {}".format(ctx.author.mention))


	@birthday.error
	async def bday_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("User does not have any birthday set!")




















async def open_birthday(user):

	users = await get_birthday_data()

	if str(user.id) in users:
		return False

async def get_birthday_data():
	with open("birthdaylist.json", "r") as f:
		users = json.load(f)

	return users



def setup(client):
	client.add_cog(Birthdays(client))