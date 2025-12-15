from telegram import Update
from telegram.ext import ContextTypes
from database.db import SessionLocal
from database.models import Service

async def service_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    service_id = int(query.data.split("_")[1])

    db = SessionLocal()
    service = db.query(Service).get(service_id)
    db.close()

    context.user_data["service_id"] = service_id

    await query.message.reply_text(
        f"📦 Xizmat: {service.name}\n"
        f"💰 Narx: {service.price}\n\n"
        f"🔗 Havolani yuboring:"
    )
