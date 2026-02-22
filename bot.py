import telebot
from telebot import types
import threading
import os
import random

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# Render dummy server
def dummy_server():
    os.system("python3 -m http.server 10000")
threading.Thread(target=dummy_server, daemon=True).start()

# Foydalanuvchi ma'lumotlari (Vaqtinchalik xotira)
user_data = {}

def get_profile_text(user):
    u_id = user.id
    if u_id not in user_data:
        user_data[u_id] = {'money': 1000, 'diamonds': 5, 'wins': 0, 'games': 0}
    
    data = user_data[u_id]
    text = (
        f"👤 *FOYDALANUVCHI PROFILI*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 *ID:* `{u_id}`\n"
        f"👤 *Ism:* {user.first_name}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 *Pullar:* {data['money']} pullar\n"
        f"💎 *Olmoslar:* {data['diamonds']}\n"
        f"🏆 *G'alabalar:* {data['wins']}\n"
        f"🎮 *O'yinlar:* {data['games']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏅 *Daraja:* {'Yangi o\'yinchi' if data['wins'] < 5 else 'Professional'}"
    )
    return text

@bot.message_handler(commands=['start', 'me', 'profil'])
def profile_handler(message):
    text = get_profile_text(message.from_user)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_add = types.InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{bot.get_me().username}?startgroup=true")
    btn_shop = types.InlineKeyboardButton("🛒 Do'kon", callback_data="open_shop")
    markup.add(btn_add)
    markup.add(btn_shop)
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['new'])
def new_game(message):
    chat_id = message.chat.id
    # O'yin boshlanganda o'yinchilar statistikasini yangilash uchun joy tayyorlaymiz
    text = (
        "🎮 *YANGI O'YIN BOSHLANDI!*\n"
        "━━━━━━━━━━━━━━━\n"
        "📝 *O'yinchilar:* ⏳ kutilmoqda...\n"
        "━━━━━━━━━━━━━━━\n"
        "🎁 Mukofot: *+200 pul* 💰"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Qo'shilish", callback_data="join_game"))
    markup.add(types.InlineKeyboardButton("🚀 Boshlash", callback_data="start_logic"))
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)

# ... (Boyagi join_game va start_logic kodlari shu yerda qoladi) ...
# Faqat start_logic ichida har bir o'yinchiga data['games'] += 1 qo'shib ketiladi.

bot.infinity_polling()

            
