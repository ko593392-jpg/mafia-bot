import os
import telebot
import time
from deep_translator import GoogleTranslator
from urllib.parse import quote  # Linkni xavfsiz qilish uchun

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def generate_art(message):
    try:
        # 1. Progress bar (Siz aytgan yashil kvadratchalar) 🟩
        progress_msg = bot.send_message(message.chat.id, "⌛ Boshladim... 0% [⬜⬜⬜⬜⬜]")
        
        # 2. Avtomatik tarjima
        translated = GoogleTranslator(source='auto', target='en').translate(message.text)
        
        # 3. Linkni AI tushunadigan formatga keltirish (MUHIM!)
        # Bu qator so'zlarni linkka xavfsiz joylaydi
        safe_query = quote(translated)
        
        # Progress bar animatsiyasi
        steps = ["40% [🟩🟩⬜⬜⬜]", "80% [🟩🟩🟩🟩⬜]", "100% [🟩🟩🟩🟩🟩]"]
        for step in steps:
            time.sleep(0.5)
            bot.edit_message_text(f"🎨 Chizilmoqda... {step}", message.chat.id, progress_msg.message_id)

        # 4. Rasm manzili (Har safar yangi rasm chiqishi uchun seed qo'shildi)
        seed = int(time.time())
        image_url = f"https://pollinations.ai/p/{safe_query}?width=1024&height=1024&seed={seed}"
        
        # 5. Rasmni yuborish
        bot.send_photo(message.chat.id, image_url, caption=f"✅ Natija: {message.text}\n✨ AI tushundi: {translated}")
        bot.delete_message(message.chat.id, progress_msg.message_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik! Qayta urinib ko'ring.")

bot.polling(none_stop=True)
