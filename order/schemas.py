from datetime import datetime

from pydantic import BaseModel, Field

from plane.schemas import Route, Seat
from users.schemas import ConsumerResponse, SellerResponse


class OrderCreate(BaseModel):
    seller_id: int = Field(example=1)
    route_id: int = Field(example=1)
    seat_number: int = Field(example=1)

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: str | None
    consumer: ConsumerResponse
    seller: SellerResponse
    route: Route
    seat: Seat
    total: float
    order_date: datetime

    class Config:
        orm_mode = True
