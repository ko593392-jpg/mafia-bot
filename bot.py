import telebot
from sclib import SoundcloudAPI, Track
import os
from telebot import apihelper

TOKEN = os.getenv('BOT_TOKEN')
apihelper.proxy = None
bot = telebot.TeleBot(TOKEN)
api = SoundcloudAPI()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men ishlayapman! Qo'shiq nomini yozing (SoundCloud orqali).")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    try:
        # SoundCloud'dan qidiramiz
        tracks = api.search(message.text)
        if tracks:
            track = tracks[0] # Eng birinchi chiqqan natija
            title = getattr(track, 'title', 'Nomsiz')
            url = getattr(track, 'permalink_url', '')
            bot.send_message(message.chat.id, f"🎵 Topildi: {title}\n🔗 {url}")
        else:
            bot.reply_to(message, "Hech narsa topilmadi.")
    except Exception as e:
        print(f"Xato: {e}")
        bot.reply_to(message, "Hozircha faqat link bera olaman. Iltimos, qaytadan urinib ko'ring.")

if __name__ == "__main__":
    bot.infinity_polling()
