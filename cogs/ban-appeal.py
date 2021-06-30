import discord
from discord.ext import commands

import asyncio

class OnBanAppealJoin(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener('on_member_join')
	async def on_member_join(self, member):
		found = False
		if member.guild.id == 788384492175884299:
			vhc = self.client.get_guild(750160850077089853)
			bans = await vhc.bans()
			for i in range(len(bans)):
				if bans[i][1].id == member.id:
					_ban_reason = bans[i][0].split('--->')
					ban_reason = _ban_reason[1].rstrip()
					moderator = _ban_reason[0].rstrip()
					found = True
					break
				
			if found == False:
				await member.send("You are not banned. Cannot join this guild.")
				await member.kick()
				return
			
			g = self.client.get_guild(788384492175884299)
			overwrites = {
					g.default_role: discord.PermissionOverwrite(read_messages = False)
						}
			channel = await g.create_text_channel(f"{member.name}-ban-appeal", overwrites=overwrites)
			await channel.edit(topic=member.id)
			await channel.send(f"You have been banned by the moderator `{moderator}`\n*Reason:*\n**{ban_reason}**")
			await channel.set_permissions(member, read_messages = True)
	
	@commands.Cog.listener('on_member_remove')
	async def on_member_remove(self, member):
		g = member.guild
		for ch in g.text_channels:
			try:
				if member.id == int(ch.topic):
					await ch.delete()
			except:
				pass


	@commands.Cog.listener('on_message')
	async def on_message(self, message: discord.Message):
		if message.guild:
			if message.guild.id == 788384492175884299:
				if message.content.lower() == 'bye':
					if 374622847672254466 in [role.id for role in message.author.roles] or message.author.id == 374622847672254466:
						found = False
						for obj in message.channel.overwrites:
							if obj.id == int(message.channel.topic):
								found = True
								mem = message.guild.get_member(obj.id)
								break
						if found == False:
							return
						def check(reaction, user):
							return str(reaction.emoji) in ['<:agree:797537027469082627>', '<:disagree:797537030980239411>'] and user.id == message.author.id
						await message.add_reaction('<:agree:797537027469082627>')
						await message.add_reaction('<:disagree:797537030980239411>')
						try:
							reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=20)

						except asyncio.TimeoutError:
							await message.clear_reactions()
							return
						
						else:
							if str(reaction.emoji) == '<:agree:797537027469082627>':
								await mem.ban(reason=f"Denied unbanning (by {message.author})")
								await message.channel.delete()
							
							elif str(reaction.emoji) == '<:disagree:797537030980239411>':
								await message.clear_reactions()
								return


def setup (client):
	client.add_cog(OnBanAppealJoin(client))