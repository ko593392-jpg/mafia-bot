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
    bot.send_message(message.chat.id, "Tayyorman! Musiqa nomini yozing:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yozing:")
        return

    msg = bot.reply_to(message, "🔍 Barqaror qidiruv tizimi ulanmoqda...")
    
    try:
        # Deezer - eng ishonchli va bloklanmaydigan bepul API
        url = f"https://api.deezer.com/search?q={query}&limit=1"
        res = requests.get(url, timeout=10).json()
        
        if res['data']:
            track = res['data'][0]
            title = track['title']
            artist = track['artist']['name']
            audio_url = track['preview']
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🚀 Ulashish", switch_inline_query=title))
            
            bot.send_audio(
                message.chat.id, 
                audio_url, 
                caption=f"🎵 **{artist} - {title}**\n\n📥 @sizning_botingiz",
                performer=artist,
                title=title,
                reply_markup=markup,
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ Hech narsa topilmadi.", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ Tizimda kichik xato, qayta urinib ko'ring.", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
