import telebot
from telebot import types

# 🔑 Bot tokeningiz
TOKEN = '8677619307:AAHfEVH5w2ucGMsg3iavJX6mcuhSd94pCR8'
bot = telebot.TeleBot(TOKEN)

# 💾 O'yin holati
active_games = {}

def get_game_markup(n):
    """Premium tugmalar va kanal linki dizayni"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [
        types.InlineKeyboardButton("✊ ᴛᴏsʜ", callback_data=f"play_rock_{n}"),
        types.InlineKeyboardButton("✌️ Qᴀʏᴄʜɪ", callback_data=f"play_scissors_{n}"),
        types.InlineKeyboardButton("🖐️ Qᴏɢ'ᴏᴢ", callback_data=f"play_paper_{n}")
    ]
    markup.add(*btns)
    # Kanal linki - Premium ko'rinishda
    markup.row(types.InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴄʜᴀɴɴᴇʟ 💎", url="https://t.me/boshqacha_edii"))
    return markup

def get_finish_markup():
    """Natija tagidagi Premium kanal linki"""
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🌟 ᴊᴏɪɴ @ʙᴏsʜǫᴀᴄʜᴀ_ᴇᴅɪɪ 🌟", url="https://t.me/boshqacha_edii"))
    return markup

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """Inline menyu - Premium tanlovlar"""
    try:
        results = []
        # Dizayn elementlari
        options = [
            {"n": 2, "title": "⚔️ ᴅᴜᴇʟ (1ᴠs1)", "desc": "Premium darajadagi jang"},
            {"n": 3, "title": "🔱 ᴛʀɪᴏ (3 ᴋɪsʜɪ)", "desc": "Uchta titan jangi"},
            {"n": 4, "title": "🍀 sǫᴜᴀᴅ (4 ᴋɪ
