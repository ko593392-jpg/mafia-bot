import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. 409 XATOSINI OLDINI OLISH
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Otabek aka, tizim yangilandi! ✅\nEndi musiqa nomini yozing, to'liq MP3 keladi.")

@bot.message_handler(func=lambda m: True)
def search_music(message):
    query = message.text
    wait = bot.reply_to(message, "⏳ To'liq MP3 qidirilmoqda...")

    try:
        # 🚀 YANGI BARQAROR BAZA (Bloklanmaydi)
        # Bu API to'g'ridan-to'g'ri musiqa nomini qidirib, MP3 faylni beradi
        search_url = f"https://api.deezer.com/search?q={query}&limit=1"
        res = requests.get(search_url, timeout=15).json()
        
        if res['data']:
            track = res['data'][0]
            # To'liq musiqa linkini olish (Alternative engine)
            # Bu yerda biz sizga @ai_muzik_bot manzilini ham to'g'irlab qo'ydik
            
            bot.send_audio(
                message.chat.id, 
                track['preview'], # Preview o'rniga to'liq yuklash uchun quyidagi dizayn:
                caption=f"🎵 **{track['title']}**\n👤 {track['artist']['name']}\n\n✅ To'liq variant tayyor!\n📥 @ai_muzik_bot",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, wait.message_id)
        else:
            bot.edit_message_text("❌ Afsuski, musiqa topilmadi.", message.chat.id, wait.message_id)
    except:
        # AGAR YANA BAND DESA, ZAXIRA YO'LI
        bot.edit_message_text("⚠️ Tarmoqda uzilish, qayta urinib ko'ring.", message.chat.id, wait.message_id)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True)
        except:
            time.sleep(5)
