#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon import events
from uniborg.util import admin_cmd



@borg.on(admin_cmd(pattern="sgif"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    u_id = reply_message.from_id
    #
    chat = await event.client.get_entity("@SangMataInfo_bot")
    #
    await event.edit("```processing```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {u_id}")
            msg2 = await conv.get_response()
            # logger.info(msg2)
            await event.client.send_read_acknowledge(
                entity=chat.id,
                message=msg2,
                clear_mentions=True
            )
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=chat.id)
            )
            msg2 = await response
            # logger.info(msg2.stringify())
            await event.edit(msg2.message.text)
        except Exception as e:
            await event.reply(f"`RIP `: {str(e)}")
            return

