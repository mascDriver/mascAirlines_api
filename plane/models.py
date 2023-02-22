from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from db.database import Base


class Plane(Base):
    __tablename__ = "plane"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model = Column(String, index=True)
    tax_business = Column(Float)
    tax_premium = Column(Float)
    is_active = Column(Boolean, default=True)

    seat = relationship("Seat", back_populates="plane")
    route = relationship("Route", back_populates="plane")


class Seat(Base):
    __tablename__ = "seat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(Integer)
    plane_id = Column(Integer, ForeignKey("plane.id"))
    is_available = Column(Boolean, default=True)
    is_business = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_economy = Column(Boolean, default=True)

    plane = relationship("Plane", back_populates="seat")
    order = relationship("Order", back_populates="seat")


class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plane_id = Column(Integer, ForeignKey("plane.id"))
    origin_id = Column(Integer, ForeignKey("city.id"))
    depart = Column(DateTime)
    destiny_id = Column(Integer, ForeignKey("city.id"))
    arrival = Column(DateTime)
    price = Column(Float, index=True)

    origin = relationship("City", foreign_keys=[origin_id])
    destiny = relationship("City", foreign_keys=[destiny_id])
    plane = relationship("Plane", back_populates="route")
    order = relationship("Order", back_populates="route")
