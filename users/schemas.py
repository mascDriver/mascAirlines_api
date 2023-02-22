from pydantic import BaseModel, Field, EmailStr, SecretStr


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
    name: str = Field(example='Diogo')
    last_name: str = Field(example='Silva')
    email: EmailStr = Field(example='diogo@hotmail.com')

    class Config:
        orm_mode = True


class User(UserBase):
    password: SecretStr = Field(example='123')

    class Config:
        orm_mode = True


class Consumer(BaseModel):
    id: int | None = Field(example=1)
    user: User
    city_id: int = Field(example=3550308)
    cellphone: int = Field(example=999999999)
    address: str = Field(example='Avenida Brasil, 777, jd Brasil')
    is_active: bool | None = Field(example=True)

    class Config:
        orm_mode = True


class Seller(BaseModel):
    user: User
    is_active: bool | None = Field(example=True)

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
