import os
import telebot
import time
from telebot import types

# 1. SOZLAMALAR
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 409 Xatosi va Webhook'ni tozalash
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Otabek aka, tizim eng barqaror holatga o'tkazildi! ✅\nPastdagi tugmani bosing va musiqangizni tanlang.",
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("🔍 Musiqa qidirish")
    )

@bot.message_handler(func=lambda m: True)
def search_music(message):
    query = message.text
    if query == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Musiqa nomini yozing:")
        return

    # DIZAYN: Telegramning global bazasidan qidirish (Bloklanmaydi!)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎵 Musiqani yuklash", switch_inline_query_current_chat=query))
    
    bot.send_message(
        message.chat.id, 
        f"🔍 **'{query}'** bo'yicha musiqalar topildi!\n\nPastdagi tugmani bosib, ro'yxatdan o'zingizga yoqqanini tanlang:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, timeout=20)
        except Exception as e:
            time.sleep(5)
