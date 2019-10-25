"""
Say something interesting...
Syntax: .belo
    by @SpEcHlDe
Quotes credits: Being logical Channel
"""

from uniborg.util import admin_cmd
import asyncio
import random


@borg.on(admin_cmd(pattern=r"belo"))

async def _(event):
	await event.edit("Typing...")
	CHANNEL_USER_NAME = "https://t.me/BeingLogical"
	channel_entity = await event.client.get_entity(CHANNEL_USER_NAME)
	channel_messages = await event.client.get_messages(channel_entity)
	total_channel_messages = channel_messages.total
	x = random.randint(1, total_channel_messages)
	one_message = await event.client.get_messages(
		entity=channel_entity,
		limit=1,
		min_id=x
	)
	await asyncio.sleep(2)
	await event.edit(one_message[0].message)
