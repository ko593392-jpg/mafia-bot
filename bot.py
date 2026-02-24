import os
import telebot
import time
from deep_translator import GoogleTranslator

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def generate_art(message):
    try:
        # 1. Progress bar boshlanishi 🟩
        progress_msg = bot.send_message(message.chat.id, "⌛ Tayyorlanmoqda... 0% [⬜⬜⬜⬜⬜]")
        
        # 2. Tarjima qilish (avtomatik)
        translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)
        
        # LINK UCHUN MATNNI TOZALASH (MUHIM QISM!)
        # Bo'shliqlarni %20 ga almashtiramiz, shunda link buzilmaydi
        clean_query = translated_text.replace(" ", "%20")
        
        # 3. Progress bar animatsiyasi
        steps = ["20% [🟩⬜⬜⬜⬜]", "60% [🟩🟩🟩⬜⬜]", "100% [🟩🟩🟩🟩🟩]"]
        for step in steps:
            time.sleep(0.5)
            bot.edit_message_text(f"🎨 Chizilmoqda... {step}", message.chat.id, progress_msg.message_id)

        # 4. TO'G'RI RASM LINKI
        seed = int(time.time())
        image_url = f"https://pollinations.ai/p/{clean_query}?width=1024&height=1024&seed={seed}"
        
        # 5. Rasmni yuborish
        bot.send_photo(message.chat.id, image_url, caption=f"✅ Natija: {message.text}\n✨ AI tushundi: {translated_text}")
        bot.delete_message(message.chat.id, progress_msg.message_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik! Qayta urinib ko'ring.")

bot.polling(none_stop=True)
