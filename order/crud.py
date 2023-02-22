from sqlalchemy.orm import Session

from order import models, schemas


def create_db_order(db: Session, order: schemas.OrderCreate, consumer, seat, route):
    total = route.price
    if seat.is_business:
        total = route.price + round(route.price * (route.plane.tax_business/100), 2)
    elif seat.is_premium:
        total = route.price + round(route.price * (route.plane.tax_premium/100), 2)
    order = order.dict()
    order.pop('seat_number')
    db_order = models.Order(**order, total=total, consumer_id=consumer.id, seat_id=seat.id)
    db.add(db_order)
    seat.is_available = False
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_order_by_consumer(db: Session, consumer_id: int):
    return db.query(models.Order).filter(models.Order.consumer_id == consumer_id).all()
