import re
import asyncio
import datetime

import disnake
from disnake.ext import commands

from utils.colors import Colours
from utils.context import Context
from utils.paginator import SimplePages

from .actions import all_roles

from main import ViHillCorner

filter_invite = re.compile(r"(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")


class TagPageEntry:
    def __init__(self, entry):

        self.name = entry['name']
        self.id = entry['_id']

    def __str__(self):
        return f'{self.name}\u2800•\u2800(`ID:` **{self.id}**)'


class TagPages(SimplePages):
    def __init__(self, ctx: Context, entries, *, per_page=12):
        converted = [TagPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page)


class Tags(commands.Cog):
    """Tag related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Tags']
        self.prefix = "!"

    async def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '🏷️'

    @commands.group(invoke_without_command=True, case_insensitive=True, ignore_extra=False, aliases=['tags'])
    async def tag(self, ctx: Context, *, tag_name: str = None):
        """Sends the tag's content."""

        if tag_name is None:
            return await ctx.send_help('tag')

        data = await self.db.find_one({'name': tag_name.lower()})
        if data is None:
            data = await self.db.find_one({'aliases': tag_name.lower()})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await ctx.send("No tag found. %s" % (ctx.author.mention))

        await self.db.update_one({'_id': data['_id']}, {'$inc': {'uses_count': 1}})
        await ctx.send(data['tag_content'], reference=ctx.replied_reference)

    @tag.command(name='search')
    async def tag_search(self, ctx: Context, *, query):
        """Search for tag matches based on the query that you've given."""

        query = str(query).lower()
        entries = await self.db.find({'name': {'$regex': query, '$options': 'i'}}).to_list(100000)
        try:
            p = TagPages(ctx=ctx, entries=entries, per_page=7)
            await p.start()
        except Exception:
            await ctx.send('No tags found. %s' % (ctx.author.mention))

    @tag.command(name='list')
    async def tag_list(self, ctx: Context, member: disnake.Member = None):
        """See the list of all the tags that the member owns."""

        member = member or ctx.author
        entries = await self.db.find({'owner_id': member.id}).to_list(100000)
        try:
            p = TagPages(ctx=ctx, entries=entries, per_page=7)
            await p.start()
        except Exception:
            await ctx.send("`{}` has no tags.".format(member))

    @tag.command(name='all')
    async def tag_all(self, ctx: Context):
        """See a list of all the existing tags."""

        entries = await self.db.find().to_list(100000)
        p = TagPages(ctx=ctx, entries=entries, per_page=7)
        await p.start()

    @tag.command(name='leaderboard', aliases=['lb', 'top'])
    async def tag_leaderboard(self, ctx: Context):
        """See top **10** most used tags."""

        results = await self.db.find().sort("uses_count", -1).to_list(10)
        index = 0
        em = disnake.Embed(color=disnake.Color.blurple())
        for result in results:
            tag_name = result['name']
            uses = result['uses_count']
            get_owner = result['owner_id']
            owner = self.bot.get_user(get_owner)
            index += 1
            em.add_field(name=f"`{index}`.\u2800{tag_name}", value=f"Uses: `{uses}`\n Owner: `{owner}`", inline=False)

        await ctx.send(embed=em)

    @tag.command(name='info')
    async def tag_info(self, ctx: Context, *, tag_name: str = None):
        """See some info about the tag."""

        if tag_name is None:
            return await ctx.reply("**!tag info <tag_name>**")

        data = await self.db.find_one({'name': tag_name.lower()})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                pass
        if data is None:
            data = await self.db.find_one({'aliases': tag_name.lower()})
        if data is None:
            return await ctx.send("Tag **%s** does not exist. %s" % (tag_name, ctx.author.mention))

        sortTags = await self.db.find().sort('uses_count', -1).to_list(100000)
        rank = 0
        for i in sortTags:
            rank += 1
            if i['_id'] == data['_id']:
                break

        tag_name = data['name']
        owner_id = data["owner_id"]
        tag_uses = data["uses_count"]
        tag_created_at = data["created_at"]
        the_tag_id = data["_id"]

        tag_owner = self.bot.get_user(owner_id)

        em = disnake.Embed(color=Colours.blurple, title=tag_name)
        em.set_author(name=tag_owner, url=tag_owner.display_avatar, icon_url=tag_owner.display_avatar)
        em.add_field(name="Owner", value=tag_owner.mention)
        em.add_field(name="Uses", value=tag_uses)
        em.add_field(name="Rank", value=f"`#{rank}`")
        em.add_field(name="Tag ID", value="`{}`".format(the_tag_id), inline=False)
        em.set_footer(text="Tag created at • {}".format(tag_created_at))

        await ctx.send(embed=em)

    @tag.group(name='aliases', aliases=['alias'], invoke_without_command=True, case_insensitive=True, ignore_extra=False)
    async def tag_aliases(self, ctx: Context, *, tag: str = None):
        """See all the aliases the tag has."""

        if tag is None:
            return await ctx.reply("You must give the tag's name. %s" % (ctx.author.mention))

        try:
            tag = int(tag)
            data = await self.db.find_one({'_id': tag})

            if data is None:
                return await ctx.send("This is not a valid tag's id or this tag does not exist. %s" % (ctx.author.mention))
            try:
                _list = []
                _list_ = data['aliases']
                for key in _list_:
                    _list.append(f"`{key}`")
            except KeyError:
                return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")

            if len(_list) <= 0:
                return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")

            tag_name = data['name']
            em = disnake.Embed(color=disnake.Color.blurple(), title="Here are all the aliases for the tag `%s`" % (tag_name))
            aliases = "\n• ".join(_list)
            if len(_list) == 1:
                em.description = f"• {aliases}"
            else:
                em.description = f"• {aliases}"
            await ctx.send(embed=em)

        except ValueError:
            tag = str(tag).lower()
            data = await self.db.find_one({'name': tag})

            if data is None:
                return await ctx.send(f"No tag named **{tag}** found. {ctx.author.mention}")

            try:
                _list = []
                _list_ = data['aliases']
                for key in _list_:
                    _list.append(f"`{key}`")
            except KeyError:
                return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")

            if len(_list) <= 0:
                return await ctx.send(f"This tag has no aliases. {ctx.author.mention}")

            em = disnake.Embed(color=disnake.Color.blurple(), title="Here are all the aliases for the tag `%s`" % (tag))
            aliases = "\n• ".join(_list)
            if len(_list) == 1:
                em.description = f"• {aliases}"
            else:
                em.description = f"• {aliases}"
            await ctx.send(embed=em)

    @tag_aliases.command(name='create', aliases=['make', 'add'])
    @commands.has_any_role(*all_roles)
    async def tag_alias_create(self, ctx: Context, *, tag: str = None):
        """Create an alias for an existing tag that you own."""

        if tag is None:
            return await ctx.reply("You must give the tag's name. %s" % (ctx.author.mention))

        all_names = []
        names = await self.db.find().to_list(100000)
        allAliases = []
        for name in names:
            all_names.append(name['name'])
            allAliases.append(name['aliases'])

        try:
            tag = int(tag)
            data = await self.db.find_one({'_id': tag})

            if data is None:
                return await ctx.send("This is not a valid tag's id or this tag does not exist. %s" % (ctx.author.mention))

            if ctx.author.id != 374622847672254466:
                if data['owner_id'] != ctx.author.id:
                    return await ctx.send("You do not own this tag. %s" % (ctx.author.mention))

            tagAliases = data['aliases']
            if ctx.author.id != 374622847672254466:
                if len(data['aliases']) > 7:
                    return await ctx.send("This tag has reached the maximum amount of aliases (`7`). %s" % (ctx.author.mention))

            await ctx.send("What do you wish the alias to be named as? %s" % (ctx.author.mention))

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                alias_name = await self.bot.wait_for('message', check=check, timeout=180)
                try:
                    e = int(alias_name.content)
                    return await ctx.send("The alias cannot be a number! %s" % (ctx.author.mention))
                except Exception:
                    pass
            except asyncio.TimeoutError:
                return await ctx.send("Took too much to respond. %s" % (ctx.author.mention))
            else:
                if str(alias_name.content).lower() in all_names:
                    return await ctx.send("There is an existing tag with that name already. %s" % (ctx.author.mention))
                elif str(alias_name.content).lower() in allAliases:
                    return await ctx.send("There is an existing alias with that name already. %s" % (ctx.author.mention))
                elif len(alias_name.content) > 75:
                    return await ctx.send("Alias cannot be longer than `75` characters!")
                if len(tagAliases) == 0:
                    await self.db.update_one({'_id': tag}, {'$set': {'aliases': [str(alias_name.content).lower()]}})
                else:
                    tagAliases.append(str(alias_name.content).lower())
                    await self.db.update_one({'_id': tag}, {'$set': {'aliases': tagAliases}})
                await ctx.send(f"{ctx.author.mention} Successfully added the alias `{str(alias_name.content).lower()}` for tag **{data['name']}**")

        except ValueError:
            tag = str(tag).lower()
            data = await self.db.find_one({'name': tag})

            if data is None:
                return await ctx.send("This is not a valid tag's id or this tag does not exist. %s" % (ctx.author.mention))

            if ctx.author.id != 374622847672254466:
                if data['owner_id'] != ctx.author.id:
                    return await ctx.send("You do not own this tag. %s" % (ctx.author.mention))

            tagAliases = data['aliases']
            if ctx.author.id != 374622847672254466:
                if len(data['aliases']) > 7:
                    return await ctx.send("This tag has reached the maximum amount of aliases (`7`). %s" % (ctx.author.mention))

            await ctx.send("What do you wish the alias to be named as? %s" % (ctx.author.mention))

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                alias_name = await self.bot.wait_for('message', check=check, timeout=180)
                try:
                    e = int(alias_name.content)  # noqa
                    return await ctx.send("The alias cannot be a number! %s" % (ctx.author.mention))
                except Exception:
                    pass
            except asyncio.TimeoutError:
                return await ctx.send("Took too much to respond. %s" % (ctx.author.mention))
            else:
                if str(alias_name.content).lower() in all_names:
                    return await ctx.send("There is an existing tag with that name already. %s" % (ctx.author.mention))
                elif str(alias_name.content).lower() in allAliases:
                    return await ctx.send("There is an existing alias with that name already. %s" % (ctx.author.mention))
                elif len(alias_name.content) > 75:
                    return await ctx.send("Alias cannot be longer than `75` characters!")
                if len(tagAliases) == 0:
                    await self.db.update_one({'name': tag}, {'$set': {'aliases': [str(alias_name.content).lower()]}})
                else:
                    tagAliases.append(str(alias_name.content).lower())
                    await self.db.update_one({'name': tag}, {'$set': {'aliases': tagAliases}})
                await ctx.send(f"{ctx.author.mention} Successfully added the alias `{str(alias_name.content).lower()}` for tag **{data['name']}**")

    @tag_aliases.command(name='delete')
    @commands.has_any_role(*all_roles)
    async def tag_alias_delete(self, ctx: Context, *, alias: str = None):
        """Delete an alias from a tag that you own."""

        if alias is None:
            return await ctx.reply("You must specify the name of the alias you wish to delete. %s" % (ctx.author.mention))
        result = await self.db.find_one({'aliases': alias.lower()})
        if result is None:
            return await ctx.send(f"{ctx.author.mention} There is no alias called **{alias}**")
        aliases = result['aliases']
        tag_name = result['name']
        owner_id = result['owner_id']
        try:
            if ctx.author.id != 374622847672254466:
                if ctx.author.id != owner_id:
                    return await ctx.send("You do not own this tag! %s" % (ctx.author.mention))

            view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
            view.message = msg = await ctx.send(
                f"{ctx.author.mention} Are you sure you want to remove the alias `{alias}` from the tag **{tag_name}**?",
                view=view
            )
            await view.wait()
            if view.response is True:
                new_aliases = []
                for _alias in aliases:
                    if not _alias == alias.lower():
                        new_aliases.append(_alias)
                await self.db.update_one({'name': tag_name}, {'$set': {'aliases': new_aliases}})
                e = f"{ctx.author.mention} Successfully removed the alias `{alias}` from tag **{tag_name}**!"
                return await msg.edit(content=e, view=view)

            elif view.response is False:
                e = "Alias has not been deleted. %s" % (ctx.author.mention)
                return await msg.edit(content=e, view=view)

        except UnboundLocalError:
            return await ctx.send("No such alias exists. %s" % (ctx.author.mention))

    @tag.command(name='create', aliases=['make', 'add'])
    @commands.has_any_role(*all_roles)
    async def tag_create(self, ctx: Context, *, tag_name: str = None):
        """Create a tag."""

        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        if tag_name is None:
            await ctx.send("What do you want the tag to be named as? {}".format(ctx.author.mention))

            try:
                pre_tag = await self.bot.wait_for('message', timeout=180, check=check)
                tag_name = pre_tag.content

            except asyncio.TimeoutError:
                return await ctx.reply("Ran out of time.")

        matches = re.findall(filter_invite, tag_name)
        if ctx.author.id != 374622847672254466:
            for tag_name in matches:
                await ctx.send("No invites or what so ever.")
                return

        data = await self.db.find_one({'name': str(tag_name).lower()})

        if data is not None:
            await ctx.send("Tag name already taken.")
            return

        elif len(tag_name) >= 75:
            await ctx.send("Tag's name cannot be longer than `75` characters!")
            return
        elif len(tag_name) < 2:
            await ctx.send("Tag's name cannot be less than `2` characters long!")
            return
        elif tag_name.isnumeric():
            await ctx.send("Tag name cannot be a number!")
            return

        await ctx.send("Please send the tag's content. {}".format(ctx.author.mention))

        try:
            pre_tag_content = await self.bot.wait_for('message', timeout=420, check=check)
            if pre_tag_content.attachments:
                await ctx.send("Tag cannot contain attachments!")
                return
            else:
                tag_content = pre_tag_content.content
                matches = re.findall(filter_invite, tag_content)

                if ctx.author.id != 374622847672254466:
                    for tag_content in matches:
                        await ctx.send("No invites or what so ever.")
                        return

        except asyncio.TimeoutError:
            return await ctx.reply("Ran out of time.")

        else:
            get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
            get_sorted = await self.db.find().sort("_id", -1).to_list(1)
            for x in get_sorted:
                last_id = x['_id']

            post = {"_id": last_id + 1,
                    "tag_content": tag_content,
                    "owner_id": ctx.author.id,
                    'name': tag_name.lower(),
                    "created_at": get_time,
                    "uses_count": 0,
                    "aliases": []
                    }

            await self.db.insert_one(post)

            await ctx.send("Tag `{}` Successfully created!".format(tag_name))

    @tag.command(name='delete')
    @commands.has_any_role(*all_roles)
    async def tag_delete(self, ctx: Context, *, tag_name: str = None):
        """Delete a tag that you own."""

        if tag_name is None:
            return await ctx.reply("**!tag delete <tag_name>**")

        data = await self.db.find_one({'name': tag_name.lower()})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await ctx.send("That tag does not exist. %s" % (ctx.author.mention))
        if data is None:
            return await ctx.send("That tag does not exist. %s" % (ctx.author.mention))
        if ctx.author.id != 374622847672254466:
            if ctx.author.id != data['owner_id']:
                return await ctx.send("You do not own the tag **%s**! %s" % (data['name'], ctx.author.mention))

        view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
        view.message = msg = await ctx.send("Are you sure you wish to delete the tag **%s**? %s" % (data['name'], ctx.author.mention), view=view)
        await view.wait()
        if view.response is True:
            await self.db.delete_one({'_id': data['_id']})
            e = "Successfully deleted the tag **%s**. %s" % (data['name'], ctx.author.mention)
            return await msg.edit(content=e, view=view)

        elif view.response is False:
            e = "Operation of deleting the tag  **%s** has been canceled. %s" % (data['name'], ctx.author.mention)
            return await msg.edit(content=e, view=view)

    @tag.command(name='remove')
    @commands.is_owner()
    async def tag_remove(self, ctx: Context, *, tag_name: str = None):
        """Remove a tag from the database."""

        if tag_name is None:
            return await ctx.reply("**!tag remove <tag_name>**")

        data = await self.db.find_one({'name': tag_name.lower()})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await ctx.send("That tag does not exist in the database. %s" % (ctx.author.mention))
        if data is None:
            return await ctx.send("That tag does not exist in the database. %s" % (ctx.author.mention))

        get_tag_owner = data['owner_id']
        tag_owner = self.bot.get_user(get_tag_owner)
        tag_name = data['name']
        tag_created_at = data['created_at']
        uses = data['uses_count']

        await self.db.delete_one({"_id": data['_id']})

        em = disnake.Embed(title="Tag Removed", color=Colours.red)
        em.add_field(name="Name", value=tag_name)
        em.add_field(name="Owner", value=tag_owner)
        em.add_field(name="Uses", value=f"`{uses}`", inline=False)
        em.set_footer(text=f"Tag created at • {tag_created_at}")

        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == 374622847672254466:
            return
        await self.db.delete_many({"owner_id": member.id})

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send("You must be at least `level 15+` in order to use this command! %s" % (ctx.author.mention))
        else:
            await self.bot.reraise(ctx, error)

    @tag.error
    async def tag_error(self, ctx: Context, error):
        if isinstance(error, commands.TooManyArguments):
            return
        else:
            if hasattr(ctx.command, 'on_error'):
                return
            await self.bot.reraise(ctx, error)


def setup(bot):
    bot.add_cog(Tags(bot))
