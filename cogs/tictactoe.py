import discord
from discord.ext import commands
import asyncio
import motor.motor_asyncio
import os
from utils.games import TicTacToe
bot_channels = [752164200222163016, 750160851822182486, 750160851822182487]

DBKEY = os.getenv('MONGODBKEY')

cluster = motor.motor_asyncio.AsyncIOMotorClient(DBKEY)
db = cluster['ViHillCornerDB']['Economy']

class TTT(commands.Cog):
	def __init__(self, client):
		self.client = client
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix and ctx.channel.id in bot_channels
	
	@commands.command(aliases=['ttt', 'tic-tac-toe'])
	async def tictactoe(self, ctx, member: discord.Member = None):
		if member is None:
			return await ctx.send(f"You must mention the person you wish to have a tic-tac-toe game with. {ctx.author.mention}")
		elif member is ctx.author:
			return await ctx.send(f"You cannot play with yourself. {ctx.author.mention}")

		user = await db.find_one({'_id': ctx.author.id})
		opponent = await db.find_one({'_id': member.id})
		
		if user is None:
			await ctx.send(f"{ctx.author.mention} You must first register. To do that type `!register`")
			return		
		if opponent is None:
			await ctx.send(f"**{member.display_name}** is not registered. {ctx.author.mention}")
			return
		
		if user['wallet'] < 10000:
			await ctx.send(f"You must have `10,000` <:carrots:822122757654577183> in your wallet to play. {ctx.author.mention}")
			return
		if opponent['wallet'] < 10000:
			await ctx.send(f"**{member.display_name}** does not have `10,000` <:carrots:822122757654577183> in their wallet. Cannot play. {ctx.author.mention}")
			return

		def check(reaction, user):
			return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == member.id
		
		msg = await ctx.send(f"{ctx.author.mention} Wants to play tic-tac-toe with you {member.mention}. Do you accept?\nWinner gets **10,000** <:carrots:822122757654577183>\nLoser loses **10,000** <:carrots:822122757654577183>")
		await msg.add_reaction('<:agree:797537027469082627>')
		await msg.add_reaction('<:disagree:797537030980239411>')

		try:
			reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)

		except asyncio.TimeoutError:
			new_msg = f"{member.mention} Did not react in time."
			await msg.edit(content=new_msg)
			await msg.clear_reactions()
			return
		
		else:
			if str(reaction.emoji) == '<:agree:797537027469082627>':
				await msg.delete()
				ttt = TicTacToe(ctx.author, member, ctx, self.client)
				await ttt.start()
			elif str(reaction.emoji) == '<:disagree:797537030980239411>':
				await ctx.reply(f"**{member.mention}** does not want to play tic-tac-toe with you.")
				await msg.delete()

	@tictactoe.error
	async def ttt_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send(error.original)


def setup (client):
	client.add_cog(TTT(client))