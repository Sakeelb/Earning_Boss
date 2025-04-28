import os
import telebot
import time
import threading
from keep_alive import keep_alive
from ping_self import start_pinger
from transformers import pipeline

# --- Critical Fixes ---
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # GPU को डिसेबल करें
MODEL_NAME = 'distilgpt2'  # हल्का मॉडल (GPT-2 का 50% साइज़)

# Env Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL")

# Init
bot = telebot.TeleBot(BOT_TOKEN)
generator = pipeline('text-generation', model=MODEL_NAME)  # अपडेटेड मॉडल
referral_data = {}
user_activity = {}
VIP_USERS = {}

# --- Memory Optimized Functions ---
def safe_generate(prompt):
    try:
        return generator(prompt, max_length=30)[0]['generated_text']  # max_length घटाया
    except Exception as e:
        print(f"Generation Error: {str(e)}")
        return "⚠️ सर्वर बिजी है, बाद में ट्राई करें"

# Auto-Poster (Optimized)
def auto_post():
    while True:
        now = time.strftime("%H:%M")
        if now in ["08:00", "12:00", "16:00"]:
            try:
                bot.send_message(PROMO_CHANNEL, "🆕 नया अपडेट! @All_Gift_Code_Earning ज्वाइन करें")
            except Exception as e:
                print(f"Posting Error: {str(e)}")
        time.sleep(3600)

# Good Morning Poster (Optimized)
def good_morning_poster():
    while True:
        now = time.strftime("%H:%M")
        if now == "05:00":
            try:
                prompt = "Write a short morning wish (under 20 words)"
                morning_msg = safe_generate(prompt)
                bot.send_message(PROMO_CHANNEL, f"☀️ {morning_msg[:100]}")  # लेंथ लिमिट
            except Exception as e:
                print(f"Morning Post Error: {str(e)}")
            time.sleep(60)
        time.sleep(30)

# ... (बाकी कोड जैसा है start_handler, referral_handler, etc में कोई बदलाव नहीं)

# Activity Tracking (Optimized)
@bot.message_handler(func=lambda msg: True)
def track_all(message):
    user_id = message.from_user.id
    user_activity[user_id] = user_activity.get(user_id, 0) + 1
    
    if user_activity[user_id] % 10 == 0:  # 5 से बढ़ाकर 10 करें
        try:
            bot.send_message(PROMO_CHANNEL, f"🏆 टॉप यूजर: @{message.from_user.username}")
        except Exception as e:
            print(f"Activity Error: {str(e)}")

# Start Services
keep_alive()
start_pinger()
threading.Thread(target=auto_post).start()
threading.Thread(target=good_morning_poster).start()
bot.infinity_polling()
