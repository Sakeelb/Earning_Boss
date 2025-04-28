import os
import telebot
import time
import threading
from keep_alive import keep_alive
from ping_self import start_pinger
from transformers import pipeline

# Env Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL")

# Init
bot = telebot.TeleBot(BOT_TOKEN)
generator = pipeline('text-generation', model='gpt2')
referral_data = {}
user_activity = {}
VIP_USERS = {}

# Auto-Poster
def auto_post():
    while True:
        now = time.strftime("%H:%M")
        if now in ["08:00", "12:00", "16:00"]:
            bot.send_message(PROMO_CHANNEL, "🆕 नया अपडेट! @All_Gift_Code_Earning ज्वाइन करें")
        time.sleep(3600)

# Commands
@bot.message_handler(commands=['start'])
def start_handler(message):
    if 'ref_' in message.text:
        referrer = int(message.text.split('ref_')[1])
        referral_data[message.from_user.id] = referrer
        bot.send_message(referrer, f"🔥 नया रेफरल आया! Total: {list(referral_data.values()).count(referrer)}")
    
    bot.forward_message(message.chat.id, '@All_Gift_Code_Earning', 398)

@bot.message_handler(commands=['ref'])
def referral_handler(message):
    referral_link = f"https://t.me/{bot.get_me().username}?start=ref_{message.from_user.id}"
    bot.reply_to(message, f"🎁 5 Referrals = VIP Status!\n\nYour Link:\n{referral_link}")

@bot.message_handler(commands=['generate'])
def ai_generate(message):
    prompt = " ".join(message.text.split()[1:])
    ai_content = generator(prompt, max_length=50)[0]['generated_text']
    bot.reply_to(message, f"🤖 AI Generated:\n\n{ai_content}")

@bot.message_handler(commands=['vip'])
def vip_command(message):
    user_id = message.from_user.id
    ref_count = list(referral_data.values()).count(user_id)
    if ref_count >= 5:
        VIP_USERS[user_id] = True
        bot.reply_to(message, "🌟 VIP स्टेटस एक्टिवेट हुआ!")
    else:
        bot.reply_to(message, f"❌ {5-ref_count} और रेफरल्स चाहिए")

# Activity Tracking
@bot.message_handler(func=lambda msg: True)
def track_all(message):
    user_id = message.from_user.id
    user_activity[user_id] = user_activity.get(user_id, 0) + 1
    
    if user_activity[user_id] % 5 == 0:
        bot.send_message(PROMO_CHANNEL, f"🏆 टॉप यूजर: @{message.from_user.username}")

    # Auto-Reply Logic
    keywords = ["join", "earn", "channel", "t.me/", "refer"]
    if any(k in message.text.lower() for k in keywords):
        bot.reply_to(message, "[[Boss >> हमारे चैनल को भी Join करें:]] [[ https://t.me/All_Gift_Code_Earning ]]")

# Start Services
keep_alive()
start_pinger()
threading.Thread(target=auto_post).start()
bot.infinity_polling()
