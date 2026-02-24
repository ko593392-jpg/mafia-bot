import telebot
from youtubesearchpython import VideosSearch
import os
from telebot import apihelper

# Render'dan tokenni olamiz
TOKEN = os.getenv('BOT_TOKEN')

# Xatoni oldini olish uchun: Proxies'ni majburan bo'sh qilamiz
apihelper.proxy = None

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Qo'shiq nomini yozing.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    try:
        query = message.text
        search = VideosSearch(query, limit=5)
        results = search.result()['result']
        
        if not results:
            bot.reply_to(message, "Hech narsa topilmadi.")
            return

        text = "🎵 Topilgan natijalar:\n\n"
        for i, res in enumerate(results):
            text += f"{i+1}. {res['title']} ({res['duration']})\n"
        
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

# Bot doimiy ishlashi uchun
if __name__ == "__main__":
    print("Bot yurgizildi...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
