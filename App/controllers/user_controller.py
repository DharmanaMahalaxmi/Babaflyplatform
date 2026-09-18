.from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserLogin
from app.services.user_service import UserService
from app.models.user import User

class UserController:
    @staticmethod
    def register(db: Session, user_data: UserRegister):
        return UserService.register_user(db, user_data)

    @staticmethod
    def login(db: Session, login_data: UserLogin):
        return UserService.authenticate_user(db, login_data)

    @staticmethod
    def get_profile(current_user: User):
        return current_user
