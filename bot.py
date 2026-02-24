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
    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}! \nMen orqali to'liq musiqalarni topishingiz mumkin.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yoki ijrochini yozing:")
        return

    msg = bot.reply_to(message, "🔍 To'liq musiqa qidirilmoqda...")
    
    try:
        # To'liq musiqa yuklash uchun barqaror API (YouTube asosi)
        search_url = f"https://api.v-s.mobi/api/v1/search?q={query}"
        response = requests.get(search_url).json()
        
        if response and 'items' in response:
            track = response['items'][0]
            video_id = track['id']
            title = track['title']
            # To'liq MP3 yuklash uchun havola
            audio_url = f"https://api.v-s.mobi/api/v1/download?id={video_id}&type=audio"
            
            # --- TINGLA BOT DIZAYNI (Inline tugmalar) ---
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_share = types.InlineKeyboardButton("🚀 Ulashish", switch_inline_query=title)
            btn_channel = types.InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/sizning_kanalingiz")
            markup.add(btn_share, btn_channel)
            
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
        bot.edit_message_text("❌ Yuklashda xato (Server band).", message.chat.id, msg.message_id)
        print(f"Xato: {e}")

bot.polling(none_stop=True)
