from pydantic import BaseModel


class Uf(BaseModel):
    id: int
    name: str
    abbreviation: str

    class Config:
        orm_mode = True


class City(BaseModel):
    id: int | None
    name: str | None
    uf: Uf | None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class User(UserBase):
    password: str

    class Config:
        orm_mode = True


class Consumer(BaseModel):
    user: User
    city_id: int
    cellphone: int
    address: str
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
    cellphone: int
    address: str
    city: City | None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    password: str | None = None
