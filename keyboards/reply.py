from telegram import ReplyKeyboardMarkup

def admin_menu():
    return ReplyKeyboardMarkup(
        [
            ["➕ Kategoriya qo‘shish", "➕ Xizmat qo‘shish"],
            ["📦 Buyurtmalar", "📥 To‘lovlar"]
        ],
        resize_keyboard=True
    )
