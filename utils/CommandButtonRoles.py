import disnake


all_roles = [
    750272224170082365, 750160850299387977, 750160850299387976, 750160850299387975, 
    750160850299387974, 750160850299518985, 750160850299518984, 750160850299518983, 
    750160850299518982, 750160850299518981, 750160850299518980, 750160850299518979, 
    750160850299518978, 750160850299518977, 750160850295324752, 750160850299518976, 
    750160850295324751, 750272729533644850, 788112413261168660, 754680420364451890]

roles = {
    'Illusion': 750160850299518980, 'Black': 750160850299387974, 'Screaming Green': 750160850299518984, 
    'Electric Violet': 750160850299518983, 'Red Orange': 750160850299387977, 'Dodger Blue': 750160850299387975, 
    'Spring Green': 750272224170082365, 'Madang': 750160850299518977, 'Perfume': 750160850299518981, 
    'Ice Cold': 750160850299518979, 'Primrose': 750160850299518976, 'Orchid': 750272729533644850, 
    'Mandys Pink': 750160850295324751, 'Perano': 750160850295324752, 'Turquoise': 750160850299387976, 
    'Wewak': 750160850299518978, 'Sunshade': 750160850299518982, 'White': 788112413261168660, 
    'Broom': 750160850299518985, 'Owner Only Red': 754680420364451890}

class CommandButtonRole(disnake.ui.Select['ButtonRoleView']):
    def __init__(self):
        super().__init__(placeholder='Select a colour...', min_values=1, max_values=1)
        self._fill_options()
    
    def _fill_options(self):
        self.add_option(label='Illusion', emoji='<:illusion:886669987660574803>')
        self.add_option(label='Black', emoji='<:black:886669987752841216>')
        self.add_option(label='Screaming Green', emoji='<:screaming_green:886669987769626636>')
        self.add_option(label='Electric Violet', emoji='<:electric_violet:886669987798986804>')
        self.add_option(label='Red Orange', emoji='<:red_orange:886669987798999062>')
        self.add_option(label='Dodger Blue', emoji='<:dodger_blue:886669987916427294>')
        self.add_option(label='Spring Green', emoji='<:spring_green:886669987924815923>')
        self.add_option(label='Madang', emoji='<:madang:886669987991941181>')
        self.add_option(label='Perfume', emoji='<:perfume:886669988008710174>')
        self.add_option(label='Ice Cold', emoji='<:ice_cold:886669988008710194>')
        self.add_option(label='Primrose', emoji='<:primrose:886669988008718336>')
        self.add_option(label='Orchid', emoji='<:orchid:886675375185350696>')
        self.add_option(label='Mandys Pink', emoji='<:mandys_pink:886669988038062154>')
        self.add_option(label='Perano', emoji='<:perano:886669988063227965>')
        self.add_option(label='Turquoise', emoji='<:turquoise:886669988176470046>')
        self.add_option(label='Wewak', emoji='<:wewak:886669988214243379>')
        self.add_option(label='Sunshade', emoji='<:sunshade:886669988289720410>')
        self.add_option(label='White', emoji='<:white:886669988558176306>')
        self.add_option(label='Broom', emoji='<:broom:886669989636100156>')

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        _roles = [role for role in interaction.author.roles if not role.id in all_roles]
        _roles.append(interaction.guild.get_role(roles[value]))
        await interaction.author.edit(roles=_roles, reason='Colour role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your colour to `{value}`')

class ButtonRoleView(disnake.ui.View):
    def __init__(self, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.add_item(CommandButtonRole())
    
    async def on_error(self, error, item, interaction):
        return await self.ctx.bot.reraise(self.ctx, error)
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'{self.ctx.author.display_name} is using this menu. If you wish to use it too please type `!colours`', ephemeral=True)
            return False
        return True


class OwnerCommandButtonRole(disnake.ui.Select['ButtonRoleView']):
    def __init__(self):
        super().__init__(placeholder='Select a colour master...', min_values=1, max_values=1)
        self._fill_options()
    
    def _fill_options(self):
        self.add_option(label='Owner Only Red', emoji='<:owner_only_red:888082854695829574>')
        self.add_option(label='Illusion', emoji='<:illusion:886669987660574803>')
        self.add_option(label='Black', emoji='<:black:886669987752841216>')
        self.add_option(label='Screaming Green', emoji='<:screaming_green:886669987769626636>')
        self.add_option(label='Electric Violet', emoji='<:electric_violet:886669987798986804>')
        self.add_option(label='Red Orange', emoji='<:red_orange:886669987798999062>')
        self.add_option(label='Dodger Blue', emoji='<:dodger_blue:886669987916427294>')
        self.add_option(label='Spring Green', emoji='<:spring_green:886669987924815923>')
        self.add_option(label='Madang', emoji='<:madang:886669987991941181>')
        self.add_option(label='Perfume', emoji='<:perfume:886669988008710174>')
        self.add_option(label='Ice Cold', emoji='<:ice_cold:886669988008710194>')
        self.add_option(label='Primrose', emoji='<:primrose:886669988008718336>')
        self.add_option(label='Orchid', emoji='<:orchid:886675375185350696>')
        self.add_option(label='Mandys Pink', emoji='<:mandys_pink:886669988038062154>')
        self.add_option(label='Perano', emoji='<:perano:886669988063227965>')
        self.add_option(label='Turquoise', emoji='<:turquoise:886669988176470046>')
        self.add_option(label='Wewak', emoji='<:wewak:886669988214243379>')
        self.add_option(label='Sunshade', emoji='<:sunshade:886669988289720410>')
        self.add_option(label='White', emoji='<:white:886669988558176306>')
        self.add_option(label='Broom', emoji='<:broom:886669989636100156>')

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        _roles = [role for role in interaction.author.roles if not role.id in all_roles]
        _roles.append(interaction.guild.get_role(roles[value]))
        await interaction.author.edit(roles=_roles, reason='Colour role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your colour to `{value}`')


class ButtonRoleViewOwner(disnake.ui.View):
    def __init__(self, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.add_item(OwnerCommandButtonRole())
    
    async def on_error(self, error, item, interaction):
        return await self.ctx.bot.reraise(self.ctx, error)
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        
    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(f'My master is using this menu 😡. If you wish to use it too please type `!colours`', ephemeral=True)
            return False
        return True