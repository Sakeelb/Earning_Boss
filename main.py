import os
import telebot
import threading
import time
from flask import Flask, request
import pytz
from datetime import datetime, timedelta
import re
import random
import traceback # traceback मॉड्यूल इंपोर्ट करें

# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ====================================================================================================
# बॉस, यह सबसे महत्वपूर्ण लाइन है!
# आपको अपने नए Telegram चैनल (https://t.me/+5bYqRYoNoPQyMDU1) की संख्यात्मक ID यहां डालनी होगी।
# यह ID '-100' से शुरू होती है (उदाहरण: "-1001234567890")।
# इसे प्राप्त करने के लिए, अपने चैनल में @getidsbot या @userinfobot को एडमिन के रूप में जोड़ें
# और फिर चैनल में /get_chat_id या /info कमांड भेजें।
PROMO_CHANNEL_ID = "-1002437678122"
# ====================================================================================================

# प्रमोशन मैसेज में उल्लेखित चैनल का यूजरनेम/लिंक (जैसा आप चाहते हैं)
PROMOTION_CHANNEL_USERNAME = "@Proper_Trending"
PROMOTION_CHANNEL_LINK = "https://t.me/Proper_Trending"

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER")

# Initialize bot and Flask app
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Image and Message Data ---

# Good Morning इमेज URLs
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

# Good Night इमेज URLs
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

# Good Morning मैसेज
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

# Good Night मैसेज
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
    "*Good Night All Members!* कल सीधा ₹400 का फायदा मिलेगा。"
]

# प्रमोशनल रिप्लाई के लिए कीवर्ड्स
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

# /start कमांड का मैसेज और इमेज
START_MESSAGE_TEXT = f"""
*Urgent Update:*
*Naya Gift Code / Offer Live ho chuka hai.*
*Isko paane ke liye hamare channel se juden:*
*[[ {PROMOTION_CHANNEL_USERNAME} ]]*
"""
START_IMAGE_URL = "https://github.com/Sakeelb/Earning_Boss/blob/fd7a30f7826fe65abb99a0baeff70878fbc04815/New/1781241774791.png"
# --- सहायक फंक्शन्स (Helper Functions) ---

def get_today_index(list_length):
    """
    वर्तमान वर्ष के दिन के आधार पर एक इंडेक्स की गणना करता है।
    यह सुनिश्चित करता है कि प्रत्येक दिन एक अलग मैसेज/इमेज का उपयोग किया जाए।
    """
    # मैसेज चक्र के साथ संरेखित करने के लिए इंडेक्स गणना के लिए IST का उपयोग करें
    india_timezone = pytz.timezone('Asia/Kolkata')
    today = int(datetime.now(india_timezone).strftime("%j")) # वर्ष का दिन (1-366)
    return today % list_length

def send_message_auto(messages, images, prefix_emoji):
    """
    प्रमोशन चैनल पर एक इमेज और रिएक्शन के साथ स्वचालित मैसेज भेजता है।
    """
    try:
        # Get message and image based on today's index
        idx = get_today_index(len(messages))
        msg = messages[idx]
        image_url = images[idx % len(images)] # सुनिश्चित करें कि इमेज इंडेक्स सही ढंग से लूप करे
        caption = f"{prefix_emoji} {msg}"

        # --- यहां PROMO_CHANNEL_ID का उपयोग करें ---
        print(f"Attempting to send message to {PROMO_CHANNEL_ID} with caption: {caption}")
        sent_message = bot.send_photo(PROMO_CHANNEL_ID, image_url, caption=caption, parse_mode='Markdown')
        print(f"Message sent! Message ID: {sent_message.message_id}")

        # भेजे गए मैसेज में रिएक्शन जोड़ें
        if sent_message:
            reactions_to_add = ['👍', '❤️'] # अपने रिएक्शन यहां कस्टमाइज़ करें
            for reaction_emoji in reactions_to_add:
                try:
                    bot.set_message_reaction(
                        chat_id=PROMO_CHANNEL_ID, # --- यहां PROMO_CHANNEL_ID का उपयोग करें ---
                        message_id=sent_message.message_id,
                        reaction=[{'type': 'emoji', 'emoji': reaction_emoji}]
                    )
                    print(f"Reaction '{reaction_emoji}' added to message ID {sent_message.message_id}")
                except Exception as reaction_e:
                    print(f"Error adding reaction '{reaction_emoji}' to message ID {sent_message.message_id}: {reaction_e}")

    except Exception as e:
        print(f"Error sending auto message or adding reaction: {e}")

def auto_poster():
    """
    थ्रेड फ़ंक्शन जो समय-समय पर गुड मॉर्निंग/नाइट मैसेज भेजता है।
    """
    posted_morning_today = False
    posted_night_today = False
    india_timezone = pytz.timezone('Asia/Kolkata')
    
    # आज के लिए रैंडम मिनट इनिशियलाइज़ करें
    morning_minute = random.randint(0, 10)  # X:00 और X:10 AM के बीच
    night_minute = random.randint(0, 10)    # Y:00 और Y:10 PM के बीच
    
    # फ्लैग्स को विश्वसनीय रूप से रीसेट करने के लिए पोस्टर के अंतिम दिन को ट्रैक करें
    last_run_day = datetime.now(india_timezone).day
    
    print(f"Auto-poster started. Morning target minute: {morning_minute}, Night target minute: {night_minute}")
    print(f"Initial last run day: {last_run_day}")

    while True:
        try: # लूप में एरर पकड़ने के लिए try-except जोड़ा गया है
            # पहले UTC में वर्तमान समय प्राप्त करें (सर्वर का संभावित डिफ़ॉल्ट)
            utc_now = datetime.utcnow()
            # UTC समय को IST में बदलें
            now = utc_now.replace(tzinfo=pytz.utc).astimezone(india_timezone)
            
            current_hour = now.hour
            current_minute = now.minute
            current_day = now.day # महीने का वर्तमान दिन प्राप्त करें

            # --- डिबगिंग लॉग्स यहां जोड़े गए हैं ---
            print(f"DEBUG: Auto-poster loop running. Current IST Time: {now.strftime('%Y-%m-%d %H:%M:%S')}, Hour: {current_hour}, Minute: {current_minute}, Day: {current_day}")
            print(f"DEBUG: Flags: Morning={posted_morning_today}, Night={posted_night_today}, Last Run Day={last_run_day}")
            # --- डिबगिंग लॉग्स का अंत ---

            # दैनिक रीसेट: जांचें कि क्या दिन बदल गया है
            if current_day != last_run_day:
                print(f"Day changed from {last_run_day} to {current_day}. Resetting flags and generating new random minutes.")
                posted_morning_today = False
                posted_night_today = False
                morning_minute = random.randint(0, 10)
                night_minute = random.randint(0, 10)
                last_run_day = current_day # अंतिम रन दिन अपडेट करें
                print(f"New morning target minute: {morning_minute}, New night target minute: {night_minute}")
            
            # गुड मॉर्निंग टाइम (5:00-5:10 AM IST)
            if current_hour == 5 and not posted_morning_today:
                if current_minute >= morning_minute:
                    print(f"Time to send Good Morning! Current: {current_hour}:{current_minute}, Target: 5:{morning_minute}")
                    send_message_auto(UNIQUE_MORNING_MESSAGES, MORNING_IMAGE_URLS, "☀️")
                    posted_morning_today = True
                    print("Good Morning message sent and flag set.")
                else: # जब 5 AM हो लेकिन मिनट पूरा न हुआ हो उसके लिए डिबगिंग लाइन
                    print(f"DEBUG: It's 5 AM but minute {current_minute} < target minute {morning_minute}. Waiting.")
            
            # गुड नाइट टाइम (10:00-10:10 PM IST)
            if current_hour == 22 and not posted_night_today:
                if current_minute >= night_minute:
                    print(f"Time to send Good Night! Current: {current_hour}:{current_minute}, Target: 22:{night_minute}")
                    send_message_auto(UNIQUE_NIGHT_MESSAGES, NIGHT_IMAGE_URLS, "🌙")
                    posted_night_today = True
                    print("Good Night message sent and flag set.")
                else: # जब 10 PM हो लेकिन मिनट पूरा न हुआ हो उसके लिए डिबगिंग लाइन
                    print(f"DEBUG: It's 10 PM but minute {current_minute} < target minute {night_minute}. Waiting.")
            
            # दोबारा जांचने से पहले कुछ देर रुकें
            time.sleep(60) # हर 60 सेकंड (1 मिनट) में जांचें
        except Exception as e:
            # अनहैंडल्ड अपवादों के लिए पूरा ट्रेसेबैक लॉग करें
            print(f"ERROR: An unhandled exception occurred in auto_poster thread: {e}")
            print(traceback.format_exc()) # पूरा ट्रेसेबैक प्रिंट करें
            time.sleep(300) # तेजी से क्रैश होने से रोकने के लिए फिर से कोशिश करने से पहले लंबी अवधि (5 मिनट) के लिए रुकें

def keyword_found(text):
    """
    जांचता है कि टेक्स्ट में कोई परिभाषित कीवर्ड या URL पैटर्न मौजूद है या नहीं।
    """
    text = text.lower()
    # चैनल नामों और कमांड के लिए @ और / को छोड़कर विराम चिह्न हटा दें
    text = re.sub(r'[^\w\s@/]', '', text) 
    
    for kw in KEYWORDS:
        # अधिकांश कीवर्ड के लिए शब्द सीमाओं का उपयोग करें ताकि आंशिक मिलान से बचा जा सके (उदाहरण के लिए, "join" "joining" से मेल नहीं खाना चाहिए)
        # हालांकि, "https" या "@" जैसे कुछ के लिए, सीधा सबस्ट्रिंग मिलान अपेक्षित हो सकता है।
        # विशिष्ट कीवर्ड को संभालने के लिए संशोधित किया गया जहां आंशिक मिलान ठीक है (जैसे 'joining' के भीतर 'join')
        if kw in ["https", "@", "t.me", "bit.ly"]: # ये अक्सर URL का हिस्सा होते हैं
             if kw in text:
                 return True
        elif re.search(r'\b' + re.escape(kw) + r'\b', text): # पूरे शब्दों के लिए
            return True
        # हिंदी शब्दों के लिए विशिष्ट जांच जो हमेशा स्पष्ट शब्द सीमाओं के साथ नहीं हो सकती हैं
        if kw in ["चैनल", "ज्वाइन", "कमई", "पैसे", "फ़ॉलो"]:
            if kw in text:
                return True

    # सामान्य URL पैटर्न के लिए स्पष्ट रूप से जांच करें
    if re.search(r'(https?://\S+|t\.me/\S+|bit\.ly/\S+)', text):
        return True
    return False

# --- टेलीग्राम बॉट मैसेज हैंडलर ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    """
    /start कमांड को हैंडल करता है, एक प्रमोशनल मैसेज और इमेज भेजता है।
    """
    print(f"Received /start command from {message.chat.id}")
    try:
        # --- यहां PROMOTION_CHANNEL_USERNAME का उपयोग करें ---
        bot.send_photo(message.chat.id, START_IMAGE_URL, caption=START_MESSAGE_TEXT, parse_mode='Markdown')
        print(f"Sent /start message to {message.chat.id}")
    except Exception as e:
        print(f"Error in /start handler for chat ID {message.chat.id}: {e}")
        bot.send_message(message.chat.id, f"Error receiving /start: {e}")

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    """
    सभी इनकमिंग मैसेज को हैंडल करता है और यदि कीवर्ड पाए जाते हैं तो प्रमोशन के साथ रिप्लाई करता है।
    """
    if not message.text:
        return # कैप्शन के बिना फोटो जैसे टेक्स्ट के बिना मैसेज को अनदेखा करें

    print(f"Received message from {message.chat.id}: {message.text}")
    try:
        if keyword_found(message.text):
            print(f"Keyword found in message from {message.chat.id}. Sending promo reply.")
            # --- यहां PROMOTION_CHANNEL_LINK का उपयोग करें ---
            promo_caption = f"*[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]]*\n*[[ {PROMOTION_CHANNEL_LINK} ]]*"
            
            bot.send_photo(
                chat_id=message.chat.id,
                photo="https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png",
                caption=promo_caption,
                parse_mode='Markdown',
                reply_to_message_id=message.message_id # यूज़र के मैसेज का रिप्लाई करें
            )
            print(f"Promo reply sent to {message.chat.id}.")
    except Exception as e:
        print(f"Error in promo_reply for message ID {message.message_id}: {e}")

# --- फ्लास्क ऐप रूट्स वेबहुक के लिए ---

@app.route('/', methods=['POST'])
def webhook():
    """
    टेलीग्राम से अपडेट प्राप्त करने के लिए वेबहुक एंडपॉइंट।
    """
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return '<h1>Bad Request!</h1>', 403

@app.route('/')
def home():
    """
    यह पुष्टि करने के लिए सरल होम पेज कि फ्लास्क ऐप चल रहा है।
    """
    return "Bot is running and listening for updates!"

# --- मुख्य निष्पादन ब्लॉक ---

if __name__ == "__main__":
    # ऑटो-पोस्टर को एक अलग थ्रेड में शुरू करें
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster thread started.")

    # Render डिप्लॉयमेंट के लिए वेबहुक कॉन्फ़िगर करें या लोकल के लिए लॉन्ग पोलिंग का उपयोग करें
    if IS_RENDER == "true": # Render पर्यावरण चर को स्ट्रिंग के रूप में सेट करता है
        if BOT_TOKEN and WEBHOOK_URL:
            try:
                bot.set_webhook(url=f"{WEBHOOK_URL}/")
                print(f"Webhook set to: {WEBHOOK_URL}/")
                # वेबहुक के लिए फ्लास्क ऐप चलाएं
                app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
            except Exception as e:
                print(f"Error setting webhook or starting Flask app: {e}")
                print("Falling back to long polling.")
                bot.infinity_polling() # फॉलबैक
        else:
            print("Environment variables BOT_TOKEN or WEBHOOK_URL not set for Render. Using long polling.")
            bot.infinity_polling()
    else:
        print("Not running on Render (IS_RENDER not 'true'). Running with long polling (for local development).")
        bot.infinity_polling()

