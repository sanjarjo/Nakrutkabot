from database.db import SessionLocal
from database.models import User, Category, Service, Order

def get_or_create_user(tg_id: int):
    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=tg_id).first()

    if not user:
        user = User(tg_id=tg_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    db.close()
    return user


def get_categories():
    db = SessionLocal()
    data = db.query(Category).all()
    db.close()
    return data


def get_services_by_category(cat_id: int):
    db = SessionLocal()
    data = db.query(Service).filter_by(category_id=cat_id).all()
    db.close()
    return data
