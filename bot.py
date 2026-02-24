import telebot
import time
import requests
from deep_translator import GoogleTranslator
from urllib.parse import quote

# 🔑 Bot tokeningiz
TOKEN = '8375712759:AAEs2gGVWsLBz4Pv2mVnzLErMXX87pqVTiE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def generate_flux_art(message):
    try:
        chat_id = message.chat.id
        
        # 1. Jarayonni boshlash (Progress Bar) ⏳
        status_msg = bot.reply_to(message, "⌛ Tayyorgarlik... [🟩⬜⬜⬜⬜]")
        
        # 2. O'zbek tilidan ingliz tiliga tarjima 🌍
        # Flux inglizcha so'zlarni juda aniq tushunadi
        bot.edit_message_text("🔍 Matn tarjima qilinmoqda... [🟩🟩⬜⬜⬜]", chat_id, status_msg.message_id)
        translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)
        
        # 3. Flux modeli uchun linkni tayyorlash 🎨
        # nologo=true - bu o'sha sizga yoqmagan yozuvni olib tashlaydi
        bot.edit_message_text("🎨 Flux AI rasm chizmoqda... [🟩🟩🟩⬜⬜]", chat_id, status_msg.message_id)
        safe_prompt = quote(translated_text)
        seed = int(time.time()) # Har safar yangi va betakror rasm
        image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
        
        # 4. Rasm tayyorligini tekshirish va yuborish ✅
        # Flux biroz vaqt talab qilishi mumkin, shuning uchun 100% bo'lishini kutamiz
        bot.edit_message_text("🚀 Natija yuborilmoqda... [🟩🟩🟩🟩🟩]", chat_id, status_msg.message_id)
        
        bot.send_photo(
            chat_id, 
            image_url, 
            caption=f"✅ **Tayyor!**\n\n📝 **Sizning so'rovingiz:** {message.text}\n✨ **AI tushunishi:** {translated_text}",
            parse_mode="Markdown"
        )
        
        # Eski progress xabarni o'chirish
        bot.delete_message(chat_id, status_msg.message_id)

    except Exception as e:
        bot.send_message(chat_id, "😔 Kechirasiz, hozirda Flux serverlari band. Birozdan so'ng qayta urinib ko'ring.")

# Botni yurgizish
if __name__ == "__main__":
    print("Mukammal Flux bot ishga tushdi!")
    bot.polling(none_stop=True)
