from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def service_menu():
    keyboard = [
        [InlineKeyboardButton("Instagram", callback_data="service_instagram")],
        [InlineKeyboardButton("Telegram", callback_data="service_telegram")],
        [InlineKeyboardButton("YouTube", callback_data="service_youtube")],
        [InlineKeyboardButton("Bepul xizmatlar", callback_data="service_free")]
    ]
    return InlineKeyboardMarkup(keyboard)
