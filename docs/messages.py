import asyncio
import re
from functools import partial
from io import BytesIO
from typing import Callable, List, Optional, Sequence, Union
import random

import disnake
from disnake import ApplicationCommandInteraction
from utils.context import Context

from .utils import create_task

from main import ViHillCorner

MODERATION_ROLES = (
    754676705741766757,
    788845429797814282,
    859060865813839892
)

NEGATIVE_REPLIES = (
    "Noooooo!!",
    "Nope.",
    "I'm sorry Dave, I'm afraid I can't do that.",
    "I don't think so.",
    "Not gonna happen.",
    "Out of the question.",
    "Huh? No.",
    "Nah.",
    "Naw.",
    "Not likely.",
    "No way, José.",
    "Not in a million years.",
    "Fat chance.",
    "Certainly not.",
    "NEGATORY.",
    "Nuh-uh.",
    "Not in my house!"
)


def reaction_check(
    bot: ViHillCorner,
    reaction: disnake.Reaction,
    user: disnake.abc.User,
    *,
    message_id: int,
    allowed_emoji: Sequence[str],
    allowed_users: Sequence[int],
    allow_mods: bool = True,
) -> bool:
    """
    Check if a reaction's emoji and author are allowed and the message is `message_id`.
    If the user is not allowed, remove the reaction. Ignore reactions made by the bot.
    If `allow_mods` is True, allow users with moderator roles even if they're not in `allowed_users`.
    """
    right_reaction = (
        user != bot.user and
        reaction.message.id == message_id and
        str(reaction.emoji) in allowed_emoji
    )
    if not right_reaction:
        return False

    is_moderator = (
        allow_mods and
        any(role.id in MODERATION_ROLES for role in getattr(user, "roles", []))
    )

    if user.id in allowed_users or is_moderator:
        return True
    else:
        create_task(
            reaction.message.remove_reaction(reaction.emoji, user),
            suppressed_exceptions=(disnake.HTTPException,),
            name=f"remove_reaction-{reaction}-{reaction.message.id}-{user}"
        )
        return False


async def wait_for_deletion(
    bot: ViHillCorner,
    message: disnake.Message,
    user_ids: Sequence[int],
    deletion_emojis: Sequence[str] = ('🗑️',),
    timeout: float = 60 * 5,
    attach_emojis: bool = True,
    allow_mods: bool = True
) -> None:
    """
    Wait for any of `user_ids` to react with one of the `deletion_emojis` within `timeout` seconds to delete `message`.
    If `timeout` expires then reactions are cleared to indicate the option to delete has expired.
    An `attach_emojis` bool may be specified to determine whether to attach the given
    `deletion_emojis` to the message in the given `context`.
    An `allow_mods` bool may also be specified to allow anyone with a role in `MODERATION_ROLES` to delete
    the message.
    """
    if message.guild is None:
        raise ValueError("Message must be sent on a guild")

    if attach_emojis:
        for emoji in deletion_emojis:
            try:
                await message.add_reaction(emoji)
            except disnake.NotFound:
                return

    check = partial(
        reaction_check,
        bot,
        message_id=message.id,
        allowed_emoji=deletion_emojis,
        allowed_users=user_ids,
        allow_mods=allow_mods,
    )

    try:
        try:
            await bot.wait_for('reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            await message.clear_reactions()
        else:
            await message.delete()
    except disnake.NotFound:
        pass


async def send_attachments(
    message: disnake.Message,
    destination: Union[disnake.TextChannel, disnake.Webhook],
    link_large: bool = True,
    use_cached: bool = False,
    **kwargs
) -> List[str]:
    """
    Re-upload the message's attachments to the destination and return a list of their new URLs.
    Each attachment is sent as a separate message to more easily comply with the request/file size
    limit. If link_large is True, attachments which are too large are instead grouped into a single
    embed which links to them. Extra kwargs will be passed to send() when sending the attachment.
    """
    webhook_send_kwargs = {
        'username': message.author.display_name,
        'avatar_url': message.author.avatar_url,
    }
    webhook_send_kwargs.update(kwargs)
    webhook_send_kwargs['username'] = sub_clyde(webhook_send_kwargs['username'])

    large = []
    urls = []
    for attachment in message.attachments:
        try:
            # Allow 512 bytes of leeway for the rest of the request.
            # This should avoid most files that are too large,
            # but some may get through hence the try-catch.
            if attachment.size <= destination.guild.filesize_limit - 512:
                with BytesIO() as file:
                    await attachment.save(file, use_cached=use_cached)
                    attachment_file = disnake.File(file, filename=attachment.filename)

                    if isinstance(destination, disnake.TextChannel):
                        msg = await destination.send(file=attachment_file, **kwargs)
                        urls.append(msg.attachments[0].url)
                    else:
                        await destination.send(file=attachment_file, **webhook_send_kwargs)
            elif link_large:
                large.append(attachment)
        except disnake.HTTPException as e:
            if link_large and e.status == 413:
                large.append(attachment)

    if link_large and large:
        desc = "\n".join(f"[{attachment.filename}]({attachment.url})" for attachment in large)
        embed = disnake.Embed(description=desc)
        embed.set_footer(text="Attachments exceed upload size limit.")

        if isinstance(destination, disnake.TextChannel):
            await destination.send(embed=embed, **kwargs)
        else:
            await destination.send(embed=embed, **webhook_send_kwargs)

    return urls


async def count_unique_users_reaction(
    message: disnake.Message,
    reaction_predicate: Callable[[disnake.Reaction], bool] = lambda _: True,
    user_predicate: Callable[[disnake.User], bool] = lambda _: True,
    count_bots: bool = True
) -> int:
    """
    Count the amount of unique users who reacted to the message.
    A reaction_predicate function can be passed to check if this reaction should be counted,
    another user_predicate to check if the user should also be counted along with a count_bot flag.
    """
    unique_users = set()

    for reaction in message.reactions:
        if reaction_predicate(reaction):
            async for user in reaction.users():
                if (count_bots or not user.bot) and user_predicate(user):
                    unique_users.add(user.id)

    return len(unique_users)


async def pin_no_system_message(message: disnake.Message) -> bool:
    """Pin the given message, wait a couple of seconds and try to delete the system message."""
    await message.pin()

    # Make sure that we give it enough time to deliver the message
    await asyncio.sleep(2)
    # Search for the system message in the last 10 messages
    async for historical_message in message.channel.history(limit=10):
        if historical_message.type == disnake.MessageType.pins_add:
            await historical_message.delete()
            return True

    return False


def sub_clyde(username: Optional[str]) -> Optional[str]:
    """
    Replace "e"/"E" in any "clyde" in `username` with a Cyrillic "е"/"E" and return the new string.
    Discord disallows "clyde" anywhere in the username for webhooks. It will return a 400.
    Return None only if `username` is None.
    """
    def replace_e(match: re.Match) -> str:
        char = "е" if match[2] == "e" else "Е"
        return match[1] + char

    if username:
        return re.sub(r"(clyd)(e)", replace_e, username, flags=re.I)
    else:
        return username  # Empty string or None


async def send_denial(ctx: Union[Context, ApplicationCommandInteraction], reason: str, *, view: disnake.ui.View = None) -> disnake.Message:
    """Send an embed denying the user with the given reason."""
    embed = disnake.Embed()
    embed.colour = disnake.Colour.red()
    embed.title = random.choice(NEGATIVE_REPLIES)
    embed.description = reason

    if isinstance(ctx, ApplicationCommandInteraction):
        return await ctx.followup.send(embed=embed, view=view, ephemeral=True)
    return await ctx.send(embed=embed, view=view)


def format_user(user: disnake.abc.User) -> str:
    """Return a string for `user` which has their mention and ID."""
    return f"{user.mention} (`{user.id}`)"
