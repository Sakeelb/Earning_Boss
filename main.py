import os
import telebot
import threading
import time
import random
import re
from datetime import datetime
import pytz
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== CONFIG ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

try:
    OWNER_ID = int(os.environ.get("OWNER_ID"))
except (TypeError, ValueError):
    OWNER_ID = 0
    print("WARNING: OWNER_ID not set or invalid numeric ID.")

PROMO_CHANNEL_ID = "-1002437678122"
PROMO_CHANNEL_LINK = "https://t.me/Proper_Trending"

# ========== IMAGE URLs ==========
PROMO_IMAGE_URL = "https://raw.githubusercontent.com/Sakeelb/Earning_Boss/refs/heads/main/New/1781241774791.png"

# Handicrafts related images
MORNING_IMAGE_URLS = [
    "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&q=80",  # Handicrafts
    "https://images.unsplash.com/photo-1532372320572-cda25653a694?w=800&q=80",  # Marble art
    "https://images.unsplash.com/photo-1576941089062-65b9f5b6ddb8?w=800&q=80",  # Handmade items
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80",  # Art pieces
    "https://images.unsplash.com/photo-1563170351-be824bc3aa6a?w=800&q=80",  # Stone crafts
    "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=800&q=80",  # Handicrafts
    "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&q=80",  # Traditional crafts
    "https://images.unsplash.com/photo-1558618666-fcd25c85f84e?w=800&q=80",  # Marble work
    "https://images.unsplash.com/photo-1598532451110-1cdb52b435da?w=800&q=80",  # Handmade decor
    "https://images.unsplash.com/photo-1565688534245-05d6b5be184a?w=800&q=80"   # Stone art
]

NIGHT_IMAGE_URLS = [
    "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&q=80",
    "https://images.unsplash.com/photo-1532372320572-cda25653a694?w=800&q=80",
    "https://images.unsplash.com/photo-1576941089062-65b9f5b6ddb8?w=800&q=80",
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80",
    "https://images.unsplash.com/photo-1563170351-be824bc3aa6a?w=800&q=80",
    "https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=800&q=80",
    "https://images.unsplash.com/photo-1558618666-fcd25c85f84e?w=800&q=80",
    "https://images.unsplash.com/photo-1598532451110-1cdb52b435da?w=800&q=80",
    "https://images.unsplash.com/photo-1565688534245-05d6b5be184a?w=800&q=80",
    "https://images.unsplash.com/photo-1602351447937-745cb720612f?w=800&q=80"
]

# ========== TEMPLATES ==========
# Handicrafts business related morning templates
MORNING_TEMPLATES = [
    "*Good Morning!* Aaj naye handicrafts collection aaye hain. 🏺",
    "*Good Morning!* White marble handcrafted items available. ⚪",
    "*Good Morning!* Natural stone art pieces ready for delivery. 🎨",
    "*Good Morning!* Handmade marble items - premium quality. ✨",
    "*Good Morning!* Naya handicrafts stock aaya hai. 🏛️",
    "*Good Morning!* White marble decor items for your home. 🏠",
    "*Good Morning!* Handmade polish stone artifacts available. 💎",
    "*Good Morning!* Best handicrafts collection today. 🌟",
    "*Good Morning!* Traditional handcrafted marble items. 🎭",
    "*Good Morning!* Natural stone handicrafts - limited stock. ⭐"
]

# Handicrafts business related night templates
NIGHT_TEMPLATES = [
    "*Good Night!* Kal naye handicrafts products aayenge. 🌙",
    "*Good Night!* Kal white marble collection launch. ⚪",
    "*Good Night!* Handmade stone art - kal milega. 🎨",
    "*Good Night!* Kal handicrafts deals available. 🏺",
    "*Good Night!* Premium marble handicrafts kal. ✨",
    "*Good Night!* Natural stone products kal aayenge. 💎",
    "*Good Night!* Handcrafted items - kal ki booking shuru. 📋",
    "*Good Night!* Kal special handicrafts offer. 🎁",
    "*Good Night!* White marble home decor kal. 🏠",
    "*Good Night!* Handmade polish items kal available. ⭐"
]

# Promo captions for handicrafts
PROMO_CAPTIONS = [
    "🏺 Premium Handicrafts Collection - Join Now",
    "✨ White Marble Handmade Items Available",
    "🎨 Natural Stone Art - Direct from Artisans",
    "⚪ Handcrafted Marble Decor - Limited Stock",
    "💎 Handmade Polish Stone Products",
    "🏛️ Traditional Handicrafts - Best Quality",
    "🎭 Exclusive Marble Art Pieces Available",
    "⭐ Premium Handicrafts - Wholesale Available",
    "🏠 Home Decor Handicrafts - Order Now",
    "🌟 Handmade Stone Crafts - Direct Sourcing"
]

# ========== KEYWORDS ==========
# Existing keywords + handicrafts related keywords
KEYWORDS = [
    # Existing keywords
    "subscribe", "chat", "reply", "join", "joining", "refer", "register", "earning",
    "https", "invite", "@", "channel", "मेरे चैनल", "मेरा चैनल", "चैनल को", "follow", "फॉलो",
    "ज्वाइन", "चैनल", "जॉइन", "link", "promo", "reward", "bonus", "gift", "win", "offer", "loot",
    "free", "telegram", "new offer", "today offer", "instant reward", "free gift code", "giveaway",
    "task earning", "refer and earn", "daily bonus", "claim reward", "kamai", "पैसे", "paise kaise",
    "online paise", "ghar baithe kamai", "extra earning", "make money online", "earn money",
    "withdrawal proof", "payment proof", "real earning", "trusted earning", "instant payment",
    "upi earning", "paytm cash", "google pay offer", "crypto earning", "bitcoin earning",
    "ethereum earning", "online job", "work from home", "part time job", "full time job",
    "referred", "referring", "ref", "referal", "refer code", "joining bonus", "joining link", "/join",
    
    # New handicrafts keywords
    "handicrafts", "हस्तशिल्प", "handmade", "हाथ से बना", "marble", "संगमरमर",
    "white marble", "सफेद संगमरमर", "stone art", "पत्थर कला", "crafts", "शिल्प",
    "handicraft items", "हस्तशिल्प सामान", "home decor", "घर सजावट",
    "traditional crafts", "पारंपरिक शिल्प", "art pieces", "कला के टुकड़े",
    "handmade items", "हस्तनिर्मित वस्तुएं", "natural stone", "प्राकृतिक पत्थर",
    "marble items", "संगमरमर सामान", "hand polish", "हाथ पॉलिश",
    "crafts business", "शिल्प व्यवसाय", "wholesale handicrafts", "थोक हस्तशिल्प",
    "artisan crafts", "कारीगर शिल्प", "handmade decor", "हस्तनिर्मित सजावट",
    "stone crafts", "पत्थर शिल्प", "marble art", "संगमरमर कला",
    "craft products", "शिल्प उत्पाद", "handicraft dealer", "हस्तशिल्प विक्रेता",
    "handicrafts wholesale", "हस्तशिल्प थोक", "marble handicraft", "संगमरमर हस्तशिल्प",
    "stone handicraft", "पत्थर हस्तशिल्प", "handmade gifts", "हस्तनिर्मित उपहार",
    "craft items", "शिल्प वस्तुएं", "handicrafts business", "हस्तशिल्प व्यवसाय",
    "मार्बल आर्ट", "स्टोन डेकोर", "हैंडमेड पॉलिश", "क्राफ्ट कलेक्शन"
]

# ========== BOT INIT ==========
bot = telebot.TeleBot(BOT_TOKEN)

# ========== HELPER FUNCTIONS ==========
def send_channel_auto(templates, images, prefix_emoji):
    """Send automated handicrafts posts to channel"""
    # Random product details for handicrafts
    profit = random.randint(500, 5000)  # Price range for handicrafts
    template = random.choice(templates)
    image_url = random.choice(images)
    
    # Add product details based on your images
    product_details = [
        "White Marble Handmade Items",
        "Natural Stone Art Pieces",
        "Hand Carved Marble Decor",
        "Traditional Stone Crafts",
        "Hand Polished Marble Products",
        "Exclusive Handicrafts Collection",
        "Premium Marble Artifacts",
        "Handmade Stone Decor Items"
    ]
    
    msg = template.format(amount=profit)
    msg += f"\n\n🛍️ *{random.choice(product_details)}*"
    msg += f"\n💰 Price: ₹{profit}/piece"
    msg += "\n📦 Wholesale Available"
    msg += "\n📱 Contact for orders"

    try:
        sent = bot.send_photo(PROMO_CHANNEL_ID, image_url, caption=msg, parse_mode='Markdown')
        if sent:
            for emoji in ['👍', '❤️', '⭐']:
                try:
                    bot.set_message_reaction(PROMO_CHANNEL_ID, sent.message_id, reaction=[{'type': 'emoji', 'emoji': emoji}])
                except:
                    pass
    except Exception as e:
        print(f"Auto-post error (Telegram): {e}")

def auto_poster():
    india_tz = pytz.timezone('Asia/Kolkata')
    morning_time = random.randint(30, 60)
    night_time = random.randint(29, 59)
    morning_sent_today = False
    night_sent_today = False
    today_date = None

    while True:
        try:
            now = datetime.now(india_tz)
            hour = now.hour
            minute = now.minute
            current_date = now.date()
            
            if current_date != today_date:
                morning_sent_today = False
                night_sent_today = False
                today_date = current_date
                morning_time = random.randint(30, 60)
                night_time = random.randint(29, 59)
                print(f"New day! Morning target: {morning_time}min after 4am, Night target: {night_time}min after 11pm")

            # Morning post
            if not morning_sent_today and 4 <= hour < 12:
                if hour == 4:
                    mins_passed = minute
                else:
                    mins_passed = (hour - 4) * 60 + minute
                
                if mins_passed >= morning_time:
                    print(f"Sending morning handicrafts post at {now.strftime('%H:%M')}")
                    send_channel_auto(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                    morning_sent_today = True
                    print("Morning handicrafts post sent successfully!")

            # Night post
            if not night_sent_today and hour == 23:
                if minute >= night_time:
                    print(f"Sending night handicrafts post at {now.strftime('%H:%M')}")
                    send_channel_auto(NIGHT_TEMPLATES, NIGHT_IMAGE_URLS, "🌙")
                    night_sent_today = True
                    print("Night handicrafts post sent successfully!")

            # Backup morning post
            if not morning_sent_today and hour == 11 and minute >= 0:
                print(f"Sending backup morning handicrafts post at {now.strftime('%H:%M')}")
                send_channel_auto(MORNING_TEMPLATES, MORNING_IMAGE_URLS, "☀️")
                morning_sent_today = True

            time.sleep(60)
            
        except Exception as e:
            print(f"Auto-poster error: {e}")
            time.sleep(60)

def keyword_found(text):
    if not text:
        return False
    text = text.lower()
    text = re.sub(r'[^\w\s@/\.]', '', text)
    for kw in KEYWORDS:
        kw_low = kw.lower()
        if kw_low in ["https", "@", "t.me", "bit.ly"]:
            if kw_low in text:
                return True
        if kw_low in ["चैनल", "ज्वाइन", "कमई", "पैसे", "फ़ॉलो", "join", "chat", "/join", "हस्तशिल्प", "मार्बल", "क्राफ्ट"]:
            if kw_low in text:
                return True
        if re.search(r'\b' + re.escape(kw_low) + r'\b', text):
            return True
    return False

def send_promo(chat_id):
    """Send handicrafts promotion message"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏺 View Handicrafts", url=PROMO_CHANNEL_LINK))
    markup.add(InlineKeyboardButton("📞 Contact Seller", url="https://t.me/Proper_Trending"))
    
    caption = random.choice(PROMO_CAPTIONS)
    caption += "\n\n🛍️ *Handmade White Marble Items Available*"
    caption += "\n⚪ Natural Stone Art Pieces"
    caption += "\n✨ Hand Polished Products"
    caption += "\n📦 Wholesale & Retail Available"
    
    try:
        bot.send_photo(chat_id, PROMO_IMAGE_URL, caption=caption, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Send promo error: {e}")

# ========== TELEGRAM HANDLERS ==========
@bot.message_handler(commands=['start'])
def start_handler(msg):
    welcome_text = """🏺 *Welcome to Handicrafts Store!*

We offer premium handmade handicrafts:
✨ White Marble Items
⚪ Natural Stone Art
🎨 Hand Polished Decor
🏛️ Traditional Crafts

*Our Products:*
• Home Decor Items
• Marble Artifacts
• Stone Crafts
• Handmade Gifts

📦 *Wholesale Available*
📞 *Contact for Orders*

Click below to see our collection!"""
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏺 View Collection", url=PROMO_CHANNEL_LINK))
    markup.add(InlineKeyboardButton("📞 Contact Seller", url="https://t.me/Proper_Trending"))
    
    try:
        bot.send_message(msg.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Start handler error: {e}")

@bot.message_handler(func=lambda m: True)
def handle_all_messages(msg):
    # Don't forward owner's messages
    if OWNER_ID != 0 and msg.from_user.id == OWNER_ID:
        return

    # Forward user messages to owner
    if OWNER_ID != 0:
        try:
            user = msg.from_user
            name = f"{user.first_name} {user.last_name or ''}".strip()
            if user.username:
                name += f" (@{user.username})"
            text_content = msg.text if msg.text else "[Non-text message]"
            forward_text = f"📩 *New Handicrafts Inquiry*\n👤 {name}\n🆔 `{user.id}`\n💬 {text_content}"
            bot.send_message(OWNER_ID, forward_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Forwarding failed: {e}")

    # Check for keywords and send promo
    if msg.text and keyword_found(msg.text):
        send_promo(msg.chat.id)

# ========== MAIN ==========
if __name__ == "__main__":
    print("=== Handicrafts Telegram Bot Starting ===")
    print(f"Bot Token: {'*' * len(BOT_TOKEN[:10])}")
    print(f"Owner ID: {OWNER_ID}")
    print(f"Channel ID: {PROMO_CHANNEL_ID}")
    print(f"Channel Link: {PROMO_CHANNEL_LINK}")
    print("=== Bot is ready for handicrafts business ===")
    
    # Clear webhook
    try:
        bot.delete_webhook()
        print("Webhook cleared successfully.")
    except Exception as e:
        print(f"Error clearing webhook: {e}")

    time.sleep(2)

    # Start auto-poster thread
    auto_thread = threading.Thread(target=auto_poster, daemon=True)
    auto_thread.start()
    print("Auto-poster thread started.")

    # Start polling
    print("Starting polling...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling crashed: {e}. Restarting in 10 seconds...")
            time.sleep(10)
