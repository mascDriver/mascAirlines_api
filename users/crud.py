from sqlalchemy.orm import Session

from users import models, schemas


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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_consumer(db: Session, consumer: schemas.Consumer):
    db_user = create_user(db, user=consumer.user)
    db_consumer = models.Consumer(user_id=db_user.id)
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


# import httpx
# from users.models import Uf
# from sqlalchemy.orm import Session
#
# db = Session
# ufs = []
# for uf in httpx.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados').json():
#     ufs.append(Uf(id=uf['id'], abbreviation=uf['sigla'], name=uf['nome']))
