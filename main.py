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
FORWARD_MESSAGE_ID = 398 # This ID is no longer used for the /start command
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 4 Good Morning इमेज URLs
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

# 4 Good Night इमेज URLs
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

# 10 Good Morning मैसेज (Original Count)
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

# 10 Good Night मैसेज (Original Count)
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

# सारे Original Keywords (जैसे पहले थे)
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

        # मैसेज भेजें और भेजे गए मैसेज का ऑब्जेक्ट प्राप्त करें
        sent_message = bot.send_photo(PROMO_CHANNEL, image_url, caption=caption, parse_mode='Markdown')

        # मैसेज भेजने के तुरंत बाद उस पर रिएक्शन डालें
        if sent_message:
            # यहाँ आप अपने पसंदीदा रिएक्शन इमोजी डाल सकते हैं
            # मैंने यहाँ '👍' और '❤️' डिफ़ॉल्ट रूप से डाले हैं.
            # आप इन्हें अपनी पसंद के अनुसार बदल सकते हैं.
            reactions_to_add = ['👍', '❤️']

            for reaction_emoji in reactions_to_add:
                try:
                    bot.set_message_reaction(
                        chat_id=PROMO_CHANNEL,
                        message_id=sent_message.message_id,
                        reaction=[{'type': 'emoji', 'emoji': reaction_emoji}]
                    )
                    print(f"Reaction '{reaction_emoji}' added to message ID {sent_message.message_id}")
                except Exception as reaction_e:
                    print(f"Error adding reaction '{reaction_emoji}': {reaction_e}")

    except Exception as e:
        print(f"Error sending auto message or adding reaction: {e}")


def auto_poster():
    posted_morning = False
    posted_night = False
    morning_minute = random.randint(0, 10)  # 5:00-5:10 AM
    night_minute = random.randint(0, 10)    # 10:00-10:10 PM
    india_timezone = pytz.timezone('Asia/Kolkata')
    
    while True:
        now = datetime.now(india_timezone)
        current_hour = now.strftime("%H")
        current_minute = int(now.strftime("%M"))
        
        # Midnight Reset
        if current_hour == "00" and current_minute == 0:
            posted_morning = False
            posted_night = False
            morning_minute = random.randint(0, 10)
            night_minute = random.randint(0, 10)
        
        # Random Morning Time (5:00-5:10 AM)
        if current_hour == "05" and not posted_morning:
            if current_minute >= morning_minute:
                send_message_auto(UNIQUE_MORNING_MESSAGES, MORNING_IMAGE_URLS, "☀️")
                posted_morning = True
        
        # Random Night Time (10:00-10:10 PM)
        if current_hour == "22" and not posted_night:
            if current_minute >= night_minute:
                send_message_auto(UNIQUE_NIGHT_MESSAGES, NIGHT_IMAGE_URLS, "🌙")
                posted_night = True
        
        time.sleep(20)

# The new, bolded Hinglish message for /start
START_MESSAGE_TEXT = """
*Urgent Update:*
*Naya Gift Code / Offer Live ho chuka hai.*
*Isko paane ke liye hamare channel se juden:*
*[[ @All_Gift_Code_Earning ]]*
"""

@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        # Send the custom, bolded message directly
        bot.send_message(message.chat.id, START_MESSAGE_TEXT, parse_mode='Markdown')
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
            promo_caption = "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]]\n *[[ https://t.me/All_Gift_Code_Earning ]]*"
            # Send the image with the promotional message as its caption
            bot.send_photo(
                chat_id=message.chat.id,
                photo="https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png",
                caption=promo_caption,
                parse_mode='Markdown',
                reply_to_message_id=message.message_id # Reply to the user's message
            )
            # The previous separate text reply and forward message are no longer needed here.
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

