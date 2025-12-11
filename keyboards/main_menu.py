from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["🛒 Xizmatlar", "💳 Hisobim"],
        ["📥 To'lov qilish", "📦 Buyurtmalarim"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
