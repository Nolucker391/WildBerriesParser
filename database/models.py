from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserProduct(Base):
    """Модель артикулов юзера."""

    __tablename__ = "user_products"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    article = Column(String(20), nullable=False)
    product_name = Column(String(255), nullable=False)
    root_id = Column(Integer, nullable=False)

    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")


class Review(Base):
    """Модель отзывов артикула."""

    __tablename__ = "reviews"

    id = Column(String(64), primary_key=True)
    product_id = Column(Integer, ForeignKey("user_products.id", ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)
    text = Column(Text)
    advantages = Column(Text)
    disadvantages = Column(Text)
    author = Column(String(100))
    created_at = Column(DateTime)

    product = relationship("UserProduct", back_populates="reviews")
