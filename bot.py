@bot.message_handler(func=lambda message: message.text in ["Tosh ✊", "Qaychi ✌️", "Qog'oz 🖐️"])
def play_game(message):
    user_choice = message.text
    bot_options = ["Tosh ✊", "Qaychi ✌️", "Qog'oz 🖐️"]
    bot_choice = random.choice(bot_options)
    
    # Natijani hisoblash (bu yerda mantiqiy solishtirish bo'ladi)
    result = ""
    if user_choice == bot_choice:
        result = "Durrang! 🤝"
    # Shu yerda g'olibni aniqlaydigan shartlar davom etadi...
    
    bot.send_message(message.chat.id, f"Siz: {user_choice}\nBot: {bot_choice}\n\n{result}")
