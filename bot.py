import os
import telebot
import time

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def generate_art(message):
    query = message.text.replace(" ", "+") # Bo'shliqlarni + ga almashtiramiz
    
    # Progress bar xabari
    progress_msg = bot.send_message(message.chat.id, "⌛ Tayyorlanmoqda... 0% [⬜⬜⬜⬜⬜]")
    
    steps = [
        "20% [🟩⬜⬜⬜⬜]",
        "40% [🟩🟩⬜⬜⬜]",
        "60% [🟩🟩🟩⬜⬜]",
        "80% [🟩🟩🟩🟩⬜]",
        "100% [🟩🟩🟩🟩🟩]"
    ]
    
    for step in steps:
        time.sleep(1) # Har bir bosqich orasida 1 soniya kutish
        bot.edit_message_text(f"🎨 Rasm chizilmoqda... {step}", message.chat.id, progress_msg.message_id)

    # AI rasm linki
    image_url = f"https://pollinations.ai/p/{query}?width=1024&height=1024"
    
    # Tayyor rasmni yuboramiz va eski xabarni o'chiramiz
    bot.send_photo(message.chat.id, image_url, caption=f"✅ Natija: {message.text}")
    bot.delete_message(message.chat.id, progress_msg.message_id)

bot.polling(none_stop=True)

