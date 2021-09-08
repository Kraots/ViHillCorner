from typing import Any, Dict, Optional
import asyncio
import disnake
from disnake.ext import commands
from disnake.ext.commands import Paginator as CommandPaginator
from . import menus

class RoboPages(menus.MenuPages):
	def __init__(self, source):
		super().__init__(source=source, check_embeds=True)

	async def finalize(self, timed_out):
		try:
			if timed_out:
				await self.message.clear_reactions()
			else:
				await self.message.delete()
		except disnake.HTTPException:
			pass

	@menus.button('\N{INFORMATION SOURCE}\ufe0f', position=menus.Last(3))
	async def show_help(self, payload):
		"""shows this message"""
		embed = disnake.Embed(title='Paginator help', description='Hello! Welcome to the help page.')
		messages = []
		for (emoji, button) in self.buttons.items():
			messages.append(f'{emoji}: {button.action.__doc__}')

		embed.add_field(name='What are these reactions for?', value='\n'.join(messages), inline=False)
		embed.set_footer(text=f'We were on page {self.current_page + 1} before this message.')
		await self.message.edit(content=None, embed=embed)

		async def go_back_to_current_page():
			await asyncio.sleep(30.0)
			await self.show_page(self.current_page)

		self.bot.loop.create_task(go_back_to_current_page())

	@menus.button('\N{INPUT SYMBOL FOR NUMBERS}', position=menus.Last(1.5))
	async def numbered_page(self, payload):
		"""lets you type a page number to go to"""
		channel = self.message.channel
		author_id = payload.user_id
		to_delete = []
		to_delete.append(await channel.send('What page do you want to go to?'))

		def message_check(m):
			return m.author.id == author_id and \
				channel == m.channel and \
				m.content.isdigit()

		try:
			msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
		except asyncio.TimeoutError:
			to_delete.append(await channel.send('Took too long.'))
			await asyncio.sleep(5)
		else:
			page = int(msg.content)
			to_delete.append(msg)
			await self.show_checked_page(page - 1)

		try:
			await channel.delete_messages(to_delete)
		except Exception:
			pass

class _RoboPages(disnake.ui.View):
	def __init__(
		self,
		source: menus.PageSource,
		*,
		ctx: commands.Context,
		check_embeds: bool = True,
		compact: bool = False,
	):
		super().__init__()
		self.source: menus.PageSource = source
		self.check_embeds: bool = check_embeds
		self.ctx: commands.Context = ctx
		self.message: Optional[disnake.Message] = None
		self.current_page: int = 0
		self.compact: bool = compact
		self.input_lock = asyncio.Lock()
		self.clear_items()
		self.fill_items()

	def fill_items(self) -> None:
		if not self.compact:
			self.numbered_page.row = 1
			self.stop_pages.row = 1

		if self.source.is_paginating():
			max_pages = self.source.get_max_pages()
			use_last_and_first = max_pages is not None and max_pages >= 2
			if use_last_and_first:
				self.add_item(self.go_to_first_page)  # type: ignore
			self.add_item(self.go_to_previous_page)  # type: ignore
			if not self.compact:
				self.add_item(self.go_to_current_page)  # type: ignore
			self.add_item(self.go_to_next_page)  # type: ignore
			if use_last_and_first:
				self.add_item(self.go_to_last_page)  # type: ignore
			if not self.compact:
				self.add_item(self.numbered_page)  # type: ignore
			self.add_item(self.stop_pages)  # type: ignore

	async def _get_kwargs_from_page(self, page: int) -> Dict[str, Any]:
		value = await disnake.utils.maybe_coroutine(self.source.format_page, self, page)
		if isinstance(value, dict):
			return value
		elif isinstance(value, str):
			return {'content': value, 'embed': None}
		elif isinstance(value, disnake.Embed):
			return {'embed': value, 'content': None}
		else:
			return {}

	async def show_page(self, interaction: disnake.Interaction, page_number: int) -> None:
		page = await self.source.get_page(page_number)
		self.current_page = page_number
		kwargs = await self._get_kwargs_from_page(page)
		self._update_labels(page_number)
		if kwargs:
			if interaction.response.is_done():
				if self.message:
					await self.message.edit(**kwargs, view=self)
			else:
				await interaction.response.edit_message(**kwargs, view=self)

	def _update_labels(self, page_number: int) -> None:
		self.go_to_first_page.disabled = page_number == 0
		if self.compact:
			max_pages = self.source.get_max_pages()
			self.go_to_last_page.disabled = max_pages is None or (page_number + 1) >= max_pages
			self.go_to_next_page.disabled = max_pages is not None and (page_number + 1) >= max_pages
			self.go_to_previous_page.disabled = page_number == 0
			return

		self.go_to_current_page.label = str(page_number + 1)
		self.go_to_previous_page.label = str(page_number)
		self.go_to_next_page.label = str(page_number + 2)
		self.go_to_next_page.disabled = False
		self.go_to_previous_page.disabled = False
		self.go_to_first_page.disabled = False

		max_pages = self.source.get_max_pages()
		if max_pages is not None:
			self.go_to_last_page.disabled = (page_number + 1) >= max_pages
			if (page_number + 1) >= max_pages:
				self.go_to_next_page.disabled = True
				self.go_to_next_page.label = '…'
			if page_number == 0:
				self.go_to_previous_page.disabled = True
				self.go_to_previous_page.label = '…'

	async def show_checked_page(self, interaction: disnake.Interaction, page_number: int) -> None:
		max_pages = self.source.get_max_pages()
		try:
			if max_pages is None:
				# If it doesn't give maximum pages, it cannot be checked
				await self.show_page(interaction, page_number)
			elif max_pages > page_number >= 0:
				await self.show_page(interaction, page_number)
		except IndexError:
			# An error happened that can be handled, so ignore it.
			pass

	async def interaction_check(self, interaction: disnake.Interaction) -> bool:
		if interaction.user and interaction.user.id in (self.ctx.bot.owner_id, self.ctx.author.id):
			return True
		await interaction.response.send_message('This pagination menu cannot be controlled by you, sorry!', ephemeral=True)
		return False

	async def on_timeout(self) -> None:
		if self.message:
			await self.message.edit(view=None)

	async def on_error(self, error: Exception, item: disnake.ui.Item, interaction: disnake.Interaction) -> None:
		if interaction.response.is_done():
			await interaction.followup.send('An unknown error occurred, sorry', ephemeral=True)
		else:
			await interaction.response.send_message('An unknown error occurred, sorry', ephemeral=True)

	async def start(self) -> None:
		if self.check_embeds and not self.ctx.channel.permissions_for(self.ctx.me).embed_links:
			await self.ctx.send('Bot does not have embed links permission in this channel.')
			return

		await self.source._prepare_once()
		page = await self.source.get_page(0)
		kwargs = await self._get_kwargs_from_page(page)
		self._update_labels(0)
		self.message = await self.ctx.send(**kwargs, view=self)

	@disnake.ui.button(label='≪', style=disnake.ButtonStyle.grey)
	async def go_to_first_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		"""go to the first page"""
		await self.show_page(interaction, 0)

	@disnake.ui.button(label='Back', style=disnake.ButtonStyle.blurple)
	async def go_to_previous_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		"""go to the previous page"""
		await self.show_checked_page(interaction, self.current_page - 1)

	@disnake.ui.button(label='Current', style=disnake.ButtonStyle.grey, disabled=True)
	async def go_to_current_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		pass

	@disnake.ui.button(label='Next', style=disnake.ButtonStyle.blurple)
	async def go_to_next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		"""go to the next page"""
		await self.show_checked_page(interaction, self.current_page + 1)

	@disnake.ui.button(label='≫', style=disnake.ButtonStyle.grey)
	async def go_to_last_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		"""go to the last page"""
		# The call here is safe because it's guarded by skip_if
		await self.show_page(interaction, self.source.get_max_pages() - 1)


	@disnake.ui.button(label='Skip to page...', style=disnake.ButtonStyle.grey)
	async def numbered_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		"""lets you type a page number to go to"""
		if self.input_lock.locked():
			await interaction.response.send_message('Already waiting for your response...', ephemeral=True)
			return

		if self.message is None:
			return

		async with self.input_lock:
			channel = self.message.channel
			author_id = interaction.user and interaction.user.id
			await interaction.response.send_message('What page do you want to go to?', ephemeral=True)

			def message_check(m):
				return m.author.id == author_id and channel == m.channel and m.content.isdigit()

			try:
				msg = await self.ctx.bot.wait_for('message', check=message_check, timeout=30.0)
			except asyncio.TimeoutError:
				await interaction.followup.send('Took too long.', ephemeral=True)
				await asyncio.sleep(5)
			else:
				page = int(msg.content)
				await msg.delete()
				await self.show_checked_page(interaction, page - 1)

	@disnake.ui.button(label='Quit', style=disnake.ButtonStyle.red)
	async def stop_pages(self, button: disnake.ui.Button, interaction: disnake.Interaction):
		"""stops the pagination session."""
		await interaction.response.defer()
		await interaction.delete_original_message()
		self.stop()

class FieldPageSource(menus.ListPageSource):
	"""A page source that requires (field_name, field_value) tuple items."""
	def __init__(self, entries, *, per_page=12):
		super().__init__(entries, per_page=per_page)
		self.embed = disnake.Embed(colour=disnake.Colour.blurple())

	async def format_page(self, menu, entries):
		self.embed.clear_fields()
		self.embed.description = disnake.Embed.Empty

		for key, value in entries:
			self.embed.add_field(name=key, value=value, inline=False)

		maximum = self.get_max_pages()
		if maximum > 1:
			text = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
			self.embed.set_footer(text=text)

		return self.embed

class TextPageSource(menus.ListPageSource):
	def __init__(self, text, *, prefix='```', suffix='```', max_size=2000):
		pages = CommandPaginator(prefix=prefix, suffix=suffix, max_size=max_size - 200)
		for line in text.split('\n'):
			pages.add_line(line)

		super().__init__(entries=pages, per_page=1)

	async def format_page(self, menu, content):
		maximum = self.get_max_pages()
		if maximum > 1:
			return f'{content}\nPage {menu.current_page + 1}/{maximum}'
		return content

class SimplePageSource(menus.ListPageSource):
	def __init__(self, entries, *, per_page=12):
		super().__init__(entries, per_page=per_page)
		self.initial_page = True

	async def format_page(self, menu, entries):
		pages = []
		for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
			pages.append(f'{index + 1}. {entry}')

		maximum = self.get_max_pages()
		if maximum > 1:
			footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
			menu.embed.set_footer(text=footer)

		if self.initial_page and self.is_paginating():
			pages.append('')
			pages.append('Confused? React with \N{INFORMATION SOURCE} for more info.')
			self.initial_page = False

		menu.embed.description = '\n'.join(pages)
		return menu.embed

class SimplePages(_RoboPages):
	"""A simple pagination session reminiscent of the old Pages interface.

	Basically an embed with some normal formatting.
	"""

	def __init__(self, entries, *, per_page=12, color=None):
		super().__init__(SimplePageSource(entries, per_page=per_page))
		if color == None:
			color = disnake.Color.blurple()
		self.embed = disnake.Embed(colour=color)




class CustomRobo(menus.MenuPages):
	def __init__(self, source):
		super().__init__(source=source, check_embeds=True)

	async def finalize(self, timed_out):
		try:
			if timed_out:
				await self.message.clear_reactions()
			else:
				await self.message.delete()
		except disnake.HTTPException:
			pass

class NewHelpMenus(menus.ListPageSource):
	def __init__(self, entries, *, per_page=12):
		super().__init__(entries, per_page=per_page)
		
	async def format_page(self, menu, entries):
		pages = []
		for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
			pages.append(f'{entry}')
		
		maximum = self.get_max_pages()
		if maximum > 1:
			footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} commands)'
			menu.embed.set_footer(text=footer)
	
		menu.embed.description = "\n".join(pages)
		return menu.embed

class NewCustomMenus(menus.ListPageSource):
	def __init__(self, entries, *, per_page=12):
		super().__init__(entries, per_page=per_page)
		
	async def format_page(self, menu, entries):
		pages = []
		for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
			pages.append(f'`{index + 1}.` {entry}')

		maximum = self.get_max_pages()
		if maximum > 1:
			footer = f'Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)'
			menu.embed.set_footer(text=footer)
	
		menu.embed.description = "\n".join(pages)
		return menu.embed

class HelpmMenu(_RoboPages):
	def __init__(self, entries, *, per_page=12, title="", color=None):
		super().__init__(NewHelpMenus(entries, per_page=per_page))
		if color == None:
			color = disnake.Color.blurple()
		self.embed = disnake.Embed(colour=color, title=title)

class CustomMenu(_RoboPages):
	def __init__(self, ctx, entries, *, per_page=12, title="", color=None):
		super().__init__(NewCustomMenus(entries, per_page=per_page), ctx=ctx)
		if color == None:
			color = disnake.Color.blurple()
		self.embed = disnake.Embed(colour=color, title=title)

class ToDoMenu(_RoboPages):
	def __init__(self, entries, *, per_page=12, title="", color=None, author_name=None, author_icon_url=None):
		super().__init__(NewHelpMenus(entries, per_page=per_page))
		if color == None:
			color = disnake.Color.blurple()
		self.embed = disnake.Embed(colour=color, title=title)
		if author_name != None:
			self.embed.set_author(name=author_name, url=author_icon_url, icon_url=author_icon_url)
