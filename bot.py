
import telebot
from telebot import types
import threading
import os

# BOT SOZLAMALARI
TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6363297151  # @muwahhid_27

# Ma'lumotlar bazasi (Xotira)
user_data = {}

# Render serverini uxlab qolmasligi uchun (Port 10000)
def dummy_server():
    os.system("python3 -m http.server 10000")
threading.Thread(target=dummy_server, daemon=True).start()

def get_profile(user_id, name="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            'name': name, 'money': 1000, 'diamonds': 5, 
            'wins': 0, 'games': 0, 'himoya': 0, 'ovoz_himoya': 0,
            'soxta_hujjat': 0, 'maska': 0, 'tizimli_qasos': 0, 'faol_rol': 0
        }
    return user_data[user_id]

# --- 1. LICHKAGA XABAR YUBORISH ---
def send_role_to_private(player_id, role_name):
    try:
        text = (f"🎮 **Mafia Baku Black**\n\n"
                f"✅ Siz o'yinga omadli qo'shildingiz!\n"
                f"🎭 Sizning rolingiz: **{role_name}**\n\n"
                f"ℹ️ O'yin guruhda boshlanishini kuting.")
        bot.send_message(player_id, text, parse_mode='Markdown')
        return True
    except Exception as e:
        print(f"Xato: {e}")
        return False

# --- 2. DO'KON TIZIMI (XATOLAR TUZATILDI) ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def process_shop(call):
    u_id = call.from_user.id
    user = get_profile(u_id)
    item = call.data.split('_')[1]
    
    if item in ['himoya', 'ovoz', 'soxta', 'maska']:
        if user['money'] >= 150:
            user['money'] -= 150
            key = 'ovoz_himoya' if item == 'ovoz' else 'soxta_hujjat' if item == 'soxta' else item
            user[key] += 1
            bot.answer_callback_query(call.id, "Sotib olindi! ✅")
        else:
            bot.answer_callback_query(call.id, "Pul yetarli emas! ❌", show_alert=True)
    elif item in ['qasos', 'faol']:
        if user['diamonds'] >= 1:
            user['diamonds'] -= 1
            key = 'tizimli_qasos' if item == 'qasos' else 'faol_rol'
            user[key] += 1
            bot.answer_callback_query(call.id, "VIP xarid! 💎")
        else:
            bot.answer_callback_query(call.id, "Olmos yetarli emas! ❌", show_alert=True)

# --- 3. PUL O'TKAZMA VA 10% KOMISSIYA ---
@bot.message_handler(commands=['ber'])
def transfer_money(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "Pul o'tkazish uchun 'Reply' qiling!")
    
    try:
        amount = int(message.text.split()[1])
        if amount < 200:
            return bot.reply_to(message, "Minimal o'tkazma: 200 pul! ❌")
        
        sender = get_profile(message.from_user.id, message.from_user.first_name)
        if sender['money'] < amount:
            return bot.reply_to(message, "Mablag' yetarli emas!")

        tax = (amount // 200) * 20
        net = amount - tax
        
        receiver = get_profile(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
        admin = get_profile(ADMIN_ID)
        
        sender['money'] -= amount
        receiver['money'] += net
        admin['money'] += tax
        
        bot.reply_to(message, f"✅ O'tkazildi: {net}\n🏦 Komissiya (@muwahhid_27): {tax}")
    except Exception:
        bot.reply_to(message, "Format: /ber 200")

# --- 4. O'YIN YAKUNI VA TOP-3 MUKOFOTLASH ---
def finish_game(chat_id, players, winners, top_3):
    count = len(players)
    report = f"🏁 **O'YIN TUGADI!**\n🏆 G'oliblar: **{winners}**\n\n"
    
    for p_id in players:
        u = get_profile(p_id)
        u['games'] += 1
        prize = 500 if winners == "Yaxshilar" else 100
        u['money'] += prize
        
        d_bonus = ""
        if count >= 25 and p_id in top_3:
            u['diamonds'] += 1
            d_bonus = " + 1 💎"
        report += f"👤 {u['name']}: +{prize} 💵{d_bonus}\n"
    
    bot.send_message(chat_id, report, parse_mode='Markdown')

# PROFIL VA START
@bot.message_handler(commands=['profile', 'me', 'start'])
def profile(message):
    d = get_profile(message.from_user.id, message.from_user.first_name)
    text = (f"👤 {d['name']}\n\n💵 Dollar: {d['money']}\n💎 Olmos: {d['diamonds']}\n\n"
            f"🛡️ Himoya: {d['himoya']}\n⚖️ Ovoz himoyasi: {d['ovoz_himoya']}\n"
            f"🎭 Maska: {d['maska']}\n💣 Qasos: {d['tizimli_qasos']}")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Do'kon", callback_data="open_shop"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "open_shop")
def shop(call):
    markup = types.InlineKeyboardMarkup(row_width=1)

            
