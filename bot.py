import telebot
from youtubesearchpython import VideosSearch
import os
from telebot import apihelper

# Tokenni Render'dan olamiz
TOKEN = os.getenv('BOT_TOKEN')

# Proxies muammosini uzil-kesil yopamiz
apihelper.proxy = None

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men tayyorman. Qo'shiq nomini yozing!")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    print(f"Qidirilmoqda: {query}") # Render logida ko'rinadi
    
    try:
        # Qidiruv qismini xavfsizroq qilamiz
        search = VideosSearch(query, limit=1)
        result = search.result()
        
        if result and len(result.get('result', [])) > 0:
            video = result['result'][0]
            title = video.get('title', 'Nomsiz')
            link = video.get('link', '')
            bot.send_message(message.chat.id, f"🎵 Topildi: {title}\n🔗 {link}")
        else:
            bot.reply_to(message, "Hech narsa topilmadi.")
            
    except Exception as e:
        # Xatolikni aniq nimaligini logga chiqaramiz
        print(f"XATO YUZ BERDI: {str(e)}")
        bot.reply_to(message, f"Xatolik: {str(e)[:50]}... Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling(timeout=20)
