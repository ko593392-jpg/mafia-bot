import os
import telebot

# BotFather'dan olingan yangi tokenni Railway Variables'ga qo'yganingizni tekshiring
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Aka, mana men ishlayapman! Nihoyat botingiz uyg'ondi. Endi musiqa qismini qo'shsak bo'ladi.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Siz yozdingiz: {message.text}. Aloqa 100% yaxshi!")

bot.polling(none_stop=True)
