from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from app.controllers.auth_controller import AuthController
from app.database.session import get_db

router = APIRouter()
controller = AuthController()

@router.post("/register", response_model=TokenResponse)
def register_user(payload: RegisterRequest, db=Depends(get_db)):
    try:
        user = controller.register(db, payload)
        token = controller.login(db, LoginRequest(email=payload.email, password=payload.password))
        return {"access_token": token["access_token"]}
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest, db=Depends(get_db)):
    try:
        return controller.login(db, payload)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
