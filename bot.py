
    
    import telebot
from telebot import types
import threading
import os

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6363297151 # @muwahhid_27

user_data = {}

def get_profile(user_id, name="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            'name': name, 'money': 1000, 'diamonds': 5, 'xp': 0, 'lvl': 1,
            'wins': 0, 'games': 0, 'himoya': 0, 'ovoz_himoya': 0, 
            'maska': 0, 'soxta_hujjat': 0, 'tizimli_qasos': 0, 'faol_rol': 0
        }
    return user_data[user_id]

# --- LEVEL VA LEGENDA (IXCHAM) ---
def get_lvl_title(lvl):
    if lvl <= 10: return f"Sarbast [L:{lvl}]"
    if lvl <= 25: return f"⚔️ Ritsar [L:{lvl}]"
    if lvl <= 45: return f"🛡️ Gvardiya [L:{lvl}]"
    if lvl <= 70: return f"⚡ Mif [L:{lvl}]"
    if lvl <= 100: return f"🔱 Boqiy [L:{lvl}]"
    if lvl <= 150: return f"👑 Hukmron [L:{lvl}]"
    return f"🌌 Legenda [L:{lvl}]"

# --- 1. PROFIL VA ASOSIY MENYU ---
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
            f"🛡️ Himoya: {u['himoya']}\n"
            f"⚖️ Ovoz himoyasi: {u['ovoz_himoya']}\n"
            f"🎭 Maska: {u['maska']}\n"
            f"📁 Soxta hujjat: {u['soxta_hujjat']}\n"
            f"💣 Qasos: {u['tizimli_qasos']}\n"
            f"⚡ Faol rol: {u['faol_rol']}")

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🛒 Do'kon", callback_data="open_shop"))
    markup.add(
        types.InlineKeyboardButton("💎 Premium Guruhlar", url="https://t.me/muwahhid_27"),
        types.InlineKeyboardButton("↗️ Yangiliklar", url="https://t.me/muwahhid_27")
    )
    markup.add(
        types.InlineKeyboardButton("Xarid qilish 💵", url="https://t.me/muwahhid_27"),
        types.InlineKeyboardButton("Xarid qilish 💎", url="https://t.me/muwahhid_27")
    )
    
    # Agar lichkada bo'lsa shaxsiy xabar yuborish
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 2. PUL O'TKAZISH (200 MIN, 10% SOLIQ) ---
@bot.message_handler(commands=['ber'])
def transfer_money(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "Pul berish uchun foydalanuvchi xabariga 'Reply' qiling!")
    
    try:
        amount = int(message.text.split()[1])
        if amount < 200:
            return bot.reply_to(message, "Minimal o'tkazma: 200 pul! ❌")
        
        sender = get_profile(message.from_user.id, message.from_user.first_name)
        if sender['money'] < amount:
            return bot.reply_to(message, "Mablag' yetarli emas! ❌")

        tax = (amount // 200) * 20
        net = amount - tax
        
        receiver = get_profile(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
        admin = get_profile(ADMIN_ID)
        
        sender['money'] -= amount
        receiver['money'] += net
        admin['money'] += tax # Komissiya @muwahhid_27 ga tushadi
        
        bot.reply_to(message, f"✅ O'tkazildi: {net}\n🏦 Komissiya (@muwahhid_27): {tax}")
    except:
        bot.reply_to(message, "Format: /ber 200")

# --- 3. RO'YXATDAN O'TISH DIZAYNI (1838.jpg) ---
def start_reg_design(chat_id, players):
    text = "<b>Mafia Baku Black 2</b>      admin\n"
    text += "<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
    text += "Ro'yxatdan o'tganlar:\n\n"
    names = [f"<i>{get_profile(p)['name']}</i>" for p in players]
    text += ", ".join(names)
    text += f"\n\nJami {len(players)}ta odam."
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤵 Qo'shilish", callback_data="join"))
    bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=markup)

# --- 4. O'YIN TUGASHI VA 25 KISHILIK BONUS (1837.jpg) ---
def game_end_report(chat_id, winners, others, top_3):
    count = len(winners) + len(others)
    text = "<b>O'yin tugadi!</b>\n\n<b>G'oliblar:</b>\n"
    
    for i, (p_id, role) in enumerate(winners, 1):
        u = get_profile(p_id)
        u['money'] += 500
        u['xp'] += 50
        bonus_d = ""
        if count >= 25 and p_id in top_3:
            u['diamonds'] += 1
            bonus_d = " + 1 💎"
        text += f"{i}. {u['name']} - {role}{bonus_d}\n"

    text += "\n<b>Qolgan o'yinchilar:</b>\n"
    for i, (p_id, role) in enumerate(others, len(winners)+1):
        u = get_profile(p_id)
        u['money'] += 100
        u['xp'] += 10
        text += f"{i}. {u['name']} - {role}\n"
        
    bot.send_message(chat_id, text, parse_mode='HTML')

# --- DO'KON ---
@bot.callback_query_handler(func=lambda call: call.data == "open_shop")
def shop(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛡️ Himoya (150 💵)", callback_data="buy_himoya"),
        types.InlineKeyboardButton("🎭 Maska (150 💵)", callback_data="buy_maska"),
        types.InlineKeyboardButton("💣 Qasos (1 💎)", callback_data="buy_qasos")
    )
    bot.edit_message_text("🛒 <b>DO'KON</b>\nSotib olishni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='HTML')

# --- RENDER DUMMY SERVER ---
def dummy():
    os.system("python3 -m http.server 10000")
threading.Thread(target=dummy, daemon=True).start()

bot.infinity_polling()
