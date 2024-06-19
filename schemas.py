from typing import Union
from pydantic import BaseModel, Field, HttpUrl

class RedirectBase(BaseModel):
    url: str # TODO: HttpUrl

class RedirectCreate(RedirectBase):
    pass

class Redirect(RedirectBase):
    id: int
    owner_id: int
    short_str: str
    redirect_count: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    redirects: list[Redirect] = []

    class Config:
        orm_mode = True
