import telebot
import requests
from urllib.parse import quote

# Sizning tokeningiz
TOKEN = '8375712759:AAEs2gGVWsLBz4Pv2mVnzLErMXX87pqVTiE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def draw(message):
    try:
        # Progress bar
        wait_msg = bot.reply_to(message, "🎨 Chizyapman... [🟩🟩⬜⬜⬜]")
        
        # Linkni tayyorlash
        query = quote(message.text)
        image_url = f"https://pollinations.ai/p/{query}?width=1024&height=1024&seed=123"
        
        # Rasmni yuborish
        bot.send_photo(message.chat.id, image_url, caption="✅ Tayyor!")
        bot.delete_message(message.chat.id, wait_msg.message_id)
    except Exception as e:
        bot.reply_to(message, "Xatolik bo'ldi!")

bot.polling(none_stop=True)



