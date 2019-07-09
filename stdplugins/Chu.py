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

            ";T..",
            ";Th..",
            ";Thi...",
            ";This....",
            ";Is.....",
            ";a...",
            ";C....",
            ";ch.....",
            ";Chu.......",
            ";Chut............",
            ";Chuti..........",
            ";Chutiyaaaa.............."'
            ";😂😂😂😂😂😂..............."'
            ";😁😁😁😁😁😁😁........................"'
            ";whooooo.................."'
            ";iiiiiiissssssss........."'
            ";w.........hooooo..."'
            
            
            

            ";waiiiiiiiiiiiiiitiiiiing....",
            ";tooooooo_seeeeeeee_this_message.."'
            ";Jaaaaaaaaaa_naaa_chuuuutiyeeee_kuchhhhhhhh_kaaaam___nahiiiiii___hai___kya_😂😂___;"
        ]

        for i in animation_ttl:


            await event.edit(animation_chars[i % 203])
