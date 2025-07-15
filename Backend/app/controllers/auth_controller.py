from sqlalchemy.orm import Session
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def register(self, db: Session, payload: RegisterRequest):
        return self.service.register_user(db, **payload.dict())

    def login(self, db: Session, payload: LoginRequest):
        return self.service.login_user(db, **payload.dict())