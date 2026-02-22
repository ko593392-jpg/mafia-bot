
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

# --- 1. LICHKAGA XABAR VA ROL TARQATISH ---
def send_role_to_private(player_id, role_name):
    try:
        text = (f"🎮 **Mafia Baku Black**\n\n"
                f"✅ Siz o'yinga omadli qo'shildingiz!\n"
                f"🎭 Sizning rolingiz: **{role_name}**\n\n"
                f"ℹ️ O'yin guruhda boshlanishini kuting.")
        bot.send_message(player_id, text, parse_mode='Markdown')
        return True
    except:
        return False

# --- 2. DO'KON TIZIMI ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def process_shop(call):
    u_id = call.from_user.id
    user = get_profile(u_id)
    item = call.data.split('_')[1]
    
    # 150 pullik narsalar
    if item in ['himoya', 'ovoz', 'soxta', 'maska']:
        if user['money'] >= 150:
            user['money'] -= 150
            key = 'ovoz_himoya' if item == 'ovoz' else 'soxta_hujjat' if item == 'soxta' else item
            user[key] += 1
            bot.answer_callback_query(call.id, "Sotib olindi! ✅ (150 pul)")
        else:
            bot.answer_callback_query(call.id, "Mablag' yetarli emas! ❌", show_alert=True)
            
    # 1 almazlik narsalar
    elif item in ['qasos', 'faol']:
        if user['diamonds'] >= 1:
            user['diamonds'] -= 1
            key = 'tizimli_qasos' if item == 'qasos' else 'faol_rol'
            user[key] += 1
            bot.answer_callback_query(call.id, "VIP xarid bajarildi! 💎 (1 almaz)")
        else:
            bot.answer_callback_query(call.id, "Olmos yetarli emas! 💎❌", show_alert=True)

# --- 3. PUL O'TKAZMA VA 10% KOMISSIYA ---
@bot.message_handler(commands=['ber'])
def transfer_money(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "Pul o'tkazish uchun foydalanuvchi xabariga 'Reply' qiling!")
    
    try:
        args = message.text.split()
        amount = int(args[1])
        if amount < 200:
            return bot.reply_to(message, "Minimal o'tkazma: 200 pul! ❌")
        
        sender = get_profile

            
