import os
import telebot
from keep_alive import keep_alive
from ping_self import start_pinger

# Env Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL")

# Init Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Start Command
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id='@All_Gift_Code_Earning',
            message_id=398
        )
    except Exception as e:
        print(f"Start Error: {str(e)}")

# Auto Reply
@bot.message_handler(func=lambda msg: True)
def auto_reply(message):
    text = message.text.lower()
    keywords = ["join", "earn", "channel", "t.me/", "refer", "promo", "मेरे चैनल", "invite"]
    if any(keyword in text for keyword in keywords):
        try:
            reply = "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]] [[ https://t.me/All_Gift_Code_Earning ]]"
            bot.reply_to(message, reply)
            bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id='@All_Gift_Code_Earning',
                message_id=398
            )
        except Exception as e:
            print(f"Reply Error: {e}")

# Keep it alive
keep_alive()
start_pinger()

# Start Bot
bot.infinity_polling()
