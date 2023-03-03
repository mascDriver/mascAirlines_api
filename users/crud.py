from sqlalchemy.orm import Session

from users import models, schemas
from users.models import City
from sqlalchemy.sql.functions import ReturnTypeFromArgs, func


def get_consumer(db: Session, consumer_id: int):
    return db.query(models.Consumer).filter(models.Consumer.id == consumer_id).first()


def get_seller(db: Session, seller_id: int):
    return db.query(models.Seller).filter(models.Seller.id == seller_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_consumer_by_email(db: Session, email: str):
    return db.query(models.Consumer).filter(models.Consumer.user.has(email=email)).first()


def get_seller_by_email(db: Session, email: str):
    return db.query(models.Seller).filter(models.Seller.user.has(email=email)).first()


def get_login(db: Session, consumer_email: str, consumer_pass: str):
    return db.query(models.Consumer).filter(
        models.Consumer.user.has(email=consumer_email),
        models.Consumer.user.has(password=consumer_pass)
    ).first()


def get_login_seller(db: Session, consumer_email: str, consumer_pass: str):
    return db.query(models.Seller).filter(
        models.Seller.user.has(email=consumer_email),
        models.Seller.user.has(password=consumer_pass)
    ).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(**user.dict())
    db_user.password = user.password.get_secret_value()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_consumer(db: Session, consumer: schemas.Consumer):
    db_user = create_user(db, user=consumer.user)
    consumer = consumer.dict()
    consumer.pop('user')
    db_consumer = models.Consumer(user_id=db_user.id, **consumer)
    db.add(db_consumer)
    db.commit()
    db.refresh(db_consumer)
    return db_consumer


def create_seller(db: Session, seller: schemas.Seller):
    db_user = create_user(db, user=seller.user)
    db_seller = models.Seller(user_id=db_user.id)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller


class unaccent(ReturnTypeFromArgs):
    pass


def get_city(db: Session, q: str):
    city = db.query(City).filter(unaccent(func.lower(City.name.ilike(f"{q.strip()}")))).all()
    if not city:
        return db.query(City).filter(City.name.ilike(f"{q.strip()}%")).all()
    return city

