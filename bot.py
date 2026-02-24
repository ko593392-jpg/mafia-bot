import telebot
from youtubesearchpython import VideosSearch
import os

# Render'dagi Environment Variable'dan tokenni oladi
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men tayyorman. Qo'shiq nomini yozing, men YouTube'dan qidirib beraman.")

@bot.message_handler(func=lambda message: True)
def search_music(message):
