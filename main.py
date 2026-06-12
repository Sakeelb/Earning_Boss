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
    print("WARNING: OWNER_ID not set. User messages will not be forwarded.")

PROMO_CHANNEL_ID = "-1002437678122"          # channel for auto morning/night posts
PROMOTION_POST_LINK = "https://t.me/Proper_Trending/1098"   # your channel post link

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER") == "true"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ========== Images ==========
PROMO_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"
START_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"

# ⚠️ Caption – bilkul neutral, helpful, non‑promotional
PROMO_CAPTION = "यह जानकारी आपके काम की हो सकती है। एक बार देख लेना फायदेमंद रहेगा।"

# ========== Good Morning / Good Night images (auto-posts in your channel) ==========
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

# ========== Random profit templates (only for auto-posts in your channel) ==========
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

# ========== Keywords – these trigger the subtle promo ==========
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

# /start message – extremely simple, no hint of promotion
START_MESSAGE_TEXT = "नमस्ते! कुछ उपयोगी बातें आपके लिए हैं। नीचे दिए बटन पर क्लिक करके देख सकते हैं।"

# ==================== Helper functions ====================
def get_today_index(list_length):
    india_tz = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(india_tz).strftime("%j")) % list_length

def send_message_auto(templates, images, prefix_emoji):
    """Auto‑post to your channel (morning/night) – user does not see this unless they are in your channel."""
    try:
        profit_amount = random.randint(100, 1000)
        idx = get_today_index(len(templates))
        template = templates[idx]
        msg = template.format(amount=profit_amount)
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
        print(f"Auto message sent with profit ₹{profit_amount}")
    except Exception as e:
        print(f"Auto send error: {e}")

def auto_poster():
    posted_morning = False
    posted_night = False
    india_tz = pytz.timezone('Asia/Kolkata')
    morning_min = random.randint(0, 10)
    night_min = random.randint(0, 10)
    last_day = datetime.now(india_tz).day

    while True:
        try:
            now = datetime.now(india_tz)
            hour = now.hour
            minute = now.minute
            today = now.day

            if today != last_day:
                posted_morning = False
                posted_night = False
                morning_min = random.randint(0, 10)
                night_min = random.randint(0, 10)
                last_day = today

            if hour == 5 and not posted_morning and minute >= morning_min:
                send_message_auto(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                posted_morning = True
            if hour == 22 and not posted_night and minute >= night_min:
                send_message_auto(NIGHT_TEMPLATES, NIGHT_IMAGE_URLS, "🌙")
                posted_night = True

            time.sleep(60)
        except Exception as e:
            print(f"Auto-poster error: {e}")
            traceback.print_exc()
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

# ========== Ultra subtle promo sender ==========
def send_subtle_info(chat_id):
    """User ko lagega ki yeh general helpful information hai, promotion nahi."""
    markup = InlineKeyboardMarkup()
    # Button text bilkul neutral – "जानकारी देखें" / "विस्तार से पढ़ें"
    markup.add(InlineKeyboardButton("📄 विस्तार से पढ़ें", url=PROMOTION_POST_LINK))
    try:
        bot.send_photo(chat_id, PROMO_IMAGE_URL, caption=PROMO_CAPTION,
                       parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Send subtle info error: {e}")

# ==================== Bot handlers ====================
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📄 जानकारी देखें", url=PROMOTION_POST_LINK))
        bot.send_photo(message.chat.id, START_IMAGE_URL, caption=START_MESSAGE_TEXT,
                       parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"/start error: {e}")

# Legacy callback handler (if any old button remains)
@bot.callback_query_handler(func=lambda call: call.data == "send_promo")
def handle_promo_button(call):
    try:
        bot.answer_callback_query(call.id, text="✅", show_alert=False)
        send_subtle_info(call.message.chat.id)
    except Exception as e:
        print(f"Callback error: {e}")

# Keyword reply – same subtle info
@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    if not message.text:
        return
    if keyword_found(message.text):
        try:
            send_subtle_info(message.chat.id)
        except Exception as e:
            print(f"Keyword reply error: {e}")

# Forward all user messages to owner (so you can talk to them)
@bot.message_handler(func=lambda msg: True, priority=1)
def forward_to_owner(message):
    if not OWNER_ID:
        return
    if message.chat.id == OWNER_ID:
        return
    try:
        user = message.from_user
        user_name = user.first_name or ""
        if user.username:
            user_name += f" (@{user.username})"
        forward_text = f"📩 *नया मैसेज*\n👤 {user_name}\n🆔 `{user.id}`\n💬 {message.text}"
        bot.send_message(OWNER_ID, forward_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Forward error: {e}")

# ==================== Flask webhook ====================
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 403

@app.route('/')
def home():
    return "Bot is running with ultra‑subtle promotion (user does not realise)."

@app.route('/health')
def health():
    return "OK", 200

# ==================== Main ====================
if __name__ == "__main__":
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster started.")

    if IS_RENDER and BOT_TOKEN and WEBHOOK_URL:
        try:
            bot.remove_webhook()
            bot.set_webhook(url=f"{WEBHOOK_URL}/")
            print(f"Webhook set to {WEBHOOK_URL}/")
            app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        except Exception as e:
            print(f"Webhook error: {e}. Fallback to polling.")
            bot.infinity_polling()
    else:
        print("Local mode: polling.")
        bot.infinity_polling()
