import os
from telethon import events
from uniborg.util import admin_cmd

from telethon.tl import functions







@borg.on(admin_cmd(pattern="usr ?(.*)"))
async def update_username(username):

    newusername = username.pattern_match.group(1)
    try:
        await borg(functions.account.UpdateUsernameRequest(  # pylint:disable=E0602
            about=username
        ))
        await username.edit("Succesfully changed my Username")
    except UsernameOccupiedError:
        await event.edit("This Username is Already Reserved")

