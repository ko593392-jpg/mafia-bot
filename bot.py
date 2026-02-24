import telebot
from youtubesearchpython import VideosSearch
import os
from telebot import apihelper

# Render'dan tokenni olamiz
TOKEN = os.getenv('BOT_TOKEN')

# MUHIM: Xatoga sabab bo'layotgan proxies funksiyasini butunlay o'chiramiz
apihelper.proxy = None

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men tayyorman. Qo'shiq nomini yozing!")

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
        # Xatolikni ko'rish uchun
        print(f"Xatolik: {e}")
        bot.reply_to(message, "Kichik texnik xatolik, qaytadan urinib ko'ring.")

if __name__ == "__main__":
    print("Bot muvaffaqiyatli yurgizildi...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
