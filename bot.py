import telebot
from telebot import types
import threading
import os
import random
import time

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# Render dummy server
def dummy_server():
    os.system("python3 -m http.server 10000")
threading.Thread(target=dummy_server, daemon=True).start()

# Ma'lumotlar ombori (Kengaytirilgan)
user_data = {}

def get_profile_text(user):
    u_id = user.id
    if u_id not in user_data:
        user_data[u_id] = {
            'money': 1000, 'diamonds': 5, 'wins': 0, 
            'games': 0, 'shield': 'Yo'q ❌', 'weapon': 'Yo'q ❌', 'id_card': 'Asliy ✅'
        }
    
    d = user_data[u_id]
    text = (
        f"👤 *FOYDALANUVCHI PROFILI*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 *ID:* `{u_id}`\n"
        f"👤 *Ism:* {user.first_name}\n"
        f"🏅 *Daraja:* {'Yangi o\'yinchi' if d['wins'] < 5 else 'Mafia Sardori'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 *Pullar:* {d['money']} pullar\n"
        f"💎 *Olmoslar:* {d['diamonds']}\n"
        f"🏆 *G'alabalar:* {d['wins']}\n"
        f"🎮 *O'yinlar:* {d['games']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🛡 *Himoya:* {d['shield']}\n"
        f"🔫 *Qurol:* {d['weapon']}\n"
        f"🪪 *Hujjat:* {d['id_card']}\n"
        f"━━━━━━━━━━━━━━━"
    )
    return text

@bot.message_handler(commands=['start', 'profil', 'me'])
def profile_handler(message):
    text = get_profile_text(message.from_user)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_shop = types.InlineKeyboardButton("🛒 Do'kon", callback_data="open_shop")
    btn_bonus = types.InlineKeyboardButton("🎁 Kunlik Bonus", callback_data="get_bonus")
    btn_add = types.InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{bot.get_me().username}?startgroup=true")
    
    markup.add(btn_shop, btn_bonus)
    markup.add(btn_add)
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "open_shop")
def shop_handler(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Siz aytgan @muwahhid_27 profiliga ulanadigan tugma
    btn_buy = types.InlineKeyboardButton("💳 Olmos/Pul sotib olish (Admin)", url="https://t.me/muwahhid_27")
    btn_back = types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_profile")
    markup.add(btn_buy, btn_back)
    
    shop_text = (
        "🛒 *MAFIA SHOP — DO'KON*\n"
        "━━━━━━━━━━━━━━━\n"
        "💎 *100 Olmos* — 10.000 so'm\n"
        "💰 *50.000 Pul* — 15.000 so'm\n"
        "🔫 *Maxsus Qurol* — 50 Olmos\n"
        "🛡 *Zirh (Shield)* — 30 Olmos\n"
        "━━━━━━━━━━━━━━━\n"
        "👇 Sotib olish uchun adminga murojaat qiling:"
    )
    bot.edit_message_text(shop_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_profile")
def back_to_profile(call):
    text = get_profile_text(call.from_user)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🛒 Do'kon", callback_data="open_shop"), 
               types.InlineKeyboardButton("🎁 Kunlik Bonus", callback_data="get_bonus"))
    markup.add(types.InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{bot.get_me().username}?startgroup=true"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "get_bonus")
def bonus_callback(call):
    # Bu yerda vaqtinchalik 500 pul beramiz (Logika boyagi kodda bor edi)
    u_id = call.from_user.id
    user_data[u_id]['money'] += 500
    bot.answer_callback_query(call.id, "🎁 Tabriklaymiz! 500 pul berildi!", show_alert=True)
    back_to_profile(call)

bot.infinity_polling()

            
