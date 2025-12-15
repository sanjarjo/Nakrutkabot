from database.db import SessionLocal
from database.models import Order
from utils.smm_api import order_status


async def check_orders(context):
    db = SessionLocal()

    orders = db.query(Order).filter(
        Order.status.in_(["processing", "pending"])
    ).all()

    for order in orders:
        api = order_status(order.api_order_id)

        if "status" not in api:
            continue

        new_status = api["status"]

        if new_status != order.status:
            order.status = new_status
            db.commit()

            # foydalanuvchiga xabar
            try:
                await context.bot.send_message(
                    chat_id=order.user_id,
                    text=(
                        "📦 Buyurtma holati yangilandi!\n\n"
                        f"🆔 Order ID: {order.api_order_id}\n"
                        f"🔄 Yangi status: {new_status}"
                    )
                )
            except:
                pass

    db.close()
