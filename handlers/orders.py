from telegram import Update
from telegram.ext import (
    ContextTypes, ConversationHandler,
    MessageHandler, filters
)
from database.db import SessionLocal
from database.models import Service, Order, User
from utils.smm_api import create_order

LINK, QUANTITY = range(2)


async def ask_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    context.user_data["link"] = link

    await update.message.reply_text(
        "📊 Miqdorni kiriting:\nMasalan: 1000"
    )
    return QUANTITY


async def ask_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quantity = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Faqat raqam kiriting")
        return QUANTITY

    service_id = context.user_data.get("service_id")
    link = context.user_data.get("link")
    tg_id = update.effective_user.id

    # ❗ himoya
    if not service_id or not link:
        await update.message.reply_text("❌ Xatolik, qaytadan xizmat tanlang")
        return ConversationHandler.END

    db = SessionLocal()
    service = db.query(Service).get(service_id)
    user = db.query(User).filter_by(tg_id=tg_id).first()

    total_price = service.price * quantity
    if user.balance < total_price:
        await update.message.reply_text(
            "❌ Balans yetarli emas\n💳 To‘lov qilib balansni to‘ldiring"
        )
        db.close()
        return ConversationHandler.END

    # 🔌 API
    api = create_order(
        service_id=service.api_service_id,
        link=link,
        quantity=quantity
    )

    if "order" not in api:
        await update.message.reply_text(f"❌ API xatosi:\n{api}")
        db.close()
        return ConversationHandler.END

    user.balance -= total_price
    order = Order(
        user_id=user.id,
        service_id=service.id,
        link=link,
        quantity=quantity,
        api_order_id=api["order"],
        status="processing"
    )

    db.add(order)
    db.commit()
    db.close()

    await update.message.reply_text(
        "✅ Buyurtma qabul qilindi!\n\n"
        f"🆔 Order ID: {api['order']}\n"
        f"📦 Xizmat: {service.name}\n"
        f"📊 Miqdor: {quantity}\n"
        f"🔄 Status: Jarayonda"
    )

    # tozalaymiz
    context.user_data.clear()
    return ConversationHandler.END


order_conversation = ConversationHandler(
    entry_points=[
        MessageHandler(filters.TEXT & ~filters.COMMAND, ask_link)
    ],
    states={
        QUANTITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, ask_quantity)
        ],
    },
    fallbacks=[],
    )
