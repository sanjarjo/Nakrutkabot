from telegram.ext import Application
from config import BOT_TOKEN
from handlers.start import start_handler
from database.init_db import init_db
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.admin import admin_panel
from handlers.services import services_menu, services_by_category
from handlers.orders import service_selected
from handlers.orders import get_link, get_quantity
from handlers.orders import order_conversation
from handlers.payments import payment_conversation
from handlers.admin import add_balance

app.add_handler(payment_conversation)
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^[0-9]+\\|"), add_balance))
app.add_handler(order_conversation)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_link))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🛒 Xizmatlar$"), services_menu))
app.add_handler(CallbackQueryHandler(services_by_category, pattern="^cat_"))
app.add_handler(CallbackQueryHandler(service_selected, pattern="^service_"))

def build_app():
    init_db()  # 🔥 DB avtomatik yaratiladi
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(start_handler)
    return app
    
def build_app():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)

    return app
