import telebot
from telebot import types
import re

# 🔑 Tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin holati
active_games = {}

def get_game_markup():
    """O'yin tugmalari dizayni"""
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Tosh ✊", callback_data="play_rock"),
        types.InlineKeyboardButton("Qaychi ✌️", callback_data="play_scissors"),
        types.InlineKeyboardButton("Qog'oz 🖐️", callback_data="play_paper")
    )
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline tanlovlar ro'yxati dizayni"""
    try:
        results = []
        game_types = [
            {"n": 2, "icon": "👥", "desc": "Do'st bilan 1ga-1"},
            {"n": 3, "icon": "☘️", "desc": "3 kishilik raqobat"},
            {"n": 4, "icon": "🍀", "desc": "4 kishilik jang"},
            {"n": 5, "icon": "🔥", "desc": "5 kishilik katta o'yin"}
        ]
        
        for game in game_types:
            n = game['n']
            results.append(types.InlineQueryResultArticle(
                id=str(n),
                title=f"{game['icon']} Yangi o'yin ({n} kishilik)",
                description=game['desc'],
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🎮 **Dondonziki boshlandi! ({n} kishilik)**\n\nIshtirokchilar, tanlovingizni qiling 👇"
                ),
                reply_markup=get_game_markup()
            ))
        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception as e:
        print(f"Dizayn xatosi: {e
        
        
