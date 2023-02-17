from sqlalchemy.orm import Session

from order import models, schemas
from plane.crud import get_plane, get_seat, get_route


def create_db_order(db: Session, order: schemas.OrderCreate, consumer):
    seat = get_seat(db, order.seat_id)
    plane = get_plane(db, seat.plane_id)
    route = get_route(db, order.route_id)
    total = route.price
    if seat.is_business:
        total = route.price + round(route.price * (plane.tax_business/100), 2)
    elif seat.is_premium:
        total = route.price + round(route.price * (plane.tax_premium/100), 2)
    db_order = models.Order(**order.dict(), total=total, consumer_id=consumer.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.id == order_id).first()
