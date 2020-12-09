import discord
from discord.ext import commands
import utils.colors as color

class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def calc(self, ctx):
        pass

    @calc.command(pass_context=True)
    async def add(self, ctx, a: float, b:float):
        await ctx.channel.send(f'{a} + {b}= `{a+b}`')
        
    @calc.command(pass_context=True)
    async def subtract(self, ctx, a: float, b:float):
        await ctx.channel.send(f'{a} - {b} =  `{a-b}`')
        
    @calc.command(pass_context=True)
    async def multiply(self, ctx, a: float, b:float):
        await ctx.channel.send(f'{a} * {b} =  `{a*b}`')
        
    @calc.command(pass_context=True)
    async def divide(self, ctx, a: float, b:float):
        await ctx.channel.send(f'{a} / {b} =  `{a/b}`')

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()

    @subtract.error
    async def substract_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()

    @multiply.error
    async def multiply_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()

    @divide.error
    async def divide_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()



def setup (client):
    client.add_cog(Calculator(client))