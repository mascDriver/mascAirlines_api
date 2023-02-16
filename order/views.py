from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from order import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

router_order = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_order.post("/order/", response_model=schemas.Order, tags=['Order'])
async def create_route(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_db_order(db=db, order=order)


@router_order.get("/order/{order_id}", response_model=schemas.Order, tags=['Order'])
async def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
