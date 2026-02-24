import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 5621376916 # Otabek aka ID raqamingiz

# 2. XATOLIKLARNI TOZALASH
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# Dizayn tugmalari
def main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Musiqa qidirish", "📊 Statistika")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Xush keldingiz Otabek aka! 🌟 Qo'shiq nomini yozing:", reply_markup=main_buttons())

@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    bot.send_message(message.chat.id, "✅ Tizim holati: Barqaror\n📡 Baza: Deezer MP3")

@bot.message_handler(func=lambda m: True)
def search_music(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yozing:")
        return

    query = message.text
    wait = bot.reply_to(message, "⏳ MP3 tayyorlanmoqda...")

    try:
        # Eng tezkor va bloklanmaydigan MP3 baza
        res = requests.get(f"https://api.deezer.com/search?q={query}&limit=1").json()
        
        if res['data']:
            track = res['data'][0]
            # DIZAYN: To'g'ridan-to'g'ri MP3 fayl
            bot.send_audio(
                message.chat.id, 
                track['preview'], 
                caption=f"🎵 **{track['title']}**\n👤 {track['artist']['name']}\n\n📥 @ai_muzik_bot",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, wait.message_id)
        else:
            bot.edit_message_text("❌ Topilmadi.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("⚠️ Tarmoq biroz band, qayta urinib ko'ring.", message.chat.id, wait.message_id)

# 3. 409 VA CRASHED-DAN HIMOYALANGAN POLLING
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, timeout=20)
        except:
            time.sleep(5)
              
