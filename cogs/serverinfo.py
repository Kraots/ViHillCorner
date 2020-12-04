import discord
from discord.ext import commands
import utils.colors as color
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class ServerInfo(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prefix = "!"
    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix


    @commands.group(aliases=['server', 'sinfo', 'si'], pass_context=True, invoke_without_command=True)
    async def serverinfo(self, ctx, *, msg=""):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            if msg:
                server = None
                try:
                    float(msg)
                    server = self.client.get_guild(int(msg))
                    if not server:
                        return await ctx.send(
                                              self.client.client_prefix + 'Server not found.')
                except:
                    for i in self.client.guilds:
                        if i.name.lower() == msg.lower():
                            server = i
                            break
                    if not server:
                        return await ctx.send(self.client.client_prefix + 'Could not find server. Note: You must be a member of the server you are trying to search.')
            else:
                server = ctx.message.guild

            online = 0
            for i in server.members:
                if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    online += 1
            all_users = []
            for user in server.members:
                all_users.append('{}#{}'.format(user.name, user.discriminator))
            all_users.sort()
            

            channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

            role_count = len(server.roles)
            emoji_count = len(server.emojis)

            diff = relativedelta(datetime.utcnow(), server.created_at)

            em = discord.Embed(color=color.lightpink)
            em.add_field(name='Name', value=server.name)
            em.add_field(name='Owner', value=server.owner, inline=False)
            em.add_field(name='Members', value=server.member_count)
            em.add_field(name='Currently Online', value=online)
            em.add_field(name='Text Channels', value=str(channel_count))
            em.add_field(name='Region', value=server.region)
            em.add_field(name='Verification Level', value=str(server.verification_level))
            em.add_field(name='Highest role', value="Staff")
            em.add_field(name='Number of roles', value=str(role_count))
            em.add_field(name='Number of emotes', value=str(emoji_count))
            em.add_field(name='Created At', value=f"{diff.months} months, {diff.weeks} weeks, {diff.days} days, {diff.hours} hours and {diff.seconds} seconds ago.")
            em.set_thumbnail(url=server.icon_url)
            em.set_author(name='Server Info')
            em.set_footer(text=f'Requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
            
            await ctx.channel.send(embed=em)

def setup (client):
    client.add_cog(ServerInfo(client))