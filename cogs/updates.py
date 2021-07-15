import motor.motor_asyncio
import os
from discord.ext import commands
import datetime
from utils import time
import discord
import utils.colors as color

DBKEY = os.getenv('MONGODBKEY')

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']['Updates']

class Updates(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.prefix = '!'
	def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.group(invoke_without_command = True, case_insensitive = True, aliases=['updates'])
	async def update(self, ctx):
		update = await db.find_one({'_id': 374622847672254466})
		updatedMsg = update['update']
		updatedDate = time.human_timedelta(dt=update['date'], accuracy=3, brief=False, suffix=True)
		em = discord.Embed(title="Here's what's new to the bot:", description=f"{updatedMsg}\n\n*{updatedDate}*", color=color.red)
		em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=em, reference=ctx.replied_reference)
	
	@update.command(aliases=['set'])
	@commands.is_owner()
	async def _set(self, ctx, *, args: str):
		args = args.replace('```py', '')
		args = args.replace('```', '')
		await db.update_one({'_id': ctx.author.id}, {'$set':{'update': args, 'date': datetime.datetime.utcnow()}})
		await ctx.reply('Operation successful.')

def setup (bot):
	bot.add_cog(Updates(bot))