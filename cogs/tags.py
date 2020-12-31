import discord
from discord.ext import commands
import json
import asyncio
import datetime
import utils.colors as color
from utils.paginator import SimplePages



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

	@commands.group(invoke_without_command=True, case_insensitive=True)
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



	@tag.command()
	async def all(self, ctx):
		entries = await get_tags_data()
		p = TagPages(entries = entries, per_page = 7)
		await p.start(ctx)



	@tag.command()
	async def info(self, ctx, *, tag_name : str = None):
		tags = await get_tags_data()

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
				em.set_footer(text="Tag created at • {}".format(tag_created_at))

				await ctx.send(embed=em)

			except KeyError:
				await ctx.send("Tag `{}` does not exist!".format(tag_name))

	@tag.command()
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

				if str(tag_name) in tags:
					await ctx.send("Tag name already taken.")
					return
				
				elif len(tag_name) >= 30:
					await ctx.send("Tag's name canot be longer than `30` characters!")
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
			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			if str(tag_name_constructor) in tags:
				await ctx.send("Tag name already taken.")
				return
			
			elif len(tag_name_constructor) >= 30:
				await ctx.send("Tag's name canot be longer than `30` characters!")
				return

			await ctx.send("Please send the tag's content. {}".format(ctx.author.mention))
			try:
				pre_tag_content = await self.client.wait_for('message', timeout=420, check=check)
				if pre_tag_content.attachments:
					await ctx.send("Tag cannot contain attachments!")
					return					
				else:
					tag_content = pre_tag_content.content

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



async def get_tags_data():
	with open("tags.json", "r") as f:
		tags = json.load(f)
	
	return tags

def setup(client):
	client.add_cog(Tags(client))