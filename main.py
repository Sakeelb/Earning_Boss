import os
import telebot
import threading
import time
from flask import Flask, request
import pytz
from datetime import datetime
import re
import random
import traceback
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

OWNER_ID = os.environ.get("OWNER_ID")
if OWNER_ID:
    OWNER_ID = int(OWNER_ID)
else:
    print("WARNING: OWNER_ID not set.")

PROMO_CHANNEL_ID = "-1002437678122"
PROMOTION_CHANNEL_LINK = "https://t.me/Proper_Trending"

# Render URL – बिना slash के
RENDER_URL = os.environ.get("RENDER_URL", "https://earning-boss.onrender.com")
WEBHOOK_URL = f"{RENDER_URL}/webhook"
IS_RENDER = os.environ.get("RENDER") == "true"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ========== Images (aapki purani wali) ==========
PROMO_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"
START_IMAGE_URL = PROMO_IMAGE_URL

MORNING_IMAGE_URLS = [ ... ]  # यहाँ आपकी morning images की लिस्ट डालें (जैसी पहले थी)
NIGHT_IMAGE_URLS = [ ... ]    # यहाँ night images की लिस्ट

MORNING_TEMPLATES = [ ... ]   # morning templates
NIGHT_TEMPLATES = [ ... ]     # night templates
PROMO_CAPTIONS = [ ... ]      # promo captions
KEYWORDS = [ ... ]            # keywords list

# (बाकी सारे arrays और functions पिछले कोड की तरह ही रखें, पर यहाँ जगह बचाने के लिए नहीं लिख रहा, आप अपना पुराना कोड ही इस्तेमाल करें)

# ==================== Helper functions (वैसे ही रखें) ====================
def get_random_promo_caption():
    return random.choice(PROMO_CAPTIONS)

def get_today_index(list_length):
    india_tz = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(india_tz).strftime("%j")) % list_length

def send_auto_post(templates, images, prefix_emoji):
    # (पुराना code)
    pass

def auto_poster():
    # (पुराना code)
    pass

def keyword_found(text):
    # (पुराना code)
    pass

def send_promo(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Start Earning", url=PROMOTION_CHANNEL_LINK))
    caption = get_random_promo_caption()
    try:
        bot.send_photo(chat_id, PROMO_IMAGE_URL, caption=caption, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Send promo error: {e}")

# ==================== Bot Handlers ====================
@bot.message_handler(commands=['start'])
def start_handler(message):
    send_promo(message.chat.id)

@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    if message.text and keyword_found(message.text):
        send_promo(message.chat.id)
    if OWNER_ID and message.chat.id != OWNER_ID:
        try:
            user = message.from_user
            user_name = user.first_name or ""
            if user.username:
                user_name += f" (@{user.username})"
            forward_text = f"📩 *नया मैसेज*\n👤 {user_name}\n🆔 `{user.id}`\n💬 {message.text}"
            bot.send_message(OWNER_ID, forward_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Forward error: {e}")

# ==================== Flask Webhook Endpoint ====================
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_str = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_str)
            bot.process_new_updates([update])
            return 'OK', 200
        except Exception as e:
            print(f"Webhook error: {e}")
            return 'Error', 500
    return 'Bad Request', 403

@app.route('/')
def home():
    return "Bot is running. Webhook at /webhook"

@app.route('/health')
def health():
    return "OK", 200

# ==================== Main ====================
if __name__ == "__main__":
    # Auto-poster thread start
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster started.")

    if IS_RENDER:
        # Render पर webhook set करो
        try:
            bot.remove_webhook()
            bot.set_webhook(url=WEBHOOK_URL)
            print(f"Webhook set to {WEBHOOK_URL}")
        except Exception as e:
            print(f"Webhook setup failed: {e}")
        # यहाँ app.run() नहीं चलाना, क्योंकि gunicorn चलाएगा
    else:
        # Local development: polling
        bot.infinity_polling()
