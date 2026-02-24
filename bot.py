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
    bot.send_message(message.chat.id, "Nihoyat ishlayapman! Musiqa nomini yozing:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yozing:")
        return

    msg = bot.reply_to(message, "🔍 To'liq musiqa qidirilmoqda...")
    
    try:
        # 1-bazadan qidirib ko'ramiz (To'liq musiqa uchun)
        search_url = f"https://api.v-s.mobi/api/v1/search?q={query}"
        response = requests.get(search_url, timeout=10).json()
        
        if response and 'items' in response:
            track = response['items'][0]
            title = track['title']
            audio_url = f"https://api.v-s.mobi/api/v1/download?id={track['id']}&type=audio"
            
            # --- Professional dizayn ---
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
            bot.edit_message_text("❌ Musiqa topilmadi.", message.chat.id, msg.message_id)
            
    except Exception as e:
        # Agar baza xato bersa, bot "qotib" qolmasligi uchun darhol xabar beradi
        bot.edit_message_text("⚠️ Server vaqtincha band, qayta urinib ko'ring.", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
