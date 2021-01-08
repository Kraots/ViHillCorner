import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient
import os

DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Custom Roles"]

nono_list = [
				"staff",
				"mod"
			]

class CustomRoles(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")	
	async def cr(self, ctx):
		await ctx.send("`!cr create` | `!cr delete`")






	@cr.command()
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def create(self, ctx):
		guild = self.client.get_guild(750160850077089853)
		user = ctx.author
		channel = ctx.message.channel
		usercheck = ctx.author.id

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])

		def check(message):
			return message.author.id == usercheck and message.channel.id == channel.id

		if ctx.author.id in all_users:
			await ctx.send("You already have a custom role.")
			return

		else:

			await channel.send("What do you want your custom role to be named as?")

			try:
				crname = await self.client.wait_for('message', timeout=50, check=check)
				if crname.content.lower() in nono_list:
					await ctx.send("You tried, but no, lol!")
					return

				elif len(crname.content.lower()) >= 20:
					await ctx.send("The name of the custom role cannot be longer than `20` characters.")
					return

				elif crname.content.lower() == "cancel":
					await ctx.send("Canceled.")
					return

			except asyncio.TimeoutError:
				return

			else:
				
				await ctx.send("What color do u want it to have, please give the hex code.\nExample: `#ffffff`")

				try:
					precolor = await self.client.wait_for('message', timeout=50, check=check)
					thecolor = precolor.content
					if "#" in thecolor:
						thefinalcolor = thecolor.replace("#", "")
						crcolor = f"0x{thefinalcolor}"


				except asyncio.TimeoutError:
					return

				else:
					newcr = await guild.create_role(name=crname.content, color=discord.Color(int(crcolor, 16)))

					await ctx.author.add_roles(newcr)

					post = {"_id": user.id, "CustomRoleName": crname.content}
					collection.insert_one(post)

					positions = {
						newcr: 65
					}
					await guild.edit_role_positions(positions=positions)

					await ctx.send("The role has been created and now you have it!")




	@cr.command()
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def delete(self, ctx):
		user = ctx.author
		channel = ctx.message.channel
		usercheck = ctx.author.id
		guild = self.client.get_guild(750160850077089853)

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		resultss = collection.find({"_id": user.id})

		for info in resultss:
			get_role = info['CustomRoleName']
		
		if ctx.author.id in all_users:

			def check(message):
				return message.author.id == usercheck and message.channel.id == channel.id

			await ctx.reply("Are you sure you want to delete your custom role? `yes` | `no`")

			try:

				reply = await self.client.wait_for('message', timeout=30, check=check)
				answer = reply.content
				if answer.lower() == "no":
					return

				elif answer.lower() == "yes":
					crname = discord.utils.get(guild.roles, name=get_role)
					await crname.delete()

					collection.delete_one({"_id": ctx.author.id})

					await ctx.send("Succesfully deleted your custom role! {}".format(ctx.author.mention))

			except asyncio.TimeoutError:
				return

		else:
			await ctx.send("You do not have a custom role! Type: `!cr create` to create your role!")



	@delete.error
	async def delete_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("You do not have any custom role! What are you trying to delete???\nType `!cr create` to create your custom role!")

	@create.error
	async def create_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("The name is too long or the hex color you put is invalid.")

	@cr.error
	async def cr_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You need to be `lvl 40+` to use this command!")











	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection.delete_one({"_id": member.id})
		






def setup(client):
	client.add_cog(CustomRoles(client))