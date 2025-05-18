import os
import telebot
import threading
import time
from flask import Flask, request
import pytz
from datetime import datetime
import re
import random

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = "@All_Gift_Code_Earning"
FORWARD_MESSAGE_ID = 398
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 4 Good Morning इमेज URLs
MORNING_IMAGE_URLS = [
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%201.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%202.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%203.jpg"
]

# 4 Good Night इमेज URLs
NIGHT_IMAGE_URLS = [
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%201.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%202.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%203.jpeg"
]

# 4 Good Morning मैसेज
UNIQUE_MORNING_MESSAGES = [
    "Good Morning! आज ₹300 तक फायदेमंद रहेगा।",
    "Good Morning! कम से कम ₹250 का फायदा तय है आज।",
    "Good Morning! दिन शुरू होते ही ₹400 का फायदा मिलेगा।",
    "Good Morning! आज का दिन ₹500 कमाने लायक है।",
    "Good Morning! सीधा ₹350 का फायदा मिलेगा Boss।",
    "Good Morning! ₹200 आज पक्का जेब में आएगा।",
    "Good Morning! आज ₹450 तक फिक्स कमाई होने वाली है।",
    "Good Morning! ₹300 की कमाई बिना रुकावट होगी आज।",
    "Good Morning! दिन की शुरुआत ₹250 के फायदे से।",
    "Good Morning! ₹500 तक का फायदा आज तय है - रुकना नहीं।"
]

# 4 Good Night मैसेज
UNIQUE_NIGHT_MESSAGES = [
    "Good Night All Members! कल का दिन ₹500 कमाना पका है।",
    "Good Night All Members! कल ₹400 की कमाई होगी।",
    "Good Night All Members! कल ₹350 का फायदा मिलेगा।",
    "Good Night All Members! कल सुबह ₹300 की कमाई शुरू होगी।",
    "Good Night All Members! कल ₹250 का फायदा पक्का है।",
    "Good Night All Members! कल ₹450 तक कमाने का मौका है।",
    "Good Night All Members! कल ₹200 से शुरू होगा दिन।",
    "Good Night All Members! कल ₹550 तक कमाने का चांस है।",
    "Good Night All Members! कल ₹300 से ₹500 तक कमाई होगी।",
    "Good Night All Members! कल सीधा ₹400 का फायदा मिलेगा।"
]

KEYWORDS = [
    "subscribe", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
    "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward",
    "bonus", "gift", "win", "offer", "loot", "free", "telegram",
    "new offer", "today offer", "instant reward", "free gift code", "giveaway",
    "task earning", "refer and earn", "daily bonus", "claim reward",
    "kamai", "पैसे", "paise kaise", "online paise", "ghar baithe kamai",
    "extra earning", "make money online", "earn money",
    "withdrawal proof", "payment proof", "real earning", "trusted earning",
    "instant payment", "upi earning", "paytm cash", "google pay offer",
    "crypto earning", "bitcoin earning", "ethereum earning", "online job",
    "work from home", "part time job", "full time job",
    "referred", "referring", "ref", "referal", "refer code", "joining bonus", "joining link",
    "/join"
]

def get_today_index(list_length):
    today = int(datetime.now().strftime("%j"))
    return today % list_length

def send_message_auto(messages, images, prefix_emoji):
    try:
        idx = get_today_index(len(messages))
        msg = messages[idx]
        image_url = images[idx % len(images)]
        caption = f"{prefix_emoji} {msg}"
        bot.send_photo(PROMO_CHANNEL, image_url, caption=caption)
    except Exception as e:
        print(f"Error sending auto message: {e}")

def auto_poster():
    posted_morning = False
    posted_night = False
    india_timezone = pytz.timezone('Asia/Kolkata')
    
    while True:
        now = datetime.now(india_timezone)
        current_hour = now.strftime("%H")
        current_minute = int(now.strftime("%M"))
        
        # Reset at midnight
        if current_hour == "00" and current_minute == 0:
            posted_morning = False
            posted_night = False
        
        # Good Morning (5:00 - 5:09 AM)
        if current_hour == "05" and not posted_morning:
            if 0 <= current_minute <= 9:
                send_message_auto(UNIQUE_MORNING_MESSAGES, MORNING_IMAGE_URLS, "☀️")
                posted_morning = True
        
        # Good Night (10:00 - 10:09 PM)
        if current_hour == "22" and not posted_night:
            if 0 <= current_minute <= 9:
                send_message_auto(UNIQUE_NIGHT_MESSAGES, NIGHT_IMAGE_URLS, "🌙")
                posted_night = True
        
        time.sleep(20)

@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=PROMO_CHANNEL,
            message_id=FORWARD_MESSAGE_ID
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"Error in /start: {e}")

def keyword_found(text):
    text = text.lower()
    text = re.sub(r'[^\w\s@/]', '', text)
    for kw in KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
        if kw in ["refer", "join", "earn", "चैनल", "ज्वाइन"]:
            if kw in text:
                return True
    if re.search(r'(https?://\S+|t\.me/\S+|bit\.ly/\S+)', text):
        return True
    return False

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    try:
        if not message.text:
            return
        if keyword_found(message.text):
            promo_text = "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]]\n[[ https://t.me/All_Gift_Code_Earning ]]"
            bot.reply_to(message, promo_text)
            bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=PROMO_CHANNEL,
                message_id=FORWARD_MESSAGE_ID
            )
    except Exception as e:
        print(f"Error in promo_reply: {e}")

@app.route('/', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def home():
    return "Bot is running."

if __name__ == "__main__":
    threading.Thread(target=auto_poster, daemon=True).start()
    if IS_RENDER:
        if WEBHOOK_URL:
            bot.set_webhook(url=f"{WEBHOOK_URL}/")
            app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        else:
            print("WEBHOOK_URL environment variable not set on Render. Webhook will not be set.")
    else:
        print("Running with long polling (for local development).")
        bot.infinity_polling()
