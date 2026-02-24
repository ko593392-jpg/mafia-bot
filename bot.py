import os
import telebot
import time
from deep_translator import GoogleTranslator # Tarjimonni qo'shdik

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def generate_art(message):
    # 1. O'zbekcha matnni inglizchaga o'giramiz
    try:
        translated_text = GoogleTranslator(source='uz', target='en').translate(message.text)
    except:
        translated_text = message.text # Agar xato bo'lsa, borini yuboradi

    query = translated_text.replace(" ", "+")
    
    # Progress bar (siz aytgan 5 bosqich) 🟩
    progress_msg = bot.send_message(message.chat.id, "⌛ Tayyorlanmoqda... 0% [⬜⬜⬜⬜⬜]")
    
    steps = [
        "20% [🟩⬜⬜⬜⬜]", "40% [🟩🟩⬜⬜⬜]", "60% [🟩🟩🟩⬜⬜]", 
        "80% [🟩🟩🟩🟩⬜]", "100% [🟩🟩🟩🟩🟩]"
    ]
    
    for step in steps:
        time.sleep(0.5)
        bot.edit_message_text(f"🎨 Rasm chizilmoqda... {step}", message.chat.id, progress_msg.message_id)

    # 2. AI rasm linki (endi inglizcha matn bilan!)
    image_url = f"https://pollinations.ai/p/{query}?width=1024&height=1024&seed={time.time()}"
    
    bot.send_photo(message.chat.id, image_url, caption=f"✅ Natija: {message.text}")
    bot.delete_message(message.chat.id, progress_msg.message_id)

bot.polling(none_stop=True)
