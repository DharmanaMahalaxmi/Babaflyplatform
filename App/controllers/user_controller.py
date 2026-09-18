from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.order import OrderCreate
from app.services.order_service import OrderService

class OrderController:
    @staticmethod
    def create(db: Session, order_data: OrderCreate, current_user: User):
        return OrderService.create_order(db, order_data, current_user)

    @staticmethod
    def get_user_orders(db: Session, current_user: User):
        return OrderService.get_user_orders(db, current_user)

    @staticmethod
    def get_by_id(db: Session, order_id: int, current_user: User):
        return OrderService.get_order_by_id(db, order_id, current_user)
