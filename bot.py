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
    init_db()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .job_queue(True)   # ✅ MUHIM QATOR
        .build()
    )

    # ✅ Endi job_queue mavjud
    application.job_queue.run_repeating(
        check_orders, interval=300, first=20
    )

    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.Regex("^📦 Buyurtmalarim$"), my_orders))
    application.add_handler(MessageHandler(filters.Regex("^🛒 Xizmatlar$"), services_menu))

    application.add_handler(CallbackQueryHandler(services_by_category, pattern="^cat_"))
    application.add_handler(CallbackQueryHandler(service_selected, pattern="^service_"))

    application.add_handler(order_conversation)
    application.add_handler(payment_conversation)

    application.add_handler(MessageHandler(filters.Regex("^[0-9]+\\|"), add_balance))
    application.add_handler(MessageHandler(filters.COMMAND, admin_panel))

    return application
