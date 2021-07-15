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
	
	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra = False, aliases=['tags'])
	async def tag(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			command = self.bot.get_command('help')
			await ctx.invoke(command, 'tag')
			return
		data = {}

		get_by_name = collection.find({'the_tag_name': tag_name.lower()})
		for i in get_by_name:
			data = i
		if len(data) == 0:
			get_by_alias = collection.find({'aliases': tag_name.lower()})
			for i in get_by_alias:
				data = i
		if len(data) == 0:
			try:
				get_by_id = collection.find({'_id': int(tag_name)})
				for i in get_by_id:
					data = i
			except ValueError:
				return await ctx.send("No tag found. %s" % (ctx.author.mention))
		
		collection.update_one({'_id': data['_id']}, {'$inc':{'uses_count': 1}})
		await ctx.send(data['tag_content'], reference=ctx.replied_reference)


	@tag.command()
	async def search(self, ctx, *, query):
		query = str(query).lower()
		entries = collection.find({'the_tag_name': {'$regex': query, '$options': 'i'}})
		try:
			p = TagPages(entries = entries, per_page = 7)
			await p.start(ctx)
		except:
			await ctx.send('No tags found. %s' % (ctx.author.mention))
	

	@tag.command(aliases=['list'])
	async def _list(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		entries = collection.find({'tag_owner_id': member.id})
		try:
			p = TagPages(entries = entries, per_page = 7)
			await p.start(ctx)
		except:
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
			owner = self.bot.get_user(get_owner)
			index += 1
			em.add_field(name=f"`{index}`.\u2800{tag_name}", value=f"Uses: `{uses}`\n Owner: `{owner}`", inline=False)
		
		await ctx.send(embed=em)

	@tag.command()
	async def info(self, ctx, *, tag_name : str = None):
		if tag_name is None:
			return await ctx.reply("**!tag info <tag_name>**")

		data = {}
		results_name = collection.find({'the_tag_name': tag_name.lower()})
		for e in results_name:
			data = e
		if len(data) == 0:
			try:
				results_id = collection.find({'_id': int(tag_name)})
				for e in results_id:
					data = e
			except ValueError:
				pass
		if len(data) == 0:
			results_aliases = collection.find({'aliases': tag_name.lower()})
			for e in results_aliases:
				data = e
		
		if len(data) == 0:
			return await ctx.send("Tag **%s** does not exist. %s" % (tag_name, ctx.author.mention))
			
		sortTags = collection.find({}).sort([('uses_count', -1)])
		rank = 0
		for i in sortTags:
			if i['_id'] == data['_id']:
				break
			
			rank += 1
		
		tag_name = data["the_tag_name"]
		tag_owner_id = data["tag_owner_id"]
		tag_uses = data["uses_count"]
		tag_created_at = data["created_at"]
		the_tag_id = data["_id"]

		tag_owner = self.bot.get_user(tag_owner_id)

		em = discord.Embed(color=color.blue, title=tag_name)
		em.set_author(name=tag_owner, url=tag_owner.avatar_url, icon_url=tag_owner.avatar_url)
		em.add_field(name="Owner", value=tag_owner.mention)
		em.add_field(name="Uses", value=tag_uses)
		em.add_field(name="Rank", value=f"`#{rank}`")
		em.add_field(name="Tag ID",value="`{}`".format(the_tag_id), inline= False)
		em.set_footer(text="Tag created at • {}".format(tag_created_at))

		await ctx.send(embed=em)

	@tag.group(aliases=['alias', 'aliases'], invoke_without_command=True, case_insensitive=True, ignore_extra = False)
	async def _aliases(self, ctx, *, tag : str = None):
		if tag is None:
			return await ctx.reply("You must give the tag's name. %s" % (ctx.author.mention))
		
		try:
			tag = int(tag)
			get_tags = collection.find({'_id': tag})
			data = {}
			for i in get_tags:
				data = i
		
			if len(data) <= 0:
				return await ctx.send("This is not a valid tag's id or this tag does not exist. %s" % (ctx.author.mention))
			try:
				_list = []
				_list_ = data['aliases']
				for key in _list_:
					_list.append(f"`{key}`")
			except KeyError:
			 	return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")

			if len(_list) <= 0:
				return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")
			
			tag_name = data['the_tag_name']
			em = discord.Embed(color=discord.Color.blurple(), title="Here are all the aliases for the tag `%s`" % (tag_name))
			aliases = "\n• ".join(_list)
			if len(_list) == 1:
				em.description = f"• {aliases}"
			else:
				em.description = f"• {aliases}"
			await ctx.send(embed=em)
	
		except ValueError:
			tag = str(tag).lower()
			results = collection.find({'the_tag_name': tag})
			data = {}
			for i in results:
				data = i

			if len(data) <= 0:
				return await ctx.send(f"No tag named **{tag}** found. {ctx.author.mention}")
			
			try:
				_list = []
				_list_ = data['aliases']
				for key in _list_:
					_list.append(f"`{key}`")
			except KeyError:
				return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")
			
			if len(_list) <= 0:
				return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")

			em = discord.Embed(color=discord.Color.blurple(), title="Here are all the aliases for the tag `%s`" % (tag))
			aliases = "\n• ".join(_list)
			if len(_list) == 1:
				em.description = f"• {aliases}"
			else:
				em.description = f"• {aliases}"
			await ctx.send(embed=em)
		
	@_aliases.command(aliases=['make', 'add', 'create'])
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def _create(self, ctx, *, tag : str = None):
		if tag is None:
			return await ctx.reply("You must give the tag's name. %s" % (ctx.author.mention))

		all_names = []
		names = collection.find()
		allAliases = []
		for name in names:
			all_names.append(name['the_tag_name'])
			allAliases.append(name['aliases'])

		try:
			tag = int(tag)
			results = collection.find({'_id': tag})
			data = {}
			for i in results:
				data = i
			
			if len(data) <= 0:
				return await ctx.send("This is not a valid tag's id or this tag does not exist. %s" % (ctx.author.mention))
			
			if ctx.author.id != 374622847672254466:
				if data['tag_owner_id'] != ctx.author.id:
					return await ctx.send("You do not own this tag. %s" % (ctx.author.mention))
			
			tagAliases = data['aliases']
			if ctx.author.id != 374622847672254466:
				if len(data['aliases']) > 7:
					return await ctx.send("This tag has reached the maximum amount of aliases (`7`). %s" % (ctx.author.mention))
		
			await ctx.send("What do you wish the alias to be named as? %s" % (ctx.author.mention))
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel
			try:
				alias_name = await self.bot.wait_for('message', check=check, timeout=180)
				try:
					e = int(alias_name.content)
					return await ctx.send("The alias cannot be a number! %s" % (ctx.author.mention))
				except:
					pass
			except asyncio.TimeoutError:
				return await ctx.send("Took too much to respond. %s" % (ctx.author.mention))
			else:
				if str(alias_name.content).lower() in all_names:
					return await ctx.send("There is an existing tag with that name already. %s" % (ctx.author.mention))
				elif str(alias_name.content).lower() in allAliases:
					return await ctx.send("There is an existing alias with that name already. %s" % (ctx.author.mention))
				elif len(alias_name.content) > 75:
					return await ctx.send("Alias cannot be longer than `75` characters!")
				if len(tagAliases) == 0:
					collection.update_one({'_id': tag}, {'$set':{'aliases': [str(alias_name.content).lower()]}})
				else:
					tagAliases.append(str(alias_name.content).lower())
					collection.update_one({'_id': tag}, {'$set':{'aliases': tagAliases}})
				await ctx.send(f"{ctx.author.mention} Successfully added the alias `{str(alias_name.content).lower()}` for tag **{data['the_tag_name']}**")
		
		except ValueError:
			tag = str(tag).lower()
			results = collection.find({'the_tag_name': tag})
			data = {}
			for i in results:
				data = i
			
			if len(data) <= 0:
				return await ctx.send("This is not a valid tag's id or this tag does not exist. %s" % (ctx.author.mention))

			if ctx.author.id != 374622847672254466:
				if data['tag_owner_id'] != ctx.author.id:
					return await ctx.send("You do not own this tag. %s" % (ctx.author.mention))
		
			tagAliases = data['aliases']
			if ctx.author.id != 374622847672254466:
				if len(data['aliases']) > 7:
					return await ctx.send("This tag has reached the maximum amount of aliases (`7`). %s" % (ctx.author.mention))
		
			await ctx.send("What do you wish the alias to be named as? %s" % (ctx.author.mention))
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel
			try:
				alias_name = await self.bot.wait_for('message', check=check, timeout=180)
				try:
					e = int(alias_name.content)
					return await ctx.send("The alias cannot be a number! %s" % (ctx.author.mention))
				except:
					pass
			except asyncio.TimeoutError:
				return await ctx.send("Took too much to respond. %s" % (ctx.author.mention))
			else:
				if str(alias_name.content).lower() in all_names:
					return await ctx.send("There is an existing tag with that name already. %s" % (ctx.author.mention))
				elif str(alias_name.content).lower() in allAliases:
					return await ctx.send("There is an existing alias with that name already. %s" % (ctx.author.mention))
				elif len(alias_name.content) > 75:
					return await ctx.send("Alias cannot be longer than `75` characters!")
				if len(tagAliases) == 0:
					collection.update_one({'the_tag_name': tag}, {'$set':{'aliases': [str(alias_name.content).lower()]}})
				else:
					tagAliases.append(str(alias_name.content).lower())
					collection.update_one({'the_tag_name': tag}, {'$set':{'aliases': tagAliases}})
				await ctx.send(f"{ctx.author.mention} Successfully added the alias `{str(alias_name.content).lower()}` for tag **{data['the_tag_name']}**")

	@_aliases.command(aliases=['delete'])
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def _delete(self, ctx, *, alias: str = None):
		if alias is None:
			return await ctx.reply("You must specify the name of the alias you wish to delete. %s" % (ctx.author.mention))
		results = collection.find({'aliases': alias.lower()})
		try:
			for result in results:
				aliases = result['aliases']
				tagName = result['the_tag_name']
				tagOwner = result['tag_owner_id']
		except KeyError:
			return await ctx.send(f"{ctx.author.mention} There is no alias called **{alias}**")
		else:
			try:
				if ctx.author.id != 374622847672254466:
					if ctx.author.id != tagOwner:
						return await ctx.send("You do not own this tag! %s" % (ctx.author.mention))
				
				def check(reaction, user):
					return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
				msg = await ctx.send(f"{ctx.author.mention} Are you sure you want to remove the alias `{alias}` from the tag **{tagName}**?")
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
					if str(reaction.emoji) == '<:agree:797537027469082627>':
						new_aliases = []
						for _alias in aliases:
							if not _alias == alias.lower():
								new_aliases.append(_alias)
						collection.update_one({'the_tag_name': tagName}, {'$set':{'aliases': new_aliases}})
						e = f"{ctx.author.mention} Successfully removed the alias `{alias}` from tag **{tagName}**!"
						await msg.edit(content=e)
						await msg.clear_reactions()
						return
					elif str(reaction.emoji) == '<:disagree:797537030980239411>':
						e = "Alias has not been deleted. %s" % (ctx.author.mention)
						await msg.edit(content=e)
						await msg.clear_reactions()
						return
			except UnboundLocalError:
				return await ctx.send("No such alias exists. %s" % (ctx.author.mention))



	@tag.command(aliases=['make', 'add'])
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")	
	async def create(self, ctx, *, tag_name : str = None):
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
		if tag_name is None:
			await ctx.send("What do you want the tag to be named as?".format(ctx.author.mention))

			try:
				pre_tag = await self.bot.wait_for('message', timeout=180, check=check)
				tag_name = pre_tag.content

			except asyncio.TimeoutError:
				return await ctx.reply("Ran out of time.")

		matches = re.findall(filter_invite, tag_name)
		if ctx.author.id != 374622847672254466:
			for tag_name in matches:
				await ctx.send("No invites or what so ever.")
				return

		results = collection.find({'the_tag_name': str(tag_name).lower()})
		data = {}
		for i in results:
			data = i

		if len(data) > 0:
			await ctx.send("Tag name already taken.")
			return
		
		elif len(tag_name) >= 75:
			await ctx.send("Tag's name cannot be longer than `75` characters!")
			return
		elif len(tag_name) < 2:
				await ctx.send("Tag's name cannot be less than `2` characters long!")
				return
		elif tag_name.isnumeric():
			await ctx.send("Tag name cannot be a number!")
			return

		await ctx.send("Please send the tag's content. {}".format(ctx.author.mention))
		
		try:
			pre_tag_content = await self.bot.wait_for('message', timeout=420, check=check)
			if pre_tag_content.attachments:
				await ctx.send("Tag cannot contain attachments!")
				return					
			else:
				tag_content = pre_tag_content.content
				matches = re.findall(filter_invite, tag_content)

				if ctx.author.id != 374622847672254466:
					for tag_content in matches:
						await ctx.send("No invites or what so ever.")
						return

		except asyncio.TimeoutError:
			return await ctx.reply("Ran out of time.")
		
		else:
			get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
			get_sorted = collection.find({}).sort([("_id", -1)]).limit(1)
			for x in get_sorted:
				last_id = x['_id']

			post = {"_id": last_id + 1,
					"tag_content": tag_content, 
					"tag_owner_id": ctx.author.id, 
					"the_tag_name": tag_name.lower(), 
					"created_at": get_time, 
					"uses_count": 0,
					"aliases": []
					}
				
			collection.insert_one(post)
			
			await ctx.send("Tag `{}` Successfully created!".format(tag_name))

	@tag.command()
	@commands.has_any_role('Mod', 'lvl 15+', 'lvl 20+', 'lvl 25+', 'lvl 30+', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+", "lvl 155+", "lvl 160+", "lvl 165+", "lvl 170+", "lvl 175+", "lvl 180+", "lvl 185+", "lvl 190+", "lvl 195+", "lvl 200+", "lvl 205+", "lvl 210+", "lvl 215+", "lvl 220+", "lvl 230+", "lvl 240+", "lvl 250+", "lvl 255+", "lvl 260+", "lvl 265+", "lvl 270+", "lvl 275+", "lvl 275+", "lvl 280+", "lvl 285+", "lvl 290+", "lvl 300+", "lvl 305+", "lvl 310+", "lvl 315+", "lvl 320+", "lvl 330+", "lvl 340+", "lvl 350+", "lvl 355+", "lvl 360+", "lvl 365+", "lvl 370+", "lvl 375+", "lvl 380+", "lvl 385+", "lvl 390+", "lvl 395+", "lvl 400+", "lvl 405+", "lvl 410+", "lvl 415+", "lvl 420+", "lvl 430+", "lvl 440+", "lvl 450+", "lvl 455+", "lvl 460+", "lvl 465+", "lvl 470+", "lvl 475+", "lvl 480+", "lvl 485+", "lvl 490+", "lvl 495+", "lvl 500+")
	async def delete(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			return await ctx.reply("**!tag delete <tag_name>**")
		
		data = {}
		results = collection.find({'the_tag_name': tag_name.lower()})
		for i in results:
			data = i
		if len(data) == 0:
			try:
				result = collection.find({'_id': int(tag_name)})
				for i in result:
					data = i
			except ValueError:
				return await ctx.send("That tag does not exist. %s" % (ctx.author.mention))
		if len(data) == 0:
			return await ctx.send("That tag does not exist. %s" % (ctx.author.mention))
		if ctx.author.id != 374622847672254466:
			if ctx.author.id != data['tag_owner_id']:
				return await ctx.send("You do not own the tag **%s**! %s" % (data['the_tag_name'], ctx.author.mention))

		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
		msg = await ctx.send("Are you sure you wish to delete the tag **%s**? %s" % (data['the_tag_name'], ctx.author.mention))
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
			if str(reaction.emoji) == '<:agree:797537027469082627>':
				collection.delete_one({'_id': data['_id']})
				e = "Successfully deleted the tag **%s**. %s" % (data['the_tag_name'], ctx.author.mention)
				await msg.clear_reactions()
				await msg.edit(content=e)
				return
			
			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = "Operation of deleting the tag  **%s** has been canceled. %s" % (data['the_tag_name'], ctx.author.mention)
				await msg.clear_reactions()
				await msg.edit(content=e)
				return




	@tag.command()
	@commands.is_owner()
	async def remove(self, ctx, *, tag_name: str = None):
		if tag_name is None:
			return await ctx.reply("**!tag remove <tag_name>**")
		
		data = {}
		results = collection.find({'the_tag_name': tag_name.lower()})
		for i in results:
			data = i
		if len(data) == 0:
			try:
				result = collection.find({'_id': int(tag_name)})
				for i in result:
					data = i
			except ValueError:
				return await ctx.send("That tag does not exist in the database. %s" % (ctx.author.mention))
		if len(data) == 0:
			return await ctx.send("That tag does not exist in the database. %s" % (ctx.author.mention))
			
		get_tag_owner = data['tag_owner_id']
		tag_owner = self.bot.get_user(get_tag_owner)
		the_tag_name = data['the_tag_name']
		tag_created_at = data['created_at']
		uses = data['uses_count']

		collection.delete_one({"_id": data['_id']})

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


	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You must be at least `level 15+` in order to use this command! %s" % (ctx.author.mention))

	@tag.error
	async def tag_error(self, ctx, error):
		if isinstance(error, commands.TooManyArguments):
			return

def setup(bot):
	bot.add_cog(Tags(bot))