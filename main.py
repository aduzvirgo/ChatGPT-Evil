import os
from config import *
from callback import *
from pyrogram import Client, filters, enums
from pyroaddon import listen
from pyrogram.errors import *
import requests
import json
from pyrogram.types import *
from time import sleep
from buttons import
import random, string

cli = Client("gpt",
             api_id=28153993,
             api_hash="976fd7cc4958ad84181a53b41919564b",
             bot_token="6730481569:AAFSu_wX_qp97wgLBaElV2FKQC8X9EqOa8A"
             )
headers = {
    'authority': 'query me',
    'Authorization': APIKEY,
    'content-type': 'application/json'
}

@cli.on_message(filters.private & filters.command(['start']))
async def start(_, m):
    usr_name = m.from_user.first_name
    await m.reply('**Dark Gpt Api Demo Bot  \ntype /HELP for help**', reply_markup=ALLBOTS)

@cli.on_message(filters.private & filters.command(['language']))
async def language_(_, m):
    await m.reply("select language", reply_markup=InlineKeyboardMarkup(Languages()[0]))

@cli.on_message(filters.private & filters.command(['tone']))
async def tone_(_, m):
    await m.reply("**select your preferred Tone **", reply_markup=APPROACH_BUTTON)

@cli.on_message(filters.private & filters.command(['mysetting']))
async def settings_(_, m):
    usr_id = m.from_user.id
    _, s, j, _ = user_setting(usr_id)
    await m.reply(f"**Approach: {s}\nLanguage: {j}**")

@cli.on_message(filters.private & filters.command(['help']))
async def help_message(_, m):
    await m.reply(f"""**type /help for this menu
    type /mysetting to see your current setting 
    type /language to set language
    type /tone to set approach/tone 
    type /apikey to get your own http Api key
    
    or directly ask a question
    
    to upgrade your Api for commercial use, contact us @ethioaiofficial or DM @aduzvirgo**""")

@cli.on_message(filters.private & filters.text)
async def handlsev(c, m):
    resp = apiprocess(m.from_user.id, "generator", "all", m.text, "i want an exact answer")
    e = resp[:4096]  # Truncate the response if it's too long
    await m.reply(e.replace('##', '•'), quote=True, parse_mode=enums.ParseMode.MARKDOWN, protect_content=False)
    f = resp.replace(e, "")
    try:
        await m.reply(f.replace('##', '•'), quote=True, parse_mode=enums.ParseMode.MARKDOWN, protect_content=False)
    except:
        pass
    fl = resp.split('```')[1]
    ext = fl.split('\n')
    fl = fl.replace(ext[0], "", 1)
    with open(f'code.{ext[0]}', 'w') as f:
        f.write(fl)
    await m.reply_document(f'code.{ext[0]}', caption='**Exercise Left for you😈**\n1 save the code \n2 run it in your best IDE ')
    os.remove(f'code.{ext[0]')

def apiprocess(user_id, task, lang, prompt, code='none'):
    _, language, tone, __ = user_setting(user_id)
    json_data = {
        'task': task,
        'program': lang,
        "prompt": prompt,
        "code": code,
        'further_description1': 'none',
        'further_description2': 'none',
        'language': language,
        'approach': tone
    }
    e = requests.post('https://darkgpt.hop.sh/neurals/api', headers=headers, json=json_data)
    rs = json.loads(e.text)
    return rs["message"]

cli.run()
