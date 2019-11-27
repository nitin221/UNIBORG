from asyncio import sleep
from os import remove
from datetime import datetime

from telethon import errors

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)

from uniborg.util import admin_cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`I am not an admin!`"
NO_PERM = "`I don't have sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe coz I'm not an admin,`" \
                "`or don't have the desired rights.`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

KICK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True
)

MUTE_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=True
)

UNMUTE_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=False
)
# ================================================


@borg.on(admin_cmd(pattern="sgp", outgoing=True))
async def set_group_photo(gpic):
    """ For .setgpic command, changes the picture of a group """
    if not gpic.is_group:
        await gpic.edit("`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@borg.on(admin_cmd(pattern="ban(?: |$)(.*)", outgoing=True))
async def ban(bon):
    """ For .ban command, bans the replied/tagged person """
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Whacking the pest!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BadRequestError:
        await bon.edit(NO_PERM)
        return        
    
    if reason:
        await bon.edit(f"Alright! [{user.first_name}](tg://user?id={user.id}) has been banned !!\n**Reason:-** `{reason}`")
    else:
        await bon.edit(f"It’s good to ban ppl actually.\nWell done [{user.first_name}](tg://user?id={user.id}) 😹 u got banned😂😅.")
    # Announce to the logging group if we have banned the person
    # successfully!
    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await bon.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID, "#BAN\n"
                f"**USER:-** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:-** `{user.id}`\n"
                f"**Chat:-** {bon.chat.title}\n"
                f"**Chat ID:-** `{bon.chat_id}`\n"
                f"**Reason:-** `{reason}`")


@borg.on(admin_cmd(pattern="unban(?: |$)(.*)", outgoing=True))
async def nothanos(unbon):
    """ For .unban command, unbans the replied/tagged person """
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # If everything goes well...
    await unbon.edit("`Reversing The Snap....`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit(f"Snap reversed.\n[{user.first_name}](tg://user?id={user.id}) has been resurrected!")

        if Config.PRIVATE_GROUP_BOT_API_ID is not None:
            await unbon.client.send_message(
                Config.PRIVATE_GROUP_BOT_API_ID, "#UNBAN\n"
                f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:-** `{user.id}`\n"
                f"**Chat:-** {unbon.chat.title}\n"
                f"**Chat ID:-** `{unbon.chat_id}`")
    except UserIdInvalidError:
        await unbon.edit("`Uh oh my unban logic broke!`")


@borg.on(admin_cmd(pattern="mute(?: |$)(.*)", outgoing=True))
async def spider(spdr):
    """
    This function is basically muting peeps
    """
    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            "`Hands too short, can't duct tape myself...\n(ヘ･_･)ヘ┳━┳`")
        return

    # If everything goes well, do announcing and mute
    await spdr.edit("`Gets a tape!`")
    
    try:
        await spdr.client(
            EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
        if reason:
            await spdr.edit(f"Shush! [{user.first_name}](tg://user?id={user.id})Stop Talking!!!!\n**Reason:-** `{reason}`")
        else:
            await spdr.edit(f"Shush! [{user.first_name}](tg://user?id={user.id}) Stop Your Dumb Talk Now..")

        # Announce to logging group
        if Config.PRIVATE_GROUP_BOT_API_ID is not None:
            await spdr.client.send_message(
                Config.PRIVATE_GROUP_BOT_API_ID, "#MUTE\n"
                f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:-** `{user.id}`\n"
                f"**Chat:-** {spdr.chat.title}\n"
                f"**Chat ID:-** `{spdr.chat_id}`\n"
                f"**Reason:-** `{reason}`")    
    except UserIdInvalidError:
        return  await spdr.edit("`Uh oh my mute logic broke!`")


@borg.on(admin_cmd(pattern="unmute(?: |$)(.*)", outgoing=True))
async def unmoot(unmot):
    """ For .unmute command, unmute the replied/tagged person """
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # If admin or creator, inform the user and start unmuting
    await unmot.edit('```Unmuting...```')
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(f"[{user.first_name}](tg://user?id={user.id}) can start talking again!")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")
            return

        if Config.PRIVATE_GROUP_BOT_API_ID is not None:
            await unmot.client.send_message(
                Config.PRIVATE_GROUP_BOT_API_ID, "#UNMUTE\n"
                f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:-** `{user.id}`\n"
                f"**Chat:-** {unmot.chat.title}\n"
                f"**Chat ID:-** `{unmot.chat_id}`")


@borg.on(admin_cmd(pattern="kick(?: |$)(.*)", outgoing=True))
async def kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Couldn't fetch user.`")
        return

    await usr.edit("`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"`RIP` [{user.first_name}](tg://user?id={user.id})`!`\n**Reason:-** `{reason}`")
    else:
        await usr.edit(
            f"`RIP` [{user.first_name}](tg://user?id={user.id})`Untill We Meet Again!`")

    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await usr.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID, "#KICK\n"
                f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
                f"**User ID:-** `{user.id}`\n"
                f"**Chat:-** {usr.chat.title}\n"
                f"**ChatID:-** `{usr.chat_id}`\n"
                f"**Reason:-** `{reason}`")


@borg.on(admin_cmd(pattern="promote(?: |$)(.*)", outgoing=True))
async def promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "admeme"  # Just in case.
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Promoted Successfully!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await promt.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID,
            "#PROMOTE\n"
            f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
            f"**User ID:-** `{user.id}`\n"
            f"**Chat:-** {promt.chat.title}\n"
            f"**Chat ID:-** `{promt.chat_id}`\n"
            f"**Rank:-** `{rank}`")


@borg.on(admin_cmd(pattern="prankpromote(?: |$)(.*)", outgoing=True))
async def prankpromote(promo):
    """ For . Prankpromote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promo.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promo.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(post_messages=True)

    await promo.edit("`Promoting...`")
    user, rank = await get_user_from_event(promo)
    if not rank:
        rank = "prank"  # Just in case.
    if user:
        pass
    else:
        return

    # Try to Prank promote if current user is admin or creator
    try:
        await promo.client(
            EditAdminRequest(promo.chat_id, user.id, new_rights, rank))
        await promo.edit("`Prank Promoted Successfully!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promo.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await promo.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID,
            "#PRANKPROMOTE\n"
            f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
            f"**User ID:-** `{user.id}`\n"
            f"**Chat:-** {promo.chat.title}\n"
            f"**Chat ID:-** `{promo.chat_id}`\n"
            f"**Rank:-** `{rank}`")


@borg.on(admin_cmd(pattern="demote(?: |$)(.*)", outgoing=True))
async def demote(dmod):
    """ For .demote command, demotes the replied/tagged person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Demoting...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Edit Admin Permission
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Well You Don't Deserve This Post!`")

    # Announce to the logging group if we have demoted successfully
    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await dmod.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID,
            "#DEMOTE\n"
            f"**User:-** [{user.first_name}](tg://user?id={user.id})\n"
            f"**User ID:-** `{user.id}`\n"
            f"**Chat:-** {dmod.chat.title}\n"
            f"**Chat ID:-** `{dmod.chat_id}`")


@borg.on(admin_cmd(pattern="pin(?: |$)(.*)", outgoing=True))
async def pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Reply to a message to pin it.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Pinned Successfully!`")

    user = await get_user_from_id(msg.from_id, msg)

    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await msg.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID, "#PIN\n"
                f"**Admin:-** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat:-** {msg.chat.title}\n"
                f"**Chat ID:-** `{msg.chat_id}`\n"
                f"**Loud:-** {not is_silent}")


@borg.on(admin_cmd(pattern="delusers(?: |$)(.*)", outgoing=True))
async def rm_deletedacc(show):
    """ For .delusers command, list all the ghost/deleted accounts in a chat. """
    if not show.is_group:
        await show.edit("`I don't think this is a group.`")
        return
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "`No deleted accounts found, Group is cleaned as Hell`"

    if con != "clean":
        await show.edit("`Searching for zombie accounts...`")
        async for user in show.client.iter_participants(show.chat_id):
                                                        
            if user.deleted:
                del_u += 1
                await sleep(3)
        if del_u > 0:
            del_status = f"Found **{del_u}** deleted account(s) in this group,\
            \nclean them by using .delusers clean"

        await show.edit(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("`I am not an admin here!`")
        return

    await show.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if Config.PRIVATE_GROUP_BOT_API_ID is not None:
        await show.client.send_message(
            Config.PRIVATE_GROUP_BOT_API_ID, "#CLEANUP\n"
            f"Cleaned **{del_u}** deleted account(s) !!\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)")


@borg.on(admin_cmd(pattern="users(?: |$)(.*)", outgoing=True))
async def get_users(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = 'Users in {}: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='Users in {}'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj
