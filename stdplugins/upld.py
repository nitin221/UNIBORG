"""Emoji
Available Commands:
.emoji shrug
.emoji apple
.emoji :/
.emoji -_-"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2.5

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "upld":

        await event.edit(input_str)

        animation_chars = [
        
            "`Uploading File To Telegram...`",
            "`File Path Selected.`",
            "`Uploading... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Uploading... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uplosding... 84%\n█████████████████████▒▒▒▒ `",
            "`Uploading... 100%\n█████████████████████████ `",
            "`File Successfully Uploaded on Telegran`"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])
