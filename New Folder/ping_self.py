import threading
import time
import requests

def ping():
    while True:
        try:
            requests.get("https://your-render-url.onrender.com")
        except:
            pass
        time.sleep(600)

def start_pinger():
    thread = threading.Thread(target=ping)
    thread.start()
