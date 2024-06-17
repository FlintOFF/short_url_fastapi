from typing import Union
from pydantic import BaseModel, Field, HttpUrl
import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class RedirectBase(BaseModel):
    short_str: str = Field(default_factory=id_generator)
    url: str # TODO: HttpUrl
    redirect_count: int = 0

class RedirectCreate(RedirectBase):
    pass

class Redirect(RedirectBase):
    id: int
    owner_id: int

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
