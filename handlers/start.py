from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🛒 Xizmatlar", "👤 Hisobim"],
        ["💳 To‘lov qilish", "📦 Buyurtmalarim"]
    ]

    await update.message.reply_text(
        "👋 Assalomu alaykum!\nSMM botga xush kelibsiz 🚀",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

start_handler = CommandHandler("start", start)
