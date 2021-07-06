import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		guild = self.client.get_guild(750160850077089853)

		COLORSMSG1 = 779389485573079071
		COLORSMSG2 = 779389533875601451
		COLORSMSG3 = 788117110475718728

		# ------------------------------------

		if payload.message_id == 862009256421359657:
			if payload.member.id != 374622847672254466:
				if str(payload.emoji) in ['<a:kiss1:761219243232067615>', '<a:kiss2:761219249896816661>', '<a:hearthug:759685245422927892>']:
					ch = guild.get_channel(payload.channel_id)
					msg = await ch.fetch_message(862009256421359657)
					await msg.remove_reaction(payload.emoji, payload.member)
					await payload.member.send("You cannot add this type of reaction you scum. That person is taken and only carrots can add them :rage:\nBtw this has been sent to me so be prepared to die :smiley: :knife:")
					kraots = guild.get_member(374622847672254466)
					await kraots.send(f"`{payload.member}` added the reaction {payload.emoji} to your bbg's intro master, punish them :smiling_imp:")

		# ------------------------------------


		message_id = payload.message_id
		member = payload.member

		all_colors = [750272224170082365, 750160850299387977, 750160850299387976, 750160850299387975, 750160850299387974, 750160850299518985, 750160850299518984, 750160850299518983, 750160850299518982, 750160850299518981, 750160850299518980, 750160850299518979, 750160850299518978, 750160850299518977, 750160850295324752, 750160850299518976, 750160850295324751, 750272729533644850, 788112413261168660]

		msg1_emojis = {'\U00000031\U0000fe0f\U000020e3': 750272224170082365, 
						'\U00000032\U0000fe0f\U000020e3': 750160850299387977, 
						'\U00000033\U0000fe0f\U000020e3': 750160850299387976,
						'\U00000034\U0000fe0f\U000020e3': 750160850299387975,
						'\U00000035\U0000fe0f\U000020e3': 750160850299387974,
						'\U00000036\U0000fe0f\U000020e3': 750160850299518985,
						'\U00000037\U0000fe0f\U000020e3': 750160850299518984,
						'\U00000038\U0000fe0f\U000020e3': 750160850299518983,
						'\U00000039\U0000fe0f\U000020e3': 750160850299518982,
						}

		msg2_emojis = {'\U00000031\U0000fe0f\U000020e3': 750160850299518981, 
						'\U00000032\U0000fe0f\U000020e3': 750160850299518980, 
						'\U00000033\U0000fe0f\U000020e3': 750160850299518979,
						'\U00000034\U0000fe0f\U000020e3': 750160850299518978,
						'\U00000035\U0000fe0f\U000020e3': 750160850299518977,
						'\U00000036\U0000fe0f\U000020e3': 750160850295324752,
						'\U00000037\U0000fe0f\U000020e3': 750160850299518976,
						'\U00000038\U0000fe0f\U000020e3': 750160850295324751,
						'\U00000039\U0000fe0f\U000020e3': 750272729533644850,
						}

		msg3_emojis = {'\U00000031\U0000fe0f\U000020e3': 788112413261168660
						}

		try:
			member_roles = []
			for x in member.roles:
				if not x.id in all_colors:
					member_roles.append(x.id)

			member_roles = set(member_roles)

			Roles = []
			for id in member_roles:
				role = guild.get_role(id)
				Roles.append(role)

		except:
			pass
				

				# COLOR
		try:
			if message_id == COLORSMSG1:
				the_emoji = payload.emoji.name
				role = msg1_emojis[the_emoji]
				final_role = guild.get_role(role)
				Roles.append(final_role)
				await member.edit(roles=Roles)
				return


			elif message_id == COLORSMSG2:
				the_emoji = payload.emoji.name
				role = msg2_emojis[the_emoji]
				final_role = guild.get_role(role)
				Roles.append(final_role)
				await member.edit(roles=Roles)
				return

			elif message_id == COLORSMSG3:
				the_emoji = payload.emoji.name
				role = msg3_emojis[the_emoji]
				final_role = guild.get_role(role)
				Roles.append(final_role)
				await member.edit(roles=Roles)
				return
		
		except:
			pass



def setup (client):
	client.add_cog(ReactionRoles(client))