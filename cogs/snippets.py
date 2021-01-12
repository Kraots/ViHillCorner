import discord
from discord.ext import commands
import asyncio
from utils.paginator_v3 import SimplePages
import datetime
import utils.colors as color
from pymongo import MongoClient
import os
DBKEY = os.getenv("MONGODBKEY")

cluster = MongoClient(DBKEY)
db = cluster["ViHillCornerDB"]
collection = db["Snippets"]

nono_names = ["huggles", "grouphug", "eat", "chew", "sip", "clap", "cry", "rofl", "lol", "kill", "pat", "rub", "nom", "catpat", "hug", "pillow", "spray", "hype", "specialkiss", "kiss", "ily", "nocry", "shrug", "smug", "bearhug", "moan"]

class SnippetPageEntry:
	def __init__(self, entry):

		self.name = entry['_id']
		self.id = entry['snippet_credits']

	def __str__(self):
		return f'{self.name}\u2800•\u2800(`Owner:` <@!{self.id}>)'

class SnippetPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [SnippetPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)

class SnippetOwnerPageEntry:
	def __init__(self, entry):

		self.name = entry['_id']
		self.created = entry['created_at']

	def __str__(self):
		return f'{self.name}\u2800•\u2800(`Created At:` **{self.created}**)'

class SnippetOwnerPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [SnippetOwnerPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)


class Snippets(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['snippets'], ignore_extra = False)
	async def snippet(self, ctx):
		entries = collection.find({})
		
		p = SnippetPages(entries = entries, per_page = 7)
		await p.start(ctx)




	@snippet.command(aliases=['lb'])
	async def leaderboard(self, ctx):
		results = collection.find({}).sort([("uses_count", -1)]).limit(10)
		index = 0
		em = discord.Embed(color=color.reds)
		for result in results:
			snippet_name = result['_id']
			uses = result['uses_count']
			get_owner = result['snippet_credits']
			owner = self.client.get_user(get_owner)
			index += 1
			em.add_field(name=f"`{index}`.\u2800{snippet_name}", value=f"Uses: `{uses}`\n Owner: `{owner}`", inline=False)
		
		await ctx.send(embed=em)








	@snippet.command()
	async def list(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		all_users = []
		results = collection.find({})
		for result in results:
			all_users.append(result['snippet_credits'])
		
		if member.id in all_users:
			entries = collection.find({"snippet_credits": member.id})
			p = SnippetOwnerPages(entries = entries, per_page = 7)
			await p.start(ctx)

		else:
			await ctx.send("`{}` has no snippets.".format(member))




	@snippet.command()
	async def info(self, ctx, *, snippet_name : str = None):
		results = collection.find({}).sort([('uses_count', -1)])
		index2 = 1
		for result in results:
			snippet_namee = result['_id']
			string1 = f"{index2} {snippet_namee}"
			string2 = f"{index2} {snippet_name.lower()}"
			if string1 == string2:
				index = index2
				break
			else:
				index2 += 1

		if snippet_name is None:
			await ctx.send("`!snippet info <snippet_name>`")
			return

		else:
			all_snippets = []
			resultss = collection.find()
			for resultt in resultss:
				all_snippets.append(result['_id'])

			if not snippet_name.lower() in all_snippets:
				await ctx.send(f"Snippet `{snippet_name}` does not exist!")
				return

			else:
				get_data = collection.find({"_id": snippet_name.lower()})

				for data in get_data:
					snippet_name = data['_id']
					snippet_owner_id = data['snippet_credits']
					snippet_uses = data['uses_count']
					snippet_created_at = data['created_at']

				snippet_owner = self.client.get_user(snippet_owner_id)

				em = discord.Embed(color=color.reds, title=snippet_name)
				em.set_author(name=snippet_owner, url=snippet_owner.avatar_url, icon_url=snippet_owner.avatar_url)
				em.add_field(name="Owner", value=snippet_owner.mention)
				em.add_field(name="Uses", value=snippet_uses)
				em.add_field(name="Rank", value="`#{}`".format(index))
				em.set_footer(text="Snippet created at • {}".format(snippet_created_at))

				await ctx.send(embed=em)



	@snippet.command(aliases=['make', 'add'])
	@commands.has_any_role('Mod', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def create(self, ctx, *, get_snippet_name : str = None):

		if get_snippet_name is None:
			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
			await ctx.send("What do you want to name this snippet?")
			try:
				presnippet_name = await self.client.wait_for('message', timeout = 60, check=check)
				snippet_name = presnippet_name.content.lower()
				if len(snippet_name) >= 35:
					await ctx.send("Snippet's name cannot be that long! Max is: `35`")
					return

				elif len(snippet_name) < 3:
					await ctx.send("Snippet's name cannot be less than `3` characters long!")
					return

				elif snippet_name.isnumeric():
					await ctx.send("Snippet name cannot be a number!")
					return
				
				elif snippet_name in nono_names:
					await ctx.send("That names are invalid! Reason: `They are used in other commands, actions, to be more specific.`")
					return

			except asyncio.TimeoutError:
				return

			else:

				await ctx.send("Please send the image of the snippet.")
				try:
					presnippet_info = await self.client.wait_for('message', timeout = 180, check=check)
					snippet_info = presnippet_info.attachments[0].url

				except asyncio.TimeoutError:
					return

				except IndexError:
					await ctx.send("That is not an image! Please send an image and nothing else!")
					return
				
				else:
					results = collection.find({})

					all_names = []

					for result in results:
						db_snippet_name = result["_id"]
						all_names.append(str(db_snippet_name))

					if str(snippet_name.lower()) in all_names:
						await ctx.send("That snippet already exists!")
					else:
						get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
						post = {"_id": str(snippet_name.lower()), 
								"snippet_content": snippet_info,
								"snippet_credits": ctx.author.id,
								"created_at": get_time,
								"uses_count": 0
								}

						collection.insert_one(post)

						await ctx.send("Snippet Added!")

		else:
			
			if len(get_snippet_name) >= 35:
					await ctx.send("Snippet's name cannot be that long! Max is: `35`")
					return
			
			elif len(get_snippet_name) < 3:
					await ctx.send("Snippet's name cannot be less than `3` characters long!")
					return
			
			elif get_snippet_name.isnumeric():
				await ctx.send("Snippet name cannot be a number!")
				return

			elif get_snippet_name.lower() in nono_names:
					await ctx.send("That names are invalid! Reason: `They are used in other commands, actions, to be more specific.`")
					return

			def check(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			await ctx.send("Please send the image of the snippet.")
			try:
				presnippet_info = await self.client.wait_for('message', timeout = 180, check=check)
				snippet_info = presnippet_info.attachments[0].url

			except asyncio.TimeoutError:
				return

			except IndexError:
				await ctx.send("That is not an image! Please send an image and nothing else!")
				return

			else:
				results = collection.find({})

				all_names = []

				for result in results:
					db_snippet_name = result["_id"]
					all_names.append(str(db_snippet_name))

				if str(get_snippet_name.lower()) in all_names:
					await ctx.send("That snippet already exists!")
				else:
					get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
					post = {"_id": get_snippet_name.lower(), 
							"snippet_content": snippet_info,
							"snippet_credits": ctx.author.id,
							"created_at": get_time,
							"uses_count": 0
							}
					

					collection.insert_one(post)

					await ctx.send("Snippet Added!")

	@snippet.command()
	@commands.has_any_role('Mod', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def delete(self, ctx, *, get_snippet_name : str = None):
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		if get_snippet_name is None:
			await ctx.send("What's the name of the snippet you wish to delete?")
			try:
				raw_get_snippet = await self.client.wait_for('message', timeout=60, check=check)
				snippet_name = raw_get_snippet.content.lower()

			except asyncio.TimeoutError:
				return

			else:
				all_snippets = []
				resultss = collection.find()
				for resultt in resultss:
					all_snippets.append(resultt['_id'])

				if not snippet_name in all_snippets:
					await ctx.send(f"Snippet `{snippet_name}` does not exist!")
					return
				
				else:
					get_data = collection.find({"_id": snippet_name})
					
					for data in get_data:
						snippet_owner = data['snippet_credits']

					if ctx.author.id != snippet_owner:
						await ctx.send("You do not own this snippet!")
						return

					else:
						collection.delete_one({"_id": snippet_name})

						await ctx.send(f"`{snippet_name}` deleted succesfully!")
				
		else:
			all_snippets = []
			resultss = collection.find()
			for resultt in resultss:
				all_snippets.append(resultt['_id'])

			if not get_snippet_name.lower() in all_snippets:
				await ctx.send(f"Snippet `{get_snippet_name}` does not exist!")
				return
			
			else:
				get_data = collection.find({"_id": get_snippet_name.lower()})
				
				for data in get_data:
					snippet_owner = data['snippet_credits']

			if ctx.author.id != snippet_owner:
					await ctx.send("You do not own this snippet!")
					return
			else:
				collection.delete_one({"_id": get_snippet_name.lower()})

				await ctx.send(f"`{get_snippet_name}` deleted succesfully!")


	@snippet.command()
	@commands.is_owner()
	async def remove(self, ctx, *, get_snippet_name : str = None):
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		if get_snippet_name is None:
			await ctx.send("What's the name of the snippet you wish to delete?")
			try:
				raw_get_snippet = await self.client.wait_for('message', timeout=60, check=check)
				snippet_name = raw_get_snippet.content.lower()

			except asyncio.TimeoutError:
				return

			else:
				all_snippets = []
				resultss = collection.find()
				for resultt in resultss:
					all_snippets.append(resultt['_id'])

				if not snippet_name in all_snippets:
					await ctx.send(f"Snippet `{snippet_name}` does not exist!")
					return
				
				else:
					get_data = collection.find({"_id": snippet_name})
					
					for data in get_data:
						get_snippet_owner = data['snippet_credits']
						snippet_owner = self.client.get_user(get_snippet_owner)
						the_snippet_name = data['_id']
						snippet_created_at = data['created_at']
						uses = data['uses_count']

					collection.delete_one({"_id": snippet_name})

					em = discord.Embed(title="Snippet Deleted", color=color.red)
					em.add_field(name = "Name", value = the_snippet_name)
					em.add_field(name = "Owner", value = snippet_owner)
					em.add_field(name="Uses", value=f"`{uses}`", inline = False)
					em.set_footer(text=f"Snippet created at • {snippet_created_at}")

					await ctx.send(embed=em)
				
		else:
			all_snippets = []
			resultss = collection.find()
			for resultt in resultss:
				all_snippets.append(resultt['_id'])

			if not get_snippet_name.lower() in all_snippets:
				await ctx.send(f"Snippet `{get_snippet_name}` does not exist!")
				return
			
			else:
				get_data = collection.find({"_id": get_snippet_name.lower()})
				
				for data in get_data:
					get_snippet_owner = data['snippet_credits']
					snippet_owner = self.client.get_user(get_snippet_owner)
					the_snippet_name = data['_id']
					snippet_created_at = data['created_at']
					uses = data['uses_count']

				collection.delete_one({"_id": get_snippet_name.lower()})

				em = discord.Embed(title="Snippet Deleted", color=color.red)
				em.add_field(name = "Name", value = the_snippet_name)
				em.add_field(name = "Owner", value = snippet_owner)
				em.add_field(name="Uses", value=f"`{uses}`", inline = False)
				em.set_footer(text=f"Snippet created at • {snippet_created_at}")

				await ctx.send(embed=em)


	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):

		if message.author.bot:
			return
		presnippet_name = message.content.lower()
		snippet_name = "".join(presnippet_name.split(";", 1))

		all_snippets = []
		results = collection.find()
		for result in results:
			all_snippets.append(result['_id'])

		if not snippet_name in all_snippets:
			return
		
		else:
			get_data = collection.find({"_id": snippet_name})

			for data in get_data:
				snippet = data['snippet_content']
				get_credits_info = data['snippet_credits']
				credits_user = self.client.get_user(get_credits_info)
				credits_avatar = credits_user.avatar_url

			collection.update_one({"_id": snippet_name}, {"$inc":{"uses_count": 1}})


			if message.content.lower().startswith(f";{snippet_name}"):
				em = discord.Embed(color=discord.Color.red())
				em.set_image(url=snippet)
				em.set_footer(text=f"Credits: {credits_user}", icon_url=credits_avatar)
				msg = await message.channel.send(embed=em)
				await msg.add_reaction('🗑️')

			else:
				pass

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection.delete_many({"snippet_credits": member.id})



	@snippet.error
	async def snippet_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You need to be `lvl 55+` to use this command!")
		elif isinstance(error, commands.TooManyArguments):
			return

	@create.error
	async def create_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You need to be `lvl 55+` to use this command!")

	@delete.error
	async def delete_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingAnyRole):
			await ctx.send("You need to be `lvl 55+` to use this command!")


def setup (client):
	client.add_cog(Snippets(client))