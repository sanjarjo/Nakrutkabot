from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.crud import get_categories, get_services_by_category
from database.db import SessionLocal
from database.models import Service


async def services_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = get_categories()

    buttons = [
        [InlineKeyboardButton(c.name, callback_data=f"cat_{c.id}")]
        for c in categories
    ]

    await update.message.reply_text(
        "🛒 Kategoriyani tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def services_by_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cat_id = int(query.data.split("_")[1])
    services = get_services_by_category(cat_id)

    buttons = [
        [InlineKeyboardButton(
            f"{s.name} - {s.price} so‘m",
            callback_data=f"service_{s.id}"
        )]
        for s in services
    ]

    await query.message.edit_text(
        "📌 Xizmatni tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 🔥 MANA ENG MUHIM QISM
async def service_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    service_id = int(query.data.split("_")[1])

    # xotirada saqlab qo‘yamiz
    context.user_data["service_id"] = service_id

    # xizmatni DB dan olib ko‘rsatamiz
    db = SessionLocal()
    service = db.query(Service).get(service_id)
    db.close()

    await query.message.reply_text(
        f"📦 Xizmat: {service.name}\n"
        f"💰 Narx (1 dona): {service.price} so‘m\n\n"
        "🔗 Iltimos, havolani yuboring:\n"
        "Masalan: https://instagram.com/username"
  )

# xizmat tanlanganda
context.user_data["service_id"] = service_id

await query.message.reply_text(
    "🔗 Iltimos, havolani yuboring:\n"
    "Masalan: https://instagram.com/username"
    )
