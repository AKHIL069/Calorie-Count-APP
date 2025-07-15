from app.database.session import engine
from app.models.user_model import User
from app.models.meal_model import Meal
from app.database.base import Base

def init_db():
    print("Creating tables....")
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()