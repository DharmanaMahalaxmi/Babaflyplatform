from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService

class ProductController:
    @staticmethod
    def get_all(
        db: Session,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        metal: Optional[str] = None,
        polish: Optional[str] = None,
        sort: Optional[str] = "latest",
        page: int = 1,
        limit: int = 10,
    ):
        return ProductService.get_products(
            db=db,
            price_min=price_min,
            price_max=price_max,
            metal=metal,
            polish=polish,
            sort=sort,
            page=page,
            limit=limit,
        )

    @staticmethod
    def get_one(db: Session, product_id: int):
        return ProductService.get_by_id(db, product_id)

    @staticmethod
    def create(db: Session, data: ProductCreate):
        return ProductService.create_product(db, data)

    @staticmethod
    def update(db: Session, product_id: int, data: ProductUpdate):
        return ProductService.update_product(db, product_id, data)

    @staticmethod
    def delete(db: Session, product_id: int):
        return ProductService.delete_product(db, product_id)
