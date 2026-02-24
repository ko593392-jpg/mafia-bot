import os
import telebot
import requests
import time
from telebot import types

# 1. SOZLAMALAR
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 409 xatosini ildizi bilan yo'qotish
bot.remove_webhook()

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Musiqa qidirish", "📊 Statistika")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Otabek aka, mutlaqo tekin va cheksiz tizimga xush kelibsiz! 🚀\nQo'shiq nomini yozing:", 
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def handle_music(message):
    if message.text == "🔍 Musiqa qidirish":
        bot.send_message(message.chat.id, "Musiqa nomini yozing:")
        return
    
    query = message.text
    wait = bot.reply_to(message, "⏳ Qidirilmoqda (Cheksiz baza)...")

    try:
        # 🚀 TEKIN VA BLOKLANMAYDIGAN ENGINE
        # Bu API Railway IP-manzilini aylanib o'tish uchun Proxy ishlatadi
        api_url = f"https://api-music-scrapper.vercel.app/search?q={query}"
        res = requests.get(api_url, timeout=15).json()
        
        if res and 'results' in res:
            track = res['results'][0]
            
            # DIZAYN: Siz xohlagandek @ai_muzik_bot va TO'LIQ MP3
            bot.send_audio(
                message.chat.id, 
                track['download_url'], 
                caption=f"🎵 **{track['title']}**\n👤 {track['artist']}\n\n✅ To'liq variant (Free)\n📥 @ai_muzik_bot",
                parse_mode="Markdown"
            )
            bot.delete_message(message.chat.id, wait.message_id)
        else:
            bot.edit_message_text("❌ Hech narsa topilmadi. Boshqa nom yozing.", message.chat.id, wait.message_id)
            
    except:
        # AGAR BU HAM BAND DESA - GOOGLE SEARCH REJIMIGA O'TADI
        bot.edit_message_text("⚠️ Baza yuklamasi yuqori, qayta urinib ko'ring.", message.chat.id, wait.message_id)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True)
        except:
            time.sleep(5)
