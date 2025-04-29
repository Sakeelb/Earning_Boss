import threading
import time
import requests

def ping():
    while True:
        try:
            requests.get("https://earning-boss-bot.onrender.com")
            print("Pinged Successfully")
        except Exception as e:
            print(f"Ping Error: {e}")
        time.sleep(600)  # every 10 mins

def start_pinger():
    thread = threading.Thread(target=ping)
    thread.daemon = True
    thread.start()
