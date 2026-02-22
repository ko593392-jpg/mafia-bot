iimport telebot
import time
import os
import http.server
import socketserver
import threading

# Render uchun soxta port yaratish
def run_on_render():
    PORT = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_on_render, daemon=True).start()

# Bot kodingiz
TOKEN = '8492024967:AAEJnp1Xl0W8DBOi70PhUwwx2o3zqWWu4CM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎙 Classic Mafia botiga xush kelibsiz!")

@bot.message_handler(func=lambda m: True)
def delete_ads(message):
    try:
        pass
    except:
        pass

while True:
    try:
        print("Bot ishga tushdi...")
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(5)






