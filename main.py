import os
import telebot
import threading
import time
import requests
from flask import Flask
import pytz
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = "@All_Gift_Code_Earning"
FORWARD_MESSAGE_ID = 398

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

KEYWORDS = [
    "subscribe", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
    "mere channel", "mera channel", "channel ko", "follow", "follow", "join", "channel", "join", "link", "promo", "reward",
    "bonus", "gift", "win", "offer", "loot", "free", "telegram", "paise kaise kamaye", "online kamai",
    "earning app", "referral", "invite", "kamai ka tarika", "free mein kamai", "kya haal hai", "kaise ho", "kitne paise", "free offer kya hai"
]

EARNING_RELATED_RESPONSES = {
    "paise kaise kamaye": "आप हमारे चैनल को ज्वाइन करके विभिन्न कमाई के अवसरों के बारे में जान सकते हैं!",
    "online kamai": "ऑनलाइन कमाई के कई तरीके हैं, जैसे रेफरल प्रोग्राम, टास्क पूरे करना आदि। हमारे चैनल पर अपडेट रहें!",
    "earning app": "हमारे चैनल पर आपको कुछ बेहतरीन अर्निंग ऐप्स के बारे में जानकारी मिलेगी।",
    "referral": "रेफरल प्रोग्राम एक अच्छा तरीका है अतिरिक्त कमाई करने का। हमारे पोस्ट ध्यान से देखें।",
    "invite": "इनवाइट करके आप बोनस और रिवॉर्ड जीत सकते हैं!",
    "kamai ka tarika": "हमारे चैनल पर हम लगातार नए कमाई के तरीके शेयर करते रहते हैं।",
    "free mein kamai": "फ्री में कमाई के कई ऑफर्स और लूट हमारे चैनल पर उपलब्ध हैं!",
    "aur jankari": "अधिक जानकारी के लिए आप हमारे चैनल के पोस्ट पढ़ सकते हैं या एडमिन से संपर्क कर सकते हैं।\n\n@All_Gift_Code_Earning जॉइन करें।",
    "kya haal hai": "मैं ठीक हूँ! आप हमारे चैनल पर नए कमाई के अवसर देखें!",
    "kaise ho": "मैं ठीक हूँ! उम्मीद है आप भी बढ़िया होंगे। चैनल को ज्वाइन करना न भूलें!\n\n@All_Gift_Code_Earning जॉइन करें।",
    "kitne paise": "कमाई की क्षमता ऑफर पर निर्भर करती है! चैनल पर डिटेल्स चेक करें।\n\n@All_Gift_Code_Earning जॉइन करें।",
    "free offer kya hai": "लेटेस्ट फ्री ऑफर्स के लिए चैनल को देखते रहें!\n\n@All_Gift_Code_Earning जॉइन करें।"
}

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

def get_today_message(messages):
    today = int(datetime.now().strftime("%j"))
    return messages[today % len(messages)]

def send_message_auto(fallback_messages, prefix_emoji):
    msg = get_today_message(fallback_messages)
    bot.send_message(PROMO_CHANNEL, f"{prefix_emoji} {msg}\n\n@All_Gift_Code_Earning जॉइन करें।")

def auto_poster():
    posted_morning = False
    posted_night = False
    india_timezone = pytz.timezone('Asia/Kolkata')
    while True:
        now = datetime.now(india_timezone).strftime("%H:%M")
        if now == "05:00" and not posted_morning:
            send_message_auto(UNIQUE_MORNING_MESSAGES, "☀️")
            posted_morning = True
        elif now != "05:00":
            posted_morning = False

        if now == "22:00" and not posted_night:
            send_message_auto(UNIQUE_NIGHT_MESSAGES, "🌙")
            posted_night = True
        elif now != "22:00":
            posted_night = False

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
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    text = message.text.lower()
    for keyword in KEYWORDS:
        if keyword in text:
            if keyword in EARNING_RELATED_RESPONSES:
                try:
                    bot.reply_to(message, EARNING_RELATED_RESPONSES[keyword])
                    bot.forward_message(
                        chat_id=message.chat.id,
                        from_chat_id=PROMO_CHANNEL,
                        message_id=FORWARD_MESSAGE_ID
                    )
                    return
                except Exception as e:
                    bot.send_message(message.chat.id, f"Error: {e}")
                    return
            else:
                try:
                    promo_text = "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]] [[ https://t.me/All_Gift_Code_Earning ]]"
                    bot.reply_to(message, promo_text)
                    bot.forward_message(
                        chat_id=message.chat.id,
                        from_chat_id=PROMO_CHANNEL,
                        message_id=FORWARD_MESSAGE_ID
                    )
                    return
                except Exception as e:
                    bot.send_message(message.chat.id, f"Error: {e}")
                    return

@app.route('/')
def home():
    return "Bot is running."

if __name__ == "__main__":
    threading.Thread(target=auto_poster, daemon=True).start()
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
