import discord
from discord.ext import commands
import json
import asyncio
from utils.paginator import SimplePages
import datetime
import utils.colors as color
from utils.paginator_v2 import WrappedPaginator, PaginatorEmbedInterface

nono_names = ["huggles", "grouphug", "eat", "chew", "sip", "clap", "cry", "rofl", "lol", "kill", "pat", "rub", "nom", "catpat", "hug", "pillow", "spray", "hype", "specialkiss", "kiss", "ily", "nocry", "shrug", "smug", "bearhug", "moan"]

class TagPageEntry:
	def __init__(self, entry):
		
		with open("snippets.json", "r") as f:
			entries = json.load(f)

		self.name = entries[entry]['snippet_name']
		self.id = entries[entry]['snippet_credits']

	def __str__(self):
		return f'{self.name}\u2800•\u2800(`Owner:` <@!{self.id}>)'

class SnippetPages(SimplePages):
	def __init__(self, entries, *, per_page=12):
		converted = [TagPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page)



class Snippets(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True, aliases=['snippets'], ignore_extra = False)
	async def snippet(self, ctx):
		with open("snippets.json", "r") as f:
			entries = json.load(f)
		
		p = SnippetPages(entries = entries, per_page = 7)
		await p.start(ctx)

	@snippet.command(aliases=['lb'])
	async def leaderboard(self, ctx, x=10):
		snippets = await get_snippets_data()

		leader_board = {}
				
		for uid, details in snippets.items():  
			snippet_namee = snippets[str(uid)]["snippet_name"]  
			leader_board[snippet_namee] = details['uses_count']  
		
		leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True) 
		
		em = discord.Embed(color=discord.Color.blurple(), title=f"Top `{x}` Snippets")

		for index, (mem, amt) in enumerate(leader_board[:x], start = 1):
			uses = snippets[str(mem)]["uses_count"]
			owner_id = snippets[str(mem)]["snippet_credits"]
			owner = self.client.get_user(owner_id)
			em.add_field(name=f"_ _ \n{index}#\u2800`{mem}`", value=f"Uses:\n\u2800`{uses}`\nOwner:\n\u2800`{owner}`", inline=True)
			
			if index == x:
				break
			
			else:
				index += 1

		em.set_footer(text="Requested by: {}".format(ctx.author), icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=em)








	@snippet.command()
	async def list(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		snippets = await get_snippets_data()

		snippets_list = []
		index = 0
		
		for key in snippets:
			owner_id = snippets[str(key)]["snippet_credits"]
			snippet_owner = self.client.get_user(owner_id)

			if str(member) in str(snippet_owner):
				snippet_name = snippets[str(key)]["snippet_name"]
				get_snippet_create_date = snippets[str(key)]["created_at"]

				fin = f"{snippet_name} (`Created At`: {get_snippet_create_date})"

				if not snippet_name in snippets_list:
					index += 1
					indexed_row = f"{index}. {fin}"
					snippets_list.append(indexed_row)

		result = "\n".join(snippets_list)

		if len(result) > 1:
			paginator = WrappedPaginator(prefix = f'**`{member}` 𝗢𝘄𝗻𝗲𝗱 𝗦𝗻𝗶𝗽𝗽𝗲𝘁𝘀** \n', suffix = '', max_size = 250)
			paginator.add_line(result)
			interface = PaginatorEmbedInterface(ctx.bot, paginator, owner = ctx.author)

			await interface.send_to(ctx)

		elif len(result) <= 1:
			await ctx.send("`{}` has no snippets.".format(member))
			return

























	@snippet.command()
	async def info(self, ctx, *, snippet_name : str = None):
		snippets = await get_snippets_data()

		if snippet_name is None:
			await ctx.send("`!snippet info <snippet_name>`")
			return

		else:
			try:

				leader_board = {}
						
				for uid, details in snippets.items():  
					snippet_namee = snippets[str(uid)]["snippet_name"]  
					leader_board[snippet_namee] = details['uses_count']  
				
				leader_board = sorted(leader_board.items(), key=lambda item: item[1], reverse=True) 

				for index2, (mem, amt) in enumerate(leader_board, start = 1):

					string1 = f"{index2} {mem}"
					string2 = f"{index2} {snippet_name}"

					if string1 == string2:
						index=index2
						break
					else:
						index2 += 1


				snippet_name = snippets[str(snippet_name.lower())]["snippet_name"]
				snippet_owner_id = snippets[str(snippet_name.lower())]["snippet_credits"]
				snippet_uses = snippets[str(snippet_name.lower())]["uses_count"]
				snippet_created_at = snippets[str(snippet_name.lower())]["created_at"]

				snippet_owner = self.client.get_user(snippet_owner_id)

				em = discord.Embed(color=color.reds, title=snippet_name)
				em.set_author(name=snippet_owner, url=snippet_owner.avatar_url, icon_url=snippet_owner.avatar_url)
				em.add_field(name="Owner", value=snippet_owner.mention)
				em.add_field(name="Uses", value=snippet_uses)
				em.add_field(name="Rank", value="`#{}`".format(index))
				em.set_footer(text="Snippet created at • {}".format(snippet_created_at))

				await ctx.send(embed=em)

			except KeyError:
				await ctx.send("Snippet `{}` does not exist!".format(snippet_name))

	@snippet.command(aliases=['make', 'add'])
	@commands.has_any_role('Mod', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def create(self, ctx, *, get_snippet_name = None):

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
				
				elif snippet_name in nono_names:
					await ctx.send("Those names are invalid! Reason: `They are used in other commands, actions, to be more specific.`")
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
					snippets = await get_snippets_data()
					if str(snippet_name) in snippets:
						await ctx.send("That snippet already exists!")
					else:
						get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
						snippets[str(snippet_name)] = {}
						snippets[str(snippet_name)]["snippet_content"] = snippet_info
						snippets[str(snippet_name)]["snippet_credits"] = ctx.author.id
						snippets[str(snippet_name)]["snippet_name"] = snippet_name
						snippets[str(snippet_name)]["created_at"] = get_time
						snippets[str(snippet_name)]["uses_count"] = 0
						with open("snippets.json", "w", encoding="utf-8") as f:
							json.dump(snippets, f, ensure_ascii = False, indent = 4)

						await ctx.send("Snippet Added!")

		else:
			
			if len(get_snippet_name) >= 35:
					await ctx.send("Snippet's name cannot be that long! Max is: `35`")
					return
			
			elif len(get_snippet_name) < 3:
					await ctx.send("Snippet's name cannot be less than `3` characters long!")
					return

			elif get_snippet_name in nono_names:
					await ctx.send("Those names are invalid! Reason: `They are used in other commands, actions, to be more specific.`")
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
				snippets = await get_snippets_data()
				if str(get_snippet_name) in snippets:
					await ctx.send("That snippet already exists!")
				else:
					get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
					snippets[str(get_snippet_name)] = {}
					snippets[str(get_snippet_name)]["snippet_content"] = snippet_info
					snippets[str(get_snippet_name)]["snippet_credits"] = ctx.author.id
					snippets[str(get_snippet_name)]["snippet_name"] = get_snippet_name
					snippets[str(get_snippet_name)]["created_at"] = get_time
					snippets[str(get_snippet_name)]["uses_count"] = 0
					with open("snippets.json", "w", encoding="utf-8") as f:
						json.dump(snippets, f, ensure_ascii = False, indent = 4)

					await ctx.send("Snippet Added!")

	@snippet.command()
	@commands.has_any_role('Mod', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', "lvl 75+", "lvl 80+", "lvl 85+", "lvl 90+", "lvl 95+", "lvl 100+", "lvl 105+", "lvl 110+", "lvl 120+", "lvl 130+", "lvl 150+")
	async def delete(self, ctx, *, get_snippet_name = None):
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
				try:
					snippets = await get_snippets_data()

					snippet_owner = snippets[str(snippet_name)]["snippet_credits"]

					if ctx.author.id != snippet_owner:
						await ctx.send("You do not own this snippet!")
						return

					else:
						del snippets[str(snippet_name)]
						with open ("snippets.json", "w", encoding="utf-8") as f:
							json.dump(snippets, f, ensure_ascii = False, indent = 4)

						await ctx.send(f"`{snippet_name}` deleted succesfully!")

				except KeyError:
					await ctx.send("That snippet does not exist!")
				
		else:
			try:
				snippets = await get_snippets_data()
				snippet_owner = snippets[str(get_snippet_name)]["snippet_credits"]

				if ctx.author.id != snippet_owner:
						await ctx.send("You do not own this snippet!")
						return
				else:

					del snippets[str(get_snippet_name)]
					with open ("snippets.json", "w", encoding="utf-8") as f:
						json.dump(snippets, f, ensure_ascii = False, indent = 4)

					await ctx.send(f"`{get_snippet_name}` deleted succesfully!")

			except KeyError:
				await ctx.send("That snippet does not exist!")


	@snippet.command()
	@commands.is_owner()
	async def remove(self, ctx, *, get_snippet_name = None):
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		if get_snippet_name is None:
			await ctx.send("What's the name of the snippet you wish to remove?")
			try:
				raw_get_snippet = await self.client.wait_for('message', timeout=60, check=check)
				snippet_name = raw_get_snippet.content.lower()

			except asyncio.TimeoutError:
				return

			else:
				try:
					snippets = await get_snippets_data()
					name = snippets[str(snippet_name)]["snippet_name"]
					get_owner = snippets[str(snippet_name)]["snippet_credits"]
					owner = self.client.get_user(get_owner)
					snippet_created_at = snippets[str(snippet_name)]["created_at"]
					
					del snippets[str(snippet_name)]
					with open ("snippets.json", "w", encoding="utf-8") as f:
						json.dump(snippets, f, ensure_ascii = False, indent = 4)

					em = discord.Embed(title="Snippet Deleted", color=color.red)
					em.add_field(name = "Name", value = name)
					em.add_field(name = "Owner", value = owner.mention)
					em.set_footer(text=f"Snippet created at • {snippet_created_at}")

					await ctx.send(embed=em)

				except KeyError:
					await ctx.send("That snippet does not exist!")
				
		else:
			try:
				snippets = await get_snippets_data()

				name = snippets[str(get_snippet_name)]["snippet_name"]
				get_owner = snippets[str(get_snippet_name)]["snippet_credits"]
				owner = self.client.get_user(get_owner)
				snippet_created_at = snippets[str(get_snippet_name)]["created_at"]

				del snippets[str(get_snippet_name)]
				with open ("snippets.json", "w", encoding="utf-8") as f:
					json.dump(snippets, f, ensure_ascii = False, indent = 4)

				em = discord.Embed(title="Snippet Deleted", color=color.red)
				em.add_field(name = "Name", value = name)
				em.add_field(name = "Owner", value = owner.mention)
				em.set_footer(text=f"Snippet created at • {snippet_created_at}")

				await ctx.send(embed=em)

			except KeyError:
				await ctx.send("That snippet does not exist!")



	@commands.Cog.listener()
	async def on_message(self, message : discord.Message):

		if message.author.bot:
			return
		presnippet_name = message.content.lower()
		snippet_name = "".join(presnippet_name.split(";", 1))

		try:
			await open_snippets(snippet_name)
			snippets = await get_snippets_data()
			snippet = snippets[str(snippet_name)]["snippet_content"]
			get_credits_info = snippets[str(snippet_name)]["snippet_credits"]
			credits_user = self.client.get_user(get_credits_info)
			credits_avatar = credits_user.avatar_url


			snippets[str(snippet_name)]["uses_count"] += 1
			with open("snippets.json", "w", encoding = "utf-8") as f:
				json.dump(snippets, f, ensure_ascii = False, indent = 4)


			if message.content.lower().startswith(f";{snippet_name}"):
				em = discord.Embed(color=discord.Color.red())
				em.set_image(url=snippet)
				em.set_footer(text=f"Credits: {credits_user}", icon_url=credits_avatar)
				msg = await message.channel.send(embed=em)
				await msg.add_reaction('🗑️')
		except KeyError:
			return

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		snippets = await get_snippets_data()

		if member.id == 374622847672254466:
			return
		
		for key in snippets:
			owner_id = snippets[str(key)]["snippet_credits"]
			snippet_owner = self.client.get_user(owner_id)

			if str(member) in str(snippet_owner):
				snippet_name = snippets[str(key)]["snippet_name"]
				del snippets[str(snippet_name)]

				with open("snippets.json", "w", encoding = 'utf-8') as f:
					json.dump(snippets, f, ensure_ascii = False, indent = 4)



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






async def open_snippets(snippet_name):

	snippets = await get_snippets_data()

	if str(snippet_name) in snippets:
		return False

async def get_snippets_data():
	with open("snippets.json", "r") as f:
		snippet = json.load(f)

	return snippet


def setup (client):
	client.add_cog(Snippets(client))