import os
import telebot
import requests
from telebot import types

# Tokeningiz o'zgarmasligi uchun Variables'dan olamiz
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"))
    bot.send_message(
        message.chat.id, 
        f"Xush kelibsiz, {message.from_user.first_name}! 👋\nMen orqali to'liq va sifatli musiqalarni topishingiz mumkin.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Qo'shiq nomini yoki ijrochini yozing:")
        return

    msg = bot.reply_to(message, "🔍 Barqaror qidiruv tizimidan foydalanilmoqda...")
    
    try:
        # 100% Barqaror va to'liq musiqa beradigan API (YouTube asosi)
        search_url = f"https://api.v-s.mobi/api/v1/search?q={query}"
        # Timeout qo'yamizki, bot qotib qolmasin
        response = requests.get(search_url, timeout=15).json()
        
        if response and 'items' in response:
            track = response['items'][0]
            title = track['title']
            # To'liq MP3 yuklash havolasi
            audio_url = f"https://api.v-s.mobi/api/v1/download?id={track['id']}&type=audio"
            
            # --- TINGLA BOT DIZAYNI ---
            markup = types.InlineKeyboardMarkup()
            btn_share = types.InlineKeyboardButton("🚀 Ulashish", switch_inline_query=title)
            markup.add(btn_share)
            
            bot.send_audio(
                message.chat.id, 
                audio_url, 
                caption=f"🎵 **{title}**\n\n✅ To'liq variant!\n📥 @sizning_bot_nomingiz",
                reply_markup=markup,
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ Afsuski, hech narsa topilmadi.", message.chat.id, msg.message_id)
            
    except Exception as e:
        # Xato bo'lsa, botni restart qilmaydigan xavfsiz blok
        bot.edit_message_text("⚠️ Hozircha bu baza band, iltimos birozdan so'ng urinib ko'ring.", message.chat.id, msg.message_id)
        print(f"Xato: {e}")

bot.polling(none_stop=True)

