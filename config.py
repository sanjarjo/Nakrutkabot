import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

SMM_API_URL = "https://uzbek-seen.uz/api/v2"
SMM_API_KEY = os.getenv("SMM_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")
ORDER_CHECK_INTERVAL = int(os.getenv("ORDER_CHECK_INTERVAL", 300))  # 5 daqiqa
