from fastapi import HTTPException, status
from app.utils.usda import USDAAPI
from app.utils.fuzzy_matcher import FuzzyMatcher


class CalorieService:
    def __init__(self):
        self.usda_api = USDAAPI()
        self.matcher = FuzzyMatcher()

    async def get_calorie_info(self, dish_name: str, servings: int):
        if servings <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid servings. Must be greater than zero."
            )

        search_results = await self.usda_api.search_dish(dish_name)
        items = search_results.get("foods", [])

        if not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dish not found in USDA database. Try a more common or clear name."
            )

        best_match, suggestions = self.matcher.find_best_match(dish_name, items)
        if not best_match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not confidently match dish. Did you mean: {', '.join(suggestions)}?"
            )

        food_nutrients = best_match.get("foodNutrients", [])
        calories = protein = fat = carbs = 0.0

        for nutrient in food_nutrients:
            name = nutrient.get("nutrientName", "").lower()
            unit = nutrient.get("unitName", "").lower()
            value = nutrient.get("value", 0)

            if "energy" in name and unit == "kcal":
                calories = value
            elif "protein" in name and unit == "g":
                protein = value
            elif ("fat" in name or "lipid" in name) and unit == "g":
                fat = value
            elif "carbohydrate" in name and unit == "g":
                carbs = value

        if calories == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Calorie data not available for the matched dish."
            )

        return {
            "dish_name": best_match.get("description", dish_name),
            "servings": servings,
            "calories_per_serving": calories,
            "total_calories": calories * servings,
            "macronutrients": {
                "protein_g": protein * servings,
                "fat_g": fat * servings,
                "carbs_g": carbs * servings
            },
            "source": "USDA FoodData Central"
        }
