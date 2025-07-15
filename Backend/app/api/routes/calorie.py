from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.calorie_schema import CalorieRequest, CalorieResponse
from app.controllers.calorie_controller import CalorieController
from app.core.rate_limiter import limiter
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user_model import User

router = APIRouter()

@router.post("/get-calories", response_model=CalorieResponse)
@limiter.limit("15/minute")
async def get_calories(request: Request, payload: CalorieRequest, db: Session = Depends(get_db),  current_user: User = Depends(get_current_user), controller: CalorieController = Depends()):
    return await controller.get_calories(payload, db=db, current_user=current_user)