import disnake


all_roles = [
	750272224170082365, 750160850299387977, 750160850299387976, 750160850299387975, 
	750160850299387974, 750160850299518985, 750160850299518984, 750160850299518983, 
	750160850299518982, 750160850299518981, 750160850299518980, 750160850299518979, 
	750160850299518978, 750160850299518977, 750160850295324752, 750160850299518976, 
	750160850295324751, 750272729533644850, 788112413261168660]

roles = {
	'vhc:reaction_roles:Illusion': 750160850299518980, 'vhc:reaction_roles:Black': 750160850299387974, 'vhc:reaction_roles:Screaming_Green': 750160850299518984, 
	'vhc:reaction_roles:Electric_Violet': 750160850299518983, 'vhc:reaction_roles:Red_Orange': 750160850299387977, 'vhc:reaction_roles:Dodger_Blue': 750160850299387975, 
	'vhc:reaction_roles:Spring_Green': 750272224170082365, 'vhc:reaction_roles:Madang': 750160850299518977, 'vhc:reaction_roles:Perfume': 750160850299518981, 
	'vhc:reaction_roles:Ice_Cold': 750160850299518979, 'vhc:reaction_roles:Primrose': 750160850299518976, 'vhc:reaction_roles:Orchid': 750272729533644850, 
	'vhc:reaction_roles:Mandys_Pink': 750160850295324751, 'vhc:reaction_roles:Perano': 750160850295324752, 'vhc:reaction_roles:Turquoise': 750160850299387976, 
	'vhc:reaction_roles:Wewak': 750160850299518978, 'vhc:reaction_roles:Sunshade': 750160850299518982, 'vhc:reaction_roles:White': 788112413261168660, 
	'vhc:reaction_roles:Broom': 750160850299518985}


class ButtonRoles(disnake.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@disnake.ui.button(label='Illusion', custom_id='vhc:reaction_roles:Illusion', emoji='<:illusion:886669987660574803>')
	async def Illusion(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Black', custom_id='vhc:reaction_roles:Black', emoji='<:black:886669987752841216>')
	async def Black(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Screaming Green', custom_id='vhc:reaction_roles:Screaming_Green', emoji='<:screaming_green:886669987769626636>')
	async def Screaming_Green(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Electric Violet', custom_id='vhc:reaction_roles:Electric_Violet', emoji='<:electric_violet:886669987798986804>')
	async def Electric_Violet(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Red Orange', custom_id='vhc:reaction_roles:Red_Orange', emoji='<:red_orange:886669987798999062>')
	async def Red_Orange(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Dodger Blue', custom_id='vhc:reaction_roles:Dodger_Blue', emoji='<:dodger_blue:886669987916427294>')
	async def Dodger_Blue(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Spring Green', custom_id='vhc:reaction_roles:Spring_Green', emoji='<:spring_green:886669987924815923>')
	async def Spring_Green(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Madang', custom_id='vhc:reaction_roles:Madang', emoji='<:madang:886669987991941181>')
	async def Madang(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Perfume', custom_id='vhc:reaction_roles:Perfume', emoji='<:perfume:886669988008710174>')
	async def Perfume(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Ice Cold', custom_id='vhc:reaction_roles:Ice_Cold', emoji='<:ice_cold:886669988008710194>')
	async def Ice_Cold(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Primrose', custom_id='vhc:reaction_roles:Primrose', emoji='<:primrose:886669988008718336>')
	async def Primrose(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Orchid', custom_id='vhc:reaction_roles:Orchid', emoji='<:orchid:886675375185350696>')
	async def Orchid(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Mandys Pink', custom_id='vhc:reaction_roles:Mandys_Pink', emoji='<:mandys_pink:886669988038062154>')
	async def Mandys_Pink(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Perano', custom_id='vhc:reaction_roles:Perano', emoji='<:perano:886669988063227965>')
	async def Perano(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Turquoise', custom_id='vhc:reaction_roles:Turquoise', emoji='<:turquoise:886669988176470046>')
	async def Turquoise(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Wewak', custom_id='vhc:reaction_roles:Wewak', emoji='<:wewak:886669988214243379>')
	async def Wewak(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Sunshade', custom_id='vhc:reaction_roles:Sunshade', emoji='<:sunshade:886669988289720410>')
	async def Sunshade(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='White', custom_id='vhc:reaction_roles:White', emoji='<:white:886669988558176306>')
	async def White(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')

	@disnake.ui.button(label='Broom', custom_id='vhc:reaction_roles:Broom', emoji='<:broom:886669989636100156>')
	async def Broom(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		_roles = [role for role in interaction.author.roles if not role.id in all_roles]
		_roles.append(interaction.guild.get_role(roles[button.custom_id]))
		await interaction.author.edit(roles=_roles, reason='Colour role update.')