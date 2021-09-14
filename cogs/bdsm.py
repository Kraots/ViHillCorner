import disnake
from disnake.ext import commands
import asyncio
import datetime

class Bdsm(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db1 = bot.db2['bdsm results']
		self.db2 = bot.db2['Confesscord Restrictions']
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def bdsm(self, ctx):
		"""Base command for all the bdsm commands."""

		await ctx.send("`!help bdsm` for a list of commands.")
	
	@bdsm.command(name='set')
	async def bdsm_set(self, ctx):
		"""Set your bdsm results"""

		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		
		await ctx.send("Please send the screenshot of your BDSM results. %s" % (ctx.author.mention))
		
		hasBdsm = await self.db1.find_one({'_id': ctx.author.id})

		try:
			while True:
				raw_result = await self.bot.wait_for('message', check=check, timeout=180)
				if raw_result.content.lower() == "!cancel":
					await raw_result.reply("Canceled.")
					return
			
				try:
					BDSMresult = raw_result.attachments[0].url

					if hasBdsm != None:
						await self.db1.update_one({'_id': ctx.author.id}, {'$set':{'BDSMresult': BDSMresult}})
						await self.db1.update_one({'_id': ctx.author.id}, {'$set':{'timestamp': datetime.datetime.utcnow()}})
						await ctx.send("Succesfully updated your bdsm result. To check your bdsm results or others, you can type `!bdsm results <member>`.")
						return
					
					post = {'_id': ctx.author.id,
							'BDSMresult': BDSMresult,
							'timestamp': datetime.datetime.utcnow()
							}
					await self.db1.insert_one(post)

					await ctx.send("Succesfully set your bdsm result. To check your bdsm results or others, you can type `!bdsm results <member>`.")
					return

				except:
					await ctx.send("You must send an image from your gallery, not an image url.")
		
		except asyncio.TimeoutError:
			await ctx.send("You ran out of time, type the command again to set your bdsm results. %s " % (ctx.author.mention))
			return
	
	@bdsm.command(name='results', aliases=['result'])
	async def bdsm_results(self, ctx, member: disnake.Member = None):
		"""See the member's bdsm results"""

		member = member or ctx.author

		BDSMresult = await self.db1.find_one({'_id': member.id})
		
		if BDSMresult != None:
			em = disnake.Embed(color=member.color, title="Here's `%s` bdsm results:" % (member.display_name))
			em.set_image(url=BDSMresult['BDSMresult'])
			BDSMtimestamp = BDSMresult['timestamp']
			BDSMtimestamp = BDSMtimestamp.strftime("%Y-%m-%d %H:%M:%S")
			em.set_footer(text=f"Result set on: {BDSMtimestamp} (UTC timezone)", icon_url=member.display_avatar)
			await ctx.send(embed=em)
		
		else:
			await ctx.send("That user did not set their bdsm results.")

	@bdsm.command(name='remove', aliases=['delete'])
	async def bdsm_remove(self, ctx):
		"""Remove your bdsm results"""

		user = ctx.author
		
		hasBdsm = await self.db1.find_one({'_id': user.id})

		if hasBdsm != None:
			view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
			view.message = msg = await ctx.send("Are you sure you want to remove your bdsm results? %s" % (user.mention), view=view)
			await view.wait()
			if view.response is True:
				await self.db1.delete_one({'_id': user.id})
				e = "Succesfully removed your bdsm results. %s" % (user.mention)
				return await msg.edit(content=e, view=view)

			elif view.response is False:
				e = "Okay, your bdsm results have not been removed. %s" % (user.mention)
				return await msg.edit(content=e, view=view)

		else:
			await ctx.send("There are no bdsm results to delete, you don't have them set. To set your bdsm results type `!bdsm set`, and then send the screenshot of your results. %s" % (user.mention))

	@bdsm.command(name='test')
	async def bdsm_test(self, ctx):
		"""Get a link to go and do your bdsm test to get your results."""

		await ctx.send("Click the link below to take your bdsm test: \nhttps://bdsmtest.org")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db1.delete_one({'_id': member.id})
		await self.db2.delete_one({'_id': member.id})

def setup(bot):
	bot.add_cog(Bdsm(bot))