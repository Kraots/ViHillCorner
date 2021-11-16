import disnake
from disnake.ext import commands

from utils.colors import Colours
from utils.context import Context
from utils.paginator import ToDoMenu
from utils.databases import ToDos

from main import ViHillCorner


class ToDoPageEntry:
    def __init__(self, entry):

        self.todo = entry['todo']

    def __str__(self):
        return f'{self.todo}'


class ToDoPages(ToDoMenu):
    def __init__(self, ctx: Context, entries, *, per_page=5, title="", color=Colours.red, author_name=None, author_icon_url=None):
        converted = [ToDoPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page, title=title, color=color, author_name=author_name, author_icon_url=author_icon_url)


class ToDo(commands.Cog):
    """Todo related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = "!"

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '📋'

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def todo(self, ctx: Context, *, todo: str):
        """Add to your todo list."""

        cmd = self.bot.get_command('todo add')
        await ctx.invoke(cmd, todo=todo)

    @todo.command(name='add')
    async def todo_add(self, ctx: Context, *, todo: str):
        """Add to your todo list."""

        res: ToDos = await ToDos.find_one({'_id': ctx.author.id})
        if not res:
            await ToDos(
                id=ctx.author.id,
                todo_data=[{'url': ctx.message.jump_url, 'todo': todo}]
            ).commit()
            return await ctx.reply("Successfully added to your todo list.")

        res.todo_data += [{'url': ctx.message.jump_url, 'todo': todo}]
        await res.commit()
        await ctx.reply("Successfully added to your todo list.")

    @todo.command(name='list')
    async def todo_list(self, ctx: Context):
        """See your todo list, if you have any."""

        res: ToDos = await ToDos.find_one({'_id': ctx.author.id})
        if not res:
            return await ctx.reply("You do not have any todo list.")

        entries = res.todo_data
        index = 0
        for i in range(len(entries)):
            index += 1
            entries[i]['todo'] = f"**[{index}.]({entries[i]['url']})** {entries[i]['todo']}"

        m = ToDoPages(ctx=ctx, entries=entries, title="Here's your todo list:", author_name=ctx.author, author_icon_url=ctx.author.display_avatar)
        await m.start()

    @todo.command(name='delete', aliases=['remove'])
    async def todo_remove(self, ctx: Context, index):
        """Remove a todo from your todo list based on its index."""

        try:
            index = int(index) - 1
        except ValueError:
            return await ctx.reply("That is not a number.")

        res: ToDos = await ToDos.find_one({'_id': ctx.author.id})
        if not res:
            return await ctx.reply("You do not have any todo list.")

        new_data = []
        if index < 0:
            return await ctx.reply("The index cannot be `0` or negative.")
        elif index > len(res.todo_data) - 1:
            return await ctx.reply("The index cannot be greater than the highest index in your todo list.")

        for i in range(len(res.todo_data)):
            if i != index:
                new_data.append(res.todo_data[i])

        if len(new_data) == 0:
            await res.delete()
        else:
            res.todo_data = new_data
            await res.commit()
        await ctx.reply("Operation successful.")

    @todo.command(name='clear')
    async def todo_clear(self, ctx: Context):
        """Delete your todo list, completely."""

        res: ToDos = await ToDos.find_one({'_id': ctx.author.id})
        if not res:
            return await ctx.reply("You do not have any todo list.")

        view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
        view.message = msg = await ctx.send("Are you sure you want to delete your todo list? %s" % (ctx.author.mention), view=view)
        await view.wait()
        if view.response is True:
            await res.delete()
            e = "Succesfully deleted your todo list. %s" % (ctx.author.mention)
            return await msg.edit(content=e, view=view)

        elif view.response is False:
            e = "Okay, your todo list has not been deleted. %s" % (ctx.author.mention)
            return await msg.edit(content=e, view=view)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id != self.bot._owner_id:
            async for todo in ToDos.find({'_id': member.id}):
                await todo.delete()


def setup(bot):
    bot.add_cog(ToDo(bot))
