from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from handlers import user, admin
from keyboards.main_menu import main_menu
from keyboards.service_menu import service_menu
from config import BOT_TOKEN

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # --- User Handlers ---
    user_conv = ConversationHandler(
        entry_points=[CommandHandler('start', user.start),
                      MessageHandler(Filters.regex("🛒 Xizmatlar"), user.service_callback)],
        states={
            user.ENTER_LINK: [MessageHandler(Filters.text & ~Filters.command, user.enter_link)],
            user.ENTER_QUANTITY: [MessageHandler(Filters.text & ~Filters.command, user.enter_quantity)],
            user.CONFIRM_ORDER: [MessageHandler(Filters.text & ~Filters.command, user.confirm_order)],
        },
        fallbacks=[]
    )
    dp.add_handler(user_conv)

    # Inline tugmalar
    dp.add_handler(CallbackQueryHandler(user.service_callback, pattern='service_.*'))

    # --- Admin Handlers ---
    dp.add_handler(CommandHandler('admin', admin.start_admin))

    # Balans qo‘shish
    add_balance_conv = ConversationHandler(
        entry_points=[CommandHandler('add_balance', admin.add_balance_start)],
        states={
            admin.ADMIN_BALANCE: [
                MessageHandler(Filters.text & ~Filters.command, admin.add_balance_enter),
                MessageHandler(Filters.text & ~Filters.command, admin.add_balance_confirm)
            ]
        },
        fallbacks=[]
    )
    dp.add_handler(add_balance_conv)

    # Buyurtma tekshirish
    check_order_conv = ConversationHandler(
        entry_points=[CommandHandler('check_order', admin.check_order_start)],
        states={
            admin.ADMIN_CHECK_ORDER: [
                MessageHandler(Filters.text & ~Filters.command, admin.check_order_enter)
            ]
        },
        fallbacks=[]
    )
    dp.add_handler(check_order_conv)

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
