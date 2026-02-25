 import telebot
from telebot import types

# 🔑 Bot tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin holati
active_games = {}

def get_game_markup(n):
    """O'yin vaqtidagi tugmalar va kanal linki"""
    markup = types.InlineKeyboardMarkup()
    # Tosh, Qaychi, Qog'oz tugmalari
    markup.row(
        types.InlineKeyboardButton("Tosh ✊", callback_data=f"play_rock_{n}"),
        types.InlineKeyboardButton("Qaychi ✌️", callback_data=f"play_scissors_{n}"),
        types.InlineKeyboardButton("Qog'oz 🖐️", callback_data=f"play_paper_{n}")
    )
    # Kanal linki doimiy turadi
    markup.row(
        types.InlineKeyboardButton("✨ @boshqacha_edii ✨", url="https://t.me/boshqacha_edii")
    )
    return markup

def get_finish_markup():
    """G'olib aniqlanganda faqat kanal linkini chiqarish"""
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🚀 Boshqa o'yin boshlash", switch_inline_query=""),
        types.InlineKeyboardButton("✨ @boshqacha_edii ✨", url="https://t.me/boshqacha_edii")
    )
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline menyu dizayni"""
    try:
        results = []
        options = [
            {"n": 2, "title": "👥 1 vs 1 (Duel)", "desc": "Do'stlar o'rtasidagi jang"},
            {"n": 3, "title": "☘️ 3 kishilik guruh", "desc": "Uchta ishtirokchi jangi"},
            {"n": 4, "title": "🍀 4 kishilik guruh", "desc": "To'rt kishi orasida g'olib"},
            {"n": 5, "title": "🔥 5 kishilik BATTLE", "desc": "Beshta ishtirokchi orasida jang"}
        ]
        
        for opt in options:
            n = opt['n']
            results.append(types.InlineQueryResultArticle(
                id=str(n),
                title=opt['title'],
                description=opt['desc'],
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🎮 **── DONDONZIKI ──**\n\n🔹 **Rejim:** {n} kishilik\n📢 **Holat:** Ishtirokchilar kutilmoqda...\n\n👇 **Tanlovni amalga oshiring:**"
                ),
                reply_markup=get_game_markup(n)
            ))
        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def handle_play(call):
    """O'yin jarayoni va chiroyli natija"""
    try:
        data = call.data.split('_')
        move_key = data[1]       
        total_needed = int(data[2]) 
        
        msg_id = call.inline_message_id
        user_id = call.from_user.id
        user_name = f"👤 {call.from_user.first_name}"
        
        emojis = {"rock": "✊", "scissors": "✌️", "paper": "🖐️"}

        if msg_id not in active_games:
            active_games[msg_id] = []

        # Takroriy bosishni tekshirish
        if any(p['id'] == user_id for p in active_games[msg_id]):
            bot.answer_callback_query(call.id, "Siz tanlov qilib bo'ldingiz! ⛔️")
            return

        active_games[msg_id].append({'id': user_id, 'name': user_name, 'move': move_key, 'emoji': emojis[move_key]})
        bot.answer_callback_query(call.id, f"Qabul qilindi: {emojis[move_key]}")

        current_players = len(active_games[msg_id])
        
        if current_players < total_needed:
            # Kutish jarayoni dizayni
            ready_list = "\n".join([f"✅ {p['name']}" for p in active_games[msg_id]])
            bot.edit_message_text(
                f"🎮 **── DONDONZIKI ──**\n\n🔹 **Rejim:** {total_needed} kishilik\n\n📋 **Tayyorlar:**\n{ready_list}\n\n⌛ **Yana {total_needed - current_players} kishi kerak...**",
                inline_message_id=msg_id,
                reply_markup=get_game_markup(total_needed)
            )
        else:
            # G'oliblar aniqlangan qism
            res_text = f"🏁 **── NATIJA ──**\n\n"
            moves_made = {}
            for p in active_games[msg_id]:
                res_text += f"{p['name']}: {p['emoji']}\n"
                moves_made[p['move']] = moves_made.get(p['move'], 0) + 1
            
            unique = list(moves_made.keys())
            
            if len(unique) == 1 or len(unique) == 3:
                res_text += "\n🤝 **DURRANG! Hamma teng kuchli.**"
            else:
                m1, m2 = unique[0], unique[1]
                win_move = m1 if (m1 == 'rock' and m2 == 'scissors') or \
                                 (m1 == 'scissors' and m2 == 'paper') or \
                                 (m1 == 'paper' and m2 == 'rock') else m2
                
                winners = [p['name'] for p in active_games[msg_id] if p['move'] == win_move]
                res_text += f"\n🏆 **G'ALABA:** {', '.join(winners)}!"

            # Natija tagiga ham kanal linkini qo'shish
            bot.edit_message_text(res_text, inline_message_id=msg_id, reply_markup=get_finish_markup())
            if msg_id in active_games:
                del active_games[msg_id]
    except Exception:
        pass

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True, skip_pending=True)
       
