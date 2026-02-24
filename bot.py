import os
import time
import logging
import telebot
from telebot.types import InlineQuery, InlineQueryResultCachedAudio

# =====================
# 1. SOZLAMALAR
# =====================
TOKEN = os.environ.get("BOT_TOKEN")  # Railway / env orqali
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

logging.basicConfig(level=logging.INFO)

# =====================
# 2. 409 CONFLICT OLDINI OLISH
# =====================
try:
    bot.remove_webhook(drop_pending_updates=True)
    time.sleep(1)
except:
    pass

# =====================
# 3. MUSIQA BAZASI (Telegram file_id)
# =====================
MUSIC_DB = [
    {
        "title": "Relax Music",
        "artist": "AI Muzik",
        "file_id": "CQACAgIAAxkBAAExampleFILEID1"
    },
    {
        "title": "Night Vibes",
        "artist": "AI Muzik",
        "file_id": "CQACAgIAAxkBAAExampleFILEID2"
    }
]

# =====================
# 4. INLINE QUERY QIDIRUV
# =====================
@bot.inline_handler(func=lambda q: len(q.query) > 0)
def inline_music(inline_query: InlineQuery):
    results = []

    for i, music in enumerate(MUSIC_DB):
        caption = (
            f"🎵 <b>{music['title']}</b>\n"
            f"👤 {music['artist']}\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"✨ <i>@ai_muzik_bot</i>"
        )

        results.append(
            InlineQueryResultCachedAudio(
                id=str(i),
                audio_file_id=music["file_id"],
                caption=caption
            )
        )

    bot.answer_inline_query(
        inline_query.id,
        results,
        cache_time=5,
        is_personal=True
    )

# =====================
# 5. BOT O‘CHIB QOLMASLIGI UCHUN
# =====================
if __name__ == "__main__":
    while True:
        try:
            logging.info("Bot polling ishga tushdi...")
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(e)
            time.sleep(5)
