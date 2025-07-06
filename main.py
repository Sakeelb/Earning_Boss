import os
import telebot
import threading
import time
from flask import Flask, request
import pytz
from datetime import datetime
import re
import random

# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROMO_CHANNEL = "@All_Gift_Code_Earning" # Your promotion channel
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
IS_RENDER = os.environ.get("RENDER") # Check if running on Render

# Initialize bot and Flask app
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Image and Message Data ---

# Good Morning Image URLs
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

# Good Night Image URLs
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

# Good Morning Messages
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

# Good Night Messages
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

# Keywords for promotional replies
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

# Start command message and image
START_MESSAGE_TEXT = """
*Urgent Update:*
*Naya Gift Code / Offer Live ho chuka hai.*
*Isko paane ke liye hamare channel se juden:*
*[[ @All_Gift_Code_Earning ]]*
"""
START_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png"

# --- Helper Functions ---

def get_today_index(list_length):
    """
    Calculates an index based on the current day of the year.
    This ensures a different message/image is used each day in a cycle.
    """
    today = int(datetime.now().strftime("%j")) # Day of the year (1-366)
    return today % list_length

def send_message_auto(messages, images, prefix_emoji):
    """
    Sends an automated message with an image and reaction to the promo channel.
    """
    try:
        # Get message and image based on today's index
        idx = get_today_index(len(messages))
        msg = messages[idx]
        image_url = images[idx % len(images)] # Ensure image index loops correctly
        caption = f"{prefix_emoji} {msg}"

        print(f"Attempting to send message to {PROMO_CHANNEL} with caption: {caption}")
        # Send the message and get the sent message object
        sent_message = bot.send_photo(PROMO_CHANNEL, image_url, caption=caption, parse_mode='Markdown')
        print(f"Message sent! Message ID: {sent_message.message_id}")

        # Add reactions to the sent message
        if sent_message:
            reactions_to_add = ['👍', '❤️'] # Customize your reactions here
            for reaction_emoji in reactions_to_add:
                try:
                    bot.set_message_reaction(
                        chat_id=PROMO_CHANNEL,
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
    Thread function to periodically send Good Morning/Night messages.
    """
    posted_morning_today = False
    posted_night_today = False
    india_timezone = pytz.timezone('Asia/Kolkata')
    
    # Initialize random minutes for today
    morning_minute = random.randint(0, 10)  # Between X:00 and X:10 AM
    night_minute = random.randint(0, 10)    # Between Y:00 and Y:10 PM
    
    # Keep track of the last day the poster ran to reset flags reliably
    last_run_day = datetime.now(india_timezone).day
    
    print(f"Auto-poster started. Morning target minute: {morning_minute}, Night target minute: {night_minute}")
    print(f"Initial last run day: {last_run_day}")

    while True:
        now = datetime.now(india_timezone)
        current_hour = now.hour
        current_minute = now.minute
        current_day = now.day # Get current day of the month

        # Daily Reset: Check if the day has changed
        if current_day != last_run_day:
            print(f"Day changed from {last_run_day} to {current_day}. Resetting flags and generating new random minutes.")
            posted_morning_today = False
            posted_night_today = False
            morning_minute = random.randint(0, 10)
            night_minute = random.randint(0, 10)
            last_run_day = current_day # Update last run day
            print(f"New morning target minute: {morning_minute}, New night target minute: {night_minute}")
        
        # Good Morning Time (5:00-5:10 AM IST)
        if current_hour == 5 and not posted_morning_today:
            if current_minute >= morning_minute:
                print(f"Time to send Good Morning! Current: {current_hour}:{current_minute}, Target: 5:{morning_minute}")
                send_message_auto(UNIQUE_MORNING_MESSAGES, MORNING_IMAGE_URLS, "☀️")
                posted_morning_today = True
                print("Good Morning message sent and flag set.")
        
        # Good Night Time (10:00-10:10 PM IST)
        if current_hour == 22 and not posted_night_today:
            if current_minute >= night_minute:
                print(f"Time to send Good Night! Current: {current_hour}:{current_minute}, Target: 22:{night_minute}")
                send_message_auto(UNIQUE_NIGHT_MESSAGES, NIGHT_IMAGE_URLS, "🌙")
                posted_night_today = True
                print("Good Night message sent and flag set.")
        
        # Sleep for a duration before checking again
        time.sleep(60) # Check every 60 seconds (1 minute)

def keyword_found(text):
    """
    Checks if any defined keyword or URL pattern is present in the text.
    """
    text = text.lower()
    # Remove punctuation except @ and / for channel names and commands
    text = re.sub(r'[^\w\s@/]', '', text) 
    
    for kw in KEYWORDS:
        # Use word boundaries for most keywords to avoid partial matches (e.g., "join" not matching "joining")
        # However, for some like 'https' or '@', direct substring match might be intended.
        # Modified to handle specific keywords where partial match is OK (like 'join' within 'joining')
        if kw in ["https", "@", "t.me", "bit.ly"]: # These are often part of URLs
             if kw in text:
                 return True
        elif re.search(r'\b' + re.escape(kw) + r'\b', text): # For whole words
            return True
        # Specific check for Hindi words that might not always have clear word boundaries
        if kw in ["चैनल", "ज्वाइन", "कमई", "पैसे", "फ़ॉलो"]:
            if kw in text:
                return True

    # Check for common URL patterns explicitly
    if re.search(r'(https?://\S+|t\.me/\S+|bit\.ly/\S+)', text):
        return True
    return False

# --- Telegram Bot Message Handlers ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    """
    Handles the /start command, sending a promotional message and image.
    """
    print(f"Received /start command from {message.chat.id}")
    try:
        bot.send_photo(message.chat.id, START_IMAGE_URL, caption=START_MESSAGE_TEXT, parse_mode='Markdown')
        print(f"Sent /start message to {message.chat.id}")
    except Exception as e:
        print(f"Error in /start handler for chat ID {message.chat.id}: {e}")
        bot.send_message(message.chat.id, f"Error receiving /start: {e}")

@bot.message_handler(func=lambda msg: True)
def promo_reply(message):
    """
    Handles all incoming messages and replies with a promotion if keywords are found.
    """
    if not message.text:
        return # Ignore messages without text (e.g., photos without caption)

    print(f"Received message from {message.chat.id}: {message.text}")
    try:
        if keyword_found(message.text):
            print(f"Keyword found in message from {message.chat.id}. Sending promo reply.")
            promo_caption = "*[[Boss >> हमारे चैनल को भी [[ Join ]] करें:]]*\n*[[ https://t.me/All_Gift_Code_Earning ]]*"
            
            bot.send_photo(
                chat_id=message.chat.id,
                photo="https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/IMG_20250605_144922.png",
                caption=promo_caption,
                parse_mode='Markdown',
                reply_to_message_id=message.message_id # Reply to the user's message
            )
            print(f"Promo reply sent to {message.chat.id}.")
    except Exception as e:
        print(f"Error in promo_reply for message ID {message.message_id}: {e}")

# --- Flask App Routes for Webhook ---

@app.route('/', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive updates from Telegram.
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
    Simple home page to confirm the Flask app is running.
    """
    return "Bot is running and listening for updates!"

# --- Main Execution Block ---

if __name__ == "__main__":
    # Start the auto-poster in a separate thread
    threading.Thread(target=auto_poster, daemon=True).start()
    print("Auto-poster thread started.")

    # Configure webhook for Render deployment or use long polling for local
    if IS_RENDER == "true": # Render sets environment variables as strings
        if BOT_TOKEN and WEBHOOK_URL:
            try:
                bot.set_webhook(url=f"{WEBHOOK_URL}/")
                print(f"Webhook set to: {WEBHOOK_URL}/")
                # Run Flask app for webhook
                app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
            except Exception as e:
                print(f"Error setting webhook or starting Flask app: {e}")
                print("Falling back to long polling.")
                bot.infinity_polling() # Fallback
        else:
            print("Environment variables BOT_TOKEN or WEBHOOK_URL not set for Render. Using long polling.")
            bot.infinity_polling()
    else:
        print("Not running on Render (IS_RENDER not 'true'). Running with long polling (for local development).")
        bot.infinity_polling()

