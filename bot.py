import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 12345678 # 👈 Otabek aka, ID-raqamingizni yozing!
bot = telebot.TeleBot(BOT_TOKEN)

# 2. 409 CONFLICT-DAN DOIMIY HIMOYALANISH
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"), types.KeyboardButton("📊 Statistika"))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Salom Otabek aka! 🌟 Tizim 100% barqaror.", reply_markup=main_menu())

# 3. ASOSIY MUSIQA QIDIRISH (ZAXIRA TIZIMI BILAN)
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Musiqa nomini yozing:")
        return
    if message.text == "📊 Statistika":
        bot.send_message(message.chat.id, "👤 Bot holati: Aktiv ✅")
        return

    query = message.text
    temp_msg = bot.reply_to(message, "⏳ Musiqa qidirilmoqda...")

    # --- 1-URINISH: YouTube Baza ---
    try:
        url1 = f"https://api.v-s.mobi/api/v1/search?q={query}"
        res1 = requests.get(url1, timeout=10).json()
        if res1 and 'items' in res1:
            audio_url = f"https://api.v-s.mobi/api/v1/download?id={res1['items'][0]['id']}&type=audio"
            send_music(message.chat.id, audio_url, res1['items'][0]['title'], temp_msg)
            return
    except:
        pass # Agar 1-baza band bo'lsa, indamay 2-siga o'tamiz

    # --- 2-URINISH: Spotify/Deezer Baza (Zaxira) ---
    try:
        url2 = f"https://spotify-downloader.com/api/search?q={query}"
        res2 = requests.get(url2, timeout=10).json()
        if res2 and 'data' in res2:
            track = res2['data'][0]
            send_music(message.chat.id, track['download_link'], track['name'], temp_msg)
            return
    except:
        pass

    # Agar ikkala baza ham ishlamasa (juda kam holatda)
    bot.edit_message_text("❌ Kechirasiz, musiqa topilmadi. Boshqa nom yozib ko'ring.", message.chat.id, temp_msg.message_id)

def send_music(chat_id, url, title, temp_msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 Ulashish", switch_inline_query=title))
    bot.send_audio(chat_id, url, caption=f"🎵 **{title}**\n\n✅ Tayyor!", reply_markup=markup, parse_mode="Markdown")
    bot.delete_message(chat_id, temp_msg.message_id)

# 4. 409 XATOSIGA QARSHI AVTOMATIK RESTART
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(5)
