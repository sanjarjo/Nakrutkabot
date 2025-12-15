from telegram import Update
from telegram.ext import ContextTypes
from database.db import SessionLocal
from database.models import Order, User


async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=tg_id).first()
    orders = db.query(Order).filter_by(user_id=user.id).order_by(Order.id.desc()).all()
    db.close()

    if not orders:
        await update.message.reply_text("📭 Sizda buyurtmalar yo‘q")
        return

    text = "📦 Buyurtmalarim:\n\n"

    for o in orders[:10]:  # oxirgi 10 ta
        text += (
            f"🆔 {o.api_order_id}\n"
            f"📊 Miqdor: {o.quantity}\n"
            f"🔄 Status: {o.status}\n"
            "────────────\n"
        )

    await update.message.reply_text(text)
