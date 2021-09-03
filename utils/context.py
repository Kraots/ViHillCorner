from disnake.ext import commands
import disnake

class Context(commands.Context):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	@property
	def session(self):
		return self.bot.session

	@disnake.utils.cached_property
	def replied_reference(self):
		ref = self.message.reference
		if ref and isinstance(ref.resolved, disnake.Message):
			return ref.resolved.to_reference()
		return None