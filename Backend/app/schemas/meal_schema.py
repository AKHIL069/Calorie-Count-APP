from pydantic import BaseModel
from datetime import datetime

class MealOut(BaseModel):
    id: int
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    protein: float
    fat: float
    carbs: float
    created_at: datetime

    class Config:
        orm_mode = True
