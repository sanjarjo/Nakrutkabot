from telegram.ext import Application
from config import BOT_TOKEN
from handlers.start import start_handler

def build_app():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)

    return app
