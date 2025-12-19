# bot.py
from telegram.ext import Application, JobQueue
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


def create_bot():
    # 1️⃣ DB init
    init_db()

    # 2️⃣ JobQueue
    job_queue = JobQueue()

    # 3️⃣ Application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .job_queue(job_queue)
        .build()
    )

    # 4️⃣ Periodic job
    application.job_queue.run_repeating(
        check_orders,
        interval=300,
        first=20
    )

    # 5️⃣ Handlers
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📦 Buyurtmalarim$"), my_orders))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🛒 Xizmatlar$"), services_menu))
    application.add_handler(CallbackQueryHandler(services_by_category, pattern="^cat_"))
    application.add_handler(CallbackQueryHandler(service_selected, pattern="^service_"))
    application.add_handler(order_conversation)
    application.add_handler(payment_conversation)
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^[0-9]+\\|"), add_balance))
    application.add_handler(MessageHandler(filters.COMMAND, admin_panel))

    return application
