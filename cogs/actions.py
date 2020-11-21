import discord
from discord.ext import commands
import utils.colors as color

class actions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def huggles(self, ctx, *, mention=None,):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/737981297212915712/751115114106585243/374622847672254466.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('<:hug:750751796317913218>')

    @commands.command(hidden=True)
    async def grouphug(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://media.tenor.com/images/8e157a9853d6537cd26859b51eff8baa/tenor.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def eat(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751185646227554394/tenor_1.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def chew(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751185891833282721/tenor_2.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def sip(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751210657973796945/tenor_3.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def clap(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751210657029816455/tenor_2.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def cry(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/752148605753884792/778205851319926794/crygifforaction.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def rofl(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751226102130671716/tenor_5.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def lol(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751228793041059910/tenor_7.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def kill(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751229626952581170/tenor_8.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def pat(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751229628202483772/tenor_9.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('<:kanna_pat:750757139001245806>')

    @commands.command(hidden=True)
    async def rub(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751275129064915054/tenor-1.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def nom(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751276651223973980/tenor-3.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def catpat(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751350319698411520/tenor_10.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def hug(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751350320222961664/tenor_11.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def pillow(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751357844497891368/tenor-4.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def spray(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/744576171110301708/751138135299064001/image0.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def hype(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/750160852380024893/751210656568705105/tenor_1.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    @commands.has_role('Staff')
    async def specialkiss(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/752148605753884792/754984869569888276/KIS.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')


    @commands.command(hidden=True)
    async def kiss(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/755149503685722193/756648389025726595/send_help_pls.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def ily(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/752148605753884792/754965447165607936/tenor-6.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def nocry(self, ctx, *, mention=None):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/752148605753884792/754398142551818291/tenor-5.gif')


            msg = await ctx.send(mention, embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def shrug(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/755149503685722193/755151733994553374/tenor_1.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def smug(self, ctx):

            version = discord.Embed(color=color.red)
            version.set_image(url='https://cdn.discordapp.com/attachments/755149503685722193/755151245206880296/smug.gif')


            msg = await ctx.send(embed=version)
            await msg.add_reaction('🗑️')

    @commands.command(hidden=True)
    async def bearhug(self, ctx, *, mention=None):

            bearhug = discord.Embed(color=color.red)
            bearhug.set_image(url="https://cdn.discordapp.com/attachments/750160851822182482/761861335922769920/image0.gif")
            
            msg = await ctx.send(mention, embed=bearhug)
            await msg.add_reaction('🗑️')




def setup (client):
    client.add_cog(actions(client))

