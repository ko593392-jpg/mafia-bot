
import telebot
from telebot import types
import threading
import os

# --- SOZLAMALAR ---
TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

user_data = {}
players_in_game = [] # O'yindagi o'yinchilar ro'yxati

def get_profile(user_id, name="O'yinchi"):
    if user_id not in user_data:
        user_data[user_id] = {
            'id': user_id, 'name': name, 'money': 1000, 'diamonds': 5,
            'himoya': 0, 'qotil_himoya': 0, 'ovoz_himoya': 0, 'miltiq': 0,
            'maska': 0, 'soxta_hujjat': 0, 'wins': 0, 'games': 0
        }
    return user_data[user_id]

# --- 1. PROFIL (Faqat /me buyrug'i uchun) ---
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
    markup.add(
        types.InlineKeyboardButton("📁 - 🟢 ON", callback_data="none"),
        types.InlineKeyboardButton("🛡️ - 🟢 ON", callback_data="none"),
        types.InlineKeyboardButton("🎭 - 🟢 ON", callback_data="none")
    )
    markup.add(types.InlineKeyboardButton("Do'kon", callback_data="shop"))
    markup.add(types.InlineKeyboardButton("Yangiliklar ↗️", url="https://t.me/classic_mafia_news"))
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 2. START VA QO'SHILISH LOGIKASI ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.chat.type != 'private':
        # Guruhdagi ro'yxat (1851.jpg dizayni)
        names_list = ", ".join([f'<a href="tg://user?id={p["id"]}">{p["name"]}</a>' for p in players_in_game]) if players_in_game else "Hozircha hech kim yo'q"
        
        text = (f"<b>classic mafia</b> 🥷      admin\n"
                f"<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
                f"Ro'yxatdan o'tganlar:\n\n"
                f"{names_list}\n\n"
                f"Jami {len(players_in_game)}ta odam.")
        
        markup = types.InlineKeyboardMarkup()
        bot_username = bot.get_me().username
        markup.add(types.InlineKeyboardButton("🤵 Qo'shilish", url=f"https://t.me/{bot_username}?start=join_{message.chat.id}"))
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)
    else:
        # Lichkada o'yinga qo'shilish tasdig'i
        if "join" in message.text:
            u = get_profile(message.from_user.id, message.from_user.first_name)
            if u not in players_in_game:
                players_in_game.append(u)
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Guruhga qaytish", url="https://t.me/classic_mafia_news")) # Bu yerga guruhingiz linkini qo'ying
            bot.send_message(message.chat.id, "✅ <b>Siz o'yinga muvaffaqiyatli qo'shildingiz!</b>\n\nO'yin boshlanishini guruhda kuting.", parse_mode='HTML', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Xush kelibsiz! Guruhda o'yinni boshlash uchun /start buyrug'ini bering.")

# --- 3. ROLLAR TAVSIFI ---
@bot.message_handler(commands=['rollar', 'rules'])
def rules_handler(message):
    roles_text = (
        "<b>🎭 classic mafia - To'liq Rollar:</b>\n\n"
        "🕵️‍♂️ <b>Sherif:</b> Kechasi tekshiradi yoki otadi.\n"
        "👩‍⚕️ <b>Hamshira:</b> Bir marta o'zini qutqara oladi.\n"
        "🕵️ <b>Detektiv:</b> O'yinchilar aloqasini biladi.\n"
        "👨‍⚕️ <b>Doktor:</b> O'yinchilarni davolaydi.\n"
        "🤵 <b>Don:</b> Mafiyalar sardori.\n"
        "💃 <b>Kezuvchi:</b> O'yinchini band qiladi.\n"
        "🐺 <b>Bo'ri:</b> Yakka qotil.\n"
        "👮‍♂️ <b>Serjant:</b> Sherif o'rnini bosadi.\n"
        "🕴️ <b>Mafia:</b> Tinch aholi dushmani."
    )
    bot.send_message(message.chat.id, roles_text, parse_mode='HTML')

# --- RENDER PORT FIX ---
def dummy_server():
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"Alive")
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('', port), Handler).serve_forever()

threading.Thread(target=dummy_server, daemon=True).start()

if __name__ == "__main__":
    bot.set_my_commands([
        types.BotCommand("/profil", "Profil"),
        types.BotCommand("/rollar", "Rollar"),
        types.BotCommand("/top", "Reyting")
    ])
    bot.infinity_polling()
