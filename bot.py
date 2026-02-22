import telebot
from telebot import types
import threading
import os

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# Render uchun portni band qilish
def dummy_server():
    os.system("python3 -m http.server 10000")

threading.Thread(target=dummy_server, daemon=True).start()

# O'yin holatini saqlash uchun lug'at
games = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_add = types.InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{bot.get_me().username}?startgroup=true")
    markup.add(btn_add)
    
    bot.send_message(
        message.chat.id, 
        "🔴 *MAFIA CLASSIC* — O'yinni boshlash uchun meni guruhga qo'shing va admin qiling!", 
        parse_mode='Markdown', 
        reply_markup=markup
    )

@bot.message_handler(commands=['new'])
def new_game(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "Bu buyruq faqat guruhlarda ishlaydi!")
        return

    chat_id = message.chat.id
    games[chat_id] = {'players': [], 'status': 'registration'}
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Qo'shilish", callback_data="join_game"))
    
    bot.send_message(
        chat_id, 
        "📢 *Yangi o'yin boshlanmoqda!*\n\nO'yinda qatnashish uchun quyidagi tugmani bosing.", 
        parse_mode='Markdown', 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "join_game")
def join(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    if chat_id not in games:
        bot.answer_callback_query(call.id, "O'yin topilmadi.")
        return

    if user_id not in games[chat_id]['players']:
        games[chat_id]['players'].append(user_id)
        bot.answer_callback_query(call.id, "Siz o'yinga qo'shildingiz!")
        
        # O'yinchilar ro'yxatini yangilash
        players_list = "\n".join([f"👤 {i+1}. {user_name}" for i, uid in enumerate(games[chat_id]['players'])])
        bot.edit_message_text(
            f"📢 *Yangi o'yin boshlanmoqda!*\n\n*Ro'yxat:*\n{players_list}\n\nKamida 4 kishi kerak.", 
            chat_id, 
            call.message.message_id, 
            parse_mode='Markdown', 
            reply_markup=call.message.reply_markup
        )
    else:
        bot.answer_callback_query(call.id, "Siz allaqachon ro'yxatdasiz.")

print("Mafia Baku uslubidagi bot ishga tushdi...")
bot.infinity_polling()
