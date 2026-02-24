import telebot
from telebot import types
import re

# 🔑 Sizning bot tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yinlarni xotirada saqlash
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
    """Inline variantlar ro'yxati (2-5 kishilik)"""
    try:
        results = []
        options = [
            {"n": 2, "icon": "👥", "title": "1ga-1 Jang"},
            {"n": 3, "icon": "☘️", "title": "3 kishilik guruh"},
            {"n": 4, "icon": "🍀", "title": "4 kishilik guruh"},
            {"n": 5, "icon": "🔥", "title": "5 kishilik KATTA jang"}
        ]
        
        for opt in options:
            n = opt['n']
            results.append(types.InlineQueryResultArticle(
                id=str(n),
                title=f"{opt['icon']} Dondonziki ({n} kishilik)",
                description=opt['title'],
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🎮 **Dondonziki boshlandi! ({n} kishilik)**\n\nIshtirokchilar, tanlovingizni qiling 👇"
                ),
                reply_markup=get_game_markup()
            ))
        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception as e:
        print(f"Inline Error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def handle_play(call):
    """O'yin mantiqi va natija dizayni"""
    msg_id = call.inline_message_id
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    move_key = call.data.split('_')[1]
    
    emojis = {"rock": "✊", "scissors": "✌️", "paper": "🖐️"}

    # Xabardan ishtirokchilar sonini qidirish
    msg_text = call.message.text if call.message else ""
    # Inline xabarlarda matn call ichida boshqacha kelishi mumkin, shuning uchun default 2 kishilik
    total_needed = 2
    match = re.search(r'\((\d+) kishilik\)', msg_text)
    if match:
        total_needed = int(match.group(1))

    if msg_id not in active_games:
        active_games[msg_id] = []

    # Bir marta tanlash cheklovi
    if any(p['id'] == user_id for p in active_games[msg_id]):
        bot.answer_callback_query(call.id, "Siz allaqachon tanladingiz! ✨")
        return

    active_games[msg_id].append({'id': user_id, 'name': user_name, 'move': move_key, 'emoji': emojis[move_key]})
    bot.answer_callback_query(call.id, f"Siz tanladingiz: {emojis[move_key]}")

    current_players = len(active_games[msg_id])
    
    if current_players < total_needed:
        # Kutish rejimi dizayni
        ready_players = "\n".join([f"
