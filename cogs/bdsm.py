import asyncio
import datetime

import disnake
from disnake.ext import commands

from utils.context import Context
from utils.databases import BDSM

from main import ViHillCorner


class Bdsm(commands.Cog):
    """Bdsm related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db2['Confesscord Restrictions']
        self.prefix = "!"

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '⛓️'

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def bdsm(self, ctx: Context):
        """Base command for all the bdsm commands."""

        await ctx.send_help('bdsm')

    @bdsm.command(name='set')
    async def bdsm_set(self, ctx: Context):
        """Set your bdsm results"""

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(f"Please send the screenshot of your BDSM results. {ctx.author.mention}")

        data: BDSM = await BDSM.find_one({'_id': ctx.author.id})

        try:
            while True:
                res = await self.bot.wait_for('message', check=check, timeout=180)
                if res.content.lower() == "!cancel":
                    await res.reply("Cancelled.")
                    return

                try:
                    result = res.attachments[0].url

                    if data is not None:
                        data.result = result
                        data.created_at = datetime.datetime.utcnow()
                        await ctx.send("Succesfully updated your bdsm result. To check your bdsm results or others, you can type `!bdsm results <member>`.")
                        return

                    bdsm = BDSM(
                        id=ctx.author.id,
                        result=result,
                        created_at=datetime.datetime.utcnow()
                    )
                    await bdsm.commit()

                    await ctx.send("Succesfully set your bdsm result. To check your bdsm results or others, you can type `!bdsm results <member>`.")
                    return

                except Exception:
                    await ctx.send("You must send an image from your gallery, not an image url.")

        except asyncio.TimeoutError:
            await ctx.send(f"You ran out of time, type the command again to set your bdsm results. {ctx.author.mention}")
            return

    @bdsm.command(name='results', aliases=('result',))
    async def bdsm_results(self, ctx: Context, member: disnake.Member = None):
        """See the member's bdsm results"""

        member = member or ctx.author

        data: BDSM = await BDSM.find_one({'_id': member.id})

        if data is not None:
            em = disnake.Embed(
                color=member.color,
                title=f"Here's `{member.display_name}` bdsm results:",
                timestamp=data.created_at
            )
            em.set_image(url=data.result)
            em.set_footer(text="Result set at", icon_url=member.display_avatar)
            await ctx.send(embed=em)

        else:
            await ctx.send("That user did not set their bdsm results.")

    @bdsm.command(name='remove', aliases=('delete',))
    async def bdsm_remove(self, ctx: Context):
        """Remove your bdsm results"""

        data: BDSM = await BDSM.find_one({'_id': ctx.author.id})

        if data is not None:
            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send(f"Are you sure you want to remove your bdsm results? {ctx.author.mention}", view=view)
            await view.wait()
            if view.response is True:
                await data.delete()
                e = f"Succesfully removed your bdsm results. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = f"Okay, your bdsm results have not been removed. {ctx.author.mention}"
                return await msg.edit(content=e, view=view)

        else:
            await ctx.send(
                "There are no bdsm results to delete, you don't have them set. To set your bdsm results type `!bdsm set`, and then send the screenshot of your "
                f"results. {ctx.author.mention}"
            )

    @bdsm.command(name='test')
    async def bdsm_test(self, ctx: Context):
        """Get a link to go and do your bdsm test to get your results."""

        await ctx.send("Click the link below to take your bdsm test: \nhttps://bdsmtest.org")

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != 374622847672254466:
            data: BDSM = await BDSM.find_one({'_id': member.id})
            if data:
                await data.delete()
            await self.db.delete_one({'_id': member.id})


def setup(bot):
    bot.add_cog(Bdsm(bot))
