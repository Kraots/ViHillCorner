import asyncio
import re

import disnake
from disnake.ext import commands

from utils.colors import Colours

from main import ViHillCorner

no_mute_these = (374622847672254466, 751724369683677275,)

filter_invite = re.compile(r"(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")


class InviteFilter(commands.Cog):
    def __init__(self, bot: ViHillCorner):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message: disnake.Message):
        if message.author.id in no_mute_these:
            return
        elif message.channel.id == 752164200222163016:
            return
        guild = self.bot.get_guild(750160850077089853)
        if message.guild:
            use_this = message.content.lower()
            matches = re.findall(filter_invite, use_this)
            muted = guild.get_role(750465726069997658)
            log_channel = guild.get_channel(781777255885570049)
            for use_this in matches:

                await message.delete()
                msg = await message.channel.send('Invites not allowed!')
                embed = disnake.Embed(
                    color=Colours.invisible,
                    title="***___INVITE WARNING___***",
                    description=f'User `{message.author}` sent an [invite link]({msg.jump_url})!!',
                    timestamp=msg.created_at.replace(tzinfo=None)
                )
                embed.set_footer(
                    text="Click the `invite link` to go to the channel and see where the user got warned. No, it's not an actual invite.",
                    icon_url=self.bot.user.display_avatar
                )
                await log_channel.send(embed=embed)
                await message.author.add_roles(muted)
                curr_snipes = self.bot.snipes[message.channel.id]
                curr_snipes.pop(0)
                self.bot.snipes[message.channel.id] = curr_snipes
                await asyncio.sleep(30)
                await message.author.remove_roles(muted)


def setup(bot):
    bot.add_cog(InviteFilter(bot))
