import telebot
from telebot import types
import re

# 🔑 Bot tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin holati
active_games = {}

def get_game_markup(n):
    """O'yin tugmalari va kanal linkini qo'shish"""
    markup = types.InlineKeyboardMarkup()
    # 1-qator: O'yin tugmalari
    markup.row(
        types.InlineKeyboardButton("Tosh ✊", callback_data=f"play_rock_{n}"),
        types.InlineKeyboardButton("Qaychi ✌️", callback_data=f"play_scissors_{n}"),
        types.InlineKeyboardButton("Qog'oz 🖐️", callback_data=f"play_paper_{n}")
    )
    # 2-qator: Kanal linki (Siz aytgan @boshqacha_edii)
    markup.row(
        types.InlineKeyboardButton("✨ @boshqacha_edii ✨", url="https://t.me/boshqacha_edii")
    )
    return markup

def get_result_markup():
    """O'yin tugagandan keyin faqat kanal linkini qoldirish"""
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✨ @boshqacha_edii ✨", url="https://t.me/boshqacha_edii")
    )
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline variantlar ro'yxati (2-5 kishilik)"""
    try:
        results = []
        game_types = [
            {"n": 2, "icon": "👥", "title": "1ga-1 Jang"},
            {"n": 3, "icon": "☘️", "title": "3 kishilik guruh"},
            {"n": 4, "icon": "🍀", "title": "4 kishilik guruh"},
            {"n": 5, "icon": "🔥", "title": "5 kishilik KATTA jang"}
        ]
        
        for opt in game_types:
            n = opt['n']
            results.append(types.InlineQueryResultArticle(
                id=str(n),
                title=f"{opt['icon']} Dondonziki ({n} kishilik)",
                description=opt['title'],
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🎮 **Dondonziki boshlandi! ({n} kishilik)**\n\nIshtirokchilar, tanlovingizni qiling 👇"
                ),
                reply_markup=get_game_markup(n)
            ))
        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception as e:
        print(f"Inline Error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def handle_play(call):
    """O'yin jarayoni va natija"""
    try:
        data = call.data.split('_')
        move_key = data[1]       
        total_needed = int(data[2]) 
        
        msg_id = call.inline_message_id
        user_id = call.from_user.id
        user_name = call.from_user.first_name
        
        emojis = {"rock": "✊", "scissors": "✌️", "paper": "🖐️"}

        if msg_id not in active_games:
            active_games[msg_id] = []

        if any(p['id'] == user_id for p in active_games[msg_id]):
            bot.answer_callback_query(call.id, "Siz tanlov qilib bo'ldingiz! ✨")
            return

        active_games[msg_id].append({
            'id': user_id, 
            'name': user_name, 
            'move': move_key, 
            'emoji': emojis[move_key]
        })
        bot.answer_callback_query(call.id, f"Siz tanladingiz: {emojis[move_key]}")

        current_players = len(active_games[msg_id])
        
        if current_players < total_needed:
            ready_list = "\n".join([f"✅ {p['name']}" for p in active_games[msg_id]])
            bot.edit_message_text(
                f"🎮 **Dondonziki ({total_needed} kishilik)**\n\n**Tayyor:**\n{ready_list}\n\n⌛ Yana {total_needed - current_players} kishi kutilmoqda...",
                inline_message_id=msg_id,
                reply_markup=get_game_markup(total_needed)
            )
        else:
            res_text = "🏁 **O'YIN NATIJALARI**\n" + "─" * 15 + "\n"
            moves_made = {}
            for p in active_games[msg_id]:
                res_text += f"👤 {p['name']}: {p['emoji']}\n"
                moves_made[p['move']] = moves_made.get(p['move'], 0) + 1
            
            unique_moves = list(moves_made.keys())
            
            if len(unique_moves) == 1 or len(unique_moves) == 3:
                res_text += "\n🤝 **Durrang!**"
            else:
                m1, m2 = unique_moves[0], unique_moves[1]
                win_move = m1 if (m1 == 'rock' and m2 == 'scissors') or \
                                 (m1 == 'scissors' and m2 == 'paper') or \
                                 (m1 == 'paper' and m2 == 'rock') else m2
                
                winners = [p['name'] for p in active_games[msg_id] if p['move'] == win_move]
                res_text += f"\n🏆 **G'ALABA:** {', '.join(winners)}!"

            # Natijada ham kanal linki tursin
            bot.edit_message_text(res_text, inline_message_id=msg_id, reply_markup=get_result_markup())
            if msg_id in active_games:
                del active_games[msg_id]
    except Exception as e:
        print(f"Callback error: {e}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True, skip_pending=True)
