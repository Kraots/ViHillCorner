import asyncio
import datetime
import string

import disnake
from disnake.ext import commands

from utils.colors import Colours

from main import ViHillCorner

invalid_names_list = tuple(list(string.digits) + list(string.punctuation))

nono_names = ("kraots", "vihillcorner", "carrots")


async def check_invalid_name(db, message, kraots) -> str:
    user = await db.find_one({'_id': message.author.id})
    if user is None:
        kr = await db.find_one({'_id': kraots.id})
        new_index = kr['TotalInvalidNames'][-1] + 1
        old_list = kr['TotalInvalidNames']
        new_list = old_list + [new_index]
        post = {
            '_id': message.author.id,
            'InvalidNameIndex': new_index
        }
        await db.insert_one(post)
        await db.update_one({'_id': kraots.id}, {'$set': {'TotalInvalidNames': new_list}})
        new_nick = f'UnpingableName{new_index}'
    else:
        new_nick = f"UnpingableName{user['InvalidNameIndex']}"

    return new_nick


# Webhook that sends a message in messages-log channel
async def send_webhook(em: disnake.Embed, view: disnake.ui.View, bot: ViHillCorner):
    webhook = await bot.get_webhook(bot.get_channel(750432155179679815))
    await webhook.send(embed=em, view=view)


class OnMessage(commands.Cog):
    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db2['InvalidName Filter']

    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, message: disnake.Message):
        if message.author.bot:
            return

        if message.author.id == 374622847672254466:
            return

        else:
            em = disnake.Embed(
                color=Colours.red,
                description=f'Message deleted in <#{message.channel.id}> \n\n**Content:** \n```{message.content}```',
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f'{message.author}', icon_url=f'{message.author.display_avatar}')
            em.set_footer(text=f'User ID: {message.author.id}')
            if message.attachments:
                em.set_image(url=message.attachments[0].proxy_url)
            ref = message.reference
            if ref and isinstance(ref.resolved, disnake.Message):
                em.add_field(name='Replying to...', value=f'[{ref.resolved.author}]({ref.resolved.jump_url})', inline=False)

            await asyncio.sleep(0.5)
            try:
                btn = disnake.ui.View()
                btn.add_item(disnake.ui.Button(label='Jump!', url=message.jump_url))
                await send_webhook(em, btn, self.bot)
            except Exception as e:
                await self.bot._owner.send(e)

    @commands.Cog.listener('on_message_edit')
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if before.author.bot:
            return
        if before.author.id == 374622847672254466:
            return
        else:
            em = disnake.Embed(
                color=Colours.yellow,
                description=f'Message edited in <#{before.channel.id}>\n\n**Before:**\n```{before.content}```\n\n**After:**\n```{after.content}```',  # noqa
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f'{before.author}', icon_url=f'{before.author.display_avatar}')
            em.set_footer(text=f'User ID: {before.author.id}')
            ref = after.reference
            if ref and isinstance(ref.resolved, disnake.Message):
                em.add_field(name='Replying to...', value=f'[{ref.resolved.author}]({ref.resolved.jump_url})', inline=False)

            await asyncio.sleep(0.5)
            try:
                btn = disnake.ui.View()
                btn.add_item(disnake.ui.Button(label='Jump!', url=after.jump_url))
                await send_webhook(em, btn, self.bot)
            except Exception as e:
                await self.bot._owner.send(e)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id == 750160850593251449:
            await message.add_reaction("<:hug:750751796317913218>")

        if message.author.bot:
            return

        if message.guild is None and not message.author.bot:
            em = disnake.Embed(
                description=f'{message.content}',
                color=Colours.invisible,
                timestamp=message.created_at.replace(tzinfo=None)
            )
            em.set_author(name=str(message.author) + ':', icon_url=message.author.display_avatar)
            em.set_footer(text=f'User ID: {message.author.id}')

            if message.attachments:
                em.set_image(url=message.attachments[0].proxy_url)

            if message.author.id == self.bot._owner_id:
                return

            else:
                await self.bot._owner.send(embed=em)

        if message.guild:

            if message.author.id == self.bot._owner.id:
                return

            else:
                user_name = message.author.name
                user_nickname = message.author.nick

                if any(x == str(user_nickname)[:1] for x in invalid_names_list):
                    new_nick = await check_invalid_name(self.db, message, self.bot._owner)
                    await message.author.edit(nick=new_nick)
                    await message.author.send(
                        "Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. "
                        f"(`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:"
                        "**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner"
                    )

                elif any(x == str(user_name)[:1] for x in invalid_names_list):

                    if user_nickname:
                        return

                    else:
                        new_nick = await check_invalid_name(self.db, message, self.bot._owner)
                        await message.author.edit(nick=new_nick)
                        await message.author.send(
                            "Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. "
                            f"(`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:"
                            "**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner"
                        )

                elif str(user_nickname).lower() in nono_names:
                    new_nick = await check_invalid_name(self.db, message, self.bot._owner)
                    await message.author.edit(nick=new_nick)
                    await message.author.send(
                        "Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. "
                        f"(`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:"
                        "**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner"
                    )
                    return

                if not user_nickname:
                    if str(user_name).lower() in nono_names:
                        new_nick = await check_invalid_name(self.db, message, self.bot._owner)
                        await message.author.edit(nick=new_nick)
                        await message.author.send(
                            "Hello! Your username/nickname doesn't follow our nickname policy. A random nickname has been assigned to you temporarily. "
                            f"(`{new_nick}`). \n\n If you want to change it, send `!nick <nickname>` in <#750160851822182486>.\n\n**Acceptable nicknames:"
                            "**\nPotato10\nTom_owo\nElieyn ♡\n\n**Unacceptable nicknames:**\nZ҉A҉L҉G҉O\n❥察爱\n! Champa\nKraots\nViHill Corner"
                        )
                        return
                else:
                    pass
        else:
            return


def setup(bot):
    bot.add_cog(OnMessage(bot))
