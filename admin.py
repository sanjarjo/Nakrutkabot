from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
from database.db import SessionLocal
from database.models import User, Order
from utils.helpers import format_currency
from config import ADMIN_TG_ID

# Conversation states
ADMIN_BALANCE, ADMIN_CHECK_ORDER = range(2)

def admin_required(func):
    """Faqat admin uchun dekorator"""
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if update.effective_user.id != ADMIN_TG_ID:
            update.message.reply_text("Siz admin emassiz!")
            return
        return func(update, context, *args, **kwargs)
    return wrapper

@admin_required
def start_admin(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Admin panelga xush kelibsiz.\n"
        "/add_balance - Foydalanuvchi balansini qo‘shish\n"
        "/check_order - Buyurtma tekshirish"
    )

# Balans qo‘shish
@admin_required
def add_balance_start(update: Update, context: CallbackContext):
    update.message.reply_text("Foydalanuvchi Telegram ID sini kiriting:")
    return ADMIN_BALANCE

def add_balance_enter(update: Update, context: CallbackContext):
    session = SessionLocal()
    try:
        tg_id = int(update.message.text)
        user = session.query(User).filter_by(tg_id=tg_id).first()
        if not user:
            update.message.reply_text("Bunday foydalanuvchi topilmadi.")
            session.close()
            return ConversationHandler.END

        context.user_data['user_id'] = user.id
        update.message.reply_text(f"Qancha summa qo‘shmoqchisiz? (so‘mda)")
        return ADMIN_BALANCE
    except ValueError:
        update.message.reply_text("Iltimos, to‘g‘ri raqam kiriting.")
        return ADMIN_BALANCE

def add_balance_confirm(update: Update, context: CallbackContext):
    session = SessionLocal()
    try:
        amount = float(update.message.text)
        user = session.query(User).filter_by(id=context.user_data['user_id']).first()
        user.balance += amount
        session.commit()
        update.message.reply_text(f"{user.username} balansiga {format_currency(amount)} qo‘shildi.")
    except ValueError:
        update.message.reply_text("Iltimos, to‘g‘ri summa kiriting.")
    finally:
        session.close()
        return ConversationHandler.END

# Buyurtmani tekshirish
@admin_required
def check_order_start(update: Update, context: CallbackContext):
    update.message.reply_text("Tekshiriladigan buyurtma ID sini kiriting:")
    return ADMIN_CHECK_ORDER

def check_order_enter(update: Update, context: CallbackContext):
    session = SessionLocal()
    order_id = update.message.text.strip()
    order = session.query(Order).filter_by(order_id=order_id).first()
    if not order:
        update.message.reply_text("Bunday buyurtma topilmadi.")
        session.close()
        return ConversationHandler.END

    update.message.reply_text(
        f"Buyurtma tafsiloti:\n"
        f"ID: {order.order_id}\n"
        f"Foydalanuvchi: @{order.user.username}\n"
        f"Xizmat: {order.service.name}\n"
        f"Link: {order.link}\n"
        f"Miqdor: {order.quantity}\n"
        f"Narx: {format_currency(order.total_price)}\n"
        f"Status: {order.status}"
    )
    session.close()
    return ConversationHandler.END
