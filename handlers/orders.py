from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database.db import SessionLocal
from database.models import Service, Order, User
from utils.smm_api import create_order

# 1️⃣ LINK QABUL QILISH
async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    context.user_data["link"] = link

    await update.message.reply_text(
        "📊 Miqdorni kiriting:\n"
        "Masalan: 1000"
    )


# 2️⃣ MIQDOR QABUL QILISH + ORDER
async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quantity = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Faqat raqam kiriting")
        return

    service_id = context.user_data.get("service_id")
    link = context.user_data.get("link")
    tg_id = update.effective_user.id

    db = SessionLocal()
    service = db.query(Service).get(service_id)
    user = db.query(User).filter_by(tg_id=tg_id).first()

    total_price = service.price * quantity

    if user.balance < total_price:
        await update.message.reply_text(
            "❌ Balansingiz yetarli emas\n"
            "💳 To‘lov qilib balansni to‘ldiring"
        )
        db.close()
        return

    # 🔌 API ga ORDER
    api_response = create_order(
        service_id=service.api_service_id,
        link=link,
        quantity=quantity
    )

    if "order" not in api_response:
        await update.message.reply_text(
            "❌ API xatosi\n"
            f"{api_response}"
        )
        db.close()
        return

    # 💾 DB ga yozamiz
    user.balance -= total_price

    order = Order(
        user_id=user.id,
        service_id=service.id,
        link=link,
        quantity=quantity,
        api_order_id=api_response["order"],
        status="processing"
    )

    db.add(order)
    db.commit()
    db.close()

    await update.message.reply_text(
        "✅ Buyurtma qabul qilindi!\n\n"
        f"🆔 Order ID: {api_response['order']}\n"
        f"📦 Xizmat: {service.name}\n"
        f"📊 Miqdor: {quantity}\n"
        f"🔄 Status: Jarayonda"
    )
