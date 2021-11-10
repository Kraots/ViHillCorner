import random
import inspect

import disnake

from utils.context import Context

from main import ViHillCorner

__all__ = (
    'Fight',
)


class Fight(disnake.ui.View):
    def __init__(self, pl1: disnake.Member, pl2: disnake.Member, ctx: Context, *, timeout=30.0):
        super().__init__(timeout=timeout)
        self.p1 = pl1
        self.p2 = pl2
        self.ctx = ctx
        self.bot: ViHillCorner = ctx.bot
        self.hp = {self.p1: 100, self.p2: 100}
        self.turn = pl1
        self.ended = False

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.turn.id:
            if interaction.author.id not in (self.p1.id, self.p2.id):
                await interaction.response.send_message(
                    'You are not playing in this game! To start a game with someone you must type `!fight <member>`',
                    ephemeral=True
                )
                return False
            await interaction.response.send_message(f'Not your turn, it\'s {self.turn.display_name}\'s turn', ephemeral=True)
            return False
        return True

    async def on_error(self, error: Exception, item, interaction):
        return await self.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        for item in self.children:
            item.style = disnake.ButtonStyle.grey
            item.disabled = True
        if self.turn == self.p1:
            winner = self.p2
        else:
            winner = self.p1
        await self.message.edit(
            content=f'{self._data}\n\n**___TIMEOUT___**\n**{self.turn.display_name}** took too much to react. {winner.mention} won.',
            view=self
        )

    def update_turn(self):
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1

    @property
    def _data(self) -> str:
        data = inspect.cleandoc(
            f'''
            `{self.p1.display_name}` **==> {self.hp[self.p1]} hp**
            `{self.p2.display_name}` **==> {self.hp[self.p2]} hp**
            '''
        )
        return data

    async def check_health(self) -> bool:
        winner = None
        if self.hp[self.p1] <= 0:
            winner = self.p2
        elif self.hp[self.p2] <= 0:
            winner = self.p1
        if winner is not None:
            self.ended = True
            for item in self.children:
                item.style = disnake.ButtonStyle.grey
                item.disabled = True
            await self.message.edit(content=f'{self._data}\n\n**{winner.display_name}** won.\n{self.turn.mention} you lost!', view=self)
            self.stop()

    @disnake.ui.button(label='Fight', style=disnake.ButtonStyle.red)
    async def _fight_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()

        p = self.turn
        self.update_turn()
        curr_hp = self.hp[self.turn]
        dmg = random.randint(1, 51)
        new_hp = curr_hp - dmg
        self.hp[self.turn] = new_hp
        await self.check_health()
        if self.ended is False:
            await self.message.edit(content=f'{self._data}\n\n**{p.display_name}** chose to fight and dealt `{dmg}` damage. Your turn now: {self.turn.mention}')

    @disnake.ui.button(label='Health', style=disnake.ButtonStyle.green)
    async def _health_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()

        p = self.turn
        curr_hp = self.hp[self.turn]
        hp = random.randint(1, 41)
        new_hp = curr_hp + hp
        self.hp[self.turn] = new_hp
        self.update_turn()
        await self.message.edit(content=f'{self._data}\n\n**{p.display_name}** chose health and got `{hp}` hp. Your turn now: {self.turn.mention}')

    @disnake.ui.button(label='Forfeit', style=disnake.ButtonStyle.blurple, row=1)
    async def _forfeit_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()

        p = self.turn
        self.update_turn()
        for item in self.children:
            item.style = disnake.ButtonStyle.grey
            item.disabled = True
        await self.message.edit(content=f'{self._data}\n\n**___FORFEIT___**\n**{p.display_name}** forfeited, {self.turn.mention} you won!', view=self)
        self.stop()
