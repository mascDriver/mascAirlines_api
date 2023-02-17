from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from order import models, schemas, crud
from users import schemas as schemas_users, security as security_user

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
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db),
                       consumer: schemas_users.Consumer = Depends(security_user.get_current_active_user)
                       ):
    return crud.create_db_order(db=db, order=order, consumer=consumer)


@router_order.get("/order/{order_id}", response_model=schemas.Order, tags=['Order'])
async def read_order(order_id: str, db: Session = Depends(get_db),
                     consumer: schemas_users.Consumer = Depends(security_user.get_current_active_user)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order.consumer.id != consumer.id:
        raise HTTPException(status_code=404, detail="Order for user not found")
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
