import threading
from flask import Flask
from bot import build_app
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "SMM Bot is up"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    # start flask in background thread (for Render health checks)
    t = threading.Thread(target=run_flask)
    t.start()

    # start telegram bot (polling)
    application = build_app()
    application.run_polling(allowed_updates=None)
