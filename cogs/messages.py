import disnake
from disnake.ext import commands, tasks
import utils.colors as color
import datetime
from dateutil.relativedelta import relativedelta
from utils import time

class MessagesTopButtons(disnake.ui.View):
	def __init__(self, db, ctx, *, timeout = 180.0):
		super().__init__(timeout=timeout)
		self.db = db
		self.ctx = ctx
	
	async def interaction_check(self, interaction: disnake.MessageInteraction):
		if interaction.author.id != self.ctx.author.id:
			await interaction.response.send_message(f'Only {self.ctx.author.display_name} can use the buttons on this message!', ephemeral=True)
			return False
		return True
	
	async def on_error(self, error, item, interaction):
		return await self.ctx.bot.reraise(self.ctx, error)
	
	async def on_timeout(self):
		for item in self.children:
			item.disabled = True
		await self.message.edit(content='Did not click any button in time.', view=self)

	@disnake.ui.button(label='Total Messages Top', style=disnake.ButtonStyle.blurple)
	async def total_messages_top(self, button: disnake.Button, inter: disnake.Interaction):
		data = await self.db.find_one({"_id": 374622847672254466})

		em = disnake.Embed(color=color.lightpink)
		
		index = 0
		pos_ = 0
		pos = 0
		guild = self.ctx.bot.get_guild(750160850077089853)
		
		results = await self.db.find().sort([("messages_count", -1)]).to_list(100000)
		for result in results:
			if result['messages_count'] != 0:
				if index != 5:
					index += 1
					mem = guild.get_member(result['_id'])
					if mem == self.ctx.author:
						em.add_field(name=f'**`#{index}\u2800 {mem.name}` (YOU)**', value=f"`{result['messages_count']:,}` messages", inline=False)
					else:
						em.add_field(name=f'`#{index}`\u2800 {mem.name}', value=f"`{result['messages_count']:,}` messages", inline=False)
				pos_ += 1
				if mem == self.ctx.author:
					pos = pos_
		em.title = "Top 5 most active members"
		if pos != 0:
			em.set_footer(text=f'Your position: {pos:,}')
		
		await self.message.edit(embed=em, view=None)
		self.stop()
	
	@disnake.ui.button(label='Weekly Messages Top', style=disnake.ButtonStyle.blurple)
	async def weekly_messages_top(self, button: disnake.Button, inter: disnake.Interaction):
		data = await self.db.find_one({"_id": 374622847672254466})

		em = disnake.Embed(color=color.lightpink)
		
		index = 0
		guild = self.ctx.bot.get_guild(750160850077089853)
		
		results = await self.db.find().sort([("weekly_messages_count", -1)]).to_list(10)
		for result in results:
			if result['weekly_messages_count'] != 0:
				index += 1
				mem = guild.get_member(result['_id'])
				if mem == self.ctx.author:
					em.add_field(name="**`#%s\u2800%s` (YOU)**" % (index, mem.name), value="`{:,}` messages".format(result['weekly_messages_count']), inline=False)
				else:
					em.add_field(name="`#%s`\u2800%s" % (index, mem.name), value="`{:,}` messages".format(result['weekly_messages_count']), inline=False)
		em.title = "Top `%s` most active members this week" % (index)
		em.set_footer(text="Resets in %s" % (time.human_timedelta(data['weekly_reset'])), icon_url=self.ctx.author.display_avatar)

		await self.message.edit(embed=em, view=None)
		self.stop()
	
	@disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red, row=1)
	async def _stop_view(self, button: disnake.Button, inter: disnake.Interaction):
		await self.message.delete()
		self.stop()

class WeeklyTop(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db2['Levels']
		self.weekly_reset.start()
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@tasks.loop(minutes=1)
	async def weekly_reset(self):
		await self.bot.wait_until_ready()
		results = await self.db.find_one({"_id": 374622847672254466})
		resetWhen = results['weekly_reset']
		a = datetime.datetime.utcnow().strftime('%Y-%m-%d')
		dateNow = datetime.datetime.strptime(a, '%Y-%m-%d')
		
		if dateNow >= resetWhen:
			users = {}
			index = 0 
			results = await self.db.find().sort([("weekly_messages_count", -1)]).to_list(3)
			for result in results:
				index += 1
				user = self.bot.get_user(result['_id'])
				users[index] = user
			_1stplace = users[1]
			_2ndplace = users[2]
			_3rdplace = users[3]
			await self.db.update_one({'_id': _1stplace.id}, {'$inc':{'xp': 50000}})
			await self.db.update_one({'_id': _2ndplace.id}, {'$inc':{'xp': 30000}})
			await self.db.update_one({'_id': _3rdplace.id}, {'$inc':{'xp': 20000}})
			await _1stplace.send(f"Congrats. You placed `1st` in the weekly top! Your reward is **50,000** XP.\nThe others placed:\n\u2800• **{_2ndplace}** -> `2nd`\n\u2800• **{_3rdplace}** -> `3rd`")
			await _2ndplace.send(f"Congrats. You placed `2nd` in the weekly top! Your reward is **30,000** XP.\nThe others placed:\n\u2800• **{_1stplace}** -> `1st`\n\u2800• **{_3rdplace}** -> `3rd`")
			await _3rdplace.send(f"Congrats. You placed `3rd` in the weekly top! Your reward is **20,000** XP.\nThe others placed:\n\u2800• **{_1stplace}** -> `1st`\n\u2800• **{_2ndplace}** -> `2nd`")

			await self.db.update_many({}, {"$set": {"weekly_messages_count": 0}})
			x = dateNow + relativedelta(weeks = 1)
			await self.db.update_one({'_id': 374622847672254466}, {'$set':{'weekly_reset': x}})

	@commands.group(name='messages', invoke_without_command = True, case_insensitive = True, aliases=['msg'])
	async def _msgs(self, ctx, member: disnake.Member = None):
		"""Check your total amount of sent messages or someone else's."""

		member = member or ctx.author

		user_db = await self.db.find_one({'_id': member.id})
		if user_db is None:
			return await ctx.reply(f'`{member.display_name}` sent no messages.')
		em = disnake.Embed(color=color.lightpink)
		em.set_author(name=f'{member.display_name}\'s message stats', url=member.display_avatar, icon_url=member.display_avatar)
		em.add_field(name='Total Messages', value=f"`{user_db['messages_count']:,}`")
		em.add_field(name='Weekly Messages', value=f"`{user_db['weekly_messages_count']:,}`")
		em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.display_avatar)
		await ctx.send(embed=em)
	
	@_msgs.command(name='reset')
	@commands.is_owner()
	async def msg_reset(self, ctx, member: disnake.Member):
		"""Reset the amount of messages from the top for the member."""

		view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
		view.message = msg = await ctx.send("Are you sure you want to reset the total message count for member %s?" % (member.mention), view=view)
		await view.wait()
		if view.response is True:
			await self.db.update_one({'_id': member.id}, {'$set':{'messages_count': 0}})
			return await msg.edit(content='The total message count for member **%s** has been reset successfully.' % (member), view=view)
		
		elif view.response is False:
			return await msg.edit(content="Command to reset the message count for user `%s` has been canceled." % (member), view=view)


	@_msgs.group(name='top', invoke_without_command = True, case_insensitive = True, aliases=['lb'])
	async def msg_top(self, ctx):
		"""See the top 15 most active members of the server and when the top restarts."""
		
		if not ctx.channel.id in [750160851822182486, 750160851822182487, 752164200222163016, 855126816271106061]:
			return

		view = MessagesTopButtons(self.db, ctx)
		em = disnake.Embed(title='Please click the button of the top you wish to see.', color=color.reds)
		view.message = await ctx.send(embed=em, view=view)
	
	@msg_top.command(name='reset')
	@commands.is_owner()
	async def msg_top_reset(self, ctx, member: disnake.Member):
		"""Reset the amount of messages from the top for the member."""

		view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
		view.message = msg = await ctx.send("Are you sure you want to reset the message count for this week for member %s?" % (member.mention), view=view)
		await view.wait()
		if view.response is True:
			await self.db.update_one({'_id': member.id}, {'$set':{'weekly_messages_count': 0}})
			return await msg.edit(content='The message count for this week for member **%s** has been reset successfully.' % (member), view=view)
		
		elif view.response is False:
			return await msg.edit(content="Command to reset the message count for user `%s` has been canceled." % (member), view=view)


	@msg_top.command(aliases=['reward'])
	async def rewards(self, ctx):
		"""See what rewards you can get from the weekly messages top."""

		em = disnake.Embed(color=color.lightpink, title="Here are the rewards for the weekly top:")
		em.add_field(name="`1st Place`", value="**50k XP**", inline=False)
		em.add_field(name="`2nd Place`", value="**30k XP**", inline=False)
		em.add_field(name="`3rd Place`", value="**20k XP**", inline=False)
		em.set_footer(text="Requested by: %s" % (ctx.author), icon_url=ctx.author.display_avatar)
		await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(WeeklyTop(bot))
