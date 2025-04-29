import threading
import time
import requests
import os

def ping():
    while True:
        try:
            url = os.environ.get("RENDER_EXTERNAL_URL", "https://earning-boss-bot.onrender.com")
            requests.get(url)
        except Exception as e:
            print("Ping error:", e)
        time.sleep(600)

def start_pinger():
    t = threading.Thread(target=ping)
    t.daemon = True
    t.start()
