import os
import telebot
import threading
import time
import openai
from keep_alive import keep_alive
from ping_self import start_pinger

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = os.environ.get("PROMO_CHANNEL", "@All_Gift_Code_Earning")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

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

# 2. /start कमांड - सिर्फ फॉरवर्ड मैसेज
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=PROMO_CHANNEL,
            message_id=398  # अपने चैनल के उस मैसेज ID से बदलें जिसे फॉरवर्ड करना है
        )
    except Exception as e:
        print(f"Start Error: {str(e)}")

# 3. /ai कमांड - OpenAI से जवाब
@bot.message_handler(commands=['ai'])
def ai_handler(message):
    prompt = message.text.split(' ', 1)[-1].strip()
    if prompt:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
            bot.send_message(message.chat.id, reply)
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")
            bot.send_message(message.chat.id, "⚠️ AI सर्वर बिजी है, बाद में ट्राई करें")
    else:
        bot.reply_to(message, "कृपया /ai के बाद सवाल लिखें।\nउदाहरण: /ai आज मौसम कैसा है?")

# 4. Keywords पर reply + forward message (सिर्फ इन case में)
@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    text = message.text.lower()
    keywords = [
        "subscribe", "join", "refer", "earning", "https", "invite", "@", "channel", 
        "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward"
    ]
    if any(keyword in text for keyword in keywords):
        try:
            # पहले reply भेजो
            reply = "[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]] [[ https://t.me/All_Gift_Code_Earning ]]"
            bot.reply_to(message, reply)
            # फिर forward message भेजो
            bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=PROMO_CHANNEL,
                message_id=398
            )
        except Exception as e:
            print(f"Promo Reply Error: {str(e)}")

# Keep alive और self-ping शुरू करें
keep_alive()
start_pinger()

# Good morning thread शुरू करें
threading.Thread(target=good_morning_poster, daemon=True).start()

# बॉट शुरू करें
bot.infinity_polling()
