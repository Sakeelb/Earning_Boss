import os
import telebot
import threading
import time
from flask import Flask, request
import pytz
from datetime import datetime
import re
import random

# पर्यावरण वैरिएबल्स से BOT_TOKEN और WEBHOOK_URL प्राप्त करें
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = "@All_Gift_Code_Earning"
# FORWARD_MESSAGE_ID = 398 # यह ID अब /start कमांड के लिए उपयोग नहीं की जाती है
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER") # यह दर्शाता है कि क्या बॉट Render पर डिप्लॉय किया गया है

# TeleBot और Flask ऐप को इनिशियलाइज़ करें
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 10 Good Morning इमेज URLs (सुनिश्चित करें कि सभी URL अद्वितीय और वैध हों)
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

# 10 Good Night इमेज URLs (सुनिश्चित करें कि सभी URL अद्वितीय और वैध हों)
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

# 10 Good Morning मैसेज
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

# 10 Good Night मैसेज
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
    "subscribe", "chat", "chat hindi", "reply", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
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
    """आज की तारीख के आधार पर सूची का इंडेक्स प्राप्त करता है।"""
    today = int(datetime.now().strftime("%j")) # वर्ष का दिन (1-366)
    return today % list_length

def send_message_auto(messages, images, prefix_emoji):
    """ऑटोमैटिक मैसेज और इमेज को प्रोमो चैनल पर भेजता है और रिएक्शन जोड़ता है।"""
    try:
        idx = get_today_index(len(messages))
        msg = messages[idx]
        image_url = images[idx % len(images)] # इमेज सूची की लंबाई के भीतर इंडेक्स सुनिश्चित करें
        caption = f"{prefix_emoji} {msg}"

        # मैसेज भेजें और भेजे गए मैसेज का ऑब्जेक्ट प्राप्त करें
        sent_message = bot.send_photo(PROMO_CHANNEL, image_url, caption=caption, parse_mode='Markdown')

        # यदि मैसेज सफलतापूर्वक भेजा गया है, तो रिएक्शन जोड़ें
        if sent_message:
            reactions_to_add = ['👍', '❤️'] # अपनी पसंद के अनुसार रिएक्शन बदलें

            for reaction_emoji in reactions_to_add:
                try:
                    bot.set_message_reaction(
                        chat_id=PROMO_CHANNEL,
                        message_id=sent_message.message_id,
                        reaction=[{'type': 'emoji', 'emoji': reaction_emoji}] # टेलीबॉट के लिए सही फॉर्मेट
                    )
                    print(f"Reaction '{reaction_emoji}' added to message ID {sent_message.message_id}")
                except Exception as reaction_e:
                    print(f"Error adding reaction '{reaction_emoji}': {reaction_e}")

    except Exception as e:
        print(f"Error sending auto message or adding reaction: {e}")

def auto_poster():
    """स्वचालित रूप से सुबह और रात के संदेशों को पोस्ट करता है।"""
    posted_morning = False
    posted_night = False
    # सुबह और रात के मैसेज भेजने के लिए रैंडम मिनट सेट करें (हर दिन अलग)
    morning_minute = random.randint(0, 10)  # 5:00-5:10 AM
    night_minute = random.randint(0, 10)    # 10:00-10:10 PM
    india_timezone = pytz.timezone('Asia/Kolkata')
    
    while True:
        now = datetime.now(india_timezone)
        current_hour = now.strftime("%H")
        current_minute = int(now.strftime("%M"))
        
        # आधी रात को रीसेट करें ताकि अगले दिन फिर से मैसेज भेजे जा सकें
        if current_hour == "00" and current_minute == 0:
            posted_morning = False
            posted_night = False
            morning_minute = random.randint(0, 10)
            night_minute = random.randint(0, 10)
            print("Midnight reset completed. Ready for new day's posts.")
        
        # सुबह के मैसेज के लिए रैंडम टाइम (5:00-5:10 AM)
        if current_hour == "05" and not posted_morning:
            if current_minute >= morning_minute:
                print(f"Attempting to send morning message at {now.strftime('%H:%M')}")
                send_message_auto(UNIQUE_MORNING_MESSAGES, MORNING_IMAGE_URLS, "☀️")
                posted_morning = True
                print("Morning message sent.")
        
        # रात के मैसेज के लिए रैंडम टाइम (10:00-10:10 PM)
        if current_hour == "22" and not posted_night:
            if current_minute >= night_minute:
                print(f"Attempting to send night message at {now.strftime('%H:%M')}")
                send_message_auto(UNIQUE_NIGHT_MESSAGES, NIGHT_IMAGE_URLS, "🌙")
                posted_night = True
                print("Night message sent.")
        
        # हर 20 सेकंड में चेक करें (आप चाहें तो इस अंतराल को बढ़ा या घटा सकते हैं)
        time.sleep(20)

# /start कमांड के लिए नया, बोल्ड हिंग्लिश मैसेज
START_MESSAGE_TEXT = """
*Urgent Update:*
*Naya Gift Code / Offer Live ho chuka hai.*
*Isko paane ke liye hamare channel se juden:*
*[[ @All_Gift_Code_Earning ]]*
"""

# /start कमांड के लिए इमेज URL
START_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png"

@bot.message_handler(commands=['start'])
def start_handler(message):
    """/start कमांड को हैंडल करता है और एक इमेज के साथ मैसेज भेजता है।"""
    try:
        # इमेज को कस्टम, बोल्ड मैसेज को कैप्शन के रूप में भेजें
        bot.send_photo(message.chat.id, START_IMAGE_URL, caption=START_MESSAGE_TEXT, parse_mode='Markdown')
        print(f"Start command received from {message.chat.id}. Sent welcome message.")
    except Exception as e:
        print(f"Error in /start handler for chat ID {message.chat.id}: {e}")
        bot.send_message(message.chat.id, f"Error in /start: {e}")

def keyword_found(text):
    """टेक्स्ट में प्रमोशनल कीवर्ड्स को चेक करता है।"""
    text = text.lower()
    # गैर-अल्फ़ान्यूमेरिक वर्णों और कुछ विशेष वर्णों को हटा दें
    text = re.sub(r'[^\w\s@/]', '', text) 
    for kw in KEYWORDS:
        # पूरे शब्द के मिलान के लिए regex का उपयोग करें
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
        # कुछ विशेष कीवर्ड के लिए आंशिक मिलान की भी जाँच करें
        if kw in ["refer", "join", "earn", "चैनल", "ज्वाइन"]:
            if kw in text:
                return True
    # लिंक्स के लिए भी जाँच करें
    if re.search(r'(https?://\S+|t\.me/\S+|bit\.ly/\S+)', text):
        return True
    return False

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    """किसी भी मैसेज को हैंडल करता है और यदि कीवर्ड पाए जाते हैं तो प्रमोशन मैसेज भेजता है।"""
    try:
        if not message.text: # यदि मैसेज में टेक्स्ट नहीं है तो बाहर निकलें
            return
        
        if keyword_found(message.text):
            # प्रमोशन मैसेज अब बोल्ड किया गया है
            promo_caption = "*[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]]*\n*[[ https://t.me/All_Gift_Code_Earning ]]*"
            
            # बोल्ड प्रमोशन मैसेज को कैप्शन के रूप में इमेज के साथ भेजें
            bot.send_photo(
                chat_id=message.chat.id,
                photo="https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png",
                caption=promo_caption,
                parse_mode='Markdown',
                reply_to_message_id=message.message_id # उपयोगकर्ता के मैसेज का जवाब दें
            )
            print(f"Promotional reply sent to chat ID {message.chat.id} for message: {message.text[:50]}...")
    except Exception as e:
        print(f"Error in promo_reply for chat ID {message.chat.id}: {e}")

@app.route('/', methods=['POST'])
def webhook():
    """टेलीग्राम वेबहुक अपडेट को हैंडल करता है।"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        # गलत content-type के लिए HTTP 403 भेजें
        print(f"Webhook received non-JSON request: {request.headers.get('content-type')}")
        return 'Forbidden', 403


@app.route('/')
def home():
    """मुख्य URL के लिए एक साधारण होम पेज प्रदान करता है।"""
    return "Bot is running."

if __name__ == "__main__":
    # ऑटो-पोस्टर को एक अलग थ्रेड में शुरू करें ताकि बॉट का मुख्य लूप बाधित न हो
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster thread started.")

    # Render पर डिप्लॉयमेंट के लिए वेबहुक सेट करें, अन्यथा लोकल पोलिंग का उपयोग करें
    if IS_RENDER:
        if WEBHOOK_URL:
            try:
                bot.set_webhook(url=f"{WEBHOOK_URL}/")
                print(f"Webhook set to: {WEBHOOK_URL}/")
                app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
            except Exception as e:
                print(f"Failed to set webhook: {e}")
                print("Falling back to long polling.")
                bot.infinity_polling() # वेबहुक सेट न हो पाए तो लॉन्ग पोलिंग पर वापस आएं
        else:
            print("WEBHOOK_URL environment variable not set on Render. Webhook will not be set.")
            print("Running with long polling (for Render deployment without webhook URL).")
            bot.infinity_polling()
    else:
        print("Running with long polling (for local development).")
        bot.infinity_polling()
