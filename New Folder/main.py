import os
import telebot
from keep_alive import keep_alive

# Get environment variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL")

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Start command handler
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id='@All_Gift_Code_Earning',
            message_id=398
        )
    except Exception as e:
        print(f"Error: {str(e)}")

# Auto-responder for messages
@bot.message_handler(func=lambda msg: True)
def auto_reply(message):
    text = message.text.lower()
    keywords = ["join", "earn", "channel", "t.me/", "refer", "promo", "मेरे चैनल", "invite"]
    
    if any(keyword in text for keyword in keywords):
        try:
            reply = (
                "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]] "
                "[[ https://t.me/All_Gift_Code_Earning ]]"
            )
            bot.reply_to(message, reply)
            bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id='@All_Gift_Code_Earning',
                message_id=398
            )
        except Exception as e:
            print(f"Auto-reply error: {e}")

# Keep bot alive with Flask
keep_alive()

# Optional self-pinger (only if using ping_self.py)
try:
    from ping_self import start_pinger
    start_pinger()
except:
    pass

# Polling loop to auto-restart on crash or Render idle
import time
while True:
    try:
        print("Bot polling started...")
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot crashed with error: {e}")
        print("Restarting in 15 seconds...")
        time.sleep(15)
