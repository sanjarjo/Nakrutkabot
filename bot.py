from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from handlers import user, admin
from database.db import init_db

def build_app():
    init_db()
    app = ApplicationBuilder().token(__import__("config").BOT_TOKEN).build()

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

    # add conversation handlers for admin flows
    add_balance_conv = ConversationHandler(
        entry_points=[CommandHandler("add_balance", admin.add_balance_start)],
        states={
            admin.ADMIN_BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_balance_handle),
                                  MessageHandler(filters.TEXT & ~filters.COMMAND, admin.add_balance_confirm)]
        },
        fallbacks=[]
    )
    app.add_handler(add_balance_conv)

    check_order_conv = ConversationHandler(
        entry_points=[CommandHandler("check_order", admin.check_order_start)],
        states={admin.CHECK_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin.check_order_handle)]},
        fallbacks=[]
    )
    app.add_handler(check_order_conv)

    return app

if __name__ == "__main__":
    application = build_app()
    application.run_polling()
