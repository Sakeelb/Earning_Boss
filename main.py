import os
import telebot
import openai

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # अपना बॉट टोकन
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # OpenAI API Key

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

PROMO_CHANNEL = "@All_Gift_Code_Earning"
FORWARD_MESSAGE_ID = 398

KEYWORDS = [
    "subscribe", "join", "joining", "refer", "register", "earning", "https", "invite", "@", "channel",
    "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो", "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward",
    "bonus", "gift", "win", "offer", "loot", "free", "telegram"
]

# /start कमांड पर सिर्फ फॉरवर्ड मैसेज
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

# /ai कमांड पर OpenAI से जवाब
@bot.message_handler(commands=['ai'])
def ai_handler(message):
    prompt = message.text.split(' ', 1)[-1].strip()
    if prompt:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
            bot.send_message(message.chat.id, reply)
        except Exception as e:
            bot.send_message(message.chat.id, f"AI Error: {str(e)}")
    else:
        bot.reply_to(message, "कृपया /ai के बाद अपना सवाल लिखें।\nउदाहरण: /ai आज मौसम कैसा है?")

# Keywords वाले मैसेज पर reply + forward दोनों
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

bot.infinity_polling()
