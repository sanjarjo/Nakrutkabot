from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from database.db import SessionLocal
from database.models import Payment

AMOUNT, CHECK = range(2)


async def start_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 To‘lov summasini kiriting:\nMasalan: 50000"
    )
    return AMOUNT


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Faqat raqam kiriting")
        return AMOUNT

    context.user_data["amount"] = amount
    await update.message.reply_text("🧾 Endi чек rasmini yuboring")
    return CHECK


async def get_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id
    tg_id = update.effective_user.id
    amount = context.user_data["amount"]

    db = SessionLocal()
    payment = Payment(
        user_id=tg_id,
        amount=amount,
        status="waiting"
    )
    db.add(payment)
    db.commit()
    db.close()

    # adminga yuboramiz
    await context.bot.send_photo(
        chat_id=context.bot_data["ADMIN_ID"],
        photo=photo,
        caption=(
            "🧾 YANGI TO‘LOV\n\n"
            f"👤 User ID: {tg_id}\n"
            f"💰 Summa: {amount}\n\n"
            "⚠️ Agar to‘g‘ri bo‘lsa admin paneldan balans qo‘shing"
        )
    )

    await update.message.reply_text(
        "✅ To‘lov yuborildi.\n"
        "⏳ Admin tekshiradi va balansni to‘ldiradi"
    )

    context.user_data.clear()
    return ConversationHandler.END
