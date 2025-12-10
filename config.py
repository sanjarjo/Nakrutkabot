import os

# Telegram Bot Token (environment variable orqali)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# SMM Panel API
SMM_API_URL = 'https://uzbek-seen.uz/api/v2'
SMM_API_KEY = os.getenv('SMM_API_KEY')  # API kalit environment orqali

# Admin Telegram ID
ADMIN_TG_ID = int(os.getenv('ADMIN_TG_ID'))

# To'lov karta raqami (environment orqali)
ADMIN_CARD_NUMBER = os.getenv('ADMIN_CARD_NUMBER')

# Database URL (PostgreSQL yoki SQLite)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database.db')

# Buyurtma ID uzunligi
ORDER_ID_LENGTH = 8
