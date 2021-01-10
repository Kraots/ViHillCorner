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
		await ctx.send("`!cr create`\n`!cr delete`\n`!cr edit color <new_color>`\n`!cr edit name <new_name>`\n`!cr share <user>`\n`!cr unrole <cr_id>`")






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
					for role in guild.roles:
						if crname.content in role.name:
							await ctx.send("A role with that name already exists!")
							return
					
					newcr = await guild.create_role(name=crname.content, color=discord.Color(int(crcolor, 16)))

					await ctx.author.add_roles(newcr)

					post = {"_id": user.id, "CustomRoleName": crname.content}
					collection.insert_one(post)

					positions = {
						newcr: 65
					}
					await guild.edit_role_positions(positions=positions)

					await ctx.send("The role has been created and now you have it!")

	@cr.group(invoke_without_command = True, case_insensitive = True)
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def edit(self, ctx):
		await ctx.send("`!cr edit color <new_color>`\n`!cr edit name <new_name>`")

	@edit.command()
	async def color(self, ctx, new_color: str = None):
		user = ctx.author
		guild = self.client.get_guild(750160850077089853)

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		resultss = collection.find({"_id": user.id})

		for info in resultss:
			get_role = info['CustomRoleName']
		
		if not ctx.author.id in all_users:
			await ctx.send("You must have a custom role to edit! Type: `!cr create` to create your custom role.")
			return
		
		else:
			crname = discord.utils.get(guild.roles, name=get_role)
			em = discord.Embed(title="Custom Role Edited")

			if new_color == None:
				await ctx.send("You must provide the new color!")
				return
			
			else:
				if new_color.startswith("#"):
					new_color = new_color.replace("#", "")
					new_color = f"0x{new_color}"
				else:
					await ctx.send("Invalid Color Hex!\nExample: `#ffffff`")
					return
				
				try:
					await crname.edit(color=discord.Color(int(new_color, 16)))
					em.add_field(name="New Color", value=f"`#{new_color[2:]}`")
					em.color = crname.color
					await ctx.send(embed=em)
				
				except ValueError:
					await ctx.send("Invalid Color Hex!\nExample: `#ffffff`")

	@edit.command()
	async def name(self, ctx, *, new_name: str = None):
		user = ctx.author
		guild = self.client.get_guild(750160850077089853)

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		resultss = collection.find({"_id": user.id})

		for info in resultss:
			get_role = info['CustomRoleName']
		
		if not ctx.author.id in all_users:
			await ctx.send("You must have a custom role to edit! Type: `!cr create` to create your custom role.")
			return
		
		else:
			crname = discord.utils.get(guild.roles, name=get_role)
			em = discord.Embed(title="Custom Role Edited")

			if new_name == None:
				await ctx.send("You must provide the new name!")
				return
			
			elif new_name.lower() in nono_list:
				await ctx.send("You tried, but no, lol!")
				return

			else:
				collection.update_one({"_id": ctx.author.id}, {"$set":{"CustomRoleName": new_name}})
				await crname.edit(name=new_name)
				em.color = crname.color
				await ctx.send(embed=em)

	@cr.command()
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def share(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send("You must specify the user that you're sharing the role to!")
			return
		user = ctx.author
		guild = self.client.get_guild(750160850077089853)

		all_users = []
		results = collection.find()
		for result in results:
			all_users.append(result['_id'])
		
		resultss = collection.find({"_id": user.id})

		for info in resultss:
			get_role = info['CustomRoleName']
		
		if ctx.author.id in all_users:
			crname = discord.utils.get(guild.roles, name=get_role)
			if crname in member.roles:
				await ctx.send("You already shared your custom role with that user!")
				return
			msg = await ctx.send(f"{member.mention} Do you accept the role <@&{crname.id}> from {user.mention}?\n\n**Note:** Any changes made to the role by {user.mention} would apply to everyone holding the role.")
			await msg.add_reaction('<:agree:797537027469082627>')
			await msg.add_reaction('<:disagree:797537030980239411>')
			
			def check(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == member.id
			
			try:
				reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)
			
			except asyncio.TimeoutError:
				msg.edit(f"{member.mention} Did not react in time.")
				return
			else:
				if str(reaction.emoji) == '<:agree:797537027469082627>':
					await member.add_roles(crname)
					em = discord.Embed(color=user.color, title=f"{member} has accepted your role")
					em.set_image(url="https://blog.hubspot.com/hubfs/giphy_1-1.gif")
					await ctx.send(ctx.author.mention, embed=em)
					return

				elif str(reaction.emoji) == '<:disagree:797537030980239411>':
					await ctx.send(f"**{member}** has denied your role {ctx.author.mention}")
					return
		else:
			await ctx.send("You do not have a custom role to share!")




	@cr.command()
	async def unrole(self, ctx, *, role : int = None):
		if role is None:
			await ctx.send("You must specfiy the role you want to unrole!")
			return
		guild = self.client.get_guild(750160850077089853)
		cr = guild.get_role(role)
		
		all_cr = []
		results = collection.find()
		for result in results:
			all_cr.append(result['CustomRoleName'])
		try:
			if not cr.name in all_cr:
				await ctx.send("That is not a custom role!")
				return
			
			else:
				get_data = collection.find({"CustomRoleName": cr.name})
				for data in get_data:
					owner = data['_id']
				
				if ctx.author.id == owner:
					await ctx.send("You cannot remove that custom role because you're the owner of it! To remove it please type: `!cr delete`")
					return
				
				else:
					await ctx.author.remove_roles(cr)
					await ctx.send(f"Removed the role <@&{cr.id}> from your profile.")
		
		except AttributeError:
			await ctx.send("That is not a valid ID! Type: `!role-id <role_name>` to get the role's ID you want to remove from your profile.")
			return

	@cr.command()
	async def clean(self, ctx):
		all_cr = []
		results = collection.find()
		guild = self.client.get_guild(750160850077089853)
		for result in results:
			user = str(result['_id'])
			if str(ctx.author.id) != user:
				all_cr.append(result['CustomRoleName'])

		try:
			member_roles = []
			for x in ctx.author.roles:
				if not x.name in all_cr:
					member_roles.append(x.id)

			member_roles = set(member_roles)

			Roles = []
			for id in member_roles:
				role = guild.get_role(id)
				Roles.append(role)

		except:
			pass
		
		await ctx.author.edit(roles=Roles)
		await ctx.send("Succesfully cleaned all the cr's on your profile.")

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

			crname = discord.utils.get(guild.roles, name=get_role)
			await ctx.reply("Are you sure you want to delete your custom role (<@&{}>)? `yes` | `no`".format(crname.id))

			try:

				reply = await self.client.wait_for('message', timeout=30, check=check)
				answer = reply.content
				if answer.lower() == "no":
					await ctx.send("Your custom role has not been deleted.")
					return

				elif answer.lower() == "yes":
					await crname.delete()

					collection.delete_one({"_id": ctx.author.id})

					await ctx.send("Succesfully deleted your custom role! {}".format(ctx.author.mention))

			except asyncio.TimeoutError:
				return

		else:
			await ctx.send("You do not have a custom role! Type: `!cr create` to create your role!")



	@commands.command(aliases=['role-id'])
	async def _role_id(self, ctx, *, role_name : str = None):
		if role_name is None:
			await ctx.send("You must give the role name that you want the ID for!")
			return
		guild = self.client.get_guild(750160850077089853)
		role = discord.utils.get(guild.roles, name=role_name)
		
		try:
			await ctx.send(f"{role.name}'s role ID **-->** `{role.id}`")
		except AttributeError:
			await ctx.send("That is not a valid role!")


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

	@unrole.error
	async def unrole_error(self, ctx, error):
		if isinstance(error, commands.errors.BadArgument):
			await ctx.send("That is not a role id! To get the role's ID please type `!role-id <role_name>`")
			return










	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = self.client.get_guild(750160850077089853)
		results = collection.find({"_id": member.id})
		for result in results:
			get_role = result['CustomRoleName']
			crname = discord.utils.get(guild.roles, name=get_role)
			await crname.delete()
		collection.delete_one({"_id": member.id})
		






def setup(client):
	client.add_cog(CustomRoles(client))