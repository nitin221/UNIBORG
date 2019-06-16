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

    if input_str == "uld":

        await event.edit(input_str)

        animation_chars = [
        
            "`Uploading File To Telegram Secure Server...`",
            "`File Arranged.`",
            "`Uploading on Telegram... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading on Telegram... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading on Telegram... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Uploading on Telegram... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading on Telegram... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading on Telegram... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Uploading on Telegram... 84%\n█████████████████████▒▒▒▒ `",
            "`Uploading on Telegram... 100%\n█████████████████████████ `",
            "`File Successfully Uploaded on Telegram...
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])
