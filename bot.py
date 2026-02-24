import telebot
from telebot import types
from youtube_search import YoutubeSearch
import yt_dlp
import os

# Sening bot tokening joylandi
TOKEN = "8579253675:AAEqmEJVXKnbsFeIC_Ue7LYegcn9huKtJMk"
bot = telebot.TeleBot(TOKEN)

# Musiqa qidirish va ro'yxat chiqarish
@bot.message_handler(content_types=['text'])
def search_music(message):
    if message.text.startswith('http'):
        bot.send_message(message.chat.id, "Ssilkani tekshirib yuklayapman, ozgina sabr...")
        download_and_send(message.chat.id, message.text)
    else:
        query = message.text
        # YouTube'dan 10 ta natijani qidirish
        results = YoutubeSearch(query, max_results=10).to_dict()
        
        if not results:
            bot.send_message(message.chat.id, "❌ Afsuski, hech narsa topilmadi.")
            return

        text = "🔍 Topilgan natijalar:\n\n"
        markup = types.InlineKeyboardMarkup(row_width=5)
        btns = []
        
        for i, res in enumerate(results, 1):
            text += f"{i}. {res['title']} | {res['duration']}\n"
            # Tanlash tugmalarini yaratish
            btns.append(types.InlineKeyboardButton(text=str(i), callback_data=f"vid:{res['id']}"))
        
        markup.add(*btns)
        bot.send_message(message.chat.id, text, reply_markup=markup)

# Tugma bosilganda musiqani yuklab yuborish mantiqi
@bot.callback_query_handler(func=lambda call: call.data.startswith('vid:'))
def callback_download(call):
    video_id = call.data.split(':')[1]
    url = f"https://www.youtube.com/watch?v={video_id}"
    bot.answer_callback_query(call.id, "Musiqa yuklanyapti...")
    download_and_send(call.message.chat.id, url)

def download_and_send(chat_id, url):
    # Yuklash sozlamalari (Audio formatda)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Faylni foydalanuvchiga yuborish
        with open('music.mp3', 'rb') as audio:
            bot.send_audio(chat_id, audio)
        
        # Serverda joy egallamasligi uchun o'chirib tashlash
        os.remove('music.mp3')
    except Exception as e:
        bot.send_message(chat_id, f"Xato yuz berdi: {e}")

bot.polling(none_stop=True)
