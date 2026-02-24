import telebot
import time
import requests
from deep_translator import GoogleTranslator
from urllib.parse import quote

TOKEN = '8375712759:AAEs2gGVWsLBz4Pv2mVnzLErMXX87pqVTiE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def generate_image(message):
    try:
        chat_id = message.chat.id
        progress_msg = bot.reply_to(message, "⌛ Jarayon boshlandi... [⬜⬜⬜⬜⬜]")
        
        # 1. Tarjima
        bot.edit_message_text("🔍 Matn tarjima qilinmoqda... [🟩⬜⬜⬜⬜]", chat_id, progress_msg.message_id)
        translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)
        
        # 2. Link tayyorlash
        safe_prompt = quote(translated_text)
        seed = int(time.time())
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
        
        bot.edit_message_text("🎨 AI rasm chizmoqda (biroz kuting)... [🟩🟩🟩⬜⬜]", chat_id, progress_msg.message_id)
        
        # 3. Qayta urinish mexanizmi (Retry logic) 🔄
        success = False
        for i in range(3): # 3 marta urinib ko'radi
            check_response = requests.get(image_url)
            if check_response.status_code == 200:
                success = True
                break
            time.sleep(2) # 2 soniya kutib qaytadan urunadi
        
        if success:
            bot.edit_message_text("✅ Rasm tayyor! Yuborilmoqda... [🟩🟩🟩🟩🟩]", chat_id, progress_msg.message_id)
            bot.send_photo(chat_id, image_url, caption=f"🖼 **Sizning so'rovingiz:** {message.text}")
            bot.delete_message(chat_id, progress_msg.message_id)
        else:
            bot.edit_message_text("❌ AI serveri juda band. Keyinroq urinib ko'ring.", chat_id, progress_msg.message_id)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik: {str(e)}")

bot.polling(none_stop=True)
