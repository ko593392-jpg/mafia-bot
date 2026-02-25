import telebot
from telebot import types

# 🔑 Bot tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin holati
active_games = {}

def get_game_markup(n):
    """Premium tugmalar va kanal linki"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("✊ ᴛᴏsʜ", callback_data=f"play_rock_{n}"),
        types.InlineKeyboardButton("✌️ Qᴀʏᴄʜɪ", callback_data=f"play_scissors_{n}"),
        types.InlineKeyboardButton("🖐️ Qᴏɢ'ᴏᴢ", callback_data=f"play_paper_{n}")
    )
    markup.row(types.InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴄʜᴀɴɴᴇʟ 💎", url="https://t.me/boshqacha_edii"))
    return markup

def get_finish_markup():
    """Natija tagidagi kanal linki"""
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🌟 @ʙᴏsʜǫᴀᴄʜᴀ_ᴇᴅɪɪ 🌟", url="https://t.me/boshqacha_edii"))
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline menyu - 2 dan 5 kishigacha o'yinlar"""
    try:
        results = []
        options = [
            {"n": 2, "title": "⚔️ ᴅᴜᴇʟ (1ᴠs1)", "desc": "Premium jang"},
            {"n": 3, "title": "🔱 ᴛʀɪᴏ (3 ᴋɪsʜɪ)", "desc": "Uchta titan jangi"},
            {"n": 4, "title": "🍀 sǫᴜᴀᴅ (4 ᴋɪsʜɪ)", "desc": "Guruhlararo to'qnashuv"},
            {"n": 5, "title": "👑 ɢʀᴀɴᴅ ʙᴀᴛᴛʟᴇ (5 ᴋɪsʜɪ)", "desc": "Eng kuchli 5 talik jangi"}
        ]
        for opt in options:
            n = opt['n']
            results.append(types.InlineQueryResultArticle(
                id=str(n),
                title=opt['title'],
                description=opt['desc'],
                input_message_content=types.InputTextMessageContent(
                    message_text=f"┏━━━━━━━━━━━━━━┓\n   🎮  **ᴅᴏɴᴅᴏɴᴢɪᴋɪ ᴘʀᴇᴍɪᴜᴍ** 🎮\n┗━━━━━━━━━━━━━━┛\n\n🔹 **ʀᴇᴊɪᴍ:** {n} kishilik\n📊 **ʜᴏʟᴀᴛ:** Kutilmoqda...\n\n👇 **ᴛᴀɴʟᴏᴠɴɪ ᴀᴍᴀʟɢᴀ ᴏsʜɪʀɪɴɢ:**"
                ),
                reply_markup=get_game_markup(n)
            ))
        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def handle_play(call):
    """O'yin mantiqi (Barcha qismlar joyida)"""
    try:
        data = call.data.split('_')
        move_key, total_needed = data[1], int(data[2])
        msg_id = call.inline_message_id
        user_id, user_name = call.from_user.id, f"👤 {call.from_user.first_name}"
        emojis = {"rock": "✊", "scissors": "✌️", "paper": "🖐️"}

        if msg_id not in active_games: active_games[msg_id] = []
        if any(p['id'] == user_id for p in active_games[msg_id]):
            bot.answer_callback_query(call.id, "ᴛᴀɴʟᴏᴠ Qɪʟɪɴᴅɪ! ⛔️")
            return

        active_games[msg_id].append({'id': user_id, 'name': user_name, 'move': move_key, 'emoji': emojis[move_key]})
        bot.answer_callback_query(call.id, f"✅ {emojis[move_key]}")

        cur = len(active_games[msg_id])
        if cur < total_needed:
            ready_list = "\n".join([f"   ✅ {p['name']}" for p in active_games[msg_id]])
            bot.edit_message_text(
                f"┏━━━━━━━━━━━━━━┓\n   🎮  **ᴅᴏɴᴅᴏɴᴢɪᴋɪ ᴘʀᴇᴍɪᴜᴍ** 🎮\n┗━━━━━━━━━━━━━━┛\n\n🔹 **ʀᴇᴊɪᴍ:** {total_needed} kishilik\n\n📋 **ᴛᴀʏʏᴏʀʟᴀʀ:**\n{ready_list}\n\n⌛ **ʏᴀɴᴀ {total_needed - cur} ᴋɪsʜɪ ᴋᴜᴛɪʟᴍᴏǫᴅᴀ...**",
                inline_message_id=msg_id,
                reply_markup=get_game_markup(total_needed)
            )
        else:
            res_text = f"┏━━━━━━━━━━━━━━┓\n   🏆  **ᴊᴀɴɢ ʏᴀᴋᴜɴʟᴀɴᴅɪ** 🏆\n┗━━━━━━━━━━━━━━┛\n\n"
            moves = {}
            for p in active_games[msg_id]:
                res_text += f"▪️ {p['name']}: {p['emoji']}\n"
                moves[p['move']] = moves.get(p['move'], 0) + 1
            
            unique = list(moves.keys())
            if len(unique) == 1 or len(unique) == 3:
                res_text += "\n🤝 **ᴅᴜʀʀᴀɴɢ!**"
            else:
                m1, m2 = unique[0], unique[1]
                win_move = m1 if (m1 == 'rock' and m2 == 'scissors') or (m1 == 'scissors' and m2 == 'paper') or (m1 == 'paper' and m2 == 'rock') else m2
                winners = [p['name'] for p in active_games[msg_id] if p['move'] == win_move]
                res_text += f"\n🏅 **ɢ'ᴏʟɪʙʟᴀʀ:** {', '.join(winners)}"

            bot.edit_message_text(res_text, inline_message_id=msg_id, reply_markup=get_finish_markup())
            del active_games[msg_id]
    except Exception: pass

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
