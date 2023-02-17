from pydantic import BaseModel
from datetime import datetime


class Plane(BaseModel):
    id: int | None
    model: str
    tax_business: float
    tax_premium: float

    class Config:
        orm_mode = True


class SeatBase(BaseModel):
    id: int | None
    is_business: bool | None
    is_premium: bool | None
    is_economy: bool | None


class SeatCreate(SeatBase):
    plane_id: int | None

    class Config:
        orm_mode = True


class Seat(SeatBase):
    plane: Plane | None
    number: int

    class Config:
        orm_mode = True


class RouteBase(BaseModel):
    id: int | None
    origin: str
    depart: datetime
    destiny: str
    arrival: datetime
    price: float


class RouteCreate(RouteBase):
    plane_id: int | None

    class Config:
        orm_mode = True


class Route(RouteBase):
    plane: Plane | None

    class Config:
        orm_mode = True
