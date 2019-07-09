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

    animation_interval = 1
    

    animation_ttl = range(0, 203)

    input_str = event.pattern_match.group(1)

    if input_str == "chu":

        await event.edit(input_str)

        animation_chars = [

            ";T.._",
            ";Th.._",
            ";Thi..._",
            ";This...._",
            ";Is....._",
            ";a..._",
            ";C...._",
            ";ch....._",
            ";Chu......._",
            ";Chut............_",
            ";Chuti.........._",
            ";Chutiyaaaa.............._",
            ";😂😂😂😂😂😂..............._",
            ";💨💨💨💨💦👓👣👅👀💣💢💤💥💬💍",
            ";whooooo.................._"'
            ";iiiiiiissssssss........._"'
            ";w.........hooooo..._"'
            
            
            

            ";waiiiiiiiiiiiiiitiiiiing...._",
            ";tooooooo_seeeeeeee_this_message.._"'
            ";Jaaaaaaaaaa_naaa_chuuuutiyeeee_kuchhhhhhhh_kaaaam___nahiiiiii___hai___kya_😂😂___;"
        ]

        for i in animation_ttl:


            await event.edit(animation_chars[i % 203])
