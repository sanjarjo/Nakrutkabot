from database.db import engine, Base
from database.models import *

def init_db():
    # PostgreSQL’da ham ishlaydi, barcha jadvallarni yaratadi
    Base.metadata.create_all(bind=engine)
