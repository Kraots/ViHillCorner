import discord
from discord.ext import commands
import utils.colors as color

class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.command()
    async def calc(self, ctx, a : float, operator, b : float):
        if operator == "+":
            title = "Sum"
            result = a+b
            operation = f"{a} + {b}"

        elif operator == "-":
            title = "Division"
            result = a-b
            operation = f"{a} - {b}"

        elif operator == "/":
            title = "Subtraction"
            result = a/b
            operation = f"{a} / {b}"

        elif operator == "*":
            title = "Multiplication"
            result = a*b
            operation = f"{a} * {b}"

        elif operator == "^":
            title = "Square Root"
            result = a**b
            operation = f"{a} ^ {b}"

        em = discord.Embed(color=color.lightpink, title=title)
        em.add_field(name="Operation:", value=operation)
        em.add_field(name="Result:", value=result)

        await ctx.send(embed=em)




def setup (client):
    client.add_cog(Calculator(client))