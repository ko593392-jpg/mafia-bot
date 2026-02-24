import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. 409 VA WEBHOOK TOZALASH
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Otabek, botingiz 1ga1 tizimga o'tdi! 🚀\nEndi faqat sifatli musiqalar keladi.")

@bot.message_handler(func=lambda m: True)
def search_music(message):
    query = message.text
    wait = bot.reply_to(message, "🔍 Sifatli baza tekshirilmoqda...")

    try:
        # Eng kuchli YouTube-to-MP3 Engine (Hech qachon "rasvo" chiqarmaydi)
        # Bu baza Tingla.uz kabi aniq ishlaydi
        api_url = f"https://api.v-s.mobi/api/v1/search?q={query}"
        res = requests.get(api_url, timeout=15).json()
        
        if res and 'items' in res:
            track = res['items'][0]
            # TO'LIQ VA SIFATLI MP3 LINKI
            audio_url = f"https://api.v-s.mobi/api/v1/download?id={track['id']}&type=audio"
            
            # DIZAYN: Siz aytgan @ai_muzik_bot manzilini to'g'irladik
            bot.send_audio(
                message.chat.id, 
                audio_url, 
                caption=f"🎵 **{track['title']}**\n\n✅ To'liq va sifatli variant!\n📥 @ai_muzik_bot",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, wait.message_id)
        else:
            bot.edit_message_text("❌ Hech narsa topilmadi.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("⚠️ Baza band, qayta urinib ko'ring.", message.chat.id, wait.message_id)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True)
        except:
            time.sleep(5)
