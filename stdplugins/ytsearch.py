from telethon import events



import os



import requests



import json



from uniborg.util import admin_cmd
@borg.on(admin_cmd(pattern="yt (.*)"))



async def _(event):



    if event.fwd_from:



        return



    input_str = event.pattern_match.group(1)



    sample_url = "https://da.gd/s?url=https://www.youtube.com/results?search_query={}".format(input_str.replace(" ","+"))



    response_api = requests.get(sample_url).text



    if response_api:



        await event.edit("Let me [UThoob](https://youtube.com) that for you:\n\n\n\n[{}]({})\n\n\nThank me later🙃 ".format(input_str,response_api.rstrip()))



    else:



        await event.edit("Something went wrong. Please try again later.")