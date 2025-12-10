import random
from config import ORDER_ID_LENGTH

def generate_order_id(length=ORDER_ID_LENGTH):
    """8 raqamli random buyurtma ID yaratadi"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def calculate_total_price(quantity, price_per_1000):
    """
    Buyurtma narxini hisoblaydi
    Narx 1000 dona uchun berilgan
    """
    total = (quantity / 1000) * price_per_1000
    return round(total, 2)  # ikki raqamgacha yaxlitlash

def format_currency(amount):
    """Summani o'zbek so'miga formatlaydi"""
    return f"{int(amount):,} so'm".replace(',', ' ')
