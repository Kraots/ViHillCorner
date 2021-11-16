import io
import time
import asyncio
import difflib
import textwrap
from pathlib import Path

from utils.context import Context
from utils.colors import Colours
from utils.helpers import run_in_executor, get_bytes

import disnake

__all__ = (
    'TypeRacer',
)


class TypeRacer:
    def __init__(self, ctx: Context):
        self.ctx = ctx

        self.to_type: str = None

    @run_in_executor
    def draw(self, image, text):
        from PIL import Image, ImageDraw, ImageFont
        im = Image.open(io.BytesIO(image))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(f'{str(Path(__file__).parents[0])}/assets/Milliard.otf', 50)

        text = textwrap.fill(text, width=30)
        draw.multiline_text((im.width / 2 - 400, im.height / 2 - 140), text, (255, 255, 255), align='center', font=font)

        buffer = io.BytesIO()
        im.save(buffer, format='png')
        return buffer.getvalue()

    async def start(self):
        bot = self.ctx.bot
        image_url = 'https://i.imgur.com/i9umepr.png'
        byt = await get_bytes(self.ctx, image_url, bot.session)
        res = await bot.session.get('https://api.quotable.io/random', params={'minLength': 30, 'maxLength': 300})
        data = await res.json()

        self.to_type = data['content']
        buffer = await self.draw(byt, self.to_type)
        em = disnake.Embed(title='Typerace!', description='Type the following sentence as fast as possible:', color=Colours.invisible)
        em.set_image(url='attachment://TypeRace.png')
        self._message = await self.ctx.send(embed=em, file=disnake.File(io.BytesIO(buffer), 'TypeRace.png'))

        await self.wait_for_response(self.ctx, self.to_type, timeout=60.0)

    async def wait_for_response(self, ctx: Context, text: str, *, timeout: int):
        emoji_map = {1: '🥇', 2: '🥈', 3: '🥉'}

        format_line = lambda i, x: f"• {emoji_map[i]} {x['user'].mention} in {x['time']:.2f}s | **WPM:** {x['wpm']:.2f} | **ACC:** {x['acc']:.2f}%"  # noqa

        text = text.replace('\n', ' ')
        participants = []

        start = time.perf_counter()

        while True:
            def check(m):
                content = m.content.replace('\n', ' ')
                if m.channel == ctx.channel and not m.author.bot and m.author not in map(lambda m: m["user"], participants):
                    sim = difflib.SequenceMatcher(None, content, text).ratio()
                    return sim >= 0.75

            try:
                message = await ctx.bot.wait_for(
                    'message',
                    timeout=timeout,
                    check=check
                )
            except asyncio.TimeoutError:
                if participants:
                    break
                else:
                    return await ctx.reply('Oops. Seems like no one responded... sad.')
            end = time.perf_counter()
            content = message.content.replace('\n', ' ')
            timeout -= round(end - start)

            participants.append({
                'user': message.author,
                'time': end - start,
                'wpm': len(text.split(' ')) / ((end - start) / 60),
                'acc': difflib.SequenceMatcher(None, content, text).ratio() * 100
            })

            await message.add_reaction(emoji_map[len(participants)])

            em = self._message.embeds[0]
            em.description = '\n'.join(
                [format_line(i, x) for i, x in enumerate(participants, 1)]
            ) + '\n\n' + 'Type the following sentence as fast as possible:'
            em.set_image(url='attachment://TypeRace.png')
            await self._message.edit(embed=em)

            if len(participants) >= 3:
                break

        desc = [format_line(i, x) for i, x in enumerate(participants, 1)]
        em = disnake.Embed(
            title='Typerace finished!',
            description=f'This typerace has finished. You can start another game by running `{ctx.prefix}typeracer`',
            color=Colours.invisible
        )
        em.add_field(name='Participants', value='\n'.join(desc))
        em.add_field(name='Prompt', value=text, inline=False)

        await self._message.reply(embed=em)
