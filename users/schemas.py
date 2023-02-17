from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    last_name: str
    email: str
    cellphone: int
    address: str

    class Config:
        orm_mode = True


class User(UserBase):
    password: str

    class Config:
        orm_mode = True


class Consumer(BaseModel):
    user: User
    is_active: bool | None

    class Config:
        orm_mode = True


class Seller(BaseModel):
    user: User
    is_active: bool | None

    class Config:
        orm_mode = True


class SellerResponse(BaseModel):
    user: UserBase

    class Config:
        orm_mode = True


class ConsumerResponse(BaseModel):
    user: UserBase

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    password: str | None = None
