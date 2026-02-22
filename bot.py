import telebot
import time

# @classic_mafia_bot tokeni
TOKEN = '8341594080:AAGK56Qjnwp0GXNKIynnUBaoaVLc9xdU5JA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🕴 Classic Mafia boti onlayn va xizmatga tayyor!")

@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in ['http', 't.me']))
def delete_ads(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "⚠️ Reklama o'chirildi!")
    except:
        pass

# Botni xatoliklardan himoya qilish (o'lmas bot)
while True:
    try:
        print("Bot ishga tushdi...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Xatolik: {e}. 5 soniyadan keyin qayta yonadi...")
        time.sleep(5)





