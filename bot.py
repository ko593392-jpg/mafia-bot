import telebot
from telebot import types
import re

# 🔑 Tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin ma'lumotlari
active_games = {}

def get_game_markup():
    """Tugmalar dizayni ✊✌️🖐️"""
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Tosh ✊", callback_data="play_rock"),
        types.InlineKeyboardButton("Qaychi ✌️", callback_data="play_scissors"),
        types.InlineKeyboardButton("Qog'oz 🖐️", callback_data="play_paper")
    )
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline variantlar (2, 3, 4, 5 kishilik)"""
    try:
        results = []
        game_options = [
            {"n": 2, "icon": "👥", "desc": "Do'stlar jangi"},
            {"n": 3, "icon": "☘️", "desc": "3 kishilik guruh"},
            {"n": 4, "icon": "🍀", "desc": "4 kishilik guruh"},
            {"n": 5, "icon": "🔥", "desc": "Katta guruhli jang"}
        ]
        
        for opt in game_options:
            n = opt['n']
            results.append(types.InlineQueryResultArticle(
                id=str(n),
                title=f"{opt['icon']} Dondonziki ({n} kishilik)",
                description=opt['desc'],
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🎮 **Dondonziki boshlandi! ({n} kishilik)**\n\nIshtirokchilar, tanlang 👇"
                ),
                reply_markup=get_game_markup()
            ))
        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception as e:
        print(f"Inline error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def handle_play(call):
    """O'yin jarayoni va chiroyli natija"""
    msg_id = call.inline_message_id
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    move_key = call.data.split('_')[1]
    
    emojis = {"rock": "✊", "scissors": "✌️", "paper": "🖐️"}

    # Xabardan ishtirokchilar sonini aniqlash
    # Inline xabarlarda matn call.message ichida bo'lmasligi mumkin
    # Shuning uchun default 2 deb olamiz yoki matndan qidiramiz
    total_needed = 2
    if call.message and call.message.text:
        match = re.search(r'\((\d+) kishilik\)', call.message.text)
        if match: total_needed = int(match.group(1))

    if msg_id not in active_games:
        active_games[msg_id] = []

    # Ikki marta tanlashni cheklash
    if any(p['id'] == user_id for p in active_games[msg_id]):
        bot.answer_callback_query(call.id, "Siz tanlov qilib bo'ldingiz! ✨")
        return

    active_games[msg_id].append({'name': user_name, 'id': user_id, 'move': move_key, 'emoji': emojis[move_key]})
    bot.answer_callback_query(call.id, f"Siz: {emojis[move_key]}")

    current_players = len(active_games[msg_id])
    
    if current_players < total_needed:
        # Kutish dizayni
        ready_names = "\n".join([f"✅ {p['name']}" for p in active_games[msg_id]])
        bot.edit_message_text(
            f"🎮 **Dondonziki ({total_needed} kishilik)**\n\n**Tanlaganlar:**\n{ready_names}\n\n⌛ Yana {total_needed - current_players} kishi kutilmoqda...",
            inline_message_id=msg_id,
            reply_markup=get_game_markup()
        )
    else:
        # Natija dizayni
        res_text = "🏁 **NATIJALAR:**\n" + "─" * 15 + "\n"
        moves = {}
        for p in active_games[msg_id]:
            res_text += f"👤 {p['name']}: {p['emoji']}\n"
            moves[p['move']] = moves.get(p['move'], 0) + 1
        
        unique = list(moves.keys())
        if len(unique) == 1 or len(unique) == 3:
            res_text += "\n🤝 **Durrang!**"
        else:
            m1, m2 = unique[0], unique[1]
            win_move = m1 if (m1 == 'rock' and m2 == 'scissors') or \
                             (m1 == 'scissors' and m2 == 'paper') or \
                             (m1 == 'paper' and m2 == 'rock') else m2
            
            winners = [p['name'] for p in active_games[msg_id] if p['move'] == win_move]
            res_text += f"\n🏆 **G'ALABA:** {', '.join(winners)}!"

        bot.edit_message_text(res_text, inline_message_id=msg_id)
        del active_games[msg_id]

bot.remove_webhook()
bot.polling(none_stop=True)
