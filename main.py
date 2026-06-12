import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_handler(msg):
    bot.reply_to(msg, "✅ बॉट अब काम कर रहा है! 🚀")

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 403

@app.route('/')
def home():
    return "Bot is running"

if __name__ == "__main__":
    # Render पर webhook सेट करो
    webhook_url = "https://earning-boss.onrender.com/webhook"
    try:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print(f"✅ Webhook set to {webhook_url}")
    except Exception as e:
        print(f"❌ Webhook error: {e}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
