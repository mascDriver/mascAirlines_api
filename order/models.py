from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship

from db.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumer.id"))
    seller_id = Column(Integer, ForeignKey("seller.id"))
    route_id = Column(Integer, ForeignKey("route.id"))
    seat_id = Column(Integer, ForeignKey("seat.id"))
    total = Column(Float, index=True)
    order_date = Column(DateTime, default=datetime.now())

    consumer = relationship("Consumer", back_populates="order")
    route = relationship("Route", back_populates="order")
    seller = relationship("Seller", back_populates="order")
    seat = relationship("Seat", back_populates="order")
