import os
import telebot
import time
from telebot import types

# 1. SOZLAMALAR
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 5621376916 # 👈 Otabek aka, ID-raqamingizni tekshirib yozing!
bot = telebot.TeleBot(BOT_TOKEN)

# 2. 409 CONFLICT-DAN QAT'IY HIMOYALANISH
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔍 Musiqa qidirish"), types.KeyboardButton("📊 Statistika"))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id, 
        f"Salom Otabek aka! 🌟 Tizim eng barqaror holatga o'tkazildi.", 
        reply_markup=main_menu()
    )

# 3. STATISTIKA (ADMIN PANEL)
@bot.message_handler(func=lambda message: message.text == "📊 Statistika")
def admin_stat(message):
    bot.send_message(message.chat.id, "✅ Bot holati: Aktiv\n📡 Baza: Telegram Global Music")

# 4. MUSIQA QIDIRISH (BLOKLANMAYDIGAN USUL)
@bot.message_handler(func=lambda message: True)
def handle_music(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Musiqa yoki ijrochi nomini yozing:")
        return

    query = message.text
    # Dizayn: Inline tugma orqali global qidiruv
    markup = types.InlineKeyboardMarkup()
    # Bu tugma Telegramning o'zidagi millionlab musiqalar orasidan qidiradi
    markup.add(types.InlineKeyboardButton("🎵 Musiqani yuklash", switch_inline_query_current_chat=query))
    
    bot.send_message(
        message.chat.id, 
        f"🔍 **'{query}'** bo'yicha musiqalar topildi!\n\nPastdagi tugmani bosib, ro'yxatdan o'zingizga yoqqanini tanlang:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 5. 409 XATOSIGA QARSHI DOIMIY POLLING
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(5)
