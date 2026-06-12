import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

bot = telebot.TeleBot(BOT_TOKEN)

# Webhook हटाओ (ताकि polling चल सके)
try:
    bot.delete_webhook()
    print("✅ Webhook deleted successfully.")
except Exception as e:
    print(f"⚠️ Webhook delete error: {e}")

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

if __name__ == "__main__":
    print("Bot started in polling mode...")
    bot.infinity_polling()
