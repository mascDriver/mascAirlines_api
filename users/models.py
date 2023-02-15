from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cellphone = Column(Integer, index=True)
    address = Column(String, index=True)
    password = Column(String)

    consumer = relationship("Consumer", back_populates="user")
    seller = relationship("Seller", back_populates="user")


class Consumer(Base):
    __tablename__ = "consumer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="consumer")
    order = relationship("Order", back_populates="consumer")


class Seller(Base):
    __tablename__ = "seller"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="seller")
    order = relationship("Order", back_populates="seller")
