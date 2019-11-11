"""Get information about an user on GitHub
Syntax: .github USERNAME"""
from telethon import events
import requests
from uniborg.util import admin_cmd
import ParseMode


@borg.on(admin_cmd(pattern="git (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://api.github.com/users/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        html_url = b["html_url"]
        gh_type = b["type"]
        name = b["name"]
        company = b["company"]
        blog = b["blog"]
        location = b["location"]
        bio = b["bio"]
        created_at = b["created_at"]
        await borg.send_file(
            event.chat_id,
            caption="""Name: [{}]({})
Type: {}
Company: {}
Blog: {}
Location: {}
Bio: {}
Profile Created: {}""".format(name, html_url, gh_type, company, blog, location, bio, created_at),
            file=avatar_url,
            force_document=False,
            allow_cache=False,
            reply_to=event
        )
        await event.delete()
    else:
        await event.reply("`{}`: {}".format(input_str, r.text))

   
@borg.on(admin_cmd(pattern="repo (.*)", allow_sudo=True))
async def _(event):
    message = update.effective_message
    text = message.text[len('/repo '):]
    url = get(f'https://api.github.com/users/{text}/repos?per_page=40').json()
    reply_text = "*Repo*\n"
    for i in range(len(usr)):
        reply_text += f"[{usr[i]['name']}]({usr[i]['html_url']})\n"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
