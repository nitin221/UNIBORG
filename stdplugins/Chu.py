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

    animation_interval = 3
    

    animation_ttl = range(0, 103)

    input_str = event.pattern_match.group(1)

    if input_str == "chu":

        await event.edit(input_str)

        animation_chars = [

             "\n ;T",
            "\n ;Th",
            "\n ;Thi",
            "\n ;This",
            "\n ;Is",
            "\n ;A",
            "\n ;C",
            "\n ;ch",
            "\n ;Chu",
            "\n ;Chut",
            "\n ;Chutia",
            "\n ;Chutiyaaaa",
            "\n ;😂😂😂😂😂😂",
            "\n ;💨💨💨💨💦👓👣👅👀💣💢💤💥💬💍",
            "\n ;whooooo",
            "\n ;iiiiiiissssssss",
            "\n ;wwwwwww",
            
   
            
            
            

            "\n ;waiiiiiiiiiiiiiitiiiiing",
            "\n ;tooooooo seeeeeeee this message",
            "\n ;Jaaaaaaaaaa naaa chuuuutiyeeee kuchhhhhhhh kaaaam nahiiiiii  hai  kya😂😂",

        ]

        for i in animation_ttl:


            await event.edit(animation_chars[i % 103])
