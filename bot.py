import os
import telebot
import time
import requests
from deep_translator import GoogleTranslator

# Railway Variables bo'limidagi TOKEN ni oladi
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Salom! Men rasm chizuvchi botman. Menga xohlagan narsangizni yozing (o'zbekcha bo'lsa ham bo'ladi), men uni chizib beraman! 🎨")

@bot.message_handler(func=lambda m: True)
def generate_art(message):
    try:
        # 1. Progress bar boshlanishi
        progress_msg = bot.send_message(message.chat.id, "⌛ Jarayon boshlandi... 0% [⬜⬜⬜⬜⬜]")
        
        # 2. Tarjima qilish
        bot.edit_message_text("🔍 So'rovingiz tahlil qilinmoqda... 20% [🟩⬜⬜⬜⬜]", message.chat.id, progress_msg.message_id)
        translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)
        query = translated_text.replace(" ", "+")
        
        # 3. Progress bar davomi
        steps = [
            ("🧠 G'oya o'ylanmoqda... 40%", "[🟩🟩⬜⬜⬜]"),
            ("🎨 Ranglar tanlanmoqda... 60%", "[🟩🟩🟩⬜⬜]"),
            ("✨ Oxirgi ishlov berish... 80%", "[🟩🟩🟩🟩⬜]"),
            ("✅ Tayyor! 100%", "[🟩🟩🟩🟩🟩]")
        ]
        
        for text, bar in steps:
            time.sleep(0.8)
            bot.edit_message_text(f"{text}\n{bar}", message.chat.id, progress_msg.message_id)

        # 4. Rasm yaratish (Seed vaqtga qarab o'zgaradi, shunda rasm takrorlanmaydi)
        seed = int(time.time())
        image_url = f"https://pollinations.ai/p/{query}?width=1024&height=1024&seed={seed}"
        
        # 5. Natijani yuborish
        bot.send_photo(message.chat.id, image_url, caption=f"🖼 Natija: {message.text}\n\n✨ AI tushundi: {translated_text}")
        bot.delete_message(message.chat.id, progress_msg.message_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Kechirasiz, xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        print(f"Xato: {e}")

bot.polling(none_stop=True)
