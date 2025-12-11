from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def service_menu():
    keyboard = [
        [InlineKeyboardButton("📷 Instagram", callback_data="cat_instagram")],
        [InlineKeyboardButton("✈️ Telegram", callback_data="cat_telegram")],
        [InlineKeyboardButton("▶️ YouTube", callback_data="cat_youtube")],
        [InlineKeyboardButton("🎁 Bepul xizmatlar", callback_data="cat_free")],
    ]
    return InlineKeyboardMarkup(keyboard)
