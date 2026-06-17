import os
import telebot
import threading
import time
import random
import re
from datetime import datetime
from flask import Flask, request
import pytz
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== CONFIG FROM ENVIRONMENT ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

OWNER_ID = os.environ.get("OWNER_ID")
if OWNER_ID:
    OWNER_ID = int(OWNER_ID)
else:
    print("WARNING: OWNER_ID not set. User messages will not be forwarded.")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL") # Render App URL (e.g., https://your-app.onrender.com)

PROMO_CHANNEL_ID = "-1002437678122"          # आपके चैनल की ID
PROMO_CHANNEL_LINK = "https://t.me/Proper_Trending"   # चैनल लिंक

bot = telebot.TeleBot(BOT_TOKEN)
flask_app = Flask(__name__)

# ========== IMAGES & TEMPLATES (UNCHANGED) ==========
PROMO_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"

MORNING_IMAGE_URLS = [
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%201.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%202.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%203.jpg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%204.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%205.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%206.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%207.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%208.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Morning%209.jpeg"
]

NIGHT_IMAGE_URLS = [
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%201.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%202.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%203.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%204.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%205.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%206.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%207.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%208.jpeg",
    "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/Good%20Night%209.jpeg"
]

MORNING_TEMPLATES = [
    "*Good Morning!* आज ₹{amount} तक फायदेमंद रहेगा।",
    "*Good Morning!* कम से कम ₹{amount} का फायदा तय है आज।",
    "*Good Morning!* दिन शुरू होते ही ₹{amount} का फायदा मिलेगा।",
    "*Good Morning!* आज का दिन ₹{amount} कमाने लायक है।",
    "*Good Morning!* सीधा ₹{amount} का फायदा मिलेगा Boss।",
    "*Good Morning!* ₹{amount} आज पक्का जेब में आएगा।",
    "*Good Morning!* आज ₹{amount} तक फिक्स कमाई होने वाली है।",
    "*Good Morning!* ₹{amount} की कमाई बिना रुकावट होगी आज।",
    "*Good Morning!* दिन की शुरुआत ₹{amount} के फायदे से।",
    "*Good Morning!* ₹{amount} तक का फायदा आज तय है - रुकना नहीं।"
]

NIGHT_TEMPLATES = [
    "*Good Night All Members!* कल का दिन ₹{amount} कमाना पका है।",
    "*Good Night All Members!* कल ₹{amount} की कमाई होगी।",
    "*Good Night All Members!* कल ₹{amount} का फायदा मिलेगा।",
    "*Good Night All Members!* कल सुबह ₹{amount} की कमाई शुरू होगी।",
    "*Good Night All Members!* कल ₹{amount} का फायदा पक्का है।",
    "*Good Night All Members!* कल ₹{amount} तक कमाने का मौका है।",
    "*Good Night All Members!* कल ₹{amount} से शुरू होगा दिन।",
    "*Good Night All Members!* कल ₹{amount} तक कमाने का चांस है।",
    "*Good Night All Members!* कल ₹{amount} तक कमाई होगी।",
    "*Good Night All Members!* कल सीधा ₹{amount} का फायदा मिलेगा।"
]

PROMO_CAPTIONS = [
    "🚀 Live New Loot! Fast Join Telegram Channel",
    "💰 Exclusive Offer: Channel Join Karo aur Kamao",
    "⚡ Limited Time: Naye Loot Codes Aaye Hain",
    "🔥 Daily Bonus: Channel Join Karke Pao",
    "📢 Urgent Update: Channel Join Karein Abhi",
    "🎁 Free Gift Code: Channel Par Available",
    "💸 बिना Investment कमाई शुरू करें, Join Now",
    "🤫 Secret Offer: Sirf Channel Members Ke Liye",
    "👑 VIP Loot: Channel Join Karo aur Claim Karo",
    "🎯 Target Complete: Channel Join Karo, Mil Sakta Hai Reward"
]

KEYWORDS = [
    "subscribe", "chat", "reply", "join", "joining", "refer", "register", "earning",
    "https", "invite", "@", "channel", "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो",
    "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward", "bonus", "gift", "win", "offer", "loot",
    "free", "telegram", "new offer", "today offer", "instant reward", "free gift code", "giveaway",
    "task earning", "refer and earn", "daily bonus", "claim reward", "kamai", "पैसे", "paise kaise",
    "online paise", "ghar baithe kamai", "extra earning", "make money online", "earn money",
    "withdrawal proof", "payment proof", "real earning", "trusted earning", "instant payment",
    "upi earning", "paytm cash", "google pay offer", "crypto earning", "bitcoin earning",
    "ethereum earning", "online job", "work from home", "part time job", "full time job",
    "referred", "referring", "ref", "referal", "refer code", "joining bonus", "joining link", "/join"
]

# ========== HELPER FUNCTIONS ==========
def get_today_index(length):
    india_tz = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(india_tz).strftime("%j")) % length

def send_channel_auto(templates, images, prefix_emoji):
    try:
        profit = random.randint(100, 1000)
        idx = get_today_index(len(templates))
        msg = templates[idx].format(amount=profit)
        img_idx = idx % len(images)
        image_url = images[img_idx]
        caption = f"{prefix_emoji} {msg}"
        sent = bot.send_photo(PROMO_CHANNEL_ID, image_url, caption=caption, parse_mode='Markdown')
        if sent:
            for emoji in ['👍', '❤️']:
                try:
                    bot.set_message_reaction(PROMO_CHANNEL_ID, sent.message_id, reaction=[{'type': 'emoji', 'emoji': emoji}])
                except:
                    pass
        print(f"Auto-post sent with profit ₹{profit}")
    except Exception as e:
        print(f"Auto-post error: {e}")

def auto_poster():
    india_tz = pytz.timezone('Asia/Kolkata')
    morning_target = random.randint(30, 60)
    night_target = random.randint(30, 60)
    posted_morning = False
    posted_night = False
    last_day = None

    while True:
        try:
            now = datetime.now(india_tz)
            hour = now.hour
            minute = now.minute
            day = now.day

            if last_day != day:
                posted_morning = False
                posted_night = False
                morning_target = random.randint(30, 60)
                night_target = random.randint(30, 60)
                last_day = day

            if not posted_morning and hour >= 4:
                mins_from_4 = (hour - 4) * 60 + minute
                if 30 <= mins_from_4 <= morning_target and mins_from_4 >= morning_target:
                    send_channel_auto(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                    posted_morning = True

            if not posted_night:
                if hour == 23:
                    mins_from_23 = minute
                elif hour == 0:
                    mins_from_23 = 60 + minute
                else:
                    mins_from_23 = -1
                if 30 <= mins_from_23 <= night_target and mins_from_23 >= night_target:
                    send_channel_auto(NIGHT_TEMPLATES, NIGHT_IMAGE_URLS, "🌙")
                    posted_night = True

            time.sleep(30)
        except Exception as e:
            print(f"Auto-poster error: {e}")
            time.sleep(300)

def keyword_found(text):
    if not text:
        return False
    text = text.lower()
    text = re.sub(r'[^\w\s@/\.]', '', text)
    for kw in KEYWORDS:
        kw_low = kw.lower()
        if kw_low in ["https", "@", "t.me", "bit.ly"]:
            if kw_low in text:
                return True
        if kw_low in ["चैनल", "ज्वाइन", "कमई", "पैसे", "फ़ॉलो", "join", "chat", "/join"]:
            if kw_low in text:
                return True
        if re.search(r'\b' + re.escape(kw_low) + r'\b', text):
            return True
    return False

def send_promo(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Start Earning", url=PROMO_CHANNEL_LINK))
    caption = random.choice(PROMO_CAPTIONS)
    try:
        bot.send_photo(chat_id, PROMO_IMAGE_URL, caption=caption, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Send promo error: {e}")

# ========== BOT HANDLERS ==========
@bot.message_handler(commands=['start'])
def start_handler(msg):
    send_promo(msg.chat.id)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(msg):
    if OWNER_ID and msg.chat.id == OWNER_ID:
        return

    if msg.text and keyword_found(msg.text):
        send_promo(msg.chat.id)

    if OWNER_ID:
        try:
            user = msg.from_user
            name = user.first_name or "No Name"
            if user.username:
                name += f" (@{user.username})"
            forward_text = f"📩 *नया मैसेज*\n👤 {name}\n🆔 `{user.id}`\n💬 {msg.text if msg.text else '[Non-text message]'}"
            bot.send_message(OWNER_ID, forward_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Forward error: {e}")

# ========== WEBHOOK & HEALTH ROUTE ==========
@flask_app.route('/health')
def health():
    return "OK", 200

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

# ========== MAIN RUNNER ==========
if __name__ == "__main__":
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster thread initialized.")

    if WEBHOOK_URL:
        try:
            bot.remove_webhook()
            bot.set_webhook(url=f"{WEBHOOK_URL.strip('/')}/webhook")
            print(f"Webhook successfully set to: {WEBHOOK_URL}/webhook")
        except Exception as e:
            print(f"Failed to set webhook: {e}")
    else:
        try:
            bot.remove_webhook()
        except:
            pass
        print("WEBHOOK_URL not found, falling back to Polling...")
        threading.Thread(target=bot.infinity_polling, daemon=True).start()

    port = int(os.environ.get('PORT', 5000))
    flask_app.run(host='0.0.0.0', port=port)
