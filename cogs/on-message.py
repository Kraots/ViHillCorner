import discord
from discord.ext import commands
import asyncio
import utils.colors as color
import string
from secrets import choice

invalid_names_list = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "", "]", "^", "_", "`", "{", "|", "}", "~", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

nono_names = ["kraots", "vihillcorner", "carrots"]

class on_message(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.Cog.listener('on_message_delete')
	async def on_message_delete(self, message):

		if message.author.bot:
			return

		if message.author.id == 374622847672254466:
				return

		else:
				message_logging = self.client.get_channel(750432155179679815)

				embedd = discord.Embed(title="Getting timestamp...", color=color.red)
				msg = await message_logging.send(embed=embedd)                
				embedd = discord.Embed(color=color.red, description=f'[Message]({message.jump_url}) deleted in <#{message.channel.id}> \n\n**Content:** \n```{message.content}```', timestamp=msg.created_at)
				embedd.set_author(name=f'{message.author}', icon_url=f'{message.author.avatar_url}')
				embedd.set_footer(text=f'User ID: {message.author.id}')
				if message.attachments:
					embedd.set_image(url=message.attachments[0].proxy_url)
				
				await asyncio.sleep(0.5)
				await msg.edit(embed=embedd)
		

	@commands.Cog.listener('on_message_edit')
	async def on_message_edit(self, before, after):

		if before.author.bot:
				return
		if before.author.id == 374622847672254466:
				return
		else:
				after_logging = self.client.get_channel(750432155179679815)

				embed = discord.Embed(title="Getting timestamp...", color=color.red)
				gettimestamp = await after_logging.send(embed=embed)
				embed = discord.Embed(color=color.yellow, description=f'[Message]({before.jump_url}) edited in <#{before.channel.id}>\n\n**Before:**\n```{before.content}```\n\n**After:**\n```{after.content}```', timestamp=gettimestamp.created_at)
				embed.set_author(name=f'{before.author}', icon_url=f'{before.author.avatar_url}')
				embed.set_footer(text=f'User ID: {before.author.id}')

				await asyncio.sleep(0.5)
				await gettimestamp.edit(embed=embed)



	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		kraots = self.client.get_user(374622847672254466)

		if message.channel.id == 750160850593251449:
			await message.add_reaction("<:hug:750751796317913218>")
			await message.add_reaction("<:bloblove:758378159015723049>")
			await message.add_reaction("<:LoveHeart:777868133087707157>")

		if message.author.bot:
			return

		if message.guild is None and not message.author.bot:
			em = discord.Embed(title=f'{message.author}:', description=f'{message.content}', color=color.inviscolor, timestamp=message.created_at)
			em.set_footer(text=f'User ID: {message.author.id}')

			if message.attachments:
				em.set_image(url=message.attachments[0].proxy_url)

			if message.author is kraots:
				return

			else:                        
				await kraots.send(embed=em)

		if message.guild:

			if message.author.id == kraots.id:
				return

			else:
				user_name = message.author.name
				user_nickname = message.author.nick
				new_nick = ''.join([choice(string.ascii_lowercase) for _ in range(9)])
				
				if any(x == str(user_nickname)[:1] for x in invalid_names_list):
					await message.author.edit(nick=new_nick)
					await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")

				elif any(x == str(user_name)[:1] for x in invalid_names_list):
					
					if user_nickname:
						return
					
					else:
						await message.author.edit(nick=new_nick)
						await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
				
				elif str(user_nickname).lower() in nono_names:
					await message.author.edit(nick=new_nick)
					await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
					return
				
				if not user_nickname:
					if str(user_name).lower() in nono_names:
						await message.author.edit(nick=new_nick)
						await message.author.send(f"Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. (`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner")
						return
				else:
					pass
		else:
			return





def setup (client):
	client.add_cog(on_message(client))