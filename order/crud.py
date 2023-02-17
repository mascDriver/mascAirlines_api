from sqlalchemy.orm import Session

from order import models, schemas
from plane.crud import get_seat_by_number, get_route


def create_db_order(db: Session, order: schemas.OrderCreate, consumer):
    route = get_route(db, order.route_id)
    seat = get_seat_by_number(db, number=order.seat_number, plane_id=route.plane_id)
    total = route.price
    if seat.is_business:
        total = route.price + round(route.price * (route.plane.tax_business/100), 2)
    elif seat.is_premium:
        total = route.price + round(route.price * (route.plane.tax_premium/100), 2)
    order = order.dict()
    order.pop('seat_number')
    db_order = models.Order(**order, total=total, consumer_id=consumer.id, seat_id=seat.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.id == order_id).first()
