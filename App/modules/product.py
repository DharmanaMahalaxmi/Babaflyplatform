from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from app.config.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), index=True, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    rating = Column(Float, default=4.5, nullable=False)
    metalType = Column(String(50), index=True, nullable=False)    # e.g., Gold, Silver, Platinum, Rose Gold
    polishType = Column(String(50), index=True, nullable=False)   # e.g., High Polish, Matte, Antique, Glossy
    imageUrl = Column(String(500), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
