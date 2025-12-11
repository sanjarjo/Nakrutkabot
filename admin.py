from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database.db import SessionLocal
from database.models import User, Order, Service
from assets import stickers
from utils.helpers import format_currency
from config import ADMIN_TG_ID

ADMIN_BALANCE, CHECK_ORDER = range(2)

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_TG_ID:
            await update.message.reply_text("Siz admin emassiz!")
            return
        return await func(update, context)
    return wrapper

@admin_only
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Admin panelga xush kelibsiz.\nCommands:\n/add_balance\n/check_order")

@admin_only
async def add_balance_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Foydalanuvchi tg_id ni kiriting:")
    return ADMIN_BALANCE

async def add_balance_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    try:
        tg = int(update.message.text.strip())
        user = session.query(User).filter_by(tg_id=tg).first()
        if not user:
            await update.message.reply_text("Foydalanuvchi topilmadi.")
            session.close()
            return ConversationHandler.END
        context.user_data['user_db_id'] = user.id
        await update.message.reply_text("Summani kiriting (so'm):")
        session.close()
        return ADMIN_BALANCE
    except ValueError:
        await update.message.reply_text("Iltimos faqat raqam kiriting.")
        session.close()
        return ADMIN_BALANCE

async def add_balance_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    try:
        amount = float(update.message.text.strip())
        user = session.query(User).get(context.user_data['user_db_id'])
        user.balance += amount
        session.commit()
        await update.message.reply_sticker(open(stickers.BALANCE_ADDED, 'rb'))
        await update.message.reply_text(f"{user.username} balansiga {format_currency(amount)} qo‘shildi.")
    except Exception as e:
        await update.message.reply_text("Xatolik: " + str(e))
    finally:
        session.close()
        return ConversationHandler.END

@admin_only
async def check_order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tekshiriladigan order_id ni kiriting:")
    return CHECK_ORDER

async def check_order_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    oid = update.message.text.strip()
    order = session.query(Order).filter_by(order_id=oid).first()
    if not order:
        await update.message.reply_text("Order topilmadi.")
        session.close()
        return ConversationHandler.END
    await update.message.reply_text(
        f"Order: {order.order_id}\nUser: @{order.user.username}\nXizmat: {order.service.name}\n"
        f"Link: {order.link}\nQty: {order.quantity}\nNarx: {format_currency(order.total_price)}\nStatus: {order.status}"
    )
    session.close()
    return ConversationHandler.END
