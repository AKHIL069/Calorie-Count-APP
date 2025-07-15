from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def register_user(self, db: Session, first_name: str, last_name: str, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if user:
            raise ValueError("User already exists")

        hashed = hash_password(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hashed
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def login_user(self, db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid Credentials")

        token = create_access_token({"sub": user.email})
        return {"access_token": token}