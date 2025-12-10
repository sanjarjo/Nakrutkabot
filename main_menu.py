from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    keyboard = [
        [KeyboardButton("🛒 Xizmatlar"), KeyboardButton("💳 Hisobim")],
        [KeyboardButton("📥 To'lov qilish"), KeyboardButton("📦 Buyurtmalarim")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
