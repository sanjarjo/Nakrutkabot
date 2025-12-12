import os
from flask import Flask, request
from bot import build_app

app = Flask(__name__)

telegram_app = build_app()
BOT_TOKEN = __import__("config").BOT_TOKEN

@app.route("/")
def home():
    return "Bot working"

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json(force=True)
    telegram_app.update_queue.put(json_update)
    return "OK", 200

@app.route("/set-webhook")
def set_webhook():
    url = f"{os.environ['RENDER_EXTERNAL_URL']}/webhook/{BOT_TOKEN}"
    telegram_app.bot.set_webhook(url)
    return {"status": "webhook set", "url": url}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
