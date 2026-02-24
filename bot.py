import os
import telebot
import requests
import time

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# ⚠️ 409 xatosini o'ldirish: Eski ulanishlarni majburan uzish
try:
    print("Eski ulanishlar tozalanmoqda...")
    bot.remove_webhook()
    time.sleep(2) # Telegram serverlariga dam beramiz
except Exception as e:
    print(f"Tozalashda xato: {e}")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Otabek aka, botingiz 409 xatosidan qutuldi! ✅\nEndi bemalol musiqa qidiring.")

@bot.message_handler(func=lambda message: True)
def handle_music(message):
    query = message.text
    msg = bot.reply_to(message, "⏳ Eng kuchli tashqi bazadan to'liq musiqa olinmoqda...")
    
    try:
        # Tashqi "Qo'l" - Bloklanmaydigan YouTube-MP3 API
        api_url = f"https://api.v-s.mobi/api/v1/search?q={query}"
        res = requests.get(api_url, timeout=20).json()
        
        if res and 'items' in res:
            audio_id = res['items'][0]['id']
            # To'g'ridan-to'g'ri to'liq yuklash linki
            download_url = f"https://api.v-s.mobi/api/v1/download?id={audio_id}&type=audio"
            
            bot.send_audio(message.chat.id, download_url, caption=f"🎵 {res['items'][0]['title']}")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ Hech narsa topilmadi.", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("⚠️ Baza vaqtincha band, qayta urinib ko'ring.", message.chat.id, msg.message_id)

# 409-ga qarshi eng kuchli himoya
while True:
    try:
        bot.polling(none_stop=True, skip_pending=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Polling xatosi: {e}")
        time.sleep(5) # Xato bo'lsa 5 soniya kutib qayta ulanadi
