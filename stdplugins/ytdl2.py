
import aiohttp
from telethon import events
from bs4 import BeautifulSoup
from uniborg.util import admin_cmd

borg.on(admin_cmd(pattern="yt_video (.*)"))
async def search_yt(event):
    url_base = "https://www.youtube.com/results"
    url_yt = "https://www.youtube.com"
    async with aiohttp.ClientSession() as session:
        r = await session.get(url_base, params=dict(q=query))
        page = await r.text()
    soup = BeautifulSoup(page, "html.parser")
    id_url = None
    list_videos = []
    for link in soup.find_all('a'):
        url = link.get('href')
        title = link.get('title')
        if url.startswith("/watch") and (id_url != url) and (title is not None):
            id_url = url
            dic = {'title': title, 'url': url_yt + url}
            list_videos.append(dic)
        else:
            pass
    return list_videos
