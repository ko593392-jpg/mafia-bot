import telebot
from telebot import types

# 🔑 BotFather'dan olingan yangi tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin ma'lumotlarini vaqtincha saqlash uchun lug'at
# Har bir xabar (inline_message_id) uchun alohida o'yin holati
active_games = {}

def get_game_markup():
    """O'yin tugmalarini yaratish ✊✌️🖐️"""
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Tosh ✊", callback_data="play_rock"),
        types.InlineKeyboardButton("Qaychi ✌️", callback_data="play_scissors"),
        types.InlineKeyboardButton("Qog'oz 🖐️", callback_data="play_paper")
    )
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline so'rovga javob berish (Chatda @bot_nomi deb yozganda)"""
    try:
        game_card = types.InlineQueryResultArticle(
            id='1',
            title="Dondonziki (2 kishilik)",
            description="Do'stlar bilan o'ynash uchun bosing",
            input_message_content=types.InputTextMessageContent(
                message_text="🎮 **Tosh-Qaychi-Qog'oz boshlandi!**\n\nIshtirokchilar, tanlovingizni qiling:"
            ),
            reply_markup=get_game_markup()
        )
        bot.answer_inline_query(inline_query.id, [game_card], cache_time=1)
    except Exception as e:
        print(f"Inline error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def handle_play(call):
    """Tugma bosilganda ishlaydigan mantiq"""
    msg_id = call.inline_message_id
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    move = call.data.split('_')[1] # rock, scissors, paper
    
    # Yangi o'yin yaratish
    if msg_id not in active_games:
        active_games[msg_id] = {'p1': {'id': user_id, 'name': user_name, 'move': move}, 'p2': None}
        bot.answer_callback_query(call.id, f"Siz tanladingiz: {move}!", show_alert=False)
    else:
        game = active_games[msg_id]
        
        # O'yinchi o'zi bilan o'zi o'ynamasligi uchun tekshiruv
        if game['p1']['id'] == user_id:
            bot.answer_callback_query(call.id, "Ikkinchi o'yinchini kuting! ⏳", show_alert=True)
            return

        # Ikkinchi o'yinchi tanlovi
        game['p2'] = {'id': user_id, 'name': user_name, 'move': move}
        
        # G'olibni aniqlash mantiqi
        p1_move = game['p1']['move']
        p2_move = game['p2']['move']
        
        result_text = f"🏁 **Natija:**\n👤 {game['p1']['name']}: {p1_move}\n👤 {game['p2']['name']}: {p2_move}\n\n"
        
        if p1_move == p2_move:
            result_text += "🤝 **Durrang!**"
        elif (p1_move == 'rock' and p2_move == 'scissors') or \
             (p1_move == 'scissors' and p2_move == 'paper') or \
             (p1_move == 'paper' and p2_move == 'rock'):
            result_text += f"🏆 **{game['p1']['name']} yutdi!**"
        else:
            result_text += f"🏆 **{game['p2']['name']} yutdi!**"
            
        bot.edit_message_text(result_text, inline_message_id=msg_id)
        # O'yin tugadi, xotiradan o'chiramiz
        del active_games[msg_id]

bot.polling(none_stop=True)
