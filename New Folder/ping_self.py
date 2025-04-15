import time
import requests

def start_pinger():
    def ping():
        while True:
            try:
                requests.get("https://earning-boss-bot.onrender.com")
                print("Pinged self.")
            except Exception as e:
                print(f"Ping error: {e}")
            time.sleep(300)  # 5 minutes

    import threading
    thread = threading.Thread(target=ping)
    thread.daemon = True
    thread.start()
