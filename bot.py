import os
import telebot
import yt_dlp

# 1. Tokenni Railway Variables'dan olamiz
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. Yuklab olish sozlamalari
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'track.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Qo'shiq nomini yozing, men darhol topib beraman.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    msg = bot.reply_to(message, "🔍 Qidirilmoqda...")

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            # YouTube va SoundCloud'dan qidiradi
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            title = info.get('title', 'Musiqa')
            
        # Musiqani yuborish
        with open('track.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✅ {title}")
        
        bot.delete_message(message.chat.id, msg.message_id)
        os.remove('track.mp3')

    except Exception as e:
        bot.edit_message_text(f"❌ Xato yuz berdi: Musiqa topilmadi yoki yuklab bo'lmadi.", message.chat.id, msg.message_id)
        print(f"Xato: {e}")

bot.polling(none_stop=True)
