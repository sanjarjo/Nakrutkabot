import random
from config import ORDER_ID_LENGTH

def generate_order_id(length=ORDER_ID_LENGTH):
    return ''.join(str(random.randint(0,9)) for _ in range(length))

def calculate_total_price(quantity, price_per_1000):
    total = (quantity / 1000) * price_per_1000
    return round(total, 2)

def format_currency(amount):
    try:
        a = int(amount)
        return f"{a:,}".replace(",", " ") + " so'm"
    except:
        return f"{amount} so'm"
