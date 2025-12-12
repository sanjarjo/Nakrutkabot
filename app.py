import os
from flask import Flask, request
from bot import build_app

app = Flask(__name__)
application = build_app()     # telegram app

# HOME
@app.route("/", methods=["GET"])
def home():
    return "SMM Bot Webhook Running"

# TELEGRAM WEBHOOK
from config import BOT_TOKEN
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    application.update_queue.put_nowait(update)
    return "ok", 200

# SET WEBHOOK
@app.route("/set-webhook")
def set_webhook():
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}{WEBHOOK_PATH}"
    application.bot.set_webhook(url)
    return f"Webhook set: {url}"

if __name__ == "__main__":
    # IMPORTANT: ONLY FLASK RUNS ON RENDER
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
