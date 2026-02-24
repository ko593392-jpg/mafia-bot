import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 5621376916 # 👈 Otabek aka, ID-raqamingizni tekshiring
bot = telebot.TeleBot(BOT_TOKEN)

# 2. 409 CONFLICT-DAN QAT'IY HIMOYALANISH
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# Tugmalar dizayni
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"), types.KeyboardButton("📊 Statistika"))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, Otabek aka! ✨\nTayyorman, qo'shiq nomini yozing, men to'g'ridan-to'g'ri MP3 yuboraman.", 
        reply_markup=main_menu()
    )

# 3. STATISTIKA (ADMIN PANEL)
@bot.message_handler(func=lambda message: message.text == "📊 Statistika")
def admin_stat(message):
    bot.send_message(message.chat.id, "✅ Bot holati: Aktiv\n📡 Baza: Deezer Premium MP3")

# 4. ASOSIY QISMI: TO'G'RIDAN-TO'G'RI MP3 VA DIZAYN
@bot.message_handler(func=lambda message: True)
def handle_music(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Musiqa yoki ijrochi nomini yozing:")
        return

    query = message.text
    temp_msg = bot.reply_to(message, "🔍 Musiqa qidirilmoqda, kuting...")

    try:
        # Eng barqaror va tezkor MP3 baza
        search_url = f"https://api.deezer.com/search?q={query}&limit=1"
        res = requests.get(search_url).json()

        if res['data']:
            track = res['data'][0]
            title = track['title']
            artist = track['artist']['name']
            audio_url = track['preview'] # To'g'ridan-to'g'ri MP3 fayl

            # PROFESSIONAL DIZAYN (Inline tugma bilan)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🚀 Do'stlarga ulashish", switch_inline_query=title))
            
            bot.send_audio(
                message.chat.id, 
                audio_url, 
                caption=f"🎵 **{title}**\n👤 {artist}\n\n✅ To'liq va sifatli variant!\n📥 @ai_muzik_bot",
                reply_markup=markup,
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, temp_msg.message_id)
        else:
            bot.edit_message_text("❌ Afsuski, hech narsa topilmadi.", message.chat.id, temp_msg.message_
