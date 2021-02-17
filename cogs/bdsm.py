import discord
from discord.ext import commands
import motor.motor_asyncio
import os
import utils.colors as color
import asyncio
import datetime
DBKEY = os.getenv('MONGODBLVLKEY')

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']
collection = db['bdsm results']

class BdsmResults(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command = True, case_insensitive = True)
	async def bdsm(self, ctx):
		em = discord.Embed(color=color.lightpink, title="BDSM commands:	", description="`!bdsm results <member>` - send the bdsm results of the specified member. \n`!bdsm set` - set your bdsm result by sending the screenshot of your results. \n`!bdsm test` - take the test, duh.")
		await ctx.send(embed=em)
	
	@bdsm.command()
	async def set(self, ctx):
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		
		await ctx.send("Please send the screenshot of your BDSM results. %s" % (ctx.author.mention))
		
		try:
			raw_result = await self.client.wait_for('message', check=check, timeout=180)
		
			try:
				BDSMresult = raw_result.attachments[0].url
				
				post = {'_id': ctx.author.id,
						'BDSMresult': BDSMresult,
						'timestamp': datetime.datetime.utcnow()
						}
				await collection.insert_one(post)

				await ctx.send("Succesfully set your bdsm result. To check your bdsm results or others, you can type `!bdsm results <member>`.")

			except:
				await ctx.send("You must send an image from your gallery, not an image url.")
		
		except asyncio.TimeoutError:
			await ctx.send("You ran out of time, type the command again to set your bdsm results. %s " % (ctx.author.mention))
			return
	
	@bdsm.command(aliases=['result'])
	async def results(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		BDSMresult = await collection.find_one({'_id': member.id})
		
		if BDSMresult != None:
			em = discord.Embed(color=member.color, title="Here's `%s` bdsm results:" % (member.display_name))
			em.set_image(url=BDSMresult['BDSMresult'])
			BDSMtimestamp = BDSMresult['timestamp']
			BDSMtimestamp = BDSMtimestamp.strftime("%Y-%m-%d %H:%M:%S")
			em.set_footer(text=f"Result set on: {BDSMtimestamp} (UTC timezone)", icon_url=member.avatar_url)
			await ctx.send(embed=em)
		
		else:
			await ctx.send("That user did not set their bdsm results.")

	@bdsm.command()
	async def test(self, ctx):
		await ctx.send("Click the link below to take your bdsm test: \nhttps://bdsmtest.org")

def setup (client):
	client.add_cog(BdsmResults(client))