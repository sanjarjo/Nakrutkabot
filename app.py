from flask import Flask, request
from telegram import Update
from bot import build_app
import asyncio
import os

app = Flask(__name__)
tg_app = build_app()

@app.route("/", methods=["GET"])
def home():
    return "SMM Bot ishlayapti 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)
    asyncio.run(tg_app.process_update(update))
    return "OK"
