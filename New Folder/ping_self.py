import threading
import time
import requests

def start_pinger():
    def ping():
        while True:
            try:
                requests.get("https://earning-boss-bot.onrender.com")
            except Exception as e:
                print(f"Ping failed: {e}")
            time.sleep(600)  # Ping every 10 minutes

    thread = threading.Thread(target=ping)
    thread.daemon = True
    thread.start()
