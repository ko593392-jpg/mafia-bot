import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

# Ma'lumotlar
API_ID = 33498259
API_HASH = "bd2c7b99af0de4fe7843ab1e8f292fd2"
BOT_TOKEN = "8681347213:AAHpYFfclpZips9HdI0_WGacOoarFzZmDLY"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("🎵 Qo'shiq nomini yozing!")
    
    m = await message.reply("🔎 Qidiryapman...")
    query = " ".join(message.command[1:])
    
    try:
        search = VideosSearch(query, limit=1).result()['result'][0]
        ydl_opts = {"format": "bestaudio/best", "quiet": True, "noplaylist": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search['link'], download=False)
            url = info['url']

        # Ovozli chatga ulanish
        await call_py.play(
            message.chat.id,
            AudioPiped(url)
        )
        await m.edit(f"✅ Ijro etilmoqda: **{search['title']}**")
    except Exception as e:
        await m.edit(f"❌ Xato: {str(e)}")

async def start_bot():
    await app.start()
    await call_py.start()
    print("🚀 Bot ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
