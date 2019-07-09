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

    animation_interval = 2
    

    animation_ttl = range(0, 10)

    input_str = event.pattern_match.group(1)

    if input_str == "chu":

        await event.edit(input_str)

        animation_chars = [

            ";T",
            ";Th",
            ";Thi",
            ";This",
            ";Is",
            ";A",
            ";C",
            ";ch",
            ";Chu",
            ";Chut",
            ";Chutia",
            ";Chutiyaaaa",
            ";😂😂😂😂😂😂",
            ";💨💨💨💨💦👓👣👅👀💣💢💤💥💬💍",
            ";whooooo",
            ";iiiiiiissssssss",
            ";wwwwwww",
            
   
            
            
            

            ";waiiiiiiiiiiiiiitiiiiing",
            ";tooooooo seeeeeeee this message",
            ";Jaaaaaaaaaa naaa chuuuutiyeeee kuchhhhhhhh kaaaam nahiiiiii  hai  kya😂😂    ;",

        ]

        for i in animation_ttl:


            await event.edit(animation_chars[i % 10])
