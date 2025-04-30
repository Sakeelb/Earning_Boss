import os
import telebot
import threading
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # अपने बॉट टोकन से बदलें
bot = telebot.TeleBot(BOT_TOKEN)

PROMO_CHANNEL = "@All_Gift_Code_Earning"
FORWARD_MESSAGE_ID = 398  # आपके चैनल के उस मैसेज की ID जिसे फॉरवर्ड करना है

KEYWORDS = [
    "subscribe", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
    "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward",
    "bonus", "gift", "win", "offer", "loot", "free", "telegram"
]

# 1. Good Morning Auto Poster (सुबह 5 बजे)
def good_morning_poster():
    while True:
        now = time.strftime("%H:%M")
        if now == "05:00":
            try:
                bot.send_message(PROMO_CHANNEL, "☀️ गुड मॉर्निंग! आपका दिन शुभ हो।\n\n@All_Gift_Code_Earning जॉइन करें।")
            except Exception as e:
                print(f"Morning Post Error: {str(e)}")
            time.sleep(60)
        time.sleep(30)

# 2. /start कमांड पर सिर्फ फॉरवर्ड मैसेज भेजना
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=PROMO_CHANNEL,
            message_id=FORWARD_MESSAGE_ID
        )
    except Exception as e:
        print(f"Start Error: {str(e)}")
        bot.send_message(message.chat.id, "कुछ समस्या हुई, कृपया बाद में प्रयास करें।")

# 3. Keywords वाले मैसेज पर पहले reply फिर forward दोनों भेजें
@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    text = message.text.lower()
    if any(keyword in text for keyword in KEYWORDS):
        try:
            promo_text = "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]] [[ https://t.me/All_Gift_Code_Earning ]]"
            bot.reply_to(message, promo_text)
            bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=PROMO_CHANNEL,
                message_id=FORWARD_MESSAGE_ID
            )
        except Exception as e:
            print(f"Promo Reply Error: {str(e)}")
            bot.send_message(message.chat.id, "कुछ समस्या हुई, कृपया बाद में प्रयास करें।")

# बॉट को चलाने के लिए गुड मॉर्निंग थ्रेड स्टार्ट करें
threading.Thread(target=good_morning_poster, daemon=True).start()

# बॉट शुरू करें
bot.infinity_polling()
