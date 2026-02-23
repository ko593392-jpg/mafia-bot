import telebot
from telebot import types
import threading
import os

# --- SOZLAMALAR ---
TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6363297151

user_data = {}

def get_profile(user_id, name="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            'name': name, 'money': 1000, 'diamonds': 5, 'xp': 0, 'lvl': 1,
            'wins': 0, 'games': 0, 'himoya': 0, 'ovoz_himoya': 0, 
            'maska': 0, 'soxta_hujjat': 0, 'tizimli_qasos': 0, 'faol_rol': 0
        }
    return user_data[user_id]

# --- LEGENDA DARAJALARI ---
def get_lvl_title(lvl):
    if lvl <= 10: return f"Sarbast [L:{lvl}]"
    elif lvl <= 25: return f"⚔️ Ritsar [L:{lvl}]"
    elif lvl <= 45: return f"🛡️ Gvardiya [L:{lvl}]"
    elif lvl <= 70: return f"⚡ Mif [L:{lvl}]"
    elif lvl <= 100: return f"🔱 Boqiy [L:{lvl}]"
    elif lvl <= 150: return f"👑 Hukmron [L:{lvl}]"
    else: return f"🌌 Legenda [L:{lvl}]"

# --- PROFIL VA LICHKA (PREMIUM & YANGILIKLAR) ---
@bot.message_handler(commands=['start', 'profile', 'me'])
def profile_handler(message):
    u_id = message.from_user.id
    u = get_profile(u_id, message.from_user.first_name)
    title = get_lvl_title(u['lvl'])
    
    text = (f"👤 <b>{u['name']}</b>\n"
            f"🎖 Maqom: {title}\n"
            f"📈 XP: {u['xp']}/{(u['lvl']*1000)}\n\n"
            f"💵 Dollar: {u['money']}\n"
            f"💎 Olmos: {u['diamonds']}\n\n"
            f"🛡️ Himoya: {u['himoya']} | 🎭 Maska: {u['maska']}\n"
            f"📁 Hujjat: {u['soxta_hujjat']} | 💣 Qasos: {u['tizimli_qasos']}")

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💎 Premium Guruhlar", url="https://t.me/muwahhid_27"),
        types.InlineKeyboardButton("↗️ Yangiliklar", url="https://t.me/muwahhid_27")
    )
    markup.add(types.InlineKeyboardButton("🛒 Do'kon", callback_data="open_shop"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- PUL O'TKAZISH (10% SOLIQ) ---
@bot.message_handler(commands=['ber'])
def transfer_money(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "Pul berish uchun 'Reply' qiling!")
    try:
        amount = int(message.text.split()[1])
        if amount < 200:
            return bot.reply_to(message, "Minimal o'tkazma: 200! ❌")
        
        sender = get_profile(message.from_user.id, message.from_user.first_name)
        if sender['money'] < amount:
            return bot.reply_to(message, "Mablag' yetarli emas!")

        tax = (amount // 200) * 20
        net = amount - tax
        
        receiver = get_profile(message.reply_to_message.from_user.id)
        admin = get_profile(ADMIN_ID)
        
        sender['money'] -= amount
        receiver['money'] += net
        admin['money'] += tax
        
        bot.reply_to(message, f"✅ O'tkazildi: {net}\n🏦 Soliq (@muwahhid_27): {tax}")
    except Exception:
        bot.reply_to(message, "Format: /ber 200")

# --- O'YIN DIZAYNLARI (RASMLAR ASOSIDA) ---
@bot.message_handler(commands=['reg'])
def start_reg(message):
    # Test uchun 1 ta o'yinchi bilan dizayn
    players = [message.from_user.id]
    text = "<b>Mafia Baku Black 2</b>      admin\n"
    text += "<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
    text += "Ro'yxatdan o'tganlar:\n\n"
    names = [f"<i>{get_profile(p)['name']}</i>" for p in players]
    text += ", ".join(names)
    text += f"\n\nJami {len(players)}ta odam."
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤵 Qo'shilish", callback_data="join"))
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- DO'KON ---
@bot.callback_query_handler(func=lambda call: call.data == "open_shop")
def shop_callback(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛡️ Himoya (150 💵)", callback_data="buy_himoya"),
        types.InlineKeyboardButton("💣 Qasos (1 💎)", callback_data="buy_qasos")
    )
    bot.edit_message_text("🛒 <b>DO'KON</b>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='HTML')

# --- RENDER UCHUN SERVER ---
def dummy_server():
    os.system("python3 -m http.server 10000")

threading.Thread(target=dummy_server, daemon=True).start()

if __name__ == "__main__":
    bot.infinity_polling()
