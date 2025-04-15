import requests
import time

def start_pinger():
    while True:
        try:
            response = requests.get("https://earning-boss-bot.onrender.com")  # Bot ka URL yaha rakhna hai
            print(f"Ping Response: {response.status_code}")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)  # Har 5 minute me ping bheje
