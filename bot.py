from telegram.ext import Application
from config import BOT_TOKEN
from database.init_db import init_db
from handlers.start import start_handler
from handlers.admin import admin_panel, add_balance
from handlers.services import services_menu, services_by_category, service_selected
from handlers.orders import order_conversation
from handlers.payments import payment_conversation
from handlers.order_status import check_orders
from handlers.orders_list import my_orders
from telegram.ext import MessageHandler, CallbackQueryHandler, filters

def build_app():
    # 1️⃣ DB init
    init_db()

    # 2️⃣ Application yaratish
    app = Application.builder().token(BOT_TOKEN).build()

    # 3️⃣ JobQueue (order status update)
    app.job_queue.run_repeating(check_orders, interval=300, first=20)

    # 4️⃣ Handlerlar
    app.add_handler(start_handler)
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📦 Buyurtmalarim$"), my_orders))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🛒 Xizmatlar$"), services_menu))
    app.add_handler(CallbackQueryHandler(services_by_category, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(service_selected, pattern="^service_"))
    app.add_handler(order_conversation)
    app.add_handler(payment_conversation)
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^[0-9]+\\|"), add_balance))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: None)) # placeholder, ConversationHandler boshqaradi
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: None))
    app.add_handler(MessageHandler(filters.COMMAND, admin_panel))

    return app
