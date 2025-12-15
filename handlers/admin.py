from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from keyboards.reply import admin_menu
from utils.helpers import is_admin
from database.db import SessionLocal
from database.models import Category, Service

ADMIN_ADD_CATEGORY = 1
ADMIN_ADD_SERVICE = 2


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "👨‍💼 Admin panel",
        reply_markup=admin_menu()
    )


# ➕ KATEGORIYA QO‘SHISH
async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    name = update.message.text
    db = SessionLocal()
    db.add(Category(name=name))
    db.commit()
    db.close()

    await update.message.reply_text("✅ Kategoriya qo‘shildi")


# ➕ XIZMAT QO‘SHISH
async def add_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    data = update.message.text.split("|")
    # format: category_id|nomi|narxi|api_service_id

    db = SessionLocal()
    db.add(Service(
        category_id=int(data[0]),
        name=data[1],
        price=float(data[2]),
        api_service_id=int(data[3])
    ))
    db.commit()
    db.close()

    await update.message.reply_text("✅ Xizmat qo‘shildi")
