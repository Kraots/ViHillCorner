import discord
from discord.ext import commands
import asyncio
import datetime
import utils.colors as color
from utils.paginator import SimplePages
import re
from pymongo import MongoClient
import os
DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Tags"]

filter_invite = re.compile("(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")


class TagPageEntry:
	def __init__(self, entry):

		self.name = entry['the_tag_name']
		self.id = entry['_id']

	def __str__(self):
		return f'{self.name}\u2800•\u2800(`ID:` **{self.id}**)'

class TagPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [TagPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)


class Tags(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra = False)
	async def tag(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			await ctx.send("`!tag <tag_name>`")
			return

		else:
			all_names = []
			results = collection.find()
			for result in results:
				all_names.append(result['the_tag_name'])
			if tag_name.lower() in all_names:
				get_tag = collection.find({"the_tag_name": tag_name.lower()})

				for data in get_tag:
					tag = data['tag_content']
					collection.update_one({"_id": data['_id']}, {"$inc":{"uses_count": 1}})
				await ctx.send(tag)
				return
		
			else:
				try:
					tag_name = int(tag_name)
				except ValueError:
					await ctx.send(f"Tag `{tag_name}` does not exist!")
					return

				all_ids = []
				get_ids = collection.find()
				for id in get_ids:
					all_ids.append(id['_id'])
				
				if not tag_name in all_ids:
					await ctx.send("That tag does not exist!")
					return
				
				else:
					get_data = collection.find({"_id": tag_name})

					for info in get_data:
						tag = info['tag_content']
						collection.update_one({"_id": info['_id']}, {"$inc":{"uses_count": 1}})
					await ctx.send(tag)



	@commands.command()
	async def tags(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		all_users = []
		results = collection.find({})
		for result in results:
			all_users.append(result['tag_owner_id'])
		
		if member.id in all_users:
			entries = collection.find({"tag_owner_id": member.id})
			p = TagPages(entries = entries, per_page = 7)
			await p.start(ctx)

		else:
			await ctx.send("`{}` has no tags.".format(member))

	@tag.command()
	async def list(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		all_users = []
		results = collection.find({})
		for result in results:
			all_users.append(result['tag_owner_id'])
		
		if member.id in all_users:
			entries = collection.find({"tag_owner_id": member.id})
			p = TagPages(entries = entries, per_page = 7)
			await p.start(ctx)

		else:
			await ctx.send("`{}` has no tags.".format(member))


	@tag.command()
	async def all(self, ctx):
		entries = collection.find({})
		p = TagPages(entries = entries, per_page = 7)
		await p.start(ctx)
	

	@tag.command(aliases=['lb'])
	async def leaderboard(self, ctx):
		results = collection.find({}).sort([("uses_count", -1)]).limit(10)
		index = 0
		em = discord.Embed(color=discord.Color.blurple())
		for result in results:
			tag_name = result['the_tag_name']
			uses = result['uses_count']
			get_owner = result['tag_owner_id']
			owner = self.client.get_user(get_owner)
			index += 1
			em.add_field(name=f"`{index}`.\u2800{tag_name}", value=f"Uses: `{uses}`\n Owner: `{owner}`", inline=False)
		
		await ctx.send(embed=em)

	@tag.command()
	async def info(self, ctx, *, tag_name : str = None):

		results = collection.find({}).sort([('uses_count', -1)])
		index2 = 1
		for result in results:
			tag_namee = result['the_tag_name']
			string1 = f"{index2} {tag_namee}"
			string2 = f"{index2} {tag_name.lower()}"
			if string1 == string2:
				index = index2
				break
			else:
				index2 += 1

		if tag_name is None:
			await ctx.send("`!tag info <tag_name>`")
			return

		else:
			all_tags = []
			resultss = collection.find()
			for resultt in resultss:
				all_tags.append(resultt['the_tag_name'])
				



			if not tag_name.lower() in all_tags:
				try:
					tag_name = int(tag_name)
				except ValueError:
					await ctx.send(f"Tag `{tag_name}` does not exist!")
					return

				all_ids = []
				get_ids = collection.find()
				for id in get_ids:
					all_ids.append(id['_id'])
				
				if not tag_name in all_ids:
					await ctx.send("That tag does not exist!")
					return
				else:
					rresults = collection.find({}).sort([('uses_count', -1)])
					index3 = 1
					for z in rresults:
						tag_id = z['_id']
						string3 = f"{index3} {tag_id}"
						string4 = f"{index3} {tag_name}"
						if string3 == string4:
							index1 = index3
							break
						else:
							index3 += 1

					get_data = collection.find({"_id": tag_name})

					for data in get_data:
						tag_name = data["the_tag_name"]
						tag_owner_id = data["tag_owner_id"]
						tag_uses = data["uses_count"]
						tag_created_at = data["created_at"]
						the_id = data["_id"]

					tag_owner = self.client.get_user(tag_owner_id)

					em = discord.Embed(color=color.blue, title=tag_name)
					em.set_author(name=tag_owner, url=tag_owner.avatar_url, icon_url=tag_owner.avatar_url)
					em.add_field(name="Owner", value=tag_owner.mention)
					em.add_field(name="Uses", value=tag_uses)
					em.add_field(name="Rank", value=f"`#{index1}`")
					em.add_field(name="Tag ID",value="`{}`".format(the_id), inline= False)
					em.set_footer(text="Tag created at • {}".format(tag_created_at))

					await ctx.send(embed=em)
				return
			



			else:
				
				get_data = collection.find({"the_tag_name": tag_name.lower()})

				for data in get_data:
					tag_name = data["the_tag_name"]
					tag_owner_id = data["tag_owner_id"]
					tag_uses = data["uses_count"]
					tag_created_at = data["created_at"]
					the_tag_id = data["_id"]

				tag_owner = self.client.get_user(tag_owner_id)

				em = discord.Embed(color=color.blue, title=tag_name)
				em.set_author(name=tag_owner, url=tag_owner.avatar_url, icon_url=tag_owner.avatar_url)
				em.add_field(name="Owner", value=tag_owner.mention)
				em.add_field(name="Uses", value=tag_uses)
				em.add_field(name="Rank", value=f"`#{index}`")
				em.add_field(name="Tag ID",value="`{}`".format(the_tag_id), inline= False)
				em.set_footer(text="Tag created at • {}".format(tag_created_at))

				await ctx.send(embed=em)






	@tag.command(aliases=['make', 'add'])
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")	
	async def create(self, ctx, *, tag_name_constructor : str = None):
		results = collection.find({})

		all_names = []

		for result in results:
			db_tag_name = result["the_tag_name"]
			all_names.append(str(db_tag_name))

		if tag_name_constructor is None:
			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			await ctx.send("What do you want the tag to be named as?".format(ctx.author.mention))

			try:
				pre_tag = await self.client.wait_for('message', timeout=180, check=check)
				tag_name = pre_tag.content.lower()
				matches = re.findall(filter_invite, tag_name)

				for tag_name in matches:
					await ctx.send("No invites or what so ever.")
					return
				

				if str(tag_name) in all_names:
					await ctx.send("Tag name already taken.")
					return
				
				elif len(tag_name) >= 35:
					await ctx.send("Tag's name canot be longer than `35` characters!")
					return
				
				elif len(tag_name) < 2:
					await ctx.send("Tag's name cannot be less than `2` characters long!")
					return
					
				elif tag_name.isnumeric():
					await ctx.send("Tag name cannot be a number!")
					return
			except asyncio.TimeoutError:
				await ctx.send("Time expired. {}".format(ctx.author.mention))

			else:
				await ctx.send("Please send the tag's content. {}".format(ctx.author.mention))
				try:
					pre_tag_content = await self.client.wait_for('message', timeout=420, check=check)
					if pre_tag_content.attachments:
						await ctx.send("Tag cannot contain attachments!")
						return					
					else:
						tag_content = pre_tag_content.content
						matches = re.findall(filter_invite, tag_content)

						for tag_content in matches:
							await ctx.send("No invites or what so ever.")
							return

				except asyncio.TimeoutError:
					await ctx.send("Time expired. {}".format(ctx.author.mention))
					return
				
				else:
					get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
					get_sorted = collection.find({}).sort([("_id", -1)]).limit(1)
					
					for x in get_sorted:
						last_id = x['_id']
					
					post = {"_id": last_id + 1,
							"tag_content": tag_content, 
							"tag_owner_id": ctx.author.id, 
							"the_tag_name": tag_name.lower(), 
							"created_at": get_time, "uses_count": 0
							}
					
					collection.insert_one(post)
					
					await ctx.send("Tag `{}` succesfully created!".format(tag_name))
			return



		else:

			matches = re.findall(filter_invite, tag_name_constructor)
			for tag_name_constructor in matches:
				await ctx.send("No invites or what so ever.")
				return

			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			if str(tag_name_constructor) in all_names:
				await ctx.send("Tag name already taken.")
				return
			
			elif len(tag_name_constructor) >= 35:
				await ctx.send("Tag's name canot be longer than `35` characters!")
				return
			elif len(tag_name_constructor) < 2:
					await ctx.send("Tag's name cannot be less than `2` characters long!")
					return
			elif tag_name_constructor.isnumeric():
				await ctx.send("Tag name cannot be a number!")
				return

			await ctx.send("Please send the tag's content. {}".format(ctx.author.mention))
			
			try:
				pre_tag_content = await self.client.wait_for('message', timeout=420, check=check)
				if pre_tag_content.attachments:
					await ctx.send("Tag cannot contain attachments!")
					return					
				else:
					tag_content = pre_tag_content.content
					matches = re.findall(filter_invite, tag_content)

					for tag_content in matches:
						await ctx.send("No invites or what so ever.")
						return

			except asyncio.TimeoutError:
				await ctx.send("Time expired. {}".format(ctx.author.mention))
				return
			
			else:
				get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
				get_sorted = collection.find({}).sort([("_id", -1)]).limit(1)
				for x in get_sorted:
					last_id = x['_id']

				post = {"_id": last_id + 1,
						"tag_content": tag_content, 
						"tag_owner_id": ctx.author.id, 
						"the_tag_name": tag_name_constructor.lower(), 
						"created_at": get_time, "uses_count": 0
						}
					
				collection.insert_one(post)
				
				await ctx.send("Tag `{}` succesfully created!".format(tag_name_constructor))




	@tag.command()
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def delete(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			await ctx.send("`!tag delete <tag_name>`")
			return
		
		else:
			results = collection.find({})

			all_names = []

			for result in results:
				db_tag_name = result["the_tag_name"]
				all_names.append(str(db_tag_name))

			if not tag_name.lower() in all_names:
				try:
					tag_name = int(tag_name)
				except ValueError:
					await ctx.send(f"Tag `{tag_name}` does not exist!")
					return

				all_ids = []
				get_ids = collection.find()
				for id in get_ids:
					all_ids.append(id['_id'])
				
				if not tag_name in all_ids:
					await ctx.send("That tag does not exist!")
					return
				
				else:
					get_info = collection.find({"_id": tag_name})
					for info in get_info:
						the_tag_name = info['the_tag_name']
						tags_owner = info['tag_owner_id']
					
					if ctx.author.id != tags_owner:
						await ctx.send("You do not own this tag, therefore, you cannot delete it.")
						return
					else:
						msg = await ctx.send("Are you sure you want to delete the tag `{}` ? {}".format(the_tag_name, ctx.author.mention))
					
						def check(reaction, user):
							return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
						
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
							if str(reaction.emoji) == '<:disagree:797537030980239411>':
								e = "Tag has not been deleted. %s" % (ctx.author.mention)
								await msg.edit(content=e)
								await msg.clear_reactions()
								return
							
							elif str(reaction.emoji) == '<:agree:797537027469082627>':
								collection.delete_one({"_id": tag_name})
								
								e = "Tag `{}` deleted succesfully! {}".format(the_tag_name, ctx.author.mention)
								await msg.edit(content=e)
								await msg.clear_reactions()
								return
					return
			
			else:
				get_data = collection.find({"the_tag_name": tag_name.lower()})

				for data in get_data:
					the_tag_name = data["the_tag_name"]
					tag_owner = data["tag_owner_id"]
			
			if ctx.author.id != tag_owner:
				await ctx.send("You do not own this tag, therefore, you cannot delete it.")
				return
			
			else:
				msg = await ctx.send("Are you sure you want to delete the tag `{}` ?".format(the_tag_name))
				
				def check(reaction, user):
					return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
				
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
					if str(reaction.emoji) == '<:disagree:797537030980239411>':
						e = "Tag has not been deleted. %s" % (ctx.author.mention)
						await msg.edit(content=e)
						await msg.clear_reactions()
						return
					
					elif str(reaction.emoji) == '<:agree:797537027469082627>':
						collection.delete_one({"the_tag_name": the_tag_name.lower()})
						
						e = "Tag deleted succesfully. %s" % (ctx.author.mention)
						await msg.edit(content=e)
						await msg.clear_reactions()
						return






	@tag.command()
	@commands.is_owner()
	async def remove(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			await ctx.send("`!tag remove <tag_name>`")
			return
		
		results = collection.find({})

		all_names = []

		for result in results:
			db_tag_name = result["the_tag_name"]
			all_names.append(str(db_tag_name))

		if not tag_name in all_names:
			try:
				tag_name = int(tag_name)
			except ValueError:
				await ctx.send(f"Tag `{tag_name}` does not exist!")
				return

			all_ids = []
			get_ids = collection.find()
			for id in get_ids:
				all_ids.append(id['_id'])
			
			if not tag_name in all_ids:
				await ctx.send("That tag does not exist!")
				return
			
			else:
				get_info = collection.find({"_id": tag_name})
				for info in get_info:
					get_tag_owner = info['tag_owner_id']
					tag_owner = self.client.get_user(get_tag_owner)
					the_tag_name = info['the_tag_name']
					tag_created_at = info['created_at']
					uses = info['uses_count']
				
				collection.delete_one({"_id": tag_name})
				
				em = discord.Embed(title="Tag Removed", color=color.red)
				em.add_field(name = "Name", value = the_tag_name)
				em.add_field(name = "Owner", value = tag_owner)
				em.add_field(name="Uses", value=f"`{uses}`", inline = False)
				em.set_footer(text=f"Tag created at • {tag_created_at}")

				await ctx.send(embed=em)
		
		else:
			get_data = collection.find({"the_tag_name": tag_name})
					
			for data in get_data:
				get_tag_owner = data['tag_owner_id']
				tag_owner = self.client.get_user(get_tag_owner)
				the_tag_name = data['the_tag_name']
				tag_created_at = data['created_at']
				uses = data['uses_count']

			collection.delete_one({"the_tag_name": tag_name})

			em = discord.Embed(title="Tag Removed", color=color.red)
			em.add_field(name = "Name", value = the_tag_name)
			em.add_field(name = "Owner", value = tag_owner)
			em.add_field(name="Uses", value=f"`{uses}`", inline = False)
			em.set_footer(text=f"Tag created at • {tag_created_at}")

			await ctx.send(embed=em)




	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		collection.delete_many({"tag_owner_id": member.id})


	@create.error
	async def tag_create_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You need to be `lvl 15+` to use this command!")

	@delete.error
	async def tag_delete_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You need to be `lvl 15+` to use this command!")

	@tag.error
	async def tag_error(self, ctx, error):
		if isinstance(error, commands.TooManyArguments):
			return

def setup(client):
	client.add_cog(Tags(client))