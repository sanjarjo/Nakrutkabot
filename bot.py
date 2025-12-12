from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from handlers import user, admin
from database.db import init_db
from config import BOT_TOKEN

def build_app():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # user conversation
    user_conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", user.start),
            MessageHandler(filters.Regex("^📦 Xizmatlar$"), user.show_services)
        ],
        states={
            user.SELECT_SERVICE: [CallbackQueryHandler(user.service_callback, pattern="^service_")],
            user.ENTER_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.enter_link)],
            user.ENTER_QTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.enter_qty)],
            user.CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.confirm_order)],
        },
        fallbacks=[]
    )

    app.add_handler(user_conv)

    # admin handlers
    app.add_handler(CommandHandler("admin", admin.admin_panel))
    app.add_handler(CommandHandler("add_balance", admin.add_balance_start))
    app.add_handler(CommandHandler("check_order", admin.check_order_start))

    return app
