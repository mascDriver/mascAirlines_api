from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.database import SessionLocal
from users.crud import get_consumer_by_email, get_seller_by_email
from users.schemas import Consumer, TokenData, Seller

SECRET_KEY = "4b0c56781e8f8e9e4d82571037cbf2e4b021ea28c6517265cace4935cb2c0a17"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(email=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_consumer_by_email(db, email=token_data.email)

    if user:
        return user

    raise CREDENTIALS_EXCEPTION


async def get_current_seller(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(email=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    user = get_seller_by_email(db, email=token_data.email)

    if user:
        return user

    raise CREDENTIALS_EXCEPTION


async def get_current_active_user(current_user: Consumer = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_seller(current_seller: Seller = Depends(get_current_seller)):
    if not current_seller.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_seller
