from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from users import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

router_user = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_user.post("/consumer/", response_model=schemas.Consumer)
async def create_consumer(consumer: schemas.Consumer, db: Session = Depends(get_db)):
    db_consumer = crud.get_user_by_email(db, email=consumer.user.email)
    if db_consumer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_consumer(db=db, consumer=consumer)


@router_user.get("/consumer/{consumer_id}", response_model=schemas.Consumer)
async def read_consumer(consumer_id: int, db: Session = Depends(get_db)):
    db_consumer = crud.get_consumer(db, consumer_id=consumer_id)
    if db_consumer is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_consumer


@router_user.post("/seller/", response_model=schemas.Consumer)
async def create_seller(seller: schemas.Seller, db: Session = Depends(get_db)):
    db_seller = crud.get_user_by_email(db, email=seller.user.email)
    if db_seller:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_seller(db=db, seller=seller)


@router_user.get("/seller/{seller_id}", response_model=schemas.Seller)
async def read_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = crud.get_seller(db, seller_id=seller_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_seller
