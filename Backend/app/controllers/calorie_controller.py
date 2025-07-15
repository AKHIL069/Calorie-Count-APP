from fastapi import Depends
from sqlalchemy.orm import Session

from app.schemas.calorie_schema import CalorieRequest
from app.services.calorie_service import CalorieService
from app.models.meal_model import Meal
from app.models.user_model import User
from app.database.session import get_db
from app.core.security import get_current_user

class CalorieController:
    def __init__(self):
        self.service = CalorieService()

    async def get_calories(self, payload: CalorieRequest,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        try:
            response =  await self.service.get_calorie_info(
                dish_name=payload.dish_name,
                servings=payload.servings
            )

            meal = Meal(
                user_id=current_user.id,
                dish_name=response["dish_name"],
                servings=response["servings"],
                calories_per_serving=response["calories_per_serving"],
                total_calories=response["total_calories"],
                protein=response["macronutrients"]["protein_g"],
                fat=response["macronutrients"]["fat_g"],
                carbs=response["macronutrients"]["carbs_g"],
            )
            db.add(meal)
            db.commit()
            db.refresh(meal)

            return response
        except ValueError as ex:
            return {"error": str(ex)}