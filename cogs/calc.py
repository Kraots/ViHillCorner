import discord
from discord.ext import commands
import utils.colors as color
import re
NUMBER_REGEX = r"[0-9\.]+"

class Calculatorr:
	operators = ("^", "/", "*", "-", "+")    

	def __init__(self, expression: str):
		self.expression = expression.lower().replace(" ", "").strip()

	def __repr__(self):
		def recur(op):
			self.sub_regex(op)
			if re.search(fr"(-?{NUMBER_REGEX}\{op}-?{NUMBER_REGEX})", self.expression):
				recur(op)
		for op in self.operators:
			if re.search(fr"(-?{NUMBER_REGEX}\{op}-?{NUMBER_REGEX})", self.expression):
				recur(op)
		return self.expression

	def append(self, obj):
		self.expression += str(obj.lower().replace(" ", "").strip())

	def sub_regex(self, operator):
		def sub_fn(v):
			try:
				x, y = v.group().split(operator)
			except ValueError:
				self.expression = "Can't contain a negative number or some error occured."
				return self.expression
			x, y = float(x), float(y)
			conv = {
				"/": x/y,
				"*": x*y,
				"-": x-y,
				"+": x+y,
				"^": x**y
			}
			return str(conv.get(operator))
		try:
			self.expression = re.sub(fr"(-?{NUMBER_REGEX}\{operator}-?{NUMBER_REGEX})", sub_fn, self.expression)
		except TypeError:
			pass
		except OverflowError:
			self.expression = "This operation is not possible."

class Calculator(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prefix = "!"
	async def cog_check(self, ctx):
		return ctx.prefix == self.prefix

	@commands.command(aliases=['calculator', 'calculate'])
	async def calc(self, ctx, *, args:str):
		result = Calculatorr(args)
		if str(result).endswith('.0'):
			result = str(result).replace('.0', '')
		em = discord.Embed(color=color.lightpink, title="Calculator")
		em.add_field(name="Operation:", value=args, inline=False)
		em.add_field(name="Result:", value=result, inline=False)
		em.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=em)



def setup(client):
	client.add_cog(Calculator(client))	