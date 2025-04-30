import os
import telebot
import threading
import time
import openai
from keep_alive import keep_alive
from ping_self import start_pinger

# Env Variables
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
                bot.send_message(PROMO_CHANNEL, "☀️ Good Morning! आपका दिन शुभ हो।\n\n@All_Gift_Code_Earning जॉइन करें।")
            except Exception as e:
                print(f"Morning Post Error: {str(e)}")
            time.sleep(60)
        time.sleep(30)

# 2. /start कमांड पर फिक्स्ड मैसेज फॉरवर्ड करें
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=PROMO_CHANNEL,
            message_id=398  # इसे अपने चैनल के उस मैसेज ID से बदलें जिसे फॉरवर्ड करना है
        )
    except Exception as e:
        print(f"Start Error: {str(e)}")

# 3. Keywords पर चैनल प्रमोशन reply (नए keywords के साथ)
@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    text = message.text.lower()
    keywords = [
        "join", "channel", "join channel", "join our channel", "join @", "join link",
        "ज्वाइन", "चैनल", "जॉइन", "refer", "https", "http", "link", "invite"
    ]
    if any(keyword in text for keyword in keywords):
        try:
            reply_text = f"👉 हमारे चैनल को जॉइन करें: {PROMO_CHANNEL}"
            bot.reply_to(message, reply_text)
        except Exception as e:
            print(f"Promo Reply Error: {str(e)}")

# 4. /ai कमांड पर AI से जवाब दो
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

# Keep alive और self-ping
keep_alive()
start_pinger()

# Good morning thread शुरू करें
threading.Thread(target=good_morning_poster, daemon=True).start()

# बॉट शुरू करें
bot.infinity_polling()
