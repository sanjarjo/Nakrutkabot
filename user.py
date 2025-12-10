from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, ConversationHandler
from keyboards.main_menu import main_menu
from keyboards.service_menu import service_menu
from utils.helpers import generate_order_id, calculate_total_price, format_currency
from utils.api import create_order
from database.db import SessionLocal
from database.models import User, Service, Order
from config import ADMIN_TG_ID

# Conversation states
SELECT_SERVICE, ENTER_LINK, ENTER_QUANTITY, CONFIRM_ORDER = range(4)

def start(update: Update, context: CallbackContext):
    tg_user = update.effective_user
    session = SessionLocal()
    user = session.query(User).filter_by(tg_id=tg_user.id).first()
    if not user:
        user = User(tg_id=tg_user.id, username=tg_user.username)
        session.add(user)
        session.commit()
    session.close()
    
    update.message.reply_text(
        "Salom! Botga xush kelibsiz.\nQuyidagi menyudan xizmat tanlang:",
        reply_markup=main_menu()
    )

# Inline tugma bosilganda xizmat tanlash
def service_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data['selected_service'] = query.data
    query.message.reply_text("Iltimos, xizmat linkini kiriting:")
    return ENTER_LINK

def enter_link(update: Update, context: CallbackContext):
    context.user_data['link'] = update.message.text
    update.message.reply_text("Iltimos, kerakli miqdorni kiriting (1000 dona = 1 paket):")
    return ENTER_QUANTITY

def enter_quantity(update: Update, context: CallbackContext):
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            raise ValueError
        context.user_data['quantity'] = quantity

        # Hisoblash narxi
        session = SessionLocal()
        service_name = context.user_data['selected_service'].replace('service_', '')
        service = session.query(Service).filter(Service.name.ilike(f"%{service_name}%"), Service.active==True).first()
        if not service:
            update.message.reply_text("Kechirasiz, tanlangan xizmat mavjud emas.")
            session.close()
            return ConversationHandler.END

        total_price = calculate_total_price(quantity, service.price_1000)
        context.user_data['total_price'] = total_price
        session.close()

        update.message.reply_text(
            f"Buyurtma tafsiloti:\nXizmat: {service.name}\nMiqdor: {quantity}\nNarx: {format_currency(total_price)}\n\nTasdiqlaysizmi? (ha/yo'q)"
        )
        return CONFIRM_ORDER
    except ValueError:
        update.message.reply_text("Iltimos, to‘g‘ri raqam kiriting.")
        return ENTER_QUANTITY

def confirm_order(update: Update, context: CallbackContext):
    answer = update.message.text.lower()
    if answer == 'ha':
        session = SessionLocal()
        user = session.query(User).filter_by(tg_id=update.effective_user.id).first()
        service_name = context.user_data['selected_service'].replace('service_', '')
        service = session.query(Service).filter(Service.name.ilike(f"%{service_name}%")).first()
        if user.balance < context.user_data['total_price']:
            update.message.reply_text("Balansingiz yetarli emas.")
            session.close()
            return ConversationHandler.END

        # Balansni yechish
        user.balance -= context.user_data['total_price']

        # Buyurtma yaratish
        order_id = generate_order_id()
        order = Order(
            order_id=order_id,
            user_id=user.id,
            service_id=service.id,
            link=context.user_data['link'],
            quantity=context.user_data['quantity'],
            total_price=context.user_data['total_price']
        )
        session.add(order)
        session.commit()
        session.close()

        update.message.reply_text(f"Buyurtma qabul qilindi! ID: {order_id}\nAdmin buyurtmani tekshiradi va statusni yangilaydi.")
        # Adminga xabar yuborish
        context.bot.send_message(
            chat_id=ADMIN_TG_ID,
            text=f"Yangi buyurtma qabul qilindi:\nUser: @{update.effective_user.username}\nID: {order_id}\nXizmat: {service.name}\nLink: {context.user_data['link']}\nMiqdor: {context.user_data['quantity']}\nNarx: {format_currency(context.user_data['total_price'])}"
        )
        return ConversationHandler.END
    else:
        update.message.reply_text("Buyurtma bekor qilindi.")
        return ConversationHandler.END
