import asyncio
import random
from uniborg import util
from telethon import events


@borg.on(util.admin_cmd(r"x"))
async def payf(e):
    paytext = e.text[3:]
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*8, paytext*8, paytext*2, paytext*2, paytext*2, paytext*6, paytext*6, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2)
    await e.edit(pay)