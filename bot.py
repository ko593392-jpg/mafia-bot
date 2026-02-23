import telebot
from telebot import types
import threading
import os

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6363297151

user_data = {}

def get_profile(user_id, name="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            'id': user_id, 'name': name, 'money': 575, 'diamonds': 0,
            'himoya': 0, 'qotil_himoya': 0, 'ovoz_himoya': 0, 'miltiq': 0,
            'maska': 0, 'soxta_hujjat': 0, 'wins': 78, 'games': 335, 'xp': 0, 'lvl': 1
        }
    return user_data[user_id]

# --- 1. PROFIL DIZAYNI (1845.jpg NUSXASI) ---
@bot.message_handler(commands=['me', 'profil'])
def show_profile(message):
    u = get_profile(message.from_user.id, message.from_user.first_name)
    text = (f"⭐ <b>ID: {u['id']}</b>\n\n"
            f"👤 <b>{u['name']}</b>\n\n"
            f"💵 Dollar: {u['money']}\n"
            f"💎 Olmos: {u['diamonds']}\n\n"
            f"🛡️ Himoya: {u['himoya']}\n"
            f"⛑️ Qotildan himoya: {u['qotil_himoya']}\n"
            f"⚖️ Ovoz berishni himoya qilish: {u['ovoz_himoya']}\n"
            f"🔫 Miltiq: {u['miltiq']}\n\n"
            f"🎭 Maska: {u['maska']}\n"
            f"📁 Soxta hujjat: {u['soxta_hujjat']}\n"
            f"🃏 Keyingi o'yindagi rolingiz: -\n\n"
            f"🎯 Побед: {u['wins']}\n"
            f"🎲 Всего игр: {u['games']}")

    markup = types.InlineKeyboardMarkup(row_width=3)
    # ON/OFF tugmalari
    markup.add(
        types.InlineKeyboardButton("📁 - 🟢 ON", callback_data="none"),
        types.InlineKeyboardButton("🛡️ - 🟢 ON", callback_data="none"),
        types.InlineKeyboardButton("🎭 - 🟢 ON", callback_data="none")
    )
    markup.add(
        types.InlineKeyboardButton("⛑️ - 🟢 ON", callback_data="none"),
        types.InlineKeyboardButton("⚖️ - 🟢 ON", callback_data="none")
    )
    markup.add(types.InlineKeyboardButton("Do'kon", callback_data="shop"))
    markup.add(
        types.InlineKeyboardButton("Xarid qilish 💵", url="https://t.me/muwahhid_27"),
        types.InlineKeyboardButton("Xarid qilish 💎", url="https://t.me/muwahhid_27")
    )
    markup.add(types.InlineKeyboardButton("🎲 Premium guruhlar", url="https://t.me/muwahhid_27"))
    markup.add(types.InlineKeyboardButton("Yangiliklar ↗️", url="https://t.me/muwahhid_27"))

    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 2. START BOSILSA GURUHDA O'YIN BOSHLANISHI ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.chat.type != 'private':
        # Guruhda bo'lsa o'yinga qo'shilish xabari (1838.jpg dizayn)
        text = "<b>Mafia Baku Black 2</b>      admin\n"
        text += "<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
        text += "Ro'yxatdan o'tganlar:\n\n"
        text += f"<i>{message.from_user.first_name}</i>\n\n"
        text += "Jami 1ta odam."
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🤵 Qo'shilish", callback_data="join"))
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)
    else:
        # Lichkada bo'lsa profil

