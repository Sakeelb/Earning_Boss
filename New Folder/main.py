import os
import telebot
import time
import threading
import openai
from keep_alive import keep_alive
from ping_self import start_pinger

# Env Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(BOT_TOKEN)
user_activity = {}

def ai_generate(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # या "gpt-4" अगर आपकी की सपोर्ट करे
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        return "⚠️ AI सर्वर बिजी है, बाद में ट्राई करें"

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
                morning_msg = ai_generate(prompt)
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

@bot.message_handler(commands=['generate', 'ai', 'ask'])
def generate_text(message):
    prompt = message.text.split(' ', 1)[-1].strip()
    if prompt:
        generated_text = ai_generate(prompt)
        bot.send_message(message.chat.id, generated_text)
    else:
        bot.reply_to(message, "कृपया कमांड के बाद सवाल लिखें।\nउदाहरण: /ai आज मौसम कैसा है?")

# Start Services
keep_alive()
start_pinger()
threading.Thread(target=auto_post, daemon=True).start()
threading.Thread(target=good_morning_poster, daemon=True).start()
bot.infinity_polling()
