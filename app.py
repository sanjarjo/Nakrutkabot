from flask import Flask, request
from telegram import Update
from bot import build_app
import asyncio
from asgiref.wsgi import WsgiToAsgi

flask_app = Flask(__name__)
tg_app = build_app()

@flask_app.route("/", methods=["GET"])
def home():
    return "SMM Bot ishlayapti 🚀"

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)

    asyncio.get_event_loop().create_task(
        tg_app.process_update(update)
    )
    return "OK"

# ASGI wrapper
app = WsgiToAsgi(flask_app)
