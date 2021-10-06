from typing import List
import disnake


class EmbedPaginator(disnake.ui.View):
    def __init__(
        self,
        ctx,
        embeds: List[disnake.Embed],
        *,
        timeout: float = 180.0
    ):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.embeds = embeds
        self.current_page = 0

    async def interaction_check(self, interaction: disnake.Interaction) -> bool:
        if interaction.user and interaction.user.id in (self.ctx.bot._owner_id, self.ctx.author.id):
            return True
        await interaction.response.send_message('This pagination menu cannot be controlled by you, sorry!', ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        if self.message:
            await self.message.edit(view=None)

    async def show_page(self, page_number: int):
        if (
            (page_number < 0) or
            (page_number > len(self.embeds) - 1)
        ):
            return
        self.current_page = page_number
        embed = self.embeds[page_number]
        embed.set_footer(text=f'Page {self.current_page + 1}/{len(self.embeds)}')
        await self.message.edit(embed=embed)

    @disnake.ui.button(label='≪', style=disnake.ButtonStyle.grey)
    async def go_to_first_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """Go to the first page."""
        await self.show_page(0)

    @disnake.ui.button(label='Back', style=disnake.ButtonStyle.blurple)
    async def go_to_previous_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """Go to the previous page."""
        await self.show_page(self.current_page - 1)

    @disnake.ui.button(label='Next', style=disnake.ButtonStyle.blurple)
    async def go_to_next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """Go to the next page."""
        await self.show_page(self.current_page + 1)

    @disnake.ui.button(label='≫', style=disnake.ButtonStyle.grey)
    async def go_to_last_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """Go to the last page."""
        await self.show_page(len(self.embeds) - 1)

    @disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red)
    async def stop_pages(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """stops the pagination session."""
        await interaction.response.defer()
        await interaction.delete_original_message()
        self.stop()

    async def start(self):
        """Start paginating over the embeds."""
        embed = self.embeds[0]
        embed.set_footer(text=f'Page 1/{len(self.embeds)}')
        self.message = await self.ctx.send(embed=embed, view=self)
