from pydantic import BaseModel


class MacronutrientInfo(BaseModel):
    protein_g: float
    fat_g: float
    carbs_g: float


class CalorieRequest(BaseModel):
    dish_name: str
    servings: int


class CalorieResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    macronutrients: MacronutrientInfo
    source: str
