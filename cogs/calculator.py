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
    async def add(self, ctx, a: int, b:int):
        await ctx.channel.send(f'{a} + {b}= `{a+b}`')
        
    @calc.command(pass_context=True)
    async def substract(self, ctx, a: int, b:int):
        await ctx.channel.send(f'{a} - {b} =  `{a-b}`')
        
    @calc.command(pass_context=True)
    async def multiply(self, ctx, a: int, b:int):
        await ctx.channel.send(f'{a} * {b} =  `{a*b}`')
        
    @calc.command(pass_context=True)
    async def divide(self, ctx, a: int, b:int):
        await ctx.channel.send(f'{a} / {b} =  `{a/b}`')

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()
            embed = discord.Embed(title='***___WARNING:___***', description='NUMBERS LIKE `2,3` OR `2.3` WILL NOT WORK! USE ONLY NUMBERS LIKE `2` OR `3`!!!*\n\nExample:\n\n`!calc divide 4 2` will result `2.0`\n`!calc divide 4.6 2.3` will result an error!!', color=color.inviscolor)
            await ctx.channel.send(embed=embed, delete_after=10)

    @substract.error
    async def substract_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()
            embed = discord.Embed(title='***___WARNING:___***', description='NUMBERS LIKE `2,3` OR `2.3` WILL NOT WORK! USE ONLY NUMBERS LIKE `2` OR `3`!!!*\n\nExample:\n\n`!calc divide 4 2` will result `2.0`\n`!calc divide 4.6 2.3` will result an error!!', color=color.inviscolor)
            await ctx.channel.send(embed=embed, delete_after=10)

    @multiply.error
    async def multiply_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()
            embed = discord.Embed(title='***___WARNING:___***', description='NUMBERS LIKE `2,3` OR `2.3` WILL NOT WORK! USE ONLY NUMBERS LIKE `2` OR `3`!!!*\n\nExample:\n\n`!calc divide 4 2` will result `2.0`\n`!calc divide 4.6 2.3` will result an error!!', color=color.inviscolor)
            await ctx.channel.send(embed=embed, delete_after=20)

    @divide.error
    async def divide_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()
            embed = discord.Embed(title='***___WARNING:___***', description='NUMBERS LIKE `2,3` OR `2.3` WILL NOT WORK! USE ONLY NUMBERS LIKE `2` OR `3`!!!*\n\nExample:\n\n`!calc divide 4 2` will result `2.0`\n`!calc divide 4.6 2.3` will result an error!!', color=color.inviscolor)
            await ctx.channel.send(embed=embed, delete_after=10)


def setup (client):
    client.add_cog(Calculator(client))