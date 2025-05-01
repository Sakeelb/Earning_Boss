import os
import telebot
import threading
import time
import openai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMO_CHANNEL = "@All_Gift_Code_Earning"
FORWARD_MESSAGE_ID = 398

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

KEYWORDS = [
    "subscribe", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
    "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward",
    "bonus", "gift", "win", "offer", "loot", "free", "telegram"
]

# यूनिक गुड मॉर्निंग मैसेज (fallback)
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

# यूनिक गुड नाइट मैसेज (fallback)
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
    today = int(time.strftime("%j"))
    return messages[today % len(messages)]

def send_ai_message(prompt, fallback_messages, prefix_emoji):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.9,
        )
        msg = response.choices[0].message.content.strip()
        bot.send_message(PROMO_CHANNEL, f"{prefix_emoji} {msg}\n\n@All_Gift_Code_Earning जॉइन करें।")
    except Exception as e:
        fallback_msg = get_today_message(fallback_messages)
        bot.send_message(PROMO_CHANNEL, f"{prefix_emoji} {fallback_msg}\n\n@All_Gift_Code_Earning जॉइन करें।")
        print(f"AI Error: {e}")

def auto_poster():
    posted_morning = False
    posted_night = False
    while True:
        now = time.strftime("%H:%M")
        if now == "05:00" and not posted_morning:
            send_ai_message(
                "हिंदी में यूनिक, एनर्जेटिक, earning motivational गुड मॉर्निंग मैसेज बनाओ (50-100 शब्दों में)।",
                UNIQUE_MORNING_MESSAGES,
                "☀️"
            )
            posted_morning = True
        elif now != "05:00":
            posted_morning = False

        if now == "22:00" and not posted_night:
            send_ai_message(
                "हिंदी में यूनिक, एनर्जेटिक, earning motivational गुड नाइट मैसेज बनाओ (50-100 शब्दों में)।",
                UNIQUE_NIGHT_MESSAGES,
                "🌙"
            )
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

threading.Thread(target=auto_poster, daemon=True).start()

bot.infinity_polling()
