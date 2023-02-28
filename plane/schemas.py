from pydantic import BaseModel, FutureDate, Field
from datetime import datetime, timedelta

from users.schemas import City


class Plane(BaseModel):
    id: int | None = Field(example=1)
    model: str = Field(example='Boeing 737')
    tax_business: float = Field(example=70)
    tax_premium: float = Field(example=20)

    class Config:
        orm_mode = True


class SeatBase(BaseModel):
    id: int | None = Field(example=1)
    is_business: bool | None = Field(example=False)
    is_premium: bool | None = Field(example=False)
    is_economy: bool | None = Field(example=True)


class SeatCreate(SeatBase):
    plane_id: int | None = Field(example=1)

    class Config:
        orm_mode = True


class Seat(SeatBase):
    plane: Plane | None
    number: int
    is_available: bool

    class Config:
        orm_mode = True


class RouteBase(BaseModel):
    depart: datetime = Field(example=datetime.now() + timedelta(hours=1))
    arrival: datetime = Field(example=datetime.now() + timedelta(hours=3))
    price: float = Field(example=280.50)


class RouteCreate(RouteBase):
    destiny_id: int = Field(example=4204202)
    origin_id: int = Field(example=3550308)
    plane_id: int = Field(example=1)

    class Config:
        orm_mode = True


class Route(RouteBase):
    id: int
    plane: Plane | None
    origin: City
    destiny: City

    class Config:
        orm_mode = True
