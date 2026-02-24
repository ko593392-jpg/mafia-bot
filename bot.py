import os
import telebot
import requests
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# To'liq musiqa yuklovchi funksiya (Zaxira bilan)
def get_music_link(query):
    # 1-bazadan qidirish (To'liq MP3)
    try:
        url1 = f"https://api.v-s.mobi/api/v1/search?q={query}"
        r1 = requests.get(url1, timeout=10).json()
        if r1 and 'items' in r1:
            return f"https://api.v-s.mobi/api/v1/download?id={r1['items'][0]['id']}&type=audio", r1['items'][0]['title']
    except:
        pass
        
    # 2-baza (Zaxira - agar 1-si ishlamasa)
    try:
        url2 = f"https://chukkun-api.vercel.app/api/music?q={query}"
        r2 = requests.get(url2, timeout=10).json()
        if r2 and 'results' in r2:
            return r2['results'][0]['download'], r2['results'][0]['title']
    except:
        return None, None

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"))
    bot.send_message(message.chat.id, "Nihoyat, to'liq musiqalar tizimi ishga tushdi!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yozing:")
        return

    msg = bot.reply_to(message, "⏳ To'liq musiqa qidirilmoqda (Zaxira tizimi bilan)...")
    
    audio_url, title = get_music_link(message.text)
    
    if audio_url:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚀 Ulashish", switch_inline_query=title))
        
        bot.send_audio(
            message.chat.id, 
            audio_url, 
            caption=f"🎵 **{title}**\n\n✅ To'liq variant!\n📥 @sizning_botingiz",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        bot.delete_message(message.chat.id, msg.message_id)
    else:
        bot.edit_message_text("❌ Hamma bazalar band. Birozdan so'ng urinib ko'ring.", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
