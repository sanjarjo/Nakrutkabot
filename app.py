# app.py
from flask import Flask, request
from telegram import Update
from bot import create_bot
import asyncio
import requests
import threading

app = Flask(__name__)
tg_app = create_bot()

# 1️⃣ Webhookni alohida thread orqali o'rnatish
def set_webhook():
    BOT_TOKEN = tg_app.bot.token
    WEBHOOK_URL = f"https://nakrutkabot-knbn.onrender.com/webhook/{BOT_TOKEN}"
    res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")
    print("Webhook response:", res.json())

# Flask ishga tushganda thread yaratib webhookni o'rnatamiz
threading.Thread(target=set_webhook).start()

@app.route("/", methods=["GET"])
def home():
    return "SMM Bot ishlayapti 🚀"

@app.route(f"/webhook/{tg_app.bot.token}", methods=["POST"])
def webhook():
    """Telegram webhook"""
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)

    # asyncio bilan async process_update
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(tg_app.process_update(update))
    else:
        loop.run_until_complete(tg_app.process_update(update))

    return "OK"
