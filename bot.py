import os
import sys

# 1. Render kutubxonalarni o'rnatmasa, ularni majburan o'rnatish
try:
    from sclib import SoundcloudAPI, Track
    import telebot
except ImportError:
    print("Kutubxonalar topilmadi. O'rnatish boshlanmoqda...")
    os.system("pip install pyTelegramBotAPI sclib")
    # O'rnatilgandan keyin qayta import qilish
    from sclib import SoundcloudAPI, Track
    import telebot

# 2. Tokenni olish (Render Environment Variables'dan)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
api = SoundcloudAPI()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! SoundCloud'dan musiqa qidirish uchun nomini yozing.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    try:
        msg = bot.reply_to(message, "Qidirilmoqda... 🔎")
        tracks = api.search_tracks(query)
        
        if tracks:
            track = tracks[0]
            with open('track.mp3', 'wb+') as fp:
                track.write_to(fp)
            
            with open('track.mp3', 'rb') as audio:
                bot.send_audio(message.chat.id, audio, title=track.title, performer=track.artist)
            
            bot.delete_message(message.chat.id, msg.message_id)
            os.remove('track.mp3')
        else:
            bot.edit_message_text("Hech narsa topilmadi 😕", message.chat.id, msg.message_id)
            
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        bot.send_message(message.chat.id, "Kichik texnik xatolik yuz berdi.")

# 3. Botni ishga tushirish
if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
