import os
import re
import random
import time
import threading
import traceback
import pytz
from datetime import datetime
from flask import Flask, request
import telebot

# ==================== CONFIGURATION ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("FATAL: BOT_TOKEN environment variable not set.")

PROMO_CHANNEL_ID = "-1002437678122"   # Must start with -100
if not PROMO_CHANNEL_ID.startswith('-100'):
    raise ValueError("PROMO_CHANNEL_ID must start with '-100'")

PROMOTION_CHANNEL_USERNAME = "@Proper_Trending"
PROMOTION_CHANNEL_LINK = "https://t.me/Proper_Trending"

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER") == "true"   # Convert to boolean

# File to remember last posted dates (avoids double‑posting after restart)
LAST_POST_FILE = "last_post.txt"

# ==================== IMAGES & MESSAGES ====================
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

UNIQUE_MORNING_MESSAGES = [
    "*Good Morning!* आज ₹300 तक फायदेमंद रहेगा।",
    "*Good Morning!* कम से कम ₹250 का फायदा तय है आज।",
    "*Good Morning!* दिन शुरू होते ही ₹400 का फायदा मिलेगा।",
    "*Good Morning!* आज का दिन ₹500 कमाने लायक है।",
    "*Good Morning!* सीधा ₹350 का फायदा मिलेगा Boss।",
    "*Good Morning!* ₹200 आज पक्का जेब में आएगा।",
    "*Good Morning!* आज ₹450 तक फिक्स कमाई होने वाली है।",
    "*Good Morning!* ₹300 की कमाई बिना रुकावट होगी आज।",
    "*Good Morning!* दिन की शुरुआत ₹250 के फायदे से।",
    "*Good Morning!* ₹500 तक का फायदा आज तय है - रुकना नहीं।"
]

UNIQUE_NIGHT_MESSAGES = [
    "*Good Night All Members!* कल का दिन ₹500 कमाना पका है।",
    "*Good Night All Members!* कल ₹400 की कमाई होगी।",
    "*Good Night All Members!* कल ₹350 का फायदा मिलेगा।",
    "*Good Night All Members!* कल सुबह ₹300 की कमाई शुरू होगी।",
    "*Good Night All Members!* कल ₹250 का फायदा पक्का है।",
    "*Good Night All Members!* कल ₹450 तक कमाने का मौका है।",
    "*Good Night All Members!* कल ₹200 से शुरू होगा दिन।",
    "*Good Night All Members!* कल ₹550 तक कमाने का चांस है।",
    "*Good Night All Members!* कल ₹300 से ₹500 तक कमाई होगी।",
    "*Good Night All Members!* कल सीधा ₹400 का फायदा मिलेगा।"
]

START_MESSAGE_TEXT = f"""
*Urgent Update:*
*Naya Gift Code / Offer Live ho chuka hai.*
*Isko paane ke liye hamare channel se juden:*
*[[ {PROMOTION_CHANNEL_USERNAME} ]]*
"""
START_IMAGE_URL = "https://github.com/Sakeelb/Earning_Boss/blob/fd7a30f7826fe65abb99a0baeff70878fbc04815/New/1781241774791.png"

# ==================== KEYWORDS (improved) ====================
KEYWORDS = [
    "subscribe", "chat", "reply", "join", "joining", "refer", "register",
    "earning", "https", "invite", "@", "channel", "मेरे चैनल", "मेरा चैनल",
    "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo",
    "reward", "bonus", "gift", "win", "offer", "loot", "free", "telegram",
    "new offer", "today offer", "instant reward", "free gift code", "giveaway",
    "task earning", "refer and earn", "daily bonus", "claim reward", "kamai",
    "पैसे", "paise kaise", "online paise", "ghar baithe kamai", "extra earning",
    "make money online", "earn money", "withdrawal proof", "payment proof",
    "real earning", "trusted earning", "instant payment", "upi earning",
    "paytm cash", "google pay offer", "crypto earning", "bitcoin earning",
    "ethereum earning", "online job", "work from home", "part time job",
    "full time job", "referred", "referring", "ref", "referal", "refer code",
    "joining bonus", "joining link", "/join"
]

# ==================== HELPER FUNCTIONS ====================
def get_today_index(list_length):
    """Return index based on day of year (1-366)"""
    india_tz = pytz.timezone('Asia/Kolkata')
    day_of_year = int(datetime.now(india_tz).strftime("%j"))
    return day_of_year % list_length

def load_last_post_dates():
    """Load last posting dates from file (prevents double posts on restart)"""
    if not os.path.exists(LAST_POST_FILE):
        return {"morning": None, "night": None}
    try:
        with open(LAST_POST_FILE, "r") as f:
            data = f.read().strip().split(",")
            return {"morning": data[0] if data[0] != "None" else None,
                    "night": data[1] if data[1] != "None" else None}
    except:
        return {"morning": None, "night": None}

def save_last_post_dates(morning_date=None, night_date=None):
    """Save last posting dates to file"""
    with open(LAST_POST_FILE, "w") as f:
        f.write(f"{morning_date},{night_date}")

def send_message_auto(messages, images, prefix_emoji, post_type):
    """
    Send photo to PROMO_CHANNEL_ID with reaction.
    post_type: "morning" or "night"
    """
    try:
        idx = get_today_index(len(messages))
        msg = messages[idx]
        # Use separate index for images, cycling if necessary
        img_idx = idx % len(images)
        image_url = images[img_idx]
        caption = f"{prefix_emoji} {msg}"

        print(f"Sending {post_type} to {PROMO_CHANNEL_ID} ...")
        sent = bot.send_photo(PROMO_CHANNEL_ID, image_url, caption=caption, parse_mode='Markdown')
        print(f"Sent, message_id = {sent.message_id}")

        # Add reactions (ignores errors if channel doesn't support reactions)
        for emoji in ['👍', '❤️']:
            try:
                bot.set_message_reaction(PROMO_CHANNEL_ID, sent.message_id, reaction=[{'type': 'emoji', 'emoji': emoji}])
            except Exception as react_err:
                print(f"Reaction {emoji} failed (ignored): {react_err}")

        # Update last post date
        today_str = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
        saved = load_last_post_dates()
        if post_type == "morning":
            save_last_post_dates(morning_date=today_str, night_date=saved["night"])
        else:
            save_last_post_dates(morning_date=saved["morning"], night_date=today_str)

    except Exception as e:
        print(f"ERROR in send_message_auto ({post_type}): {e}")
        print(traceback.format_exc())

def keyword_found(text):
    """Check if message contains any promotional keyword (Hindi friendly)"""
    if not text:
        return False
    text_lower = text.lower()
    # Remove punctuation except @, /, ., and space
    text_clean = re.sub(r'[^\w\s@/\.]', '', text_lower)

    for kw in KEYWORDS:
        kw_lower = kw.lower()
        # Special handling for URL parts
        if kw_lower in ["https", "@", "t.me", "bit.ly"]:
            if kw_lower in text_clean:
                return True
        # For Hindi and short English words, use simple substring
        if kw_lower in ["चैनल", "ज्वाइन", "कमई", "पैसे", "फ़ॉलो", "join", "chat", "/join"]:
            if kw_lower in text_clean:
                return True
        # For normal English keywords, use word boundaries (ASCII only)
        if re.search(r'\b' + re.escape(kw_lower) + r'\b', text_clean):
            return True
    return False

# ==================== AUTO POSTER THREAD ====================
def auto_poster():
    """Background thread: posts Good Morning (5:00-5:10 AM) and Good Night (10:00-10:10 PM) IST"""
    india_tz = pytz.timezone('Asia/Kolkata')
    # Random minute offset for the day (0-10)
    morning_target_min = random.randint(0, 10)
    night_target_min = random.randint(0, 10)

    print(f"Auto-poster started. Morning target: 05:{morning_target_min:02d}, Night target: 22:{night_target_min:02d}")

    while True:
        try:
            now = datetime.now(india_tz)
            current_date = now.strftime("%Y-%m-%d")
            hour = now.hour
            minute = now.minute

            # Load last posted dates
            last_posts = load_last_post_dates()

            # ---- Morning post (5:00-5:10) ----
            if hour == 5 and minute >= morning_target_min and last_posts["morning"] != current_date:
                print("Time to send Good Morning!")
                send_message_auto(UNIQUE_MORNING_MESSAGES, MORNING_IMAGE_URLS, "☀️", "morning")
                # After posting, regenerate random minutes for next day
                morning_target_min = random.randint(0, 10)
                night_target_min = random.randint(0, 10)
                print(f"New targets for tomorrow: 05:{morning_target_min:02d}, 22:{night_target_min:02d}")

            # ---- Night post (22:00-22:10) ----
            if hour == 22 and minute >= night_target_min and last_posts["night"] != current_date:
                print("Time to send Good Night!")
                send_message_auto(UNIQUE_NIGHT_MESSAGES, NIGHT_IMAGE_URLS, "🌙", "night")
                # Regenerate random minutes for next day
                morning_target_min = random.randint(0, 10)
                night_target_min = random.randint(0, 10)
                print(f"New targets for tomorrow: 05:{morning_target_min:02d}, 22:{night_target_min:02d}")

            time.sleep(60)  # check every minute

        except Exception as e:
            print(f"Auto-poster error: {e}")
            print(traceback.format_exc())
            time.sleep(300)

# ==================== TELEGRAM HANDLERS ====================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.send_photo(message.chat.id, START_IMAGE_URL, caption=START_MESSAGE_TEXT, parse_mode='Markdown')
    except Exception as e:
        print(f"/start error for {message.chat.id}: {e}")

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    if not message.text:
        return
    print(f"Msg from {message.chat.id}: {message.text[:50]}")
    if keyword_found(message.text):
        try:
            promo_caption = f"*[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]]*\n*[[ {PROMOTION_CHANNEL_LINK} ]]*"
            bot.send_photo(
                chat_id=message.chat.id,
                photo="https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png",
                caption=promo_caption,
                parse_mode='Markdown',
                reply_to_message_id=message.message_id
            )
        except Exception as e:
            print(f"Promo reply error: {e}")

# ==================== FLASK WEBHOOK ====================
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 403

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

# ==================== MAIN ====================
if __name__ == "__main__":
    # Start the auto-poster thread
    threading.Thread(target=auto_poster, daemon=True).start()

    if IS_RENDER:
        if BOT_TOKEN and WEBHOOK_URL:
            try:
                bot.remove_webhook()
                bot.set_webhook(url=f"{WEBHOOK_URL}/")
                print(f"Webhook set to {WEBHOOK_URL}/")
                app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
            except Exception as e:
                print(f"Webhook failed: {e}. Falling back to long polling.")
                bot.infinity_polling()
        else:
            print("Missing BOT_TOKEN or WEBHOOK_URL for Render. Using long polling.")
            bot.infinity_polling()
    else:
        print("Running locally with long polling.")
        bot.infinity_polling()
