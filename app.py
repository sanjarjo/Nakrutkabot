from flask import Flask, request
from telegram import Update
import asyncio

from bot import build_app
from config import BOT_TOKEN

app = Flask(__name__)

# 🔹 Telegram Application
tg_app = build_app()

# 🔹 Event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 🔹 Telegram app start
loop.run_until_complete(tg_app.initialize())
loop.run_until_complete(tg_app.start())


@app.route("/", methods=["GET"])
def home():
    return "✅ SMM Bot ishlayapti (Webhook)"


@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    loop.run_until_complete(tg_app.process_update(update))
    return "OK", 200
