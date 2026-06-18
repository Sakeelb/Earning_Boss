import os
import telebot
import threading
import time
import random
import re
from datetime import datetime
from flask import Flask
import pytz
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== CONFIG ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

try:
    OWNER_ID = int(os.environ.get("OWNER_ID"))
except (TypeError, ValueError):
    OWNER_ID = 0
    print("WARNING: OWNER_ID not set or invalid numeric ID.")

PROMO_CHANNEL_ID = "-1002437678122"
PROMO_CHANNEL_LINK = "https://t.me/Proper_Trending"

bot = telebot.TeleBot(BOT_TOKEN)
flask_app = Flask(__name__)

@flask_app.route('/health')
def health():
    return "OK", 200

# ========== इमेज URLs ==========
PROMO_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"

# Real-looking random morning images (Unsplash free)
MORNING_IMAGE_URLS = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=800&q=80",
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&q=80",
    "https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=800&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80",
    "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=800&q=80",
    "https://images.unsplash.com/photo-1490682143684-14369e18dce8?w=800&q=80",
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
    "https://images.unsplash.com/photo-1418065460487-3e41a6c84dc5?w=800&q=80",
    "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&q=80",
    "https://images.unsplash.com/photo-1526749837599-b4eba9fd855e?w=800&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "https://images.unsplash.com/photo-1462275646964-a0e3386b89fa?w=800&q=80",
    "https://images.unsplash.com/photo-1445543949571-ffc3e0e2f55e?w=800&q=80",
    "https://images.unsplash.com/photo-1484821582734-6c6c9f99a672?w=800&q=80"
]

# Real-looking random night images (Unsplash free)
NIGHT_IMAGE_URLS = [
    "https://images.unsplash.com/photo-1475274047050-1d0c0975c63e?w=800&q=80",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800&q=80",
    "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800&q=80",
    "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&q=80",
    "https://images.unsplash.com/photo-1493514789931-586cb221d7a7?w=800&q=80",
    "https://images.unsplash.com/photo-1507400492013-162706c8c05e?w=800&q=80",
    "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=800&q=80",
    "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9?w=800&q=80",
    "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=800&q=80",
    "https://images.unsplash.com/photo-1536514498073-50e69d39c6cf?w=800&q=80",
    "https://images.unsplash.com/photo-1518655048521-f130df041f66?w=800&q=80",
    "https://images.unsplash.com/photo-1505765050516-f72dcac9c60e?w=800&q=80",
    "https://images.unsplash.com/photo-1511497584788-876760111969?w=800&q=80",
    "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=800&q=80",
    "https://images.unsplash.com/photo-1490750967868-88df5691cc4c?w=800&q=80"
]

# ========== REAL-LOOKING TEMPLATES ==========
MORNING_TEMPLATES = [
    "*Good Morning!* Aaj ₹{amount} tak ki earning possible hai. 💰",
    "*Good Morning!* Aaj ₹{amount} ka mauka hai — miss mat karna. ⚡",
    "*Good Morning!* Subah ho gayi, aaj ₹{amount} tak kama sakte ho. ☀️",
    "*Good Morning!* Aaj ₹{amount} tak ki direct earning hai. 🔥",
    "*Good Morning!* ₹{amount} aaj possible hai — join karo. 💸",
    "*Good Morning!* Aaj ka din ₹{amount} kamane wala hai. 🌅",
    "*Good Morning!* ₹{amount} aaj pak ka hai — deri mat karo. ⏰",
    "*Good Morning!* Aaj ₹{amount} tak ki kamai ho sakti hai. 💰",
    "*Good Morning!* Naya din, naya mauka — ₹{amount} aaj. 🌄",
    "*Good Morning!* ₹{amount} aaj milega — taiyar raho. ⚡"
]

NIGHT_TEMPLATES = [
    "*Good Night All Members!* Kal ₹{amount} tak milega — taiyar raho. 🌙",
    "*Good Night All Members!* Kal ₹{amount} ka mauka aayega. ⚡",
    "*Good Night All Members!* Kal ₹{amount} ki kamai hogi. 💰",
    "*Good Night All Members!* Kal subah ₹{amount} earn karne ka mauka hai. 🌙",
    "*Good Night All Members!* Kal ₹{amount} tak milega — miss mat karna. 🔥",
    "*Good Night All Members!* Kal ₹{amount} tak kama sakte ho. 💸",
    "*Good Night All Members!* Kal ka din ₹{amount} wala hai. 🌙",
    "*Good Night All Members!* Kal ₹{amount} tak earning possible hai. ⚡",
    "*Good Night All Members!* Kal ₹{amount} milega — channel pe active raho. 💰",
    "*Good Night All Members!* Kal seedha ₹{amount} ka fayda milega. 🌙"
]

# ========== रैंडम कैप्शन ==========
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

# ========== कीवर्ड्स की लिस्ट ==========
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

# ========== हेल्पर फंक्शंस ==========
def get_today_index(length):
    india_tz = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(india_tz).strftime("%j")) % length

def send_channel_auto(templates, images, prefix_emoji):
    try:
        profit = random.randint(100, 1000)
        # Random template + random image (independent — zyada variety)
        template = random.choice(templates)
        image_url = random.choice(images)
        msg = template.format(amount=profit)
        sent = bot.send_photo(PROMO_CHANNEL_ID, image_url, caption=msg, parse_mode='Markdown')
        if sent:
            for emoji in ['👍', '❤️']:
                try:
                    bot.set_message_reaction(PROMO_CHANNEL_ID, sent.message_id, reaction=[{'type': 'emoji', 'emoji': emoji}])
                except:
                    pass
    except Exception as e:
        print(f"Auto-post error: {e}")

def auto_poster():
    india_tz = pytz.timezone('Asia/Kolkata')
    morning_target = random.randint(30, 60)
    night_target = random.randint(29, 59)
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
                night_target = random.randint(29, 59)
                last_day = day

            # Morning post: 4:30 AM to 5:00 AM
            if not posted_morning and hour >= 4:
                mins_from_4 = (hour - 4) * 60 + minute
                if mins_from_4 >= morning_target:
                    send_channel_auto(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                    posted_morning = True

            # Night post: 11:29 PM to 11:59 PM guaranteed
            if not posted_night and hour == 23 and minute >= night_target:
                send_channel_auto(NIGHT_TEMPLATES, NIGHT_IMAGE_URLS, "🌙")
                posted_night = True

            time.sleep(30)
        except Exception as e:
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

# ========== बॉट हैंडलर ==========
@bot.message_handler(commands=['start'])
def start_handler(msg):
    send_promo(msg.chat.id)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(msg):
    if OWNER_ID != 0 and msg.from_user.id == OWNER_ID:
        return

    if OWNER_ID != 0:
        try:
            user = msg.from_user
            name = f"{user.first_name} {user.last_name or ''}".strip()
            if user.username:
                name += f" (@{user.username})"
            text_content = msg.text if msg.text else "[Non-text message]"
            forward_text = f"📩 *नया मैसेज*\n👤 {name}\n🆔 `{user.id}`\n💬 {text_content}"
            bot.send_message(OWNER_ID, forward_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Forwarding failed: {e}")

    if msg.text and keyword_found(msg.text):
        send_promo(msg.chat.id)

# ========== फ्लास्क रनर ==========
def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# ========== मेन रनर ==========
if __name__ == "__main__":
    try:
        bot.delete_webhook()
    except:
        pass

    threading.Thread(target=auto_poster, daemon=True).start()
    threading.Thread(target=run_flask, daemon=True).start()

    print("Bot is running with standard python main.py setup...")
    bot.infinity_polling()
