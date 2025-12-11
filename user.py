from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards.main_menu import main_menu
from keyboards.service_menu import service_menu
from assets import stickers
from database.db import SessionLocal, init_db
from database.models import User, Service, Order
from utils.helpers import generate_order_id, calculate_total_price, format_currency
from utils.api import create_order_panel

SELECT_SERVICE, ENTER_LINK, ENTER_QTY, CONFIRM = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_db()
    session = SessionLocal()
    tg = update.effective_user
    user = session.query(User).filter_by(tg_id=tg.id).first()
    if not user:
        user = User(tg_id=tg.id, username=tg.username)
        session.add(user)
        session.commit()
    session.close()

    # sticker + menu
    await update.message.reply_sticker(open(stickers.WELCOME, 'rb'))
    await update.message.reply_text(
        f"Assalomu alaykum, {tg.first_name}!\nXizmatni tanlang:",
        reply_markup=main_menu()
    )

async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xizmatlar:", reply_markup=service_menu())
    return SELECT_SERVICE

async def service_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service_key = query.data  # e.g. service_instagram
    context.user_data['service_key'] = service_key
    # send sticker for chosen category
    if 'instagram' in service_key:
        await query.message.reply_sticker(open(stickers.INSTAGRAM, 'rb'))
    elif 'telegram' in service_key:
        await query.message.reply_sticker(open(stickers.TELEGRAM, 'rb'))
    elif 'youtube' in service_key:
        await query.message.reply_sticker(open(stickers.YOUTUBE, 'rb'))
    else:
        await query.message.reply_sticker(open(stickers.FREE_SERVICE, 'rb'))

    await query.message.reply_text("Iltimos, linkni yuboring:")
    return ENTER_LINK

async def enter_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['link'] = update.message.text.strip()
    await update.message.reply_text("Miqdorni kiriting (butun son):")
    return ENTER_QTY

async def enter_qty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        qty = int(update.message.text.strip())
        if qty <= 0:
            raise ValueError
        context.user_data['quantity'] = qty

        # find selected service in DB by partial name
        session = SessionLocal()
        skey = context.user_data.get('service_key', 'service_instagram')
        service_name = skey.replace('service_','')
        service = session.query(Service).filter(Service.name.ilike(f"%{service_name}%"), Service.active==True).first()
        if not service:
            await update.message.reply_text("Kechirasiz, tanlangan xizmat topilmadi. Admin bilan bog‘laning.")
            session.close()
            return ConversationHandler.END

        total = calculate_total_price(qty, service.price_1000)
        context.user_data['total'] = total
        context.user_data['service_id'] = service.id

        await update.message.reply_text(
            f"Buyurtma:\nXizmat: {service.name}\nMiqdor: {qty}\nNarx: {format_currency(total)}\n\nTasdiqlaysizmi? (ha/yo'q)"
        )
        session.close()
        return CONFIRM
    except ValueError:
        await update.message.reply_text("Iltimos, to‘g‘ri butun son kiriting.")
        return ENTER_QTY

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip().lower()
    if txt not in ['ha', 'yes', 'y']:
        await update.message.reply_text("Buyurtma bekor qilindi.")
        return ConversationHandler.END

    session = SessionLocal()
    tg = update.effective_user
    user = session.query(User).filter_by(tg_id=tg.id).first()
    if not user:
        await update.message.reply_text("Ro'yxatdan o'tmagan foydalanuvchi.")
        session.close()
        return ConversationHandler.END

    total = context.user_data.get('total', 0)
    if user.balance < total:
        await update.message.reply_text("Balansingiz yetarli emas. To'lov bo'limidan yuboring yoki admin bilan bog'laning.")
        session.close()
        return ConversationHandler.END

    # yechish
    user.balance -= total

    # create order in DB
    order_id = generate_order_id()
    service = session.query(Service).get(context.user_data['service_id'])
    order = Order(
        order_id=order_id,
        user_id=user.id,
        service_id=service.id,
        link=context.user_data['link'],
        quantity=context.user_data['quantity'],
        total_price=total,
        status='pending'
    )
    session.add(order)
    session.commit()

    # send to panel (non-blocking simple call)
    panel_resp = create_order_panel(service.panel_service_id, order.link, order.quantity)
    if panel_resp.get('error'):
        # store error in panel_order_id or status
        order.panel_order_id = None
        order.status = 'error'
        session.commit()
        await update.message.reply_sticker(open(stickers.ERROR, 'rb'))
        await update.message.reply_text("Panelga yuborishda xatolik yuz berdi, admin tekshiradi.")
    else:
        # typical response may include 'order'
        panel_order_id = panel_resp.get('order') or panel_resp.get('id') or None
        if panel_order_id:
            order.panel_order_id = str(panel_order_id)
            order.status = 'processing'
            session.commit()
            await update.message.reply_sticker(open(stickers.ORDER_RECEIVED, 'rb'))
            await update.message.reply_text(f"Buyurtma qabul qilindi! ID: {order.order_id}")
        else:
            order.status = 'pending'
            session.commit()
            await update.message.reply_text("Buyurtma qabul qilindi, admin tekshiradi.")
    # notify admin
    from config import ADMIN_TG_ID
    if ADMIN_TG_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_TG_ID,
                text=(
                    f"Yangi buyurtma:\nUser: @{tg.username}\nID: {order.order_id}\n"
                    f"Xizmat: {service.name}\nLink: {order.link}\nMiqdor: {order.quantity}\nNarx: {format_currency(total)}"
                )
            )
        except Exception:
            pass

    session.close()
    return ConversationHandler.END
