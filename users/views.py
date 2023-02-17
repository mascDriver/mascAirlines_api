from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from users.security import create_access_token, get_current_active_user, get_current_active_seller
from users import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

router_user = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 120


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router_user.post("/consumer/", response_model=schemas.Consumer, tags=['User'])
async def create_consumer(consumer: schemas.Consumer, db: Session = Depends(get_db)):
    db_consumer = crud.get_user_by_email(db, email=consumer.user.email)
    if db_consumer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_consumer(db=db, consumer=consumer)


@router_user.get("/consumer/", response_model=schemas.Consumer, tags=['User'])
async def read_consumer(consumer: schemas.Consumer = Depends(get_current_active_user)):
    if consumer:
        return consumer
    raise HTTPException(status_code=404, detail="User not found")


@router_user.post("/seller/", response_model=schemas.Consumer, tags=['User'])
async def create_seller(seller: schemas.Seller, db: Session = Depends(get_db)):
    db_seller = crud.get_user_by_email(db, email=seller.user.email)
    if db_seller:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_seller(db=db, seller=seller)


@router_user.get("/seller/", response_model=schemas.Seller, tags=['User'])
async def read_seller(seller: schemas.Seller = Depends(get_current_active_seller)):
    if seller:
        return seller
    raise HTTPException(status_code=404, detail="User not found")


@router_user.post("/token", response_model=schemas.Token, tags=['User'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_login(db, form_data.username, form_data.password)
    if not user:
        user = crud.get_login_seller(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
