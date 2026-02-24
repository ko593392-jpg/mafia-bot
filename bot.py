import os
import telebot
import requests
from telebot import types

# Tokenni yangilagan bo'lsangiz, uni Variables'ga qo'shishni unutmang
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"))
    bot.send_message(
        message.chat.id, 
        f"Xush kelibsiz! Musiqa nomini yozing, men uni to'liq formatda topib beraman.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yozing:")
        return

    msg = bot.reply_to(message, "🔍 Qidirilmoqda...")
    
    try:
        # Barqaror musiqa qidiruv tizimi
        search_url = f"https://chukkun-api.vercel.app/api/music?q={query}"
        data = requests.get(search_url).json()
        
        if data and 'results' in data:
            track = data['results'][0]
            audio_url = track['download']
            title = track['title']
            artist = track['artist']
            
            # --- TINGLA BOT DIZAYNI ---
            markup = types.InlineKeyboardMarkup()
            btn_share = types.InlineKeyboardButton("🚀 Ulashish", switch_inline_query=f"{artist} - {title}")
            markup.add(btn_share)
            
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
            bot.edit_message_text("❌ Musiqa topilmadi.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: Qidiruv tizimi vaqtincha band.", message.chat.id, msg.message_id)
