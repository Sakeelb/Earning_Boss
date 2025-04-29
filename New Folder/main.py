import os
import telebot
import time
import threading
from keep_alive import keep_alive
from ping_self import start_pinger
import gc

# --- AI Section (RAM Friendly) ---
try:
    from transformers import pipeline
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    generator = pipeline('text-generation', model='distilgpt2')
except Exception as e:
    generator = None
    print("AI model couldn't load (RAM issue?):", e)

# Env Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL")

bot = telebot.TeleBot(BOT_TOKEN)
referral_data = {}
user_activity = {}
VIP_USERS = {}

def safe_generate(prompt):
    if generator is None:
        return "⚠️ AI सर्वर बिजी है, बाद में ट्राई करें"
    try:
        return generator(prompt, max_length=20)[0]['generated_text']
    except Exception as e:
        print(f"Generation Error: {str(e)}")
        return "⚠️ सर्वर बिजी है, बाद में ट्राई करें"

def auto_post():
    while True:
        now = time.strftime("%H:%M")
        if now in ["08:00", "12:00", "16:00"]:
            try:
                bot.send_message(PROMO_CHANNEL, "🆕 नया अपडेट! @All_Gift_Code_Earning ज्वाइन करें")
            except Exception as e:
                print(f"Posting Error: {str(e)}")
        time.sleep(3600)

def good_morning_poster():
    while True:
        now = time.strftime("%H:%M")
        if now == "05:00":
            try:
                prompt = "Write a short morning wish (under 20 words)"
                morning_msg = safe_generate(prompt)
                bot.send_message(PROMO_CHANNEL, f"☀️ {morning_msg[:100]}")
            except Exception as e:
                print(f"Morning Post Error: {str(e)}")
            time.sleep(60)
        time.sleep(30)

@bot.message_handler(func=lambda msg: True)
def track_all(message):
    user_id = message.from_user.id
    user_activity[user_id] = user_activity.get(user_id, 0) + 1
    if user_activity[user_id] % 10 == 0:
        try:
            bot.send_message(PROMO_CHANNEL, f"🏆 टॉप यूजर: @{message.from_user.username}")
        except Exception as e:
            print(f"Activity Error: {str(e)}")

@bot.message_handler(commands=['generate'])
def generate_text(message):
    prompt = message.text[10:].strip()
    if prompt:
        generated_text = safe_generate(prompt)
        bot.send_message(message.chat.id, generated_text)
    gc.collect()

# Start Services
keep_alive()
start_pinger()
threading.Thread(target=auto_post, daemon=True).start()
threading.Thread(target=good_morning_poster, daemon=True).start()
bot.infinity_polling()
