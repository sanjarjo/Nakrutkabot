import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_TG_ID = int(os.getenv("ADMIN_TG_ID")) if os.getenv("ADMIN_TG_ID") else None
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL", "https://uzbek-seen.uz/api/v2")
ADMIN_CARD_NUMBER = os.getenv("ADMIN_CARD_NUMBER")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
ORDER_ID_LENGTH = int(os.getenv("ORDER_ID_LENGTH", 8))
