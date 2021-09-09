import disnake
from disnake.ext import commands
import utils.colors as color
from utils.paginator import ToDoMenu

class ToDoPageEntry:
	def __init__(self, entry):
		
		self.data = entry['data']
		
	def __str__(self):
		return f'{self.data}'

class ToDoPages(ToDoMenu):
	def __init__(self, ctx, entries, *, per_page=5, title="", color=color.red, author_name=None, author_icon_url=None):
		converted = [ToDoPageEntry(entry) for entry in entries]
		super().__init__(ctx=ctx, entries=converted, per_page=per_page, title=title, color=color, author_name=author_name, author_icon_url=author_icon_url)

class ToDo(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db2['Todo Data']
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def todo(self, ctx, *, todo: str):
		"""Add to your todo list."""

		cmd = self.bot.get_command('todo add')
		await ctx.invoke(cmd, todo=todo)
	
	@todo.command(name='add')
	async def todo_add(self, ctx, *, todo: str):
		"""Add to your todo list."""

		user = await self.db.find_one({'_id': ctx.author.id})
		if user is None:
			post = {
			'_id': ctx.author.id,
			'data': [
					{'url': ctx.message.jump_url,
					'data': todo
					}
					]
				}
			await self.db.insert_one(post)
			await ctx.reply("Successfully added to your todo list.")
			return

		array = user['data']
		todo = {'url': ctx.message.jump_url,
				'data': todo
				}
		array.append(todo)
		await self.db.update_one({'_id': ctx.author.id}, {'$set':{'data': array}})
		await ctx.reply("Successfully added to your todo list.")
		return
	
	@todo.command(name='list')
	async def todo_list(self, ctx):
		"""See your todo list, if you have any."""

		entries = await self.db.find_one({'_id': ctx.author.id})
		if entries is None:
			return await ctx.reply("You do not have any todo list.")

		entries = entries['data']
		index = 0
		for i in range(len(entries)):
			index += 1
			entries[i]['data'] = f"**[{index}.]({entries[i]['url']})** {entries[i]['data']}"

		m = ToDoPages(ctx=ctx, entries=entries, title="Here's your todo list:", author_name=ctx.author, author_icon_url=ctx.author.avatar.url)
		await m.start()

	@todo.command(name='delete', aliases=['remove'])
	async def todo_remove(self, ctx, index):
		"""Remove a todo from your todo list based on its index."""

		try:
			index = int(index) - 1
		except ValueError:
			return await ctx.reply("That is not a number.")
		
		user = await self.db.find_one({'_id': ctx.author.id})
		if user is None:
			return await ctx.reply("You do not have any todo list.")
		
		data = user['data']
		new_data = []
		if index < 0:
			return await ctx.reply("The index cannot be `0` or negative.")
		elif index > len(data) - 1:
			return await ctx.reply("The index cannot be greater than the highest index in your todo list.")

		for i in range(len(data)):
			if i != index:
				new_data.append(data[i])
		
		if len(new_data) == 0:
			await self.db.delete_one({'_id': ctx.author.id})
		else:
			await self.db.update_one({'_id': ctx.author.id}, {'$set':{'data': new_data}})
		await ctx.reply("Operation successful.")

	@todo.command(name='clear')
	async def todo_clear(self, ctx):
		"""Delete your todo list, completely."""

		user = await self.db.find_one({'_id': ctx.author.id})
		if user is None:
			return await ctx.reply("You do not have any todo list.")
		view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
		view.message = msg = await ctx.send("Are you sure you want to delete your todo list? %s" % (ctx.author.mention), view=view)
		await view.wait()
		if view.response is True:
			await self.db.delete_one({'_id': ctx.author.id})
			e = "Succesfully deleted your todo list. %s" % (ctx.author.mention)
			return await msg.edit(content=e, view=view)
		
		elif view.response is False:
			e = "Okay, your todo list has not been deleted. %s" % (ctx.author.mention)
			return await msg.edit(content=e, view=view)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db.delete_one({'_id': member.id})


def setup(bot):
	bot.add_cog(ToDo(bot))
