import telebot
import time
from deep_translator import GoogleTranslator
from urllib.parse import quote

# Sizning tokeningiz
TOKEN = '8375712759:AAEs2gGVWsLBz4Pv2mVnzLErMXX87pqVTiE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men rasm chizuvchi botman. 🎨\nO'zbekcha yozsangiz ham bo'ladi, men tushunaman!")

@bot.message_handler(func=lambda m: True)
def generate_art(message):
    try:
        # 1. Jarayon boshlanishi
        progress = bot.send_message(message.chat.id, "⌛ Boshladim... 0% [⬜⬜⬜⬜⬜]")
        
        # 2. O'zbekchadan inglizchaga tarjima
        translated = GoogleTranslator(source='auto', target='en').translate(message.text)
        safe_query = quote(translated) # Linkni xavfsiz qilish
        
        # 3. Progress bar animatsiyasi 🟩
        steps = [
            ("🧠 G'oya o'ylanmoqda... 40%", "[🟩🟩⬜⬜⬜]"),
            ("🎨 Rang berilmoqda... 80%", "[🟩🟩🟩🟩⬜]"),
            ("✅ Tayyor! 100%", "[🟩🟩🟩🟩🟩]")
        ]
        
        for text, bar in steps:
            time.sleep(0.6)
            bot.edit_message_text(f"{text}\n{bar}", message.chat.id, progress.message_id)

        # 4. Rasm yaratish linki (Har safar yangi rasm chiqishi uchun seed qo'shildi)
        seed = int(time.time())
        image_url = f"https://pollinations.ai/p/{safe_query}?width=1024&height=1024&seed={seed}"
        
        # 5. Natijani yuborish
        bot.send_photo(message.chat.id, image_url, caption=f"🖼 Natija: {message.text}\n\n✨ AI tushundi: {translated}")
        bot.delete_message(message.chat.id, progress.message_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik! Qayta urinib ko'ring.")

# Botni ishga tushirish
bot.polling(none_stop=True)
