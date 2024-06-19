from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from functions import id_generator

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    redirects = relationship("Redirect", back_populates="owner")

class Redirect(Base):
    __tablename__ = "redirects"

    id = Column(Integer, primary_key=True)
    short_str = Column(String, index=True, default=id_generator())
    url = Column(String, index=False)
    redirect_count = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="redirects")
