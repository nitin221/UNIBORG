import os
from telethon import events
from uniborg.util import admin_cmd

from telethon.tl import functions

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import UpdateUsernameRequest




@borg.on(admin_cmd(pattern="usr ?(.*)"))
async def update_username(username):

    newusername = username.pattern_match.group(1)
    try:
        await borg(UpdateUsernameRequest(newusername))
        
        await username.edit("Succesfully changed my Username")
    except UsernameOccupiedError:
        await event.edit("This Username is Already Reserved")

        
