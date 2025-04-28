from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running - Boss Mode"

def run():
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))  # Render.com का PORT इस्तेमाल करें
    )

def keep_alive():
    t = Thread(target=run)
    t.start()
