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
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

PROMO_CHANNEL_ID = "-1002437678122"   # आपकी चैनल ID (जहाँ ऑटो-पोस्ट जाएगा)
if not PROMO_CHANNEL_ID.startswith('-100'):
    raise ValueError("PROMO_CHANNEL_ID must start with '-100'")

# ⭐ यही लिंक खुलेगा जब यूजर "Start Earning" बटन दबाएगा
PROMOTION_CHANNEL_LINK = "https://t.me/Proper_Trending"

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER") == "true"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ========== इमेज URLs (गुड मॉर्निंग/नाइट के लिए) ==========
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

# ========== रैंडम प्रॉफिट टेम्पलेट ==========
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

# ========== बड़ी कीवर्ड लिस्ट ==========
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
    "referred", "referring", "ref", "referal", "refer code", "joining bonus", "joining link", "/join",
    "लाल", "लोग", "भाई", "दोस्त", "कमाई", "लाभ", "मुनाफा", "धन", "पैसा", "इनाम",
    "vip", "premium", "exclusive", "limited", "today only", "urgent", "flash sale",
    "सुनो", "देखो", "करो", "अभी", "जल्दी", "मौका", "तुरंत", "फायदा", "प्रॉफिट", "गिफ्ट",
    "कोड", "गुप्त", "सीक्रेट", "बंपर", "ऑफर", "डील", "लकी", "विनर", "कांटेस्ट",
    "free money", "cash", "withdraw", "payment", "upi", "bank", "account", "wallet"
]

# ========== बटन हेल्पर ==========
def get_start_earning_button():
    """सीधे चैनल खोलने वाला इनलाइन बटन"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💰 Start Earning 💰", url=PROMOTION_CHANNEL_LINK))
    return markup

def get_persistent_keyboard():
    """नीचे दिखने वाला मेनू कीबोर्ड"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    btn1 = KeyboardButton("🚀 Start Earning")
    btn2 = KeyboardButton("💰 आज का प्रॉफिट")
    btn3 = KeyboardButton("📢 चैनल लिंक")
    btn4 = KeyboardButton("❓ Help")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# ========== फंक्शन्स ==========
def get_today_index(list_length):
    india_tz = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(india_tz).strftime("%j")) % list_length

def send_auto_message(templates, images, prefix_emoji):
    try:
        profit = random.randint(100, 1000)
        idx = get_today_index(len(templates))
        msg = templates[idx].format(amount=profit)
        img_idx = idx % len(images)
        caption = f"{prefix_emoji} {msg}"
        bot.send_photo(PROMO_CHANNEL_ID, images[img_idx], caption=caption,
                       parse_mode='Markdown', reply_markup=get_start_earning_button())
        print(f"Auto-posted with ₹{profit}")
    except Exception as e:
        print(f"Auto-post error: {e}")

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
                send_auto_message(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                posted_morning = True
            if hour == 22 and not posted_night and minute >= night_min:
                send_auto_message(NIGHT_TEMPLATES, NIGHT_IMAGE_URLS, "🌙")
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
        if kw_low in ["चैनल", "ज्वाइन", "कमई", "पैसे", "फ़ॉलो", "join", "chat", "/join", "लाल", "लोग", "भाई", "दोस्त"]:
            if kw_low in text:
                return True
        if re.search(r'\b' + re.escape(kw_low) + r'\b', text):
            return True
    return False

# ========== हैंडलर ==========
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.send_message(message.chat.id,
                         "*🎉 चैनल से जुड़ें और कमाई शुरू करें!*\n\n👇 नीचे बटन दबाएँ:",
                         parse_mode='Markdown', reply_markup=get_start_earning_button())
        # पर्सिस्टेंट कीबोर्ड दिखाएँ
        bot.send_message(message.chat.id, "यह रहा आपका मेनू (हमेशा नीचे):",
                         reply_markup=get_persistent_keyboard())
    except Exception as e:
        print(f"/start error: {e}")

@bot.message_handler(func=lambda msg: msg.text == "🚀 Start Earning")
def handle_start_earning_text(message):
    bot.send_message(message.chat.id, "✅ नीचे दिए बटन पर क्लिक करके चैनल जॉइन करें:",
                     reply_markup=get_start_earning_button())

@bot.message_handler(func=lambda msg: msg.text == "💰 आज का प्रॉफिट")
def handle_profit(message):
    profit = random.randint(100, 1000)
    bot.send_message(message.chat.id, f"🔥 आज का अनुमानित प्रॉफिट: *₹{profit} तक*\n\nचैनल जॉइन करें:",
                     parse_mode='Markdown', reply_markup=get_start_earning_button())

@bot.message_handler(func=lambda msg: msg.text == "📢 चैनल लिंक")
def handle_channel_link(message):
    bot.send_message(message.chat.id, f"📢 हमारा Telegram चैनल:\n{PROMOTION_CHANNEL_LINK}",
                     reply_markup=get_start_earning_button())

@bot.message_handler(func=lambda msg: msg.text == "❓ Help")
def handle_help(message):
    bot.send_message(message.chat.id, "किसी भी सहायता के लिए /start दबाएं और 'Start Earning' बटन पर क्लिक करें।",
                     reply_markup=get_start_earning_button())

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    if message.text and keyword_found(message.text):
        bot.send_message(message.chat.id,
                         "*🔑 आपने कीवर्ड टाइप किया! नीचे दिए बटन से चैनल जॉइन करें और कमाई शुरू करें:*",
                         parse_mode='Markdown', reply_markup=get_start_earning_button())

# ========== फ्लास्क वेबहुक ==========
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 403

@app.route('/')
def home():
    return "Bot is running with 'Start Earning' button that opens channel directly!"

@app.route('/health')
def health():
    return "OK", 200

# ========== मेन ==========
if __name__ == "__main__":
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster started.")

    if IS_RENDER and BOT_TOKEN and WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/")
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        bot.infinity_polling()
