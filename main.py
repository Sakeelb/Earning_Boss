import os
import telebot
import threading
import time
from flask import Flask, request
import pytz
from datetime import datetime
import re
import random # यह सुनिश्चित कर लें कि यह इम्पोर्टेड है

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

# 10 Good Morning मैसेज (Original Count)
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

# 10 Good Night मैसेज (Original Count)
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
    today = int(datetime.now().strftime("%j")) # साल का दिन (1-366)
    return today % list_length # लिस्ट की लंबाई के हिसाब से इंडेक्स

def send_message_auto(messages, images, prefix_emoji):
    try:
        idx = get_today_index(len(messages)) # मैसेज के लिए आज का इंडेक्स
        msg = messages[idx]
        
        # *** यहाँ बदलाव है: इमेज लिस्ट से एक रैंडम इमेज चुनें ***
        image_url = random.choice(images) # अब यह पूरी तरह से रैंडम इमेज चुनेगा
        
        caption = f"{prefix_emoji} {msg}"
        bot.send_photo(PROMO_CHANNEL, image_url, caption=caption)
    except Exception as e:
        print(f"Error sending auto message: {e}")

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
    text = re.sub(r'[^\w\s@/]', '', text) # केवल अक्षर, अंक, whitespace, @ और / रहने दें
    for kw in KEYWORDS:
        # पूरे शब्द का मिलान करें (जैसे 'join' 'joining' में नहीं)
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return True
        # कुछ खास कीवर्ड के लिए आंशिक मिलान भी देखें (जैसे 'चैनल' 'मेरे चैनल' में)
        if kw in ["refer", "join", "earn", "चैनल", "ज्वाइन"]: # इन कीवर्ड के लिए आंशिक मिलान भी चेक करें
            if kw in text:
                return True
    # किसी भी URL या t.me लिंक का पता लगाएं
    if re.search(r'(https?://\S+|t\.me/\S+|bit\.ly/\S+)', text):
        return True
    return False

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    try:
        # सुनिश्चित करें कि मैसेज में टेक्स्ट हो
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
    # ऑटो-पोस्टर को एक अलग थ्रेड में शुरू करें
    threading.Thread(target=auto_poster, daemon=True).start()
    
    # वेबहुक या लॉन्ग पोलिंग के माध्यम से बॉट चलाएं
    if IS_RENDER: # अगर Render पर डिप्लॉय किया गया है
        if WEBHOOK_URL:
            bot.set_webhook(url=f"{WEBHOOK_URL}/")
            app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        else:
            print("WEBHOOK_URL environment variable not set on Render. Webhook will not be set.")
            # Render पर वेबहुक URL के बिना लॉन्ग पोलिंग काम नहीं करेगी, इसलिए बॉट शुरू नहीं होगा।
            # अगर आप इसे फिर भी चलाना चाहते हैं तो यहां bot.infinity_polling() जोड़ सकते हैं,
            # लेकिन यह Render के लिए सुझाया नहीं गया है।
    else: # लोकल डेवलपमेंट या अन्य वातावरण के लिए
        print("Running with long polling (for local development).")
        bot.infinity_polling()

