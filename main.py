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

PROMO_CHANNEL_ID = "-1002437678122"
PROMOTION_CHANNEL_LINK = "https://t.me/Proper_Trending"

# IMPORTANT: Render ka primary URL (बिना slash के)
RENDER_URL = os.environ.get("RENDER_URL", "https://earning-boss.onrender.com")
WEBHOOK_URL = f"{RENDER_URL}/webhook"

IS_RENDER = os.environ.get("RENDER") == "true"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ========== Images (your existing URLs) ==========
PROMO_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"
START_IMAGE_URL = PROMO_IMAGE_URL

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

# ========== Random profit templates ==========
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

# ========== Random attractive captions for users ==========
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

# ==================== Helper functions ====================
def get_random_promo_caption():
    return random.choice(PROMO_CAPTIONS)

def get_today_index(list_length):
    india_tz = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(india_tz).strftime("%j")) % list_length

def send_auto_post(templates, images, prefix_emoji):
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
        print(f"Auto post sent with profit ₹{profit_amount}")
    except Exception as e:
        print(f"Auto post error: {e}")

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
            current_hour = now.hour
            current_minute = now.minute
            current_day = now.day

            if last_day != current_day:
                posted_morning = False
                posted_night = False
                morning_target = random.randint(30, 60)
                night_target = random.randint(30, 60)
                last_day = current_day
                print(f"New targets - morning: {morning_target} min after 4:00, night: {night_target} min after 23:00")

            if not posted_morning and current_hour >= 4:
                mins_from_4 = (current_hour - 4) * 60 + current_minute
                if 30 <= mins_from_4 <= morning_target and mins_from_4 >= morning_target:
                    send_auto_post(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                    posted_morning = True

            if not posted_night:
                if current_hour == 23:
                    mins_from_23 = current_minute
                elif current_hour == 0:
                    mins_from_23 = 60 + current_minute
                else:
                    mins_from_23 = -1
                if 30 <= mins_from_23 <= night_target and mins_from_23 >= night_target:
                    send_auto_post(NIGHT_TEMPLATES, NIGHT_IMAGE_URLS, "🌙")
                    posted_night = True

            time.sleep(30)
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

@bot.callback_query_handler(func=lambda call: call.data == "send_promo")
def handle_legacy(call):
    try:
        bot.answer_callback_query(call.id, text="✅", show_alert=False)
        send_promo(call.message.chat.id)
    except Exception as e:
        print(f"Legacy callback error: {e}")

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

# ==================== Flask Webhook Endpoints ====================
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_str = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_str)
            bot.process_new_updates([update])
            return 'OK', 200
        except Exception as e:
            print(f"Webhook processing error: {e}")
            return 'Error', 500
    return 'Bad Request', 403

@app.route('/')
def home():
    return "Bot is running with webhook endpoint /webhook"

@app.route('/health')
def health():
    return "OK", 200

# ==================== Main ====================
if __name__ == "__main__":
    # Start auto-poster thread
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster started.")

    if IS_RENDER:
        # On Render: set webhook and run gunicorn (gunicorn will call app)
        # But here we are not running app.run() because gunicorn will import app.
        # However, this script is executed directly? In Render with gunicorn, __name__ is not "__main__".
        # So we need to set webhook at module level, not inside if __name__.
        # Let's set webhook now.
        try:
            bot.remove_webhook()
            webhook_success = bot.set_webhook(url=WEBHOOK_URL)
            if webhook_success:
                print(f"✅ Webhook set successfully to {WEBHOOK_URL}")
            else:
                print(f"❌ Failed to set webhook to {WEBHOOK_URL}")
        except Exception as e:
            print(f"Webhook setup error: {e}")
    else:
        # Local development: use polling
        print("Local mode: polling.")
        bot.infinity_polling()

# This is important: when gunicorn imports this module, it will create the 'app' object.
# The webhook setting code above will run at import time (outside if __name__) only if IS_RENDER is true.
# But careful: we don't want to set webhook multiple times. It's fine.
# For gunicorn, we need to ensure that webhook is set after the server is ready.
# A better approach: use a startup hook. But for simplicity, we set webhook at import.
# Render will call gunicorn, which imports this file, then runs the app.
