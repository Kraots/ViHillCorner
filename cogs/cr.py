import asyncio
import datetime

import disnake
from disnake.ext import commands

from utils import time
from utils.context import Context
from utils.databases import CustomRole

from main import ViHillCorner

nono_list = ('staff', 'mod')
all_roles = (
    'Staff', 'lvl 40+', 'lvl 45+', 'lvl 50+', 'lvl 55+', 'lvl 60+', 'lvl 65+', 'lvl 69+', 'lvl 75+', 'lvl 80+',
    'lvl 85+', 'lvl 90+', 'lvl 95+', 'lvl 100+', 'lvl 105+', 'lvl 110+', 'lvl 120+', 'lvl 130+', 'lvl 150+', 'lvl 155+', 'lvl 160+', 'lvl 165+', 'lvl 170+',
    'lvl 175+', 'lvl 180+', 'lvl 185+', 'lvl 190+', 'lvl 195+', 'lvl 200+', 'lvl 205+', 'lvl 210+', 'lvl 215+', 'lvl 220+', 'lvl 230+', 'lvl 240+',
    'lvl 250+', 'lvl 255+', 'lvl 260+', 'lvl 265+', 'lvl 270+', 'lvl 275+', 'lvl 275+', 'lvl 280+', 'lvl 285+', 'lvl 290+', 'lvl 300+', 'lvl 305+',
    'lvl 310+', 'lvl 315+', 'lvl 320+', 'lvl 330+', 'lvl 340+', 'lvl 350+', 'lvl 355+', 'lvl 360+', 'lvl 365+', 'lvl 370+', 'lvl 375+', 'lvl 380+',
    'lvl 385+', 'lvl 390+', 'lvl 395+', 'lvl 400+', 'lvl 405+', 'lvl 410+', 'lvl 415+', 'lvl 420+', 'lvl 430+', 'lvl 440+', 'lvl 450+', 'lvl 455+',
    'lvl 460+', 'lvl 465+', 'lvl 470+', 'lvl 475+', 'lvl 480+', 'lvl 485+', 'lvl 490+', 'lvl 495+', 'lvl 500+'
)


class CustomRoles(commands.Cog):
    """Custom roles related commands."""

    def __init__(self, bot: ViHillCorner):
        self.bot = bot
        self.prefix = '!'

    def cog_check(self, ctx: Context):
        return ctx.prefix == self.prefix

    @property
    def display_emoji(self) -> str:
        return '💎'

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.has_any_role(*all_roles)
    async def cr(self, ctx: Context):
        """Base command for all the cr commands."""

        await ctx.send_help('cr')

    @cr.command(name='create')
    @commands.has_any_role(*all_roles)
    async def cr_create(self, ctx: Context):
        """Create your custom role."""

        guild = self.bot.get_guild(750160850077089853)
        user = ctx.author
        channel = ctx.message.channel
        usercheck = ctx.author.id

        data: CustomRole = await CustomRole.find_one({"_id": user.id})

        def check(message):
            return message.author.id == usercheck and message.channel.id == channel.id

        if data:
            return await ctx.send("You already have a custom role.")

        else:
            await channel.send("What do you want your custom role to be named as?\n\n*To cancel type `!cancel`*")

            try:
                while True:
                    crname = await self.bot.wait_for('message', timeout=50, check=check)
                    if crname.content.lower() in nono_list:
                        await ctx.send("You tried, but no, lol!")

                    elif len(crname.content.lower()) >= 20:
                        await ctx.send("The name of the custom role cannot be longer than `20` characters.")

                    elif crname.content.lower() == "!cancel":
                        await ctx.send("Cancelled. %s" % (ctx.author.mention))
                        return

                    else:
                        break

            except asyncio.TimeoutError:
                await ctx.send("Ran out of time.")
                return

            else:
                await ctx.send("What color do u want it to have, please give the hex code.\nExample: `#ffffff`")

                try:
                    while True:
                        crcolor = await self.bot.wait_for('message', timeout=50, check=check)
                        crcolor = crcolor.content.lower()
                        if crcolor == '!cancel':
                            await ctx.send("Cancelled. %s" % (ctx.author.mention))
                            return
                        if "#" in crcolor:
                            crcolor = crcolor.replace("#", "")
                            crcolor = f"0x{crcolor}"
                            try:
                                _ = disnake.Color(int(crcolor, 16))
                                break
                            except Exception:
                                await ctx.send("Invalid hex colour.")
                                pass
                        else:
                            await ctx.send("Invalid hex colour.")

                except asyncio.TimeoutError:
                    await ctx.send("Ran out of time.")
                    return

                else:
                    for role in guild.roles:
                        if crname.content in role.name:
                            await ctx.send("A role with that name already exists!")
                            return

                    newcr = await guild.create_role(name=crname.content, color=disnake.Color(int(crcolor, 16)))

                    await ctx.author.add_roles(newcr)

                    await CustomRole(
                        id=user.id,
                        name=crname.content,
                        role_id=newcr.id,
                        shares=0,
                        created_at=datetime.datetime.utcnow()
                    ).commit()

                    positions = {
                        newcr: 129
                    }
                    await guild.edit_role_positions(positions=positions)

                    await ctx.send("The role has been created and now you have it!")

    @cr.group(invoke_without_command=True, case_insensitive=True, name='edit')
    @commands.has_any_role(*all_roles)
    async def cr_edit(self, ctx: Context):
        """Invokes `!help cr edit`."""

        await ctx.send_help('cr edit')

    @cr_edit.command()
    async def color(self, ctx: Context, new_color: str = None):
        """Edit the colour of your custom role."""

        user = ctx.author
        guild = self.bot.get_guild(750160850077089853)

        data: CustomRole = await CustomRole.find_one({"_id": user.id})

        if not data:
            await ctx.send("You must have a custom role to edit! Type: `!cr create` to create your custom role.")
            return

        role = guild.get_role(data.role_id)
        em = disnake.Embed(title="Custom Role Edited")

        if new_color is None:
            await ctx.send("You must provide the new color!")
            return

        else:
            if new_color.startswith("#"):
                new_color = new_color.replace("#", "")
                new_color = f"0x{new_color}"
            else:
                await ctx.send("Invalid Color Hex!\nExample: `#ffffff`")
                return

            try:
                await role.edit(color=disnake.Color(int(new_color, 16)))
                em.add_field(name="New Color", value=f"`#{new_color[2:]}`")
                em.color = role.color
                await ctx.send(embed=em)

            except ValueError:
                await ctx.send("Invalid Color Hex!\nExample: `#ffffff`")

    @cr_edit.command()
    async def name(self, ctx: Context, *, new_name: str = None):
        """Edit the name of your custom role."""

        user = ctx.author
        guild = self.bot.get_guild(750160850077089853)

        data: CustomRole = await CustomRole.find_one({"_id": user.id})

        if not data:
            await ctx.send("You must have a custom role to edit! Type: `!cr create` to create your custom role.")
            return

        role = guild.get_role(data.role_id)
        em = disnake.Embed(title="Custom Role Edited")

        if new_name is None:
            await ctx.send("You must provide the new name!")
            return

        elif new_name.lower() in nono_list:
            await ctx.send("You tried, but no, lol!")
            return

        else:
            data.name = new_name
            await data.commit()
            await role.edit(name=new_name)
            em.add_field(name="New Name", value=f"`{new_name}`")
            em.color = role.color
            await ctx.send(embed=em)

    @cr.command()
    @commands.has_any_role(*all_roles)
    async def share(self, ctx: Context, member: disnake.Member = None):
        """Share your custom role with a member."""

        if member is None:
            return await ctx.send("You must specify the user that you're sharing the role to!")
        user = ctx.author
        guild = self.bot.get_guild(750160850077089853)

        data: CustomRole = await CustomRole.find_one({"_id": user.id})

        if not data:
            return await ctx.send("You do not have a custom role to share!")

        role = guild.get_role(data.role_id)
        if role in member.roles:
            return await ctx.send("You already shared your custom role with that user!")

        view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.", member)
        view.message = msg = await ctx.send(
            f"{member.mention} Do you accept the role {role.mention} from {user.mention}?\n\n**Note:** Any changes made to the "
            "role by {user.mention} would apply to everyone holding the role.",
            view=view
        )
        await view.wait()
        if view.response is True:
            data.shares += 1
            await data.commit()
            await member.add_roles(role)
            em = disnake.Embed(color=user.color, title=f"{member} has accepted your role")
            em.set_image(url="https://blog.hubspot.com/hubfs/giphy_1-1.gif")
            await msg.edit(view=view)
            return await ctx.send(ctx.author.mention, embed=em)

        elif view.response is False:
            await msg.edit(view=view)
            return await ctx.send(f"**{member}** has denied your role {ctx.author.mention}")

    @cr.command(name='info')
    async def cr_info(self, ctx: Context, *, role_id: int = None):
        """Get some data about a custom role, it doesn't have to be yours, but the <role_id> parameter must be a integer (the role's id)."""

        if role_id is None:
            data: CustomRole = await CustomRole.find_one({'_id': ctx.author.id})
            if not data:
                return await ctx.send("You do not have a custom role.")
        else:
            data = await CustomRole.find_one({'role_id': role_id})
            if not data:
                return await ctx.send("That is not a custom role.")

        index = 0
        role = ctx.guild.get_role(role_id)
        for m in ctx.guild.members:
            if role in m.roles:
                index += 1
        role_owner = ctx.guild.get_member(data.id)

        def format_date(dt):
            if dt is None:
                return 'N/A'
            return f'{dt:%Y-%m-%d %H:%M} ({time.human_timedelta(dt, accuracy=3)})'

        em = disnake.Embed(color=role_owner.color, title=f"Role Info About `{role.name}`")
        em.add_field(name="Custom Role Owner", value=role_owner, inline=False)
        em.add_field(name="Hex Code", value=role.color, inline=False)
        em.add_field(name="People That Have The Role", value=index, inline=False)
        em.add_field(name="Total Role Shares", value=data.shares, inline=False)
        em.add_field(name="Created At", value=format_date(data.created_at), inline=False)

        await ctx.send(embed=em)

    @cr.command()
    async def unrole(self, ctx: Context, *, role_id: int = None):
        """Remove a custom role from your roles, the <role_id> parameter must be a integer (role's id)."""

        if role_id is None:
            return await ctx.send("You must give the role ID, to get it use `!role-id <role_name>`")
        guild = self.bot.get_guild(750160850077089853)
        role = guild.get_role(role_id)

        data: CustomRole = await CustomRole.find_one({"name": role.name})
        if not data:
            return await ctx.send("That is not a custom role!")
        try:
            if ctx.author.id == data.id:
                await ctx.send("You cannot remove that custom role because you're the owner of it! To remove it please type: `!cr delete`")
                return

            else:
                await ctx.author.remove_roles(role)
                await ctx.send(f"Removed the role {role.mention} from your profile.")

        except AttributeError:
            await ctx.send("That is not a valid ID! Type: `!role-id <role_name>` to get the role's ID you want to remove from your profile.")
            return

    @cr.command()
    async def clean(self, ctx: Context):
        """Remove all of your custom roles from your roles ***except*** your own custom role."""

        all_cr = []
        data: list[CustomRole] = await CustomRole.find().to_list(100000)
        guild = self.bot.get_guild(750160850077089853)
        for result in data:
            if ctx.author.id != result.id:
                all_cr.append(result.role_id)

        try:
            member_roles = []
            for x in ctx.author.roles:
                if x.id not in all_cr:
                    member_roles.append(x.id)

            member_roles = set(member_roles)

            roles = []
            for role_id in member_roles:
                role = guild.get_role(role_id)
                roles.append(role)

        except Exception:
            pass

        await ctx.author.edit(roles=roles)
        await ctx.send("Succesfully cleaned all the cr's on your profile.")

    @cr.command(name='delete')
    @commands.has_any_role(*all_roles)
    async def cr_delete(self, ctx: Context):
        """Delete your custom role."""

        user = ctx.author
        guild = self.bot.get_guild(750160850077089853)

        data: CustomRole = await CustomRole.find_one({"_id": user.id})

        if not data:
            return await ctx.send("You do not have a custom role! Type: `!cr create` to create your role!")

        role = guild.get_role(data.role_id)
        view = self.bot.confirm_view(ctx, f"{ctx.author.mention} Did not react in time.")
        view.message = msg = await ctx.send(f"Are you sure you want to delete your custom role ({role.mention})?", view=view)
        await view.wait()
        if view.response is False:
            e = "Your custom role has not been deleted. %s" % (ctx.author.mention)
            return await msg.edit(content=e, view=view)

        elif view.response is True:
            await role.delete()
            await data.delete()
            e = "Succesfully deleted your custom role! {}".format(ctx.author.mention)
            return await msg.edit(content=e, view=view)

    @commands.command(name='role-id')
    async def _role_id(self, ctx: Context, *, role_name: str = None):
        """Get the role id from the name of a role."""

        if role_name is None:
            await ctx.send("You must give the role name that you want the ID for!")
            return
        guild = self.bot.get_guild(750160850077089853)
        role = disnake.utils.get(guild.roles, name=role_name)

        try:
            await ctx.send(f"**{role.name}**'s role ID **-->** `{role.id}`")
        except AttributeError:
            await ctx.send("That is not a valid role!")

    @cr_delete.error
    async def delete_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You do not have any custom role! What are you trying to delete???\nType `!cr create` to create your custom role!")
        else:
            await self.bot.reraise(ctx, error)

    @unrole.error
    async def unrole_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("That is not a role id! To get the role's ID please type `!role-id <role_name>`")
        else:
            await self.bot.reraise(ctx, error)

    @cr_info.error
    async def info_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("That is not a role id! To get the role's ID please type `!role-id <role_name>`")
        else:
            await self.bot.reraise(ctx, error)

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.MissingAnyRole):
            await ctx.send("You must be at least `level 40+` in order to use this command! %s" % (ctx.author.mention))
        else:
            if hasattr(ctx.command, 'on_error'):
                return
            await self.bot.reraise(ctx, error)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        guild = self.bot.get_guild(750160850077089853)
        data: CustomRole = await CustomRole.find_one({"_id": member.id})
        if data:
            role = guild.get_role(data.role_id)
            await role.delete()
            await data.delete()


def setup(bot):
    bot.add_cog(CustomRoles(bot))
