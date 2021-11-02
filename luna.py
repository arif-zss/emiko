import re
import os
from asyncio import gather, get_event_loop, sleep
from asyncio import Lock
from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from random import choice
from messageing_data import sticker_list, INSULT_STRINGS
from kki import tkuki
is_config = os.path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

bot_id = int(bot_token.split(":")[0])
arq = None
buttons = [[InlineKeyboardButton("Join Us", url="t.me/anime_sigma"),
                    ]]

async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    kresp = tkuki(message.text)
    response = choice([response, kresp])
    await message.reply_text(response.replace("Luna","Emiko"))
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
         """Beautiful is better than ugly.
         Explicit is better than implicit.
         Simple is better than complex."""
    )

@luna.on_message(
    filters.command("dance", "/") & ~filters.edited & ~filters.private
)
async def dance(client, message: Message):
    await client.send_sticker(message.chat.id, sticker=choice(sticker_list))
    await sleep(3)
    
    
    
@luna.on_message(
    filters.command("insult", ".")
    & ~filters.private
    & ~filters.edited
)
async def insult(_, message):
    if message.reply_to_message:
        await message.reply_to_message.reply_text(choice(INSULT_STRINGS))
        await message.delete(message.command) 
        await sleep(2)
    else:
        await message.reply_text(choice(INSULT_STRINGS), quote = False)
        await message.delete(message.command)
        await sleep(2)
    
    
    
    
    
@luna.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("Nice Try u little bud ")
    await sleep(1)
    await message.reply_text("Try joining our group for more info 😁", reply_markup=InlineKeyboardMarkup(buttons))
    await sleep(3)


@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "emiko|@emikochatbot|love|lonely",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private & ~filters.command("help") & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await type_and_send(message)
    
    
ASQ_LOCK = Lock()
@luna.on_message(filters.command("asq") & ~filters.edited)
async def asq(_, message):
    err = "Reply to text message or pass the question as argument"
    if message.reply_to_message:
        if not message.reply_to_message.text:
            return await message.reply(err)
        question = message.reply_to_message.text
    else:
        if len(message.command) < 2:
            return await message.reply(err)
        question = message.text.split(None, 1)[1]
    m = await message.reply("Thinking...")
    async with ASQ_LOCK:
        resp = await arq.asq(question)
        await m.edit(resp.result)
        
        
async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
-----------------
| Luna Started! |
-----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
