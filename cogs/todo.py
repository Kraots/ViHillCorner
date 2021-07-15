import motor.motor_asyncio
import os
import asyncio
from discord.ext import commands
import utils.colors as color
from utils.paginator import ToDoMenu

DBKEY = os.getenv("MONGODBLVLKEY")
cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']['Todo Data']

class ToDoPageEntry:
	def __init__(self, entry):
		
		self.data = entry['data']
		
	def __str__(self):
		return f'{self.data}'

class ToDoPages(ToDoMenu):
	def __init__(self, entries, *, per_page=12, title="", color=color.red, author_name=None, author_icon_url=None):
		converted = [ToDoPageEntry(entry) for entry in entries]
		super().__init__(converted, per_page=per_page, title=title, color=color, author_name=author_name, author_icon_url=author_icon_url)

class ToDo(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix
	
	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def todo(self, ctx, *, todo: str):
		cmd = self.bot.get_command('todo add')
		await ctx.invoke(cmd, todo=todo)
	
	@todo.command()
	async def add(self, ctx, *, todo: str):
		user = await db.find_one({'_id': ctx.author.id})
		if user is None:
			post = {
			'_id': ctx.author.id,
			'data': [{'url': ctx.message.jump_url,
					'data': todo
					}]
				}
			await db.insert_one(post)
			await ctx.reply("Successfully added to your todo list.")
			return

		array = user['data']
		todo = {'url': ctx.message.jump_url,
				'data': todo
				}
		array.append(todo)
		await db.update_one({'_id': ctx.author.id}, {'$set':{'data': array}})
		await ctx.reply("Successfully added to your todo list.")
		return
	
	@todo.command(aliases=['list'])
	async def _list(self, ctx):
		entries = await db.find_one({'_id': ctx.author.id})
		if entries is None:
			return await ctx.reply("You do not have any todo list.")

		entries = entries['data']
		index = 0
		for i in range(len(entries)):
			index += 1
			entries[i]['data'] = f"**[{index}.]({entries[i]['url']})** {entries[i]['data']}"

		m = ToDoPages(entries=entries, per_page=10, title="Here's your todo list:", author_name=ctx.author, author_icon_url=ctx.author.avatar_url)
		await m.start(ctx)

	@todo.command(aliases=['delete'])
	async def remove(self, ctx, index):
		try:
			index = int(index) - 1
		except ValueError:
			return await ctx.reply("That is not a number.")
		
		user = await db.find_one({'_id': ctx.author.id})
		if user is None:
			return await ctx.reply("You do not have any todo list.")
		
		data = user['data']
		new_data = []
		for i in range(len(data)):
			if i != index:
				new_data.append(data[i])
		
		if len(new_data) == 0:
			await db.delete_one({'_id': ctx.author.id})
		else:
			await db.update_one({'_id': ctx.author.id}, {'$set':{'data': new_data}})
		await ctx.reply("Operation successful.")

	@todo.command()
	async def clear(self, ctx):
		user = await db.find_one({'_id': ctx.author.id})
		if user is None:
			return await ctx.reply("You do not have any todo list.")
		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
		msg = await ctx.send("Are you sure you want to delete your todo list? %s" % (ctx.author.mention))
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
				await db.delete_one({'_id': ctx.author.id})
				e = "Succesfully deleted your todo list. %s" % (ctx.author.mention)
				await msg.edit(content=e)
				await msg.clear_reactions()
				return
			
			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				e = "Okay, your todo list has not been deleted. %s" % (ctx.author.mention)
				await msg.edit(content=e)
				await msg.clear_reactions()
				return


def setup(bot):
	bot.add_cog(ToDo(bot))