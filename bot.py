import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 5621376916 # Otabek aka ID raqamingiz

# 2. 409 XATOSINI O'LDIRISH
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

def main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Musiqa qidirish", "📊 Statistika")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Xush keldingiz Otabek aka! ✨\nIsmni yozing, men to'liq MP3 yuboraman.", reply_markup=main_buttons())

@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    bot.send_message(message.chat.id, "✅ Tizim holati: Barqaror\n📡 Baza: Global MP3 Engine")

@bot.message_handler(func=lambda m: True)
def search_music(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yozing:")
        return

    query = message.text
    wait = bot.reply_to(message, "⏳ To'liq MP3 tayyorlanmoqda, kuting...")

    try:
        # TO'LIQ MUSIQA BERADIGAN BAZA
        res = requests.get(f"https://api.v-s.mobi/api/v1/search?q={query}").json()
        
        if res['items']:
            track = res['items'][0]
            # TO'LIQ MP3 LINKINI SHAKLLANTIRISH
            audio_full_url = f"https://api.v-s.mobi/api/v1/download?id={track['id']}&type=audio"
            
            # DIZAYN VA TO'G'RI MANZIL
            bot.send_audio(
                message.chat.id, 
                audio_full_url, 
                caption=f"🎵 **{track['title']}**\n\n✅ To'liq variant!\n📥 @ai_muzik_bot",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, wait.message_id)
        else:
            bot.edit_message_text("❌ Topilmadi.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("⚠️ Baza hozir band, yana bir marta urinib ko'ring.", message.chat.id, wait.message_id)

# 3. 409 VA CRASHED-DAN HIMOYALANGAN POLLING
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, timeout=20)
        except:
            time.sleep(5)
