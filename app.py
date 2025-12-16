# app.py
from quart import Quart, request
from telegram import Update
from bot import create_bot
import asyncio
import requests

app = Quart(__name__)
tg_app = create_bot()

# 🔹 Webhookni o'rnatish (bir marta ishga tushirilganda)
BOT_TOKEN = tg_app.bot.token
WEBHOOK_URL = f"https://nakrutkabot-knbn.onrender.com/webhook/{BOT_TOKEN}"

try:
    res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")
    print("Webhook response:", res.json())
except Exception as e:
    print("Webhook o'rnatishda xatolik:", e)

@app.route("/", methods=["GET"])
async def home():
    return "SMM Bot ishlayapti 🚀"

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    """Telegram webhook uchun endpoint"""
    data = await request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return "OK"
