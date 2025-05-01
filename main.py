import os
import telebot
import threading
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = "@All_Gift_Code_Earning"  # अपना चैनल यूजरनेम
FORWARD_MESSAGE_ID = 398  # चैनल का वो मैसेज जो फॉरवर्ड करना है

bot = telebot.TeleBot(BOT_TOKEN)

KEYWORDS = [
    "subscribe", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
    "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward",
    "bonus", "gift", "win", "offer", "loot", "free", "telegram"
]

# आपके दिए गए यूनिक गुड मॉर्निंग कमाई वाले मैसेज
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

def get_today_message():
    # हर दिन के लिए एक यूनिक मैसेज (date के हिसाब से)
    today = int(time.strftime("%j"))  # साल का दिन (1-366)
    return UNIQUE_MORNING_MESSAGES[today % len(UNIQUE_MORNING_MESSAGES)]

# 1. Good Morning Auto Poster (सुबह 5 बजे)
def good_morning_poster():
    while True:
        now = time.strftime("%H:%M")
        if now == "05:00":
            try:
                msg = get_today_message()
                bot.send_message(PROMO_CHANNEL, f"☀️ {msg}\n\n@All_Gift_Code_Earning जॉइन करें।")
            except Exception as e:
                print(f"Morning Post Error: {str(e)}")
            time.sleep(60)
        time.sleep(30)

# 2. /start कमांड पर सिर्फ फॉरवर्ड मैसेज
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

# 3. Keywords वाले मैसेज पर reply + forward दोनों
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
            bot.send_message(message.chat.id, f"Error: {e}")

# गुड मॉर्निंग थ्रेड शुरू करें
threading.Thread(target=good_morning_poster, daemon=True).start()

# बॉट शुरू करें
bot.infinity_polling()
