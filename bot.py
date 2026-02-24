import telebot
import time
import requests
from deep_translator import GoogleTranslator
from urllib.parse import quote

# 🔑 Sizning Telegram Bot Tokeningiz
TOKEN = '8375712759:AAEs2gGVWsLBz4Pv2mVnzLErMXX87pqVTiE'
bot = telebot.TeleBot(TOKEN)

# 🎨 Rasm chizish funksiyasi
@bot.message_handler(func=lambda m: True)
def generate_image(message):
    try:
        # 1. Foydalanuvchi yuborgan matnni olish
        user_text = message.text
        chat_id = message.chat.id
        
        # 2. Jarayon boshlanganini bildirish ⌛
        progress_msg = bot.reply_to(message, "⌛ Jarayon boshlandi... [⬜⬜⬜⬜⬜]")
        
        # 3. Matnni ingliz tiliga tarjima qilish 🔍
        bot.edit_message_text("🔍 Matn tarjima qilinmoqda... [🟩⬜⬜⬜⬜]", chat_id, progress_msg.message_id)
        try:
            translated_text = GoogleTranslator(source='auto', target='en').translate(user_text)
        except:
            translated_text = user_text # Tarjima o'xshamasa o'zini qoldiradi
        
        # 4. Linkni shakllantirish (Eng ishonchli variant) ✅
        safe_prompt = quote(translated_text)
        seed = int(time.time()) # Har safar yangi rasm chiqishi uchun
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
        
        # 5. Rasm tayyor bo'lishini kutish (HTTP 400 xatosini oldini olish uchun) 🎨
        bot.edit_message_text("🎨 AI rasm chizmoqda... [🟩🟩🟩⬜⬜]", chat_id, progress_msg.message_id)
        
        # Telegram rasmga ulanishidan oldin AI serveriga so'rov yuborib rasm borligini tekshiramiz
        check_response = requests.get(image_url)
        
        if check_response.status_code == 200:
            bot.edit_message_text("✅ Rasm tayyor! Yuborilmoqda... [🟩🟩🟩🟩🟩]", chat_id, progress_msg.message_id)
            
            # 6. Rasmni yuborish
            bot.send_photo(
                chat_id, 
                image_url, 
                caption=f"🖼 **Sizning so'rovingiz:** {user_text}\n✨ **AI tushunishi:** {translated_text}",
                parse_mode="Markdown"
            )
            bot.delete_message(chat_id, progress_msg.message_id)
        else:
            bot.edit_message_text("❌ AI serveri javob bermadi. Qaytadan urinib ko'ring.", chat_id, progress_msg.message_id)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik yuz berdi: {str(e)}")

# 🔄 Botni tinimsiz ishga tushirish
if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi!")
    bot.polling(none_stop=True)
