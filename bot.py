import telebot
from shazamio import Shazam
import asyncio
import os
import threading

# --- SOZLAMALAR ---
TOKEN = '8579253675:AAEqmEJVXKnbsFeIC_Ue7LYegcn9huKtJMk'
bot = telebot.TeleBot(TOKEN)
shazam = Shazam()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Menga musiqa yoki ovozli xabar yuboring, men uni topib beraman. 🎵")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    bot.reply_to(message, "🔍 Musiqani qidiryapman, ozgina sabr...")
    
    try:
        file_id = message.voice.file_id if message.voice else message.audio.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        file_name = f"music_{message.chat.id}.ogg"
        with open(file_name, 'wb') as f:
            f.write(downloaded_file)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(shazam.recognize_song(file_name))
        
        if result.get('track'):
            track = result['track']
            bot.send_message(message.chat.id, f"✅ <b>Topildi!</b>\n\n🎵 Nomi: <b>{track.get('title')}</b>\n👤 Ijrochi: <b>{track.get('subtitle')}</b>", parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "❌ Afsuski, topilmadi.")
        
        if os.path.exists(file_name):
            os.remove(file_name)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Xatolik yuz berdi.")

# Render uchun server
def dummy_server():
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"Live")
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('', port), Handler).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=dummy_server, daemon=True).start()
    bot.infinity_polling()
