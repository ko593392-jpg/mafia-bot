import telebot
from telebot import types
import threading
import os

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# Render dummy server
def dummy_server():
    os.system("python3 -m http.server 10000")
threading.Thread(target=dummy_server, daemon=True).start()

user_data = {}

def get_pro_profile(user):
    u_id = user.id
    if u_id not in user_data:
        user_data[u_id] = {
            'money': 1000, 'diamonds': 5, 'wins': 0, 'games': 0,
            'himoya': 0, 'qotil_himoya': 0, 'ovoz_himoya': 0,
            'miltiq': 0, 'maska': 0, 'soxta_hujjat': 0
        }
    
    d = user_data[u_id]
    text = (
        f"O'yin tugadi!\n"
        f"⭐ ID: {u_id}\n\n"
        f"👤 {user.first_name}\n\n"
        f"💵 Dollar: {d['money']}\n"
        f"💎 Olmos: {d['diamonds']}\n\n"
        f"🛡️ Himoya: {d['himoya']}\n"
        f"⛑️ Qotildan himoya: {d['qotil_himoya']}\n"
        f"⚖️ Ovoz berishni himoya qilish: {d['ovoz_himoya']}\n"
        f"🔫 Miltiq: {d['miltiq']}\n\n"
        f"🎭 Maska: {d['maska']}\n"
        f"📁 Soxta hujjat: {d['soxta_hujjat']}\n"
        f"🃏 Keyingi o'yindagi rolingiz: -\n\n"
        f"🎯 Побед: {d['wins']}\n"
        f"🎲 Всего игр: {d['games']}"
    )
    return text

@bot.message_handler(commands=['start', 'profil', 'me'])
def show_pro_profile(message):
    text = get_pro_profile(message.from_user)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_shop = types.InlineKeyboardButton("Do'kon", callback_data="open_shop")
    btn_buy_cash = types.InlineKeyboardButton("Xarid qilish 💵", url="https://t.me/muwahhid_27")
    btn_buy_dia = types.InlineKeyboardButton("Xarid qilish 💎", url="https://t.me/muwahhid_27")
    btn_premium = types.InlineKeyboardButton("🎲 Premium guruhlar", callback_data="premium")
    btn_news = types.InlineKeyboardButton("↗️ Yangiliklar", url="https://t.me/muwahhid_27")
    
    markup.add(btn_shop)
    markup.add(btn_buy_cash, btn_buy_dia)
    markup.add(btn_premium)
    markup.add(btn_news)
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "open_shop")
def shop_handler(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_profile"))
    bot.edit_message_text("🛒 DO'KON\nBuyumlarni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_profile")
def back_to_profile(call):
    text = get_pro_profile(call.from_user)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Do'kon", callback_data="open_shop"))
    markup.add(types.InlineKeyboardButton("Xarid qilish 💵", url="https://t.me/muwahhid_27"), types.InlineKeyboardButton("Xarid qilish 💎", url="https://t.me/muwahhid_27"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

bot.infinity_polling()


            
