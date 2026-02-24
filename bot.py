import os
import telebot
import yt_dlp

# 1. Tokenni olish
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. FFmpeg talab qilmaydigan sozlamalar
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Tayyorman! Qo'shiq nomini yozing, men darhol topib beraman.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    msg = bot.reply_to(message, "🔍 Qidirilmoqda...")

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            # Musiqani qidirish
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            audio_url = info['url']
            title = info.get('title', 'Musiqa')
            duration = info.get('duration', 0)
            
        # Musiqani audio havola orqali yuborish
        bot.send_audio(
            message.chat.id, 
            audio_url, 
            caption=f"✅ {title}",
            title=title,
            duration=duration
        )
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Xato: Musiqa topilmadi.", message.chat.id, msg.message_id)
        print(f"Xato: {e}")

bot.polling(none_stop=True)
