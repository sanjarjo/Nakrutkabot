from telegram import Update
from telegram.ext import CallbackContext
from database.db import SessionLocal
from database.models import Order, User, Service
from utils.api import check_order_status
from utils.helpers import format_currency

def update_order_status(context: CallbackContext):
    """
    Buyurtmalar statusini tekshiradi va foydalanuvchiga xabar yuboradi
    """
    session = SessionLocal()
    orders = session.query(Order).filter(Order.status != 'completed').all()

    for order in orders:
        if not order.panel_order_id:
            continue  # panel order ID hali berilmagan

        status_response = check_order_status(order.panel_order_id)
        if status_response['success']:
            new_status = status_response['status']
            if order.status != new_status:
                order.status = new_status
                session.commit()
                # Foydalanuvchiga xabar yuborish
                context.bot.send_message(
                    chat_id=order.user.tg_id,
                    text=f"Buyurtma ID: {order.order_id}\n"
                         f"Xizmat: {order.service.name}\n"
                         f"Status yangilandi: {new_status}"
                )
    session.close()

def get_user_orders(tg_id):
    """
    Foydalanuvchining barcha buyurtmalarini qaytaradi
    """
    session = SessionLocal()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    if not user:
        session.close()
        return []

    orders_data = []
    for order in user.orders:
        orders_data.append({
            'order_id': order.order_id,
            'service': order.service.name,
            'quantity': order.quantity,
            'total_price': format_currency(order.total_price),
            'status': order.status
        })
    session.close()
    return orders_data
