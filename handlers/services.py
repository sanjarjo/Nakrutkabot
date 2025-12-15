from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.crud import get_categories, get_services_by_category

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
