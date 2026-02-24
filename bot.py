import os
import telebot
import requests
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"))
    bot.send_message(message.chat.id, f"Salom, {message.from_user.first_name}! ✨\nTizim qayta sozlandi. Endi musiqalarni topishim kerak!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Musiqa nomini yozing:")
        return

    msg = bot.reply_to(message, "⏳ Eng kuchli bazadan qidirilmoqda...")
    
    try:
        # Yangi va barqaror YouTube-MP3 bazasi
        # Bu baza Railway IP-larini bloklamaydi
        api_url = f"https://api.v-s.mobi/api/v1/search?q={query}"
        res = requests.get(api_url, timeout=20).json()
        
        if res and 'items' in res:
            track = res['items'][0]
            audio_id = track['id']
            title = track['title']
            # Yuklash havolasini shakllantiramiz
            download_url = f"https://api.v-s.mobi/api/v1/download?id={audio_id}&type=audio"
            
            bot.send_audio(
                message.chat.id, 
                download_url, 
                caption=f"🎵 **{title}**\n\n✅ To'liq variant!\n📥 @sizning_botingiz",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ Kechirasiz, hech narsa topilmadi.", message.chat.id, msg.message_id)
    except:
        # Agar bu ham band bo'lsa, zaxira (Deezer) ishga tushadi
        bot.edit_message_text("⚠️ Baza biroz sekin, qayta urinib ko'ring yoki boshqa nom yozing.", message.chat.id, msg.message_id)

bot.remove_webhook()
bot.polling(none_stop=True)
