import discord
from discord.ext import commands
import asyncio
import datetime
from utils import time

nono_list = [
				"staff",
				"mod"
			]

class CustomRoles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db1['Custom Roles']
		self.prefix = '!'
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")	
	async def cr(self, ctx):
		"""Invokes this command."""

		await ctx.send_help('cr')


	@cr.command(name='create')
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def cr_create(self, ctx):
		"""Create your custom role."""

		guild = self.bot.get_guild(750160850077089853)
		user = ctx.author
		channel = ctx.message.channel
		usercheck = ctx.author.id

		results = await self.db.find_one({"_id": user.id})
		def check(message):
			return message.author.id == usercheck and message.channel.id == channel.id

		if results != None:
			await ctx.send("You already have a custom role.")
			return

		else:
			await channel.send("What do you want your custom role to be named as?\n\n*To cancel type `!cancel`*")

			try:
				while True:
					crname = await self.bot.wait_for('message', timeout=50, check=check)
					if crname.content.lower() in nono_list:
						await ctx.send("You tried, but no, lol!")

					elif len(crname.content.lower()) >= 20:
						await ctx.send("The name of the custom role cannot be longer than `20` characters.")

					elif crname.content.lower() == "!cancel":
						await ctx.send("Canceled. %s" % (ctx.author.mention))
						return
					
					else:
						break

			except asyncio.TimeoutError:
				await ctx.send("Ran out of time.")
				return

			else:
				await ctx.send("What color do u want it to have, please give the hex code.\nExample: `#ffffff`")

				try:
					while True:
						crcolor = await self.bot.wait_for('message', timeout=50, check=check)
						crcolor = crcolor.content.lower()
						if crcolor == '!cancel':
							await ctx.send("Canceled. %s" % (ctx.author.mention))
							return
						if "#" in crcolor:
							crcolor = crcolor.replace("#", "")
							crcolor = f"0x{crcolor}"
							try:
								e = discord.Color(int(crcolor, 16))
								break
							except:
								await ctx.send("Invalid hex colour.")
								pass
						else:
							await ctx.send("Invalid hex colour.")


				except asyncio.TimeoutError:
					await ctx.send("Ran out of time.")
					return

				else:
					for role in guild.roles:
						if crname.content in role.name:
							await ctx.send("A role with that name already exists!")
							return
					
					newcr = await guild.create_role(name=crname.content, color=discord.Color(int(crcolor, 16)))

					await ctx.author.add_roles(newcr)

					post = {"_id": user.id,
							"CustomRoleName": crname.content,
							"roleID": newcr.id,
							"shares": 0,
							"createdAt": datetime.datetime.utcnow()
							}
					await self.db.insert_one(post)

					positions = {
						newcr: 125
					}
					await guild.edit_role_positions(positions=positions)

					await ctx.send("The role has been created and now you have it!")

	@cr.group(invoke_without_command = True, case_insensitive = True, name='edit')
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def cr_edit(self, ctx):
		"""Invokes `!help cr edit`."""

		await ctx.send_help('cr edit')

	@cr_edit.command()
	async def color(self, ctx, new_color: str = None):
		"""Edit the colour of your custom role."""

		user = ctx.author
		guild = self.bot.get_guild(750160850077089853)
		
		results = await self.db.find_one({"_id": user.id})

		if results is None:
			await ctx.send("You must have a custom role to edit! Type: `!cr create` to create your custom role.")
			return

		get_role = results['CustomRoleName']
	
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

	@cr_edit.command()
	async def name(self, ctx, *, new_name: str = None):
		"""Edit the name of your custom role."""

		user = ctx.author
		guild = self.bot.get_guild(750160850077089853)

		results = await self.db.find_one({"_id": user.id})

		if results == None:
			await ctx.send("You must have a custom role to edit! Type: `!cr create` to create your custom role.")
			return

		get_role = results['CustomRoleName']

		crname = discord.utils.get(guild.roles, name=get_role)
		em = discord.Embed(title="Custom Role Edited")
		
		if new_name == None:
			await ctx.send("You must provide the new name!")
			return
		
		elif new_name.lower() in nono_list:
			await ctx.send("You tried, but no, lol!")
			return

		else:
			await self.db.update_one({"_id": ctx.author.id}, {"$set":{"CustomRoleName": new_name}})
			await crname.edit(name=new_name)
			em.add_field(name="New Name", value=f"`{new_name}`")
			em.color = crname.color
			await ctx.send(embed=em)

	@cr.command()
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def share(self, ctx, member: discord.Member = None):
		"""Share your custom role with a member."""

		if member is None:
			await ctx.send("You must specify the user that you're sharing the role to!")
			return
		user = ctx.author
		guild = self.bot.get_guild(750160850077089853)

		results = await self.db.find_one({"_id": user.id})

		if results is None:
			await ctx.send("You do not have a custom role to share!")
			return

		get_role = results['CustomRoleName']
		
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
			reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)
		
		except asyncio.TimeoutError:
			new_msg = f"{member.mention} Did not react in time."
			await msg.edit(content=new_msg)
			await msg.clear_reactions()
			return
		else:
			if str(reaction.emoji) == '<:agree:797537027469082627>':
				await self.db.update_one({'roleID': crname.id}, {'$inc':{'shares': 1}})
				await member.add_roles(crname)
				em = discord.Embed(color=user.color, title=f"{member} has accepted your role")
				em.set_image(url="https://blog.hubspot.com/hubfs/giphy_1-1.gif")
				await ctx.send(ctx.author.mention, embed=em)
				return

			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				await ctx.send(f"**{member}** has denied your role {ctx.author.mention}")
				return


	@cr.command(name='info')
	async def cr_info(self, ctx, *, role: int = None):
		"""Get some data about a custom role, it doesn't have to be yours, but the <role> parameter must be a ingere (the role's id)."""

		if role == None:
			await ctx.send("You must give the role ID, to get it use `!role-id <role_name>`")
			return
		
		result = await self.db.find_one({'roleID': role})

		if result is None:
			return await ctx.send("That is not a custom role.")

		createdAt = result['createdAt']
		shares = result['shares']
		roleName = result['CustomRoleName']
		index = 0
		guildRole = ctx.guild.get_role(role)
		for m in ctx.guild.members:
			if guildRole in m.roles:
				index += 1
		roleOwner = ctx.guild.get_member(result['_id'])
		
		def format_date(dt):
				if dt is None:
					return 'N/A'
				return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

		em = discord.Embed(color=guildRole.color, title="Role Info About `%s`" % (roleName))
		em.add_field(name="Custom Role Owner", value=roleOwner, inline=False)
		em.add_field(name="Hex Code", value=guildRole.color, inline=False)
		em.add_field(name="People That Have The Role", value=index, inline=False)
		em.add_field(name="Total Role Shares", value=shares, inline = False)
		em.add_field(name="Created At", value="%s" % (format_date(createdAt)), inline=False)

		await ctx.send(embed=em)


	@cr.command()
	async def unrole(self, ctx, *, role : int = None):
		"""Remove a custom role from your roles, the <role> parameter must be a integer (role's id)."""

		if role == None:
			await ctx.send("You must give the role ID, to get it use `!role-id <role_name>`")
			return
		guild = self.bot.get_guild(750160850077089853)
		cr = guild.get_role(role)
		
		results = await self.db.find_one({"CustomRoleName": cr.name})
		if results is None:
			await ctx.send("That is not a custom role!")
			return
		try:
			owner = results['_id']

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
		"""Remove all of your custom roles from your roles ***except*** your own custom role."""

		all_cr = []
		results = await self.db.find().to_list(100000)
		guild = self.bot.get_guild(750160850077089853)
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

	@cr.command(name='delete')
	@commands.has_any_role('Mod', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def cr_delete(self, ctx):
		"""Delete your custom role."""

		user = ctx.author
		guild = self.bot.get_guild(750160850077089853)

		results = await self.db.find_one({"_id": user.id})

		if results is None:
			await ctx.send("You do not have a custom role! Type: `!cr create` to create your role!")
			return

		get_role = results['CustomRoleName']

		def check(reaction, user):
				return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id

		crname = discord.utils.get(guild.roles, name=get_role)
		msg = await ctx.send("Are you sure you want to delete your custom role (<@&{}>)?".format(crname.id))
		await msg.add_reaction('<:agree:797537027469082627>')
		await msg.add_reaction('<:disagree:797537030980239411>')
		
		try:
				reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)

		except asyncio.TimeoutError:
			new_msg = f"{ctx.author.mention} Did not react in time."
			await msg.edit(content=new_msg)
			await msg.clear_reactions()
			return

		else:
			if str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = "Your custom role has not been deleted. %s" % (ctx.author.mention)
				await msg.edit(content=e)
				await msg.clear_reactions()
				return

			elif str(reaction.emoji) == '<:agree:797537027469082627>':
				await crname.delete()
				await self.db.delete_one({"_id": ctx.author.id})
				e = "Succesfully deleted your custom role! {}".format(ctx.author.mention)
				await msg.edit(content=e)
				await msg.clear_reactions()
				return

	@commands.command(name='role-id')
	async def _role_id(self, ctx, *, role_name : str = None):
		"""Get the role id from the name of a role."""

		if role_name is None:
			await ctx.send("You must give the role name that you want the ID for!")
			return
		guild = self.bot.get_guild(750160850077089853)
		role = discord.utils.get(guild.roles, name=role_name)
		
		try:
			await ctx.send(f"**{role.name}**'s role ID **-->** `{role.id}`")
		except AttributeError:
			await ctx.send("That is not a valid role!")


	@cr_delete.error
	async def delete_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("You do not have any custom role! What are you trying to delete???\nType `!cr create` to create your custom role!")
		else:
			await self.bot.reraise(ctx, error)

	@unrole.error
	async def unrole_error(self, ctx, error):
		if isinstance(error, commands.errors.BadArgument):
			await ctx.send("That is not a role id! To get the role's ID please type `!role-id <role_name>`")
		else:
			await self.bot.reraise(ctx, error)

	@cr_info.error
	async def info_error(self, ctx, error):
		if isinstance(error, commands.errors.BadArgument):
			await ctx.send("That is not a role id! To get the role's ID please type `!role-id <role_name>`")
		else:
			await self.bot.reraise(ctx, error)

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You must be at least `level 40+` in order to use this command! %s" % (ctx.author.mention))
		else:
			await self.bot.reraise(ctx, error)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = self.bot.get_guild(750160850077089853)
		results = await self.db.find_one({"_id": member.id})
		if results != None:
			get_role = results['CustomRoleName']
			crname = discord.utils.get(guild.roles, name=get_role)
			await crname.delete()
			await self.db.delete_one({"_id": member.id})
		






def setup(bot):
	bot.add_cog(CustomRoles(bot))