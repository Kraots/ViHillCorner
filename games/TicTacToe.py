import disnake
from utils.context import Context


class TicTacToe(disnake.ui.View):
    def __init__(self, p1: disnake.Member, p2: disnake.Member, ctx: Context, *, timeout= 60.0):
        super().__init__(timeout=timeout)
        self.p1 = p1
        self.p2 = p2
        self.ctx = ctx
        self.bot = ctx.bot
        self.db = ctx.bot.db1['Economy']
        self.turn = p1
        self.new_label = {self.p1: 'X', self.p2: 'O'}
        self.new_style = {self.p1: disnake.ButtonStyle.red, self.p2: disnake.ButtonStyle.green}
        self.board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.ended = False

    async def on_error(self, error, item, interaction):
        return await self.bot.reraise(self.ctx, error)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.turn == self.p1:
            winner = self.p2
        else:
            winner = self.p1
        await self.db.update_one({'_id': self.turn.id}, {'$inc':{'wallet': -10000}})
        await self.db.update_one({'_id': winner.id}, {'$inc':{'wallet': 10000}})
        return await self.message.edit(content=f'The game has ended, **{self.turn.display_name}** took too much to react and lost **10,000** <:carrots:822122757654577183>.\n{winner.mention} won **10,000** <:carrots:822122757654577183>', view=self)
    
    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.turn.id:
            if interaction.author.id not in (self.p1.id, self.p2.id):
                await interaction.response.send_message('You are not playing in this game! To start a game with someone you must have 10k carrots, if you do then type `!ttt <user>` to play.', ephemeral=True)
                return False
            await interaction.response.send_message(f'Not your turn, it\'s {self.turn.display_name}\'s turn', ephemeral=True)
            return False
        return True
    
    async def check_board_winner(self):
        won = False
        if self.board[0] == self.board[1] == self.board[2]: # Check 1-3
            won = True
        elif self.board[3] == self.board[4] == self.board[5]: # Check 4-6
            won = True
        elif self.board[6] == self.board[7] == self.board[8]: # Check 7-9
            won = True
        elif self.board[0] == self.board[3] == self.board[6]: # Check 1-7
            won = True
        elif self.board[1] == self.board[4] == self.board[7]: # Check 2-8
            won = True
        elif self.board[2] == self.board[5] == self.board[8]: # Check 3-9
            won = True
        elif self.board[0] == self.board[4] == self.board[8]: # Check 1-9
            won = True
        elif self.board[2] == self.board[4] == self.board[6]: # Check 3-7
            won = True
        
        if won == True:
            self.ended = True
            if self.turn == self.p1:
                loser = self.p2
            else:
                loser = self.p1
            for item in self.children:
                item.disabled = True
            await self.db.update_one({'_id': self.turn.id}, {'$inc':{'wallet': 10000}})
            await self.db.update_one({'_id': loser.id}, {'$inc':{'wallet': -10000}})
            await self.message.edit(content=f'{self.turn.mention} won **10,000** <:carrots:822122757654577183>\n{loser.mention} lost **10,000** <:carrots:822122757654577183>', view=self)
            self.stop()
    
        else:
            total = 0
            for i in range(9):
                if self.board[i] == str(i + 1):
                    total += 1
            if total == 0:
                self.ended = True
                for item in self.children:
                    item.disabled = True
                await self.message.edit(content='**___DRAW___**', view=self)
                self.stop()

    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=0)
    async def top_1(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[0] = self.new_label[self.turn]
        await self.check_board_winner()
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)
    
    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=0)
    async def top_2(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[1] = self.new_label[self.turn]
        await self.check_board_winner()
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)
    
    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=0)
    async def top_3(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[2] = self.new_label[self.turn]
        await self.check_board_winner()
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)

    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=1)
    async def mid_1(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[3] = self.new_label[self.turn]
        await self.check_board_winner()
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)
    
    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=1)
    async def mid_2(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[4] = self.new_label[self.turn]
        await self.check_board_winner()	
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)
    
    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=1)
    async def mid_3(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[5] = self.new_label[self.turn]
        await self.check_board_winner()	
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)

    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=2)
    async def bottom_1(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[6] = self.new_label[self.turn]
        await self.check_board_winner()	
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)

    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=2)
    async def bottom_2(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[7] = self.new_label[self.turn]
        await self.check_board_winner()	
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)

    @disnake.ui.button(label='\u200b', style=disnake.ButtonStyle.grey, row=2)
    async def bottom_3(self, button: disnake.ui.Button, inter: disnake.Interaction):
        button.disabled = True
        button.label = self.new_label[self.turn]
        button.style = self.new_style[self.turn]
        self.board[8] = self.new_label[self.turn]
        await self.check_board_winner()	
        
        if self.ended == False:
            if self.turn == self.p1:
                self.turn = self.p2
            else:
                self.turn = self.p1
            await self.message.edit(content=f'Your turn now: {self.turn.mention}', view=self)

    @disnake.ui.button(label='Forfeit', style=disnake.ButtonStyle.blurple, row=3)
    async def forfeit_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        if self.turn == self.p1:
            winner = self.p2
        else:
            winner = self.p1
        for item in self.children:
            item.disabled = True
        await self.db.update_one({'_id': self.turn.id}, {'$inc':{'wallet': -10000}})
        await self.db.update_one({'_id': winner.id}, {'$inc':{'wallet': 10000}})
        await self.message.edit(content=f'**___FORFEIT___**\n{self.turn.mention} forfeited and lost **10,000** <:carrots:822122757654577183>\n{winner.mention} won **10,000** <:carrots:822122757654577183>', view=self)
        self.stop()