
import telebot
from telebot import types
import threading
import os
import random

# --- SOZLAMALAR ---
TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

# O'yin holati va o'yinchilar
players_in_game = [] 

def get_profile(user_id, name="O'yinchi"):
    # Foydalanuvchi ma'lumotlari (1847.jpg dizayni uchun xizmat qiladi)
    return {'id': user_id, 'name': name}

# --- 1. RO'YXATDAN O'TISHNI BOSHLASH (/game) ---
@bot.message_handler(commands=['game'])
def start_registration(message):
    global players_in_game
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "O'yinni guruhda boshlang!")
        return
    
    players_in_game = [] # Yangi o'yin uchun ro'yxatni tozalash
    
    text = (f"<b>classic mafia</b> 🥷      admin\n"
            f"<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
            f"Ro'yxatdan o'tganlar: Hozircha hech kim yo'q\n\n"
            f"Jami 0ta odam.")
    
    markup = types.InlineKeyboardMarkup()
    bot_username = bot.get_me().username
    markup.add(types.InlineKeyboardButton("🤵 Qo'shilish", url=f"https://t.me/{bot_username}?start=join_{message.chat.id}"))
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 2. LICHKADA QO'SHILISH VA GURUHNI YANGILASH ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    global players_in_game
    
    # Lichkada qo'shilishni tasdiqlash
    if message.chat.type == 'private' and "join_" in message.text:
        chat_id = message.text.split("_")[1]
        user_info = {'id': message.from_user.id, 'name': message.from_user.first_name}
        
        if not any(p['id'] == user_info['id'] for p in players_in_game):
            players_in_game.append(user_info)
            
            markup = types.InlineKeyboardMarkup()
            # Guruhga qaytish tugmasi
            markup.add(types.InlineKeyboardButton("⬅️ Guruhga qaytish", url=f"https://t.me/c/{(str(chat_id).replace('-100',''))}"))
            
            bot.send_message(message.chat.id, "✅ <b>Siz o'yinga muvaffaqiyatli qo'shildingiz!</b>\nO'yin boshlanishini guruhda kuting.", 
                             parse_mode='HTML', reply_markup=markup)
            
            # Guruhdagi ro'yxatni yangilash (1851.jpg dizayni)
            names_list = ", ".join([f'<a href="tg://user?id={p["id"]}">{p["name"]}</a>' for p in players_in_game])
            update_text = (f"<b>classic mafia</b> 🥷      admin\n"
                           f"<b>Ro'yxatdan o'tish davom etmoqda</b>\n"
                           f"Ro'yxatdan o'tganlar:\n\n"
                           f"{names_list}\n\n"
                           f"Jami {len(players_in_game)}ta odam.")
            
            markup_join = types.InlineKeyboardMarkup()
            markup_join.add(types.InlineKeyboardButton("🤵 Qo'shilish", url=f"https://t.me/{bot.get_me().username}?start=join_{chat_id}"))
            
            # Oxirgi xabarni tahrirlash o'rniga yangi xabar yuborsa ham bo'ladi, lekin tahrirlash tozirroq
            try:
                bot.send_message(chat_id, update_text, parse_mode='HTML', reply_markup=markup_join)
            except:
                pass
        return

    # Guruhda /start bosilganda o'yinni boshlash
    if message.chat.type != 'private':
        if len(players_in_game) >= 2: # Kamida 2 kishi bo'lsa
            start_real_game(message.chat.id)
        else:
            bot.send_message(message.chat.id, "O'yinni boshlash uchun kamida 2 kishi ro'yxatdan o'tishi kerak!")

# --- 3. O'YINNI BOSHLASH VA ROLLARNI TARQATISH ---
def start_real_game(chat_id):
    bot.send_message(chat_id, "<b>O'yin boshlandi! Rollar tarqatilmoqda...</b> 🌙", parse_mode='HTML')
    
    # Barcha rollar (1836.jpg va 1837.jpg asosida)
    all_roles =
