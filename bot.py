import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

API_ID = 33498259 
API_HASH = "bd2c7b99af0de4fe7843ab1e8f292c23"
BOT_TOKEN = "8681347213:AAHpYFfclpZips9Hd2H7843ab1e8f292c23"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("🎵 Qo'shiq nomini yozing.")
    
    m = await message.reply("🔎 Qidirilmoqda...")
    query = " ".join(message.command[1:])
    
    try:
        search = VideosSearch(query, limit=1)
        result = search.result()["result"][0]
        link = result["link"]
        title = result["title"]
    except Exception as e:
        return await m.edit(f"❌ Topilmadi: {e}")

    ydl_opts = {"format": "bestaudio/best", "quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        audio_url = info['url']

    try:
        await call_py.play(message.chat.id, AudioPiped(audio_url))
        await m.edit(f"▶️ Ijro etilmoqda: **{title}**")
    except Exception as e:
        await m.edit(f"❌ Xato: {e}")

async def start_bot():
    await app.start()
    await call_py.start()
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
