import disnake
from disnake.ext import commands

import asyncio

class OnBanAppealJoin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener('on_member_join')
	async def on_member_join(self, member):
		found = False
		if member.guild.id == 788384492175884299:
			vhc = self.bot.get_guild(750160850077089853)
			bans = await vhc.bans()
			for i in range(len(bans)):
				if bans[i][1].id == member.id:
					_ban_reason = bans[i][0].split(':', 1)
					ban_reason = _ban_reason[1].rstrip()
					moderator = _ban_reason[0].rstrip()
					found = True
					break
				
			if found == False:
				await member.send("You are not banned. Cannot join this guild.")
				await member.kick()
				return
			
			g = self.bot.get_guild(788384492175884299)
			overwrites = {
					g.default_role: disnake.PermissionOverwrite(read_messages = False)
						}
			channel = await g.create_text_channel(f"{member.name}-ban-appeal", overwrites=overwrites)
			await channel.edit(topic=member.id)
			em = disnake.Embed(title="Ban Reason", description=ban_reason)
			m = await channel.send(f"Hello {member.name}! You have been banned by moderator: `{moderator}`\nSend your unban appeal here. {member.mention}", embed=em)
			await m.pin()
			await channel.purge(limit=1)
			await channel.set_permissions(member, read_messages = True)
			ch = member.guild.get_channel(788488359306592316)
			await ch.send('A new member has joined the ban appeal. <@!374622847672254466> <@!747329236695777340>')
	
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
	async def on_message(self, message: disnake.Message):
		if message.guild:
			if message.guild.id == 788384492175884299:
				if message.content.lower() == 'bye':
					if 788384677987352608 in [role.id for role in message.author.roles] or message.author.id == 374622847672254466:
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
							reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20)

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


def setup(bot):
	bot.add_cog(OnBanAppealJoin(bot))