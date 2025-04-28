from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running - Boss Mode"

def run():
    port = int(os.environ.get('PORT', 10000))  # PORT यहाँ से लें
    app.run(
        host='0.0.0.0',
        port=port
    )

def keep_alive():
    t = Thread(target=run)
    t.start()
