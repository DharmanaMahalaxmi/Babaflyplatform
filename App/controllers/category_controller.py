from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate
from app.services.category_service import CategoryService

class CategoryController:
    @staticmethod
    def get_all(db: Session):
        return CategoryService.get_all(db)

    @staticmethod
    def get_products_by_category(db: Session, category_id: int):
        return CategoryService.get_category_products(db, category_id)

    @staticmethod
    def create(db: Session, data: CategoryCreate):
        return CategoryService.create_category(db, data)
