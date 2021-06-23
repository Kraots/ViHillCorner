from discord.ext import commands
import discord

class Context(commands.Context):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@property
	def session(self):
		return self.bot.session

	@discord.utils.cached_property
	def replied_reference(self):
		ref = self.message.reference
		if ref and isinstance(ref.resolved, discord.Message):
			return ref.resolved.to_reference()
		return None