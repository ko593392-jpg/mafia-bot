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
        
        # 2. Jarayon boshlanganini bildirish (Progress Bar) 🟩
        progress_msg = bot.reply_to(message, "⌛ Jarayon boshlandi: 10% [⬜⬜⬜⬜⬜]")
        
        # 3. Matnni ingliz tiliga tarjima qilish (AI inglizchani yaxshi tushunadi)
        bot.edit_message_text("🔍 Matn tarjima qilinmoqda... 30% [🟩⬜⬜⬜⬜]", message.chat.id, progress_msg.message_id)
        translated_text = GoogleTranslator(source='auto', target='en').translate(user_text)
        
        # 4. Linkni xavfsiz shaklga keltirish (Simvollar va bo'shliqlarni to'g'irlash)
        safe_prompt = quote(translated_text)
        
        # 5. Har safar yangi rasm chiqishi uchun tasodifiy son (seed) yaratish
        seed = int(time.time())
        
        # 6. AI uchun to'g'ri va to'liq linkni shakllantirish
        # image.pollinations.ai - eng barqaror server
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
        
        # 7. Progress barni yakunlash
        bot.edit_message_text("🎨 Rasm chizilmoqda... 70% [🟩🟩🟩⬜⬜]", message.chat.id, progress_msg.message_id)
        time.sleep(1) # Foydalanuvchi ko'rishi uchun ozgina kutish
        bot.edit_message_text("✅ Tayyor bo'ldi! 100% [🟩🟩🟩🟩🟩]", message.chat.id, progress_msg.message_id)
        
        # 8. Rasmni Telegramga yuborish
        bot.send_photo(
            message.chat.id, 
            image_url, 
            caption=f"🖼 **Sizning so'rovingiz:** {user_text}\n✨ **AI tushunishi:** {translated_text}",
            parse_mode="Markdown"
        )
        
        # 9. Progress xabarini o'chirib tashlash (ekran toza turishi uchun)
        bot.delete_message(message.chat.id, progress_msg.message_id)

    except Exception as e:
        # Xatolik yuz bersa xabar berish
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {str(e)}")

# 🔄 Botni tinimsiz ishlashini ta'minlash
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
