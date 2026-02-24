import os
import telebot
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Musiqa nomini yozing, men bazadan qidirib beraman.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    msg = bot.reply_to(message, "🔍 Bazadan qidirilmoqda...")
    
    # Deezer va boshqa ochiq bazalardan qidirish (Bloklanmaydi)
    try:
        search_url = f"https://api.deezer.com/search?q={query}&limit=1"
        response = requests.get(search_url).json()
        
        if response['data']:
            track = response['data'][0]
            audio_url = track['preview'] # Musiqa namunasi (preview)
            title = track['title']
            artist = track['artist']['name']
            
            bot.send_audio(
                message.chat.id, 
                audio_url, 
                caption=f"✅ {artist} - {title}\n\n@sizning_botingiz",
                title=title,
                performer=artist
            )
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ Afsuski, musiqa topilmadi.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ Xato yuz berdi.", message.chat.id, msg.message_id)
        print(f"Xato: {e}")

bot.polling(none_stop=True)
