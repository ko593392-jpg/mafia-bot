import telebot
from telebot import types
import threading
import os
import random

# --- SOZLAMALAR ---
TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# O'yin ma'lumotlari
players_in_game = [] 
game_chat_id = None

# --- 1. O'YIN RO'YXATINI BOSHLASH (/game) ---
@bot.message_handler(commands=['game'])
def start_registration(message):
    global players_in_game, game_chat_id
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "O'yinni guruhda boshlang!")
        return
    
    players_in_game = [] 
    game_chat_id = message.chat.id
    
    text = (f"<b>classic mafia</b> 🥷      admin\n"
            f"<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
            f"Ro'yxatdan o'tganlar: Hozircha hech kim yo'q\n\n"
            f"Jami 0ta odam.")
    
    markup = types.InlineKeyboardMarkup()
    bot_username = bot.get_me().username
    markup.add(types.InlineKeyboardButton("🤵 Qo'shilish", url=f"https://t.me/{bot_username}?start=join"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 2. LICHKADA QO'SHILISH VA GURUHNI YANGILASH (/start) ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    global players_in_game, game_chat_id
    
    # Lichkada o'yinga qo'shilish
    if message.chat.type == 'private' and "join" in message.text:
        user_info = {'id': message.from_user.id, 'name': message.from_user.first_name}
        
        if not any(p['id'] == user_info['id'] for p in players_in_game):
            players_in_game.append(user_info)
            
            # Guruhga qaytish tugmasi (1849.jpg dagi kabi)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Guruhga qaytish", url="https://t.me/classic_mafia_news"))
            
            bot.send_message(message.chat.id, "✅ <b>Siz o'yinga muvaffaqiyatli qo'shildingiz!</b>\n\nO'yin boshlanishini guruhda kiting.", 
                             parse_mode='HTML', reply_markup=markup)
            
            # Guruhdagi ro'yxatni yangilash (1851.jpg dagi kabi profil linki bilan)
            if game_chat_id:
                names_list = ", ".join([f'<a href="tg://user?id={p["id"]}">{p["name"]}</a>' for p in players_in_game])
                update_text = (f"<b>classic mafia</b> 🥷      admin\n"
                               f"<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
                               f"Ro'yxatdan o'tganlar:\n\n"
                               f"{names_list}\n\n"
                               f"Jami {len(players_in_game)}ta odam.")
                
                markup_join = types.InlineKeyboardMarkup()
                markup_join.add(types.InlineKeyboardButton("🤵 Qo'shilish", url=f"https://t.me/{bot.get_me().username}?start=join"))
                bot.send_message(game_chat_id, update_text, parse_mode='HTML', reply_markup=markup_join)
        return

    # Gur
