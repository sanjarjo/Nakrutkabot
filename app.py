from flask import Flask, request
from telegram import Update
from bot import create_bot
import asyncio

app = Flask(__name__)
tg_app = create_bot()

# 🔴 MUHIM: Telegram application ishga tushadi
asyncio.run(tg_app.initialize())
asyncio.run(tg_app.start())

@app.route("/", methods=["GET"])
def home():
    return "SMM Bot ishlayapti 🚀"

@app.route(f"/webhook/{tg_app.bot.token}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)

    asyncio.get_event_loop().create_task(
        tg_app.process_update(update)
    )

    return "OK"
