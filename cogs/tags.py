from typing import List
import re
import asyncio
import datetime
import textwrap

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Param

from utils import fuzzy
from utils.colors import Colours
from utils.paginator import SimplePages
from utils.helpers import clean_inter_content, safe_send_prepare

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
    def __init__(self, ctx, entries, *, per_page=12):
        converted = [TagPageEntry(entry) for entry in entries]
        super().__init__(ctx=ctx, entries=converted, per_page=per_page)


async def autocomplete_tags(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    all_tags = inter.bot.tags + inter.bot.tag_aliases
    return fuzzy.finder(string, all_tags, lazy=False)[:25]


async def autocomplete_tags_names_only(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    tags = inter.bot.tags
    return fuzzy.finder(string, tags, lazy=False)[:25]


async def autocomplete_tags_aliases_only(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    tags = inter.bot.tag_aliases
    return fuzzy.finder(string, tags, lazy=False)[:25]


async def tag_name(inter: disnake.ApplicationCommandInteraction, argument: str):
    converted = await clean_inter_content()(inter, argument)
    lower = converted.lower().strip()

    if not lower:
        raise commands.BadArgument('Missing tag name.')

    if len(lower) > 50:
        raise commands.BadArgument('Tag name must be less than 50 characters.')
    elif len(lower) < 3:
        raise commands.BadArgument('Tag must be greater than 3 characters.')
    elif lower.isnumeric():
        raise commands.BadArgument('Tag must not be digits.')

    return lower


async def alias_name(inter: disnake.ApplicationCommandInteraction, argument: str):
    converted = await clean_inter_content()(inter, argument)
    lower = converted.lower().strip()

    if not lower:
        raise commands.BadArgument('Missing alias name.')

    if len(lower) > 50:
        raise commands.BadArgument('Tag alias must be less than 50 characters.')
    elif len(lower) < 3:
        raise commands.BadArgument('Tag alias must be greater than 3 characters.')
    elif lower.isnumeric():
        raise commands.BadArgument('Tag alias must not be digits.')

    return lower


class InteractiveTagCreation(disnake.ui.View):
    def __init__(
        self,
        bot: ViHillCorner,
        original_interaction: ApplicationCommandInteraction,
        edit: dict = None
    ):
        super().__init__(timeout=300.0)
        self.bot = bot
        self.original_inter = original_interaction
        self.author = original_interaction.author
        self._edit = edit
        self.aborted = False

        if edit is not None:
            self.remove_item(self.set_name)
            self.name = edit['name']
            self.content = edit['tag_content']
        else:
            self.name = self.content = None

    async def on_error(self, error: Exception, item, interaction: disnake.MessageInteraction) -> None:
        if isinstance(error, asyncio.TimeoutError):
            if interaction.response.is_done():
                method = self.message.edit
            else:
                method = interaction.response.edit_message
            await method(content='You took too long. Goodbye.', view=None, embed=None)
            return self.stop()
        raise error

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        if inter.author.id != self.author.id:
            await inter.response.send_message(f'Only `{self.author}` can use the buttons on this message.', ephemeral=True)
            return False
        return True

    def lock_all(self):
        for child in self.children:
            if child.label == 'Abort':
                continue
            child.disabled = True

    def unlock_all(self):
        for child in self.children:
            if child.label == 'Confirm':
                if self._edit:
                    if self._edit['tag_content'] != self.content:
                        child.disabled = False
                        continue
                elif self.name is not None and self.content is not None:
                    child.disabled = False
                else:
                    child.disabled = True
            else:
                child.disabled = False

    def prepare_embed(self):
        em = disnake.Embed(title='Tag creation', color=Colours.blurple)
        em.add_field(name='Name', value=str(self.name), inline=False)
        em.add_field(name='Content', value=textwrap.shorten(str(self.content), 1024), inline=False)

        if len(str(self.content)) > 1024:
            em.description = '\n**Hint:** Tag content reached embed field limitation, this will not affect the content itself.'
        return em

    @disnake.ui.button(label='Name', style=disnake.ButtonStyle.blurple)
    async def set_name(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.lock_all()
        msg_content = 'Cool, let\'s make a name. Send the tag name in the next message...'
        await inter.response.edit_message(content=msg_content, view=self)

        msg = await self.bot.wait_for(
            'message',
            timeout=60.0,
            check=lambda m: m.author.id == self.author.id and m.channel.id == inter.channel.id
        )
        if self.is_finished():
            return

        content = None
        try:
            name = await tag_name(inter, msg.content)
        except commands.BadArgument as e:
            content = f'{e}. Press "Name" to retry.'
        else:
            data = await self.bot.db1['Tags'].find_one({'name': name})
            if data is None:
                data = await self.bot.db1['Tags'].find_one({'aliases': name})
                if data is None:
                    self.name = name
                    self.remove_item(button)
                else:
                    content = 'An alias with that name already exists.'
            else:
                content = 'A tag with that name already exists.'

        self.unlock_all()
        await self.message.edit(content=content, embed=self.prepare_embed(), view=self)

    @disnake.ui.button(label='Content', style=disnake.ButtonStyle.blurple)
    async def set_content(self, button: disnake.Button, inter: disnake.MessageInteraction):
        self.lock_all()
        msg_content = f'Cool, let\'s {"edit the" if self._edit else "make a"} content. Send the tag content in the next message...'

        await inter.response.edit_message(content=msg_content, view=self)
        msg = await self.bot.wait_for(
            'message',
            timeout=300.0,
            check=lambda m: m.author.id == self.author.id and m.channel.id == inter.channel.id
        )
        if self.is_finished():
            return

        if msg.content:
            clean_content = await clean_inter_content()(inter, msg.content)
        else:
            clean_content = msg.content

        if msg.attachments:
            clean_content += f'\n{msg.attachments[0].url}'

        c = None
        if len(clean_content) > 2000:
            c = 'Tag content is a maximum of 2000 characters.'
        else:
            self.content = clean_content

        self.unlock_all()
        await self.message.edit(content=c, embed=self.prepare_embed(), view=self)

    @disnake.ui.button(label='Confirm', style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.Button, inter: disnake.MessageInteraction):
        if self._edit and self._edit['tag_content'] == self.content:
            return await inter.response.edit_message(
                content='Content still the same...\nHint: edit it by pressing "Content"'
            )
        for child in self.children:
            child.disabled = True
        await inter.response.edit_message(view=self)
        self.stop()

    @disnake.ui.button(label='Abort', style=disnake.ButtonStyle.red)
    async def cancel(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(
            content=f'Tag {"edi" if self._edit else "crea"}tion aborted.',
            view=None,
            embed=None
        )
        self.aborted = True
        self.stop()


class Tags(commands.Cog):
    """Tag related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.db = bot.db1['Tags']

    @commands.Cog.listener()
    async def on_ready(self):
        tags = await self.db.find().to_list(1000000)
        for tag in tags:
            self.bot.tags.append(tag['name'])
            for alias in tag['aliases']:
                self.bot.tag_aliases.append(alias)

    @property
    def display_emoji(self) -> str:
        return '🏷️'

    @commands.slash_command(name='tag')
    async def base_tag(self, inter):
        """Base tag which holds the slash subcommands for it."""
        pass

    @base_tag.sub_command(name='show')
    async def tag_show(
        self,
        inter: ApplicationCommandInteraction,
        tag_name: str = Param(
            description='The tag\'s name to search for',
            autocomplete=autocomplete_tags
        ),
        type=Param(
            'rich',
            choices=[
                disnake.OptionChoice('Rich', 'rich'),
                disnake.OptionChoice('Raw', 'raw')
            ],
            description='The type of the content'
        )
    ):
        """Search for a tag and show it."""

        data = await self.db.find_one({'name': tag_name.lower()})
        if data is None:
            data = await self.db.find_one({'aliases': tag_name.lower()})
            if data is None:
                try:
                    data = await self.db.find_one({'_id': int(tag_name)})
                    if data is None:
                        return await inter.response.send_message("Tag not found.", ephemeral=True)
                except ValueError:
                    return await inter.response.send_message("Tag not found.", ephemeral=True)

        await self.db.update_one({'_id': data['_id']}, {'$inc': {'uses_count': 1}})
        if type == 'raw':
            first_step = disnake.utils.escape_markdown(data['tag_content'])
            kwargs = await safe_send_prepare(first_step.replace('<', '\\<'))
        else:
            kwargs = dict(content=data['tag_content'])

        await inter.response.send_message(**kwargs)

    @base_tag.sub_command(name='list')
    async def tag_list(
        self,
        inter: ApplicationCommandInteraction,
        member: disnake.Member = Param(default=lambda inter: inter.author)
    ):
        """See the list of all the tags that the member owns."""

        entries = await self.db.find({'owner_id': member.id}).to_list(100000)
        try:
            p = TagPages(ctx=inter, entries=entries, per_page=7)
            await p.start()
        except Exception:
            await inter.response.send_message(f"`{member}` has no tags.", ephemeral=True)

    @base_tag.sub_command(name='all')
    async def tag_all(self, inter: ApplicationCommandInteraction):
        """See a list of all the existing tags."""

        entries = await self.db.find().to_list(100000)
        p = TagPages(ctx=inter, entries=entries, per_page=7)
        await p.start()

    @base_tag.sub_command(name='leaderboard')
    async def tag_leaderboard(self, inter: ApplicationCommandInteraction):
        """See top 10 most used tags."""

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

        await inter.response.send_message(embed=em)

    @base_tag.sub_command(name='info')
    async def tag_info(
        self,
        inter: ApplicationCommandInteraction,
        tag_name: str = Param(
            description='The tag to show info about',
            autocomplete=autocomplete_tags
        )
    ):
        """See some info about the tag."""

        data = await self.db.find_one({'name': tag_name.lower()})
        if data is None:
            data = await self.db.find_one({'aliases': tag_name.lower()})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await inter.response.send_message("Tag not found.", ephemeral=True)
        if data is None:
            return await inter.response.send_message("Tag not found.", ephemeral=True)

        sort_tags = await self.db.find().sort('uses_count', -1).to_list(100000)
        rank = 0
        for i in sort_tags:
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

        await inter.response.send_message(embed=em)

    @base_tag.sub_command_group(name='alias')
    async def base_tag_alias(self, inter):
        """Base tag alias command for all the tag aliases subcommands."""
        pass

    @base_tag_alias.sub_command(name='show')
    async def tag_alias_show(
        self,
        inter: ApplicationCommandInteraction,
        tag_name: str = Param(
            description='The tag of which aliases to see',
            autocomplete=autocomplete_tags_names_only
        )
    ):
        """See all the aliases the tag has."""

        try:
            tag = int(tag_name)
            data = await self.db.find_one({'_id': tag})

            if data is None:
                return await inter.response.send_message("Tag not found.", ephemeral=True)
            try:
                _list = []
                _list_ = data['aliases']
                for key in _list_:
                    _list.append(f"`{key}`")
            except KeyError:
                return await inter.response.send_message("This tag has no aliases.", ephemeral=True)

            if len(_list) <= 0:
                return await inter.response.send_message("This tag has no aliases.", ephemeral=True)

            name = data['name']
            em = disnake.Embed(color=disnake.Color.blurple(), title=f"Here are all the aliases for the tag `{name}`")
            aliases = "\n• ".join(_list)
            if len(_list) == 1:
                em.description = f"• {aliases}"
            else:
                em.description = f"• {aliases}"
            await inter.response.send_message(embed=em)

        except ValueError:
            tag = tag_name.lower()
            data = await self.db.find_one({'name': tag})
            if data is None:
                return await inter.response.send_message("Tag not found.", ephemeral=True)

            try:
                _list = []
                _list_ = data['aliases']
                for key in _list_:
                    _list.append(f"`{key}`")
            except KeyError:
                return await inter.response.send_message("This tag has no aliases.", ephemeral=True)

            if len(_list) <= 0:
                return await inter.response.send_message("This tag has no aliases.", ephemeral=True)

            em = disnake.Embed(color=disnake.Color.blurple(), title="Here are all the aliases for the tag `%s`" % (tag))
            aliases = "\n• ".join(_list)
            if len(_list) == 1:
                em.description = f"• {aliases}"
            else:
                em.description = f"• {aliases}"
            await inter.response.send_message(embed=em)

    @base_tag_alias.sub_command(name='create')
    async def tag_alias_create(
        self,
        inter: ApplicationCommandInteraction,
        tag_name: str = Param(
            description='The tag for which to add the alias to',
            autocomplete=autocomplete_tags_names_only
        ),
        alias: str = Param(description='The alias to add')
    ):
        """Create an alias for an existing tag that you own."""

        found = False
        if inter.author.id != self.bot._owner_id:
            for role in inter.author.roles:
                if role.id in all_roles:
                    found = True
                    break
        if not found:
            return await inter.response.send_message('You must be at least `level 15+` in order to use this command!', ephemeral=True)

        alias = alias.lower()
        data = await self.db.find_one({'name': alias})
        if data is None:
            data = await self.db.find_one({'aliases': alias})
            if data is not None:
                return await inter.response.send_message('There is an existing alias with this name already.', ephemeral=True)
        else:
            return await inter.response.send_message('There is an existing tag with this name already.', ephemeral=True)

        try:
            alias = await alias_name(inter, alias)
        except commands.BadArgument as e:
            return await inter.response.send_message(e, ephemeral=True)

        tag_name = tag_name.lower()
        data = await self.db.find_one({'name': tag_name})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await inter.response.send_message("Tag not found.", ephemeral=True)
            else:
                if data is None:
                    return await inter.response.send_message("Tag not found.", ephemeral=True)

        else:
            if inter.author.id != self.bot._owner_id:
                if data['owner_id'] != inter.author.id:
                    return await inter.response.send_message("This tag is not owned by you.", ephemeral=True)

            tag_aliases = data['aliases']
            if inter.author.id != self.bot._owner_id:
                if len(data['aliases']) > 7:
                    return await inter.response.send_message("This tag has reached the maximum amount of aliases (`7`)", ephemeral=True)
            else:
                if len(tag_aliases) == 0:
                    await self.db.update_one({'_id': data['_id']}, {'$set': {'aliases': [alias]}})
                else:
                    tag_aliases.append(alias)
                    await self.db.update_one({'_id': data['_id']}, {'$set': {'aliases': tag_aliases}})
                self.bot.tag_aliases.append(alias)
                await inter.response.send_message(f"Successfully added the alias `{alias}` for tag **{data['name']}**")

    @base_tag_alias.sub_command(name='delete')
    async def tag_alias_delete(
        self,
        inter: ApplicationCommandInteraction,
        alias: str = Param(
            description='The alias to delete',
            autocomplete=autocomplete_tags_aliases_only
        )
    ):
        """Delete an alias from a tag that you own."""

        found = False
        if inter.author.id != self.bot._owner_id:
            for role in inter.author.roles:
                if role.id in all_roles:
                    found = True
                    break
        if not found:
            return await inter.response.send_message('You must be at least `level 15+` in order to use this command!', ephemeral=True) 

        alias = alias.lower()
        result = await self.db.find_one({'aliases': alias})
        if result is None:
            return await inter.response.send_message("Alias not found.", ephemeral=True)
        aliases = result['aliases']
        tag_name = result['name']
        owner_id = result['owner_id']
        try:
            if inter.author.id != self.bot._owner_id:
                if inter.author.id != owner_id:
                    return await inter.response.send_message("This tag is not owned by you.", ephemeral=True)

            view = self.bot.confirm_view(inter, "Did not react in time.")
            await inter.response.send_message(
                f"Are you sure you want to remove the alias `{alias}` from the tag **{tag_name}**?",
                view=view
            )
            await view.wait()
            if view.response is True:
                new_aliases = []
                for _alias in aliases:
                    if not _alias == alias.lower():
                        new_aliases.append(_alias)
                await self.db.update_one({'name': tag_name}, {'$set': {'aliases': new_aliases}})
                e = f"Successfully removed the alias `{alias}` from tag **{tag_name}**!"
                self.bot.tag_aliases.pop(self.bot.tag_aliases.index(alias))
                return await inter.edit_original_message(content=e, view=view)

            elif view.response is False:
                e = "Alias has not been deleted."
                return await inter.edit_original_message(content=e, view=view)

        except UnboundLocalError:
            return await inter.response.send_message("Alias not found.", ephemeral=True)

    @base_tag.sub_command(name='create')
    async def tag_create(self, inter: ApplicationCommandInteraction):
        """Create a tag."""

        found = False
        if inter.author.id != self.bot._owner_id:
            for role in inter.author.roles:
                if role.id in all_roles:
                    found = True
                    break
        if not found:
            return await inter.response.send_message('You must be at least `level 15+` in order to use this command!', ephemeral=True) 

        view = InteractiveTagCreation(self.bot, inter)
        await inter.response.send_message(embed=view.prepare_embed(), view=view)
        view.message = await inter.original_message()

        if await view.wait():
            return await view.message.edit(content='You took too long. Goodbye.', view=None, embed=None)
        else:
            if view.aborted:
                return
            await view.message.edit(view=None)

        get_time = datetime.datetime.utcnow().strftime("%d/%m/%Y")
        get_sorted = await self.db.find().sort("_id", -1).to_list(1)
        for x in get_sorted:
            last_id = x['_id']

        post = {
            "_id": last_id + 1,
            "tag_content": view.content,
            "owner_id": inter.author.id,
            'name': view.name,
            "created_at": get_time,
            "uses_count": 0,
            "aliases": []
        }

        await self.db.insert_one(post)
        self.bot.tags.append(view.name)
        await inter.followup.send(f'Tag `{view.name}` successfully created.')

    @base_tag.sub_command(name='edit')
    async def tag_edit(
        self,
        inter: ApplicationCommandInteraction,
        tag_name: str = Param(
            description='The tag to edit',
            autocomplete=autocomplete_tags_names_only
        )
    ):
        """Edits a tag that you own."""

        found = False
        if inter.author.id != self.bot._owner_id:
            for role in inter.author.roles:
                if role.id in all_roles:
                    found = True
                    break
        if not found:
            return await inter.response.send_message('You must be at least `level 15+` in order to use this command!', ephemeral=True) 

        tag_name = tag_name.lower()
        data = await self.db.find_one({'name': tag_name})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await inter.response.send_message("Tag not found.", ephemeral=True)
            else:
                if data is None:
                    return await inter.response.send_message("Tag not found.", ephemeral=True)

        if inter.author.id != self.bot._owner_id:
            if inter.author.id != data['owner_id']:
                return await inter.response.send_message("This tag is not owned by you.", ephemeral=True)

        view = InteractiveTagCreation(self.bot, inter, data)
        await inter.response.send_message(embed=view.prepare_embed(), view=view)
        view.message = await inter.original_message()

        if await view.wait():
            return await view.message.edit(content='You took too long. Goodbye.', view=None, embed=None)
        else:
            if view.aborted:
                return
            await view.message.edit(view=None)

        await self.db.update_one({'_id': data['_id']}, {'$set': {'tag_content': view.content}})
        await inter.followup.send(f'Tag `{view.name}` successfully updated.')

    @base_tag.sub_command(name='delete')
    async def tag_delete(
        self,
        inter: ApplicationCommandInteraction,
        tag_name: str = Param(
            description='The tag to delete',
            autocomplete=autocomplete_tags_names_only
        )
    ):
        """Delete a tag that you own."""

        found = False
        if inter.author.id != self.bot._owner_id:
            for role in inter.author.roles:
                if role.id in all_roles:
                    found = True
                    break
        if not found:
            return await inter.response.send_message('You must be at least `level 15+` in order to use this command!', ephemeral=True) 

        tag_name = tag_name.lower()
        data = await self.db.find_one({'name': tag_name})
        if data is None:
            try:
                data = await self.db.find_one({'_id': int(tag_name)})
            except ValueError:
                return await inter.response.send_message("Tag not found.", ephemeral=True)
            else:
                if data is None:
                    return await inter.response.send_message("Tag not found.", ephemeral=True)

        if inter.author.id != self.bot._owner_id:
            if inter.author.id != data['owner_id']:
                return await inter.response.send_message("This tag is not owned by you.", ephemeral=True)

        view = self.bot.confirm_view(inter, "Did not react in time.")
        await inter.response.send_message("Are you sure you wish to delete the tag **%s**?" % (data['name']), view=view)
        await view.wait()
        if view.response is True:
            await self.db.delete_one({'_id': data['_id']})
            e = "Successfully deleted the tag **%s**." % (data['name'])
            self.bot.tags.pop(self.bot.tags.index(data['name']))
            for alias in data['aliases']:
                self.bot.tag_aliases.pop(self.bot.tag_aliases.index(alias))
            return await inter.edit_original_message(content=e, view=view)

        elif view.response is False:
            e = "Operation of deleting the tag  **%s** has been cancelled." % (data['name'])
            return await inter.edit_original_message(content=e, view=view)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.id == self.bot._owner_id:
            return
        await self.db.delete_many({"owner_id": member.id})


def setup(bot):
    bot.add_cog(Tags(bot))
