from quart import Quart, request
from telegram import Update
import asyncio
from bot import build_app
from config import BOT_TOKEN

app = Quart(__name__)
tg_app = build_app()

loop = asyncio.get_event_loop()
loop.run_until_complete(tg_app.initialize())
loop.run_until_complete(tg_app.start())


@app.route("/", methods=["GET"])
async def home():
    return "✅ SMM Bot ishlayapti (Webhook)"


@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    data = await request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return "OK", 200
