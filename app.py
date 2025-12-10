from flask import Flask, request
from telegram import Bot, Update
from config import BOT_TOKEN
from bot import main  # Agar polling bilan ishlashni xohlasa

app = Flask(__name__)
bot = Bot(BOT_TOKEN)

@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    # Dispatcher handlerlari orqali update ni ishlatish
    # Agar bot polling emas, webhook bilan ishlasa, quyidagi kodni ishlatish kerak
    from bot import main  # dispatcher import qilinadi
    main()  # webhook bilan ishlash uchun moslashtirish kerak
    return 'ok'

@app.route('/')
def index():
    return "SMM Bot ishlayapti!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
