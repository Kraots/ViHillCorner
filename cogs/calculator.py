import discord
from discord.ext import commands

class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.group()
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

def setup (client):
    client.add_cog(Calculator(client))