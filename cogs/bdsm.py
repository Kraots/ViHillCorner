import discord
from discord.ext import commands
import asyncio
import datetime

class BdsmResults(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db1 = bot.db2['bdsm results']
		self.db2 = bot.db2['Confesscord Restrictions']
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def bdsm(self, ctx):
		command = self.bot.get_command('help')
		await ctx.invoke(command, 'bdsm')
	
	@bdsm.command()
	async def set(self, ctx):
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
	
	@bdsm.command(aliases=['result'])
	async def results(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		BDSMresult = await self.db1.find_one({'_id': member.id})
		
		if BDSMresult != None:
			em = discord.Embed(color=member.color, title="Here's `%s` bdsm results:" % (member.display_name))
			em.set_image(url=BDSMresult['BDSMresult'])
			BDSMtimestamp = BDSMresult['timestamp']
			BDSMtimestamp = BDSMtimestamp.strftime("%Y-%m-%d %H:%M:%S")
			em.set_footer(text=f"Result set on: {BDSMtimestamp} (UTC timezone)", icon_url=member.avatar_url)
			await ctx.send(embed=em)
		
		else:
			await ctx.send("That user did not set their bdsm results.")

	@bdsm.command(aliases=['delete'])
	async def remove(self, ctx):
		user = ctx.author
		
		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == ctx.author.id
		
		msg = await ctx.send("Are you sure you want to remove your bdsm results? %s" % (user.mention))
		await msg.add_reaction('<:agree:797537027469082627>')
		await msg.add_reaction('<:disagree:797537030980239411>')
		hasBdsm = await self.db1.find_one({'_id': user.id})

		if hasBdsm != None:			
			try:
				reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=180)

			except asyncio.TimeoutError:
				new_msg = f"{ctx.author.mention} Did not react in time."
				await msg.edit(content=new_msg)
				await msg.clear_reactions()
				return
			
			else:
				if str(reaction.emoji) == '<:agree:797537027469082627>':
					await self.db1.delete_one({'_id': user.id})
					e = "Succesfully removed your bdsm results. %s" % (user.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return
				
				elif str(reaction.emoji) == '<:disagree:797537030980239411>':
					e = "Okay, your bdsm results have not been removed. %s" % (user.mention)
					await msg.edit(content=e)
					await msg.clear_reactions()
					return

		else:
			await ctx.send("There are no bdsm results to delete, you don't have them set. To set your bdsm results type `!bdsm set`, and then send the screenshot of your results. %s" % (user.mention))

	@bdsm.command()
	async def test(self, ctx):
		await ctx.send("Click the link below to take your bdsm test: \nhttps://bdsmtest.org")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id == 374622847672254466:
			return
		await self.db1.delete_one({'_id': member.id})
		await self.db2.delete_one({'_id': member.id})

def setup(bot):
	bot.add_cog(BdsmResults(bot))