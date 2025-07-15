from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.models.meal_model import Meal
from app.schemas.meal_schema import MealOut

router = APIRouter()

@router.get("/meals", response_model=List[MealOut])
def get_meal_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Meal)\
             .filter(Meal.user_id == current_user.id)\
             .order_by(Meal.created_at.desc())\
             .all()
