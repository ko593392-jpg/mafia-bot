import telebot
from telebot import types
import threading
import os
import random

TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# Render uchun dummy server
def dummy_server():
    os.system("python3 -m http.server 10000")
threading.Thread(target=dummy_server, daemon=True).start()

games = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_add = types.InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{bot.get_me().username}?startgroup=true")
    markup.add(btn_add)
    bot.send_message(message.chat.id, "🔴 *MAFIA CLASSIC* — O'yinni boshlash uchun meni guruhga qo'shing!", parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['new'])
def new_game(message):
    chat_id = message.chat.id
    games[chat_id] = {'players': [], 'names': {}, 'status': 'registration'}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Qo'shilish", callback_data="join_game"))
    markup.add(types.InlineKeyboardButton("🚀 O'yinni boshlash", callback_data="start_logic"))
    bot.send_message(chat_id, "📢 *Yangi o'yin boshlanmoqda!*\n\nQatnashuvchilar kutilmoqda...", parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "join_game")
def join(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if user_id not in games[chat_id]['players']:
        games[chat_id]['players'].append(user_id)
        games[chat_id]['names'][user_id] = call.from_user.first_name
        bot.answer_callback_query(call.id, "Siz o'yinga qo'shildingiz!")
        players_list = "\n".join([f"👤 {i+1}. {games[chat_id]['names'][uid]}" for i, uid in enumerate(games[chat_id]['players'])])
        bot.edit_message_text(f"📢 *Yangi o'yin boshlanmoqda!*\n\n*Ro'yxat:*\n{players_list}", chat_id, call.message.message_id, parse_mode='Markdown', reply_markup=call.message.reply_markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_logic")
def start_logic(call):
    chat_id = call.message.chat.id
    players = games[chat_id]['players']
    if len(players) < 3: # Test uchun 3 kishi qildim
        bot.answer_callback_query(call.id, "Kamida 3 kishi bo'lishi kerak!", show_alert=True)
        return
    
    random.shuffle(players)
    roles = ['Mafia', 'Sherif', 'Aholi'] # Rollar ro'yxati
    # Rollarni taqsimlash
    for i, user_id in enumerate(players):
        role = roles[i] if i < len(roles) else 'Aholi'
        try:
            bot.send_message(user_id, f"🎭 Sizning rolingiz: *{role}*", parse_mode='Markdown')
        except:
            bot.send_message(chat_id, f"⚠️ {games[chat_id]['names'][user_id]} botga /start bosmagan, unga rol yuborib bo'lmadi!")

    bot.send_message(chat_id, "🎮 *O'yin boshlandi!* Rollar hamma o'yinchilarga shaxsiy xabar orqali yuborildi.")

bot.infinity_polling()
            
