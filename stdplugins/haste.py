
from telethon import events
import os
import requests
import json
from uniborg.util import admin_cmd


BASE = "https://haste.thevillage.chat"


@borg.on(admin_cmd(pattern="haste ?(.*)"))
def haste(client, message):
    reply = message.reply_to_message

    if reply.text is None:
        return

    message.delete()

    result = requests.post(
        "{}/documents".format(BASE),
        data=reply.text.encode("UTF-8")
    ).json()

    message.reply(
        "{}/{}.py".format(BASE, result["key"]),
        reply_to_message_id=reply.message_id
    )
