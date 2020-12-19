import discord
from discord.ext import commands
import json
import asyncio


class Snippets(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command=True, case_insensitive=True)
	@commands.has_role("Staff")
	async def snippet(self, ctx):
		await ctx.send("Invalid usage!\nPlease use `!snippet create` or `!snippet delete`")

	@snippet.command()
	@commands.has_role("Staff")
	async def create(self, ctx):
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
		await ctx.send("What do you want to name this snippet?")
		try:
			presnippet_name = await self.client.wait_for('message', timeout = 60, check=check)
			snippet_name = presnippet_name.content.lower()

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
					snippets[str(snippet_name)] = {}
					snippets[str(snippet_name)]["snippet_content"] = snippet_info
					snippets[str(snippet_name)]["snippet_credits"] = ctx.author.id
					with open("snippets.json", "w") as f:
						json.dump(snippets, f)

					await ctx.send("Snippet Added!")

	@snippet.command(aliases=['remove'])
	async def delete(self, ctx):
		def check(m):
			return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

		await ctx.send("What's the name of the snippet you wish to delete?")
		try:
			raw_get_snippet = await self.client.wait_for('message', timeout=60, check=check)
			snippet_name = raw_get_snippet.content.lower()

		except asyncio.TimeoutError:
			return

		else:
			try:
				snippets = await get_snippets_data()
				del snippets[str(snippet_name)]
				with open ("snippets.json", "w") as f:
					json.dump(snippets, f)

				await ctx.send(f"`{snippet_name}` deleted succesfully!")

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

			if message.content.lower().startswith(f";{snippet_name}"):
				em = discord.Embed(color=discord.Color.red())
				em.set_image(url=snippet)
				em.set_footer(text=f"Credits: {credits_user}", icon_url=credits_avatar)
				msg = await message.channel.send(embed=em)
				await msg.add_reaction('🗑️')

		except KeyError:
			return







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