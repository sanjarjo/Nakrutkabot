from telegram.ext import Application
from config import BOT_TOKEN
from handlers.start import start_handler
from database.init_db import init_db

def build_app():
    init_db()  # 🔥 DB avtomatik yaratiladi
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(start_handler)
    return app
    
def build_app():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)

    return app
