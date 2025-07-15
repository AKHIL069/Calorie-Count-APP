import httpx
import os
from dotenv import load_dotenv
load_dotenv()


class USDAAPI:
    BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
    API_KEY = os.getenv("USDA_API_KEY")

    async def search_dish(self, dish_name: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params={
                "query": dish_name,
                "api_key": self.API_KEY,
                "pageSize": 10
            })
            return response.json()