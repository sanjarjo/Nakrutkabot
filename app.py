from flask import Flask, request
from telegram import Update
from bot import create_bot
import asyncio

app = Flask(__name__)
tg_app = build_app()


@app.route("/", methods=["GET"])
def home():
    return "SMM Bot ishlayapti 🚀"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)

    asyncio.run(tg_app.process_update(update))
    return "OK"
