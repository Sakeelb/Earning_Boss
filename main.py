import os
import telebot
import threading
import time
import pytz
from datetime import datetime
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

bot = telebot.TeleBot(BOT_TOKEN)

# प्रोमोशन लिंक
PROMO_LINK = "https://t.me/Proper_Trending"

@bot.message_handler(commands=['start'])
def start_handler(msg):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Start Earning", url=PROMO_LINK))
    bot.send_photo(msg.chat.id, 
                   "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png",
                   caption="🔥 Live New Loot! Fast Join Telegram Channel",
                   reply_markup=markup)

# Auto-poster thread (optional, हटा भी सकते हो अभी)
def auto_poster():
    # तुम्हारा auto-poster कोड यहाँ डालना, पर अभी काम नहीं करेगा क्योंकि चैनल ID नहीं डाली
    pass

if __name__ == "__main__":
    # कोई webhook नहीं, सीधा polling
    print("Bot started in polling mode...")
    bot.infinity_polling()
