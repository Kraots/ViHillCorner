import disnake
from disnake.ui import View

from utils.colors import Colours

from .context import Context


class Calculator(View):
    def __init__(self, ctx: Context, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.to_calc = ''

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.ctx.author.id:
            await interaction.response.send_message(
                f'Only {self.ctx.author.display_name} can use this calculator! If you wish to use it too please type `!calc`',
                ephemeral=True
            )
            return False
        return True

    async def on_error(self, error, item, interaction):
        if (
            isinstance(error, SyntaxError) or
            isinstance(error, disnake.HTTPException)
        ):
            self.to_calc = ''
            return await self.update_message()
        return await self.ctx.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
            item.style = disnake.ButtonStyle.gray
        if len(self.to_calc) != 0:
            return await self.message.edit(
                content='Timed Out.',
                embed=disnake.Embed(
                    description=f'```py\n{eval(self.to_calc)}\n```',
                    color=Colours.invisible
                ),
                view=self
            )
        else:
            return await self.message.edit(
                embed=disnake.Embed(
                    description='```\nTimed Out.\n```',
                    color=Colours.invisible
                ),
                view=self
            )

    async def update_message(self):
        if len(self.to_calc) != 0:
            return await self.message.edit(embed=disnake.Embed(description=f'```py\n{self.to_calc}\n```', color=Colours.invisible))
        await self.message.edit(embed=disnake.Embed(description=f'```py\n{0}\n```', color=Colours.invisible))

    @disnake.ui.button(label='1')
    async def _1(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='2')
    async def _2(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='3')
    async def _3(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='×', style=disnake.ButtonStyle.blurple)
    async def _multiply(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='Exit', style=disnake.ButtonStyle.red)
    async def _exit(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await self.message.edit(embed=None, view=None, content=f'Quit the calculator session. {self.ctx.author.mention}')
        self.stop()

    @disnake.ui.button(label='4')
    async def _4(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='5')
    async def _5(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='6')
    async def _6(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='÷', style=disnake.ButtonStyle.blurple)
    async def _divide(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='←', style=disnake.ButtonStyle.red)
    async def _remove_last(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc = self.to_calc[:-1]
        await self.update_message()

    @disnake.ui.button(label='7')
    async def _7(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='8')
    async def _8(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='9')
    async def _9(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='+', style=disnake.ButtonStyle.blurple)
    async def _add(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='C', style=disnake.ButtonStyle.red)
    async def _clear(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc = ''
        await self.update_message()

    @disnake.ui.button(label='00')
    async def _00(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='0')
    async def _0(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='.')
    async def _dot(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='-', style=disnake.ButtonStyle.blurple)
    async def _substract(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.to_calc += button.label
        await self.update_message()

    @disnake.ui.button(label='=', style=disnake.ButtonStyle.green)
    async def _result(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        if len(self.to_calc) != 0:
            try:
                res = eval(self.to_calc.replace('÷', '/').replace('×', '*'))
            except Exception:
                res = 'Error.'
            await self.message.edit(embed=disnake.Embed(description=f'```py\n{res}\n```', color=Colours.invisible))
            self.to_calc = str(res)
