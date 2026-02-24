import telebot
from youtube_search_python import VideosSearch
import os

# Tokenni o'zgartirmang, Render'dagi Environment Variable'dan oladi
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Qo'shiq nomini yozing, men topib beraman.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    try:
        query = message.text
        # Mana shu joyi youtube-search-python kutubxonasiga moslandi
        search = VideosSearch(query, limit=10)
        results = search.result()['result']
        
        if not results:
            bot.reply_to(message, "Hech narsa topilmadi.")
            return

        text = "Topilgan natijalar:\n\n"
        for i, res in enumerate(results):
            text += f"{i+1}. {res['title']} ({res['duration']})\n"
        
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. Keyinroq urinib ko'ring.")

bot.polling(none_stop=True)
