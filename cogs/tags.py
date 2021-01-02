import discord
from discord.ext import commands
import json
import asyncio
import datetime
import utils.colors as color
from utils.paginator import SimplePages
import re
from utils.paginator_v3 import WrappedPaginator, PaginatorEmbedInterface

filter_invite = re.compile("(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")


class TagPageEntry:
	def __init__(self, entry):
		
		with open("tags.json", "r") as f:
			entries = json.load(f)

		self.name = entries[entry]['the_tag_name']
		self.owner_id = entries[entry]['tag_owner_id']

	def __str__(self):
		return f'{self.name}\u2800•\u2800(`Owner:` <@!{self.owner_id}>)'

class TagPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [TagPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)


class Tags(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra = False)
	async def tag(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			await ctx.send("`!tag <tag_name>`")
			return

		else:
			tags = await get_tags_data()

			try:
				tag = tags[str(tag_name.lower())]["tag_content"]
				tags[str(tag_name.lower())]["uses_count"] += 1

				with open("tags.json", "w", encoding = "utf-8") as f:
					json.dump(tags, f, ensure_ascii = False, indent = 4)
			
				await ctx.send(tag)
			
			except KeyError:
				await ctx.send("Tag `{}` does not exist!".format(tag_name))


	@commands.command()
	async def tags(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		tags = await get_tags_data()

		tags_list = []
		index = 0
		
		for key in tags:
			owner_id = tags[str(key)]["tag_owner_id"]
			tag_owner = self.client.get_user(owner_id)

			if str(member) in str(tag_owner):
				tag_name = tags[str(key)]["the_tag_name"]
				get_snippet_create_date = tags[str(key)]["created_at"]

				fin = f"{tag_name} (`Created At`: {get_snippet_create_date})"

				if not tag_name in tags_list:
					index += 1
					indexed_row = f"{index}. {fin}"
					tags_list.append(indexed_row)

		result = "\n".join(tags_list)

		if len(result) > 35:
			paginator = WrappedPaginator(prefix = f"**`{member}`'𝘀 𝗢𝘄𝗻𝗲𝗱 𝗧𝗮𝗴𝘀** \n", suffix = '', max_size = 250)
			paginator.add_line(result)
			interface = PaginatorEmbedInterface(ctx.bot, paginator, owner = ctx.author)

			await interface.send_to(ctx)

	@tag.command()
	async def list(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		tags = await get_tags_data()

		tags_list = []
		index = 0
		
		for key in tags:
			owner_id = tags[str(key)]["tag_owner_id"]
			tag_owner = self.client.get_user(owner_id)

			if str(member) in str(tag_owner):
				tag_name = tags[str(key)]["the_tag_name"]
				get_snippet_create_date = tags[str(key)]["created_at"]

				fin = f"{tag_name} (`Created At`: {get_snippet_create_date})"

				if not tag_name in tags_list:
					index += 1
					indexed_row = f"{index}. {fin}"
					tags_list.append(indexed_row)

		result = "\n".join(tags_list)

		if len(result) > 1:
			paginator = WrappedPaginator(prefix = f"**`{member}`'𝘀 𝗢𝘄𝗻𝗲𝗱 𝗧𝗮𝗴𝘀** \n", suffix = '', max_size = 250)
			paginator.add_line(result)
			interface = PaginatorEmbedInterface(ctx.bot, paginator, owner = ctx.author)

			await interface.send_to(ctx)


	@tag.command()
	async def all(self, ctx):
		entries = await get_tags_data()
		p = TagPages(entries = entries, per_page = 7)
		await p.start(ctx)

	@tag.command(aliases=['lb'])
	async def leaderboard(self, ctx, x=10):
		tags = await get_tags_data()

		leader_board = {}
				
		for uid, details in tags.items():  
			tag_namee = tags[str(uid)]["the_tag_name"]  
			leader_board[tag_namee] = details['uses_count']  
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True) 
		
		em = discord.Embed(color=discord.Color.blurple(), title=f"Top `{x}` Tags")

		for index, (mem, amt) in enumerate(leader_board[:x], start = 1):
			uses = tags[str(mem)]["uses_count"]
			owner_id = tags[str(mem)]["tag_owner_id"]
			owner = self.client.get_user(owner_id)
			em.add_field(name=f"_ _ \n{index}#\u2800`{mem}`", value=f"Uses:\n\u2800`{uses}`\nOwner:\n\u2800`{owner}`", inline=True)
			
			if index == x:
				break
			
			else:
				index += 1

		em.set_footer(text="Requested by: {}".format(ctx.author), icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=em)


	@tag.command()
	async def info(self, ctx, *, tag_name : str = None):
		tags = await get_tags_data()

		leader_board = {}
				
		for uid, details in tags.items():  
			tag_namee = tags[str(uid)]["the_tag_name"]  
			leader_board[tag_namee] = details['uses_count']  
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True) 

		for index2, (mem, amt) in enumerate(leader_board, start = 1):

			string1 = f"{index2} {mem}"
			string2 = f"{index2} {tag_name}"

			if string1 == string2:
				index=index2
				break
			else:
				index2 += 1


		if tag_name is None:
			await ctx.send("`!tag info <tag_name>`")
			return

		else:
			try:
				tag_name = tags[str(tag_name.lower())]["the_tag_name"]
				tag_owner_id = tags[str(tag_name.lower())]["tag_owner_id"]
				tag_uses = tags[str(tag_name.lower())]["uses_count"]
				tag_created_at = tags[str(tag_name.lower())]["created_at"]

				tag_owner = self.client.get_user(tag_owner_id)

				em = discord.Embed(color=color.blue, title=tag_name)
				em.set_author(name=tag_owner, url=tag_owner.avatar_url, icon_url=tag_owner.avatar_url)
				em.add_field(name="Owner", value=tag_owner.mention)
				em.add_field(name="Uses", value=tag_uses)
				em.add_field(name="Rank", value=f"`#{index}`")
				em.set_footer(text="Tag created at • {}".format(tag_created_at))

				await ctx.send(embed=em)

			except KeyError:
				await ctx.send("Tag `{}` does not exist!".format(tag_name))

	@tag.command(aliases=['make', 'add'])
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")	
	async def create(self, ctx, *, tag_name_constructor : str = None):
		tags = await get_tags_data()

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

				if str(tag_name) in tags:
					await ctx.send("Tag name already taken.")
					return
				
				elif len(tag_name) >= 35:
					await ctx.send("Tag's name canot be longer than `35` characters!")
					return
				
				elif len(tag_name) < 3:
					await ctx.send("Tag's name cannot be less than `3` characters long!")
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
					tags[str(tag_name)] = {}
					tags[str(tag_name)]["tag_content"] = tag_content
					tags[str(tag_name)]["tag_owner_id"] = ctx.author.id
					tags[str(tag_name)]["the_tag_name"] = tag_name
					tags[str(tag_name)]["created_at"] = get_time
					tags[str(tag_name)]["uses_count"] = 0
					with open("tags.json", "w", encoding="utf-8") as f:
						json.dump(tags, f, ensure_ascii = False, indent = 4)
					
					await ctx.send("Tag `{}` succesfully created!".format(tag_name))



		else:

			matches = re.findall(filter_invite, tag_name_constructor)
			for tag_name_constructor in matches:
				await ctx.send("No invites or what so ever.")
				return

			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			if str(tag_name_constructor) in tags:
				await ctx.send("Tag name already taken.")
				return
			
			elif len(tag_name_constructor) >= 35:
				await ctx.send("Tag's name canot be longer than `35` characters!")
				return
			elif len(tag_name_constructor) < 3:
					await ctx.send("Tag's name cannot be less than `3` characters long!")
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
				tags[str(tag_name_constructor)] = {}
				tags[str(tag_name_constructor)]["tag_content"] = tag_content
				tags[str(tag_name_constructor)]["tag_owner_id"] = ctx.author.id
				tags[str(tag_name_constructor)]["the_tag_name"] = tag_name_constructor
				tags[str(tag_name_constructor)]["created_at"] = get_time
				tags[str(tag_name_constructor)]["uses_count"] = 0
				with open("tags.json", "w", encoding="utf-8") as f:
					json.dump(tags, f, ensure_ascii = False, indent = 4)
				
				await ctx.send("Tag `{}` succesfully created!".format(tag_name_constructor))

	@tag.command()
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def delete(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			await ctx.send("`!tag delete <tag_name>`")
			return
		
		else:
			tags = await get_tags_data()
			try:
				the_tag_name = tags[str(tag_name)]["the_tag_name"]
				tag_owner = tags[str(tag_name)]["tag_owner_id"]

			except KeyError:
				await ctx.send("Tag does not exist!")
				return
			
			else:
				if ctx.author.id != tag_owner:
					await ctx.send("You do not own this tag, therefore, you cannot delete it.")
					return
				
				else:
					await ctx.send("Are you sure you want to delete the tag `{}` ? `yes` | `no`".format(the_tag_name))
					
					def check(m):
						return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
					
					try:
						response = await self.client.wait_for('message', timeout=60, check=check)
						if response.content.lower() == "no":
							await ctx.send("Tag has not been deleted.")
						
						elif response.content.lower() == "yes":
							del tags[str(tag_name)]

							with open("tags.json", "w", encoding = "utf-8") as f:
								json.dump(tags, f, ensure_ascii = False, indent = 4)
							
							await ctx.send("Tag deleted succesfully.")
					
					except asyncio.TimeoutError:
						await ctx.send("Time expired!")
						return


	@tag.command()
	@commands.is_owner()
	async def remove(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			await ctx.send("`!tag delete <tag_name>`")
			return
		
		else:
			tags = await get_tags_data()
			try:
				the_tag_name = tags[str(tag_name)]["the_tag_name"]
				get_tag_owner = tags[str(tag_name)]["tag_owner_id"]
				tag_created_at = tags[str(tag_name)]["created_at"]
				tag_owner = self.client.get_user(get_tag_owner)

			except KeyError:
				await ctx.send("Tag does not exist!")
				return
			
			else:
			
				del tags[str(tag_name)]

				with open("tags.json", "w", encoding = "utf-8") as f:
					json.dump(tags, f, ensure_ascii = False, indent = 4)
				
				em = discord.Embed(title="Tag Deleted", color=color.red)
				em.add_field(name = "Name", value = the_tag_name)
				em.add_field(name = "Owner", value = tag_owner)
				em.set_footer(text=f"Tag created at • {tag_created_at}")

				await ctx.send(embed=em)
		

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		tags = await get_tags_data()

		for key in tags:
			the_owner = tags[str(key)]["tag_owner_id"]

			if member.id == the_owner:
				del tags[str(key)]

				with open("tags.json", "w", encoding = "utf-8") as f:
					json.dump(tags, f, ensure_ascii = False, indent = 4)


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



async def get_tags_data():
	with open("tags.json", "r") as f:
		tags = json.load(f)
	
	return tags


def setup(client):
	client.add_cog(Tags(client))