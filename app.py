from flask import Flask, request
from telegram import Update
from bot import build_app
import asyncio

app = Flask(__name__)
tg_app = build_app()

@app.route("/", methods=["GET"])
def home():
    return "SMM Bot ishlayapti 🚀"

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return "OK"
