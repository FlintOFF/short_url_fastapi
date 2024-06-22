from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.responses import RedirectResponse
import functions

from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET = 'your-secret-key'
manager = LoginManager(SECRET, "/login")

@manager.user_loader()
def get_user(email: str):
    with SessionLocal() as db:
        return crud.get_user_by_email(db=db, email=email)

@app.get("/protected")
def protected_route(user=Depends(manager)):
    return {"user": user}

@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = data.username
    password = data.password

    user = crud.get_user_by_email(db=db, email=email)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    elif not functions.compare_password_with_hash(password=password, hashed_password=user.hashed_password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": email})
    return {"access_token": access_token}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/redirects/", response_model=schemas.Redirect)
def create_redirect_for_user(user_id: int, redirect: schemas.RedirectCreate, db: Session = Depends(get_db), user=Depends(manager)):
    return crud.create_user_redirect(db=db, redirect=redirect, user_id=user_id)

@app.get("/{short_str}")
def read_item(short_str: str, db: Session = Depends(get_db)):
    redirect = crud.get_redirect_by_short_str(db=db, short_str=short_str)
    if not redirect:
        raise HTTPException(status_code=404, detail="Redirect not found")
    else:
        crud.increment_redirect_count(db=db, redirect=redirect)
        return RedirectResponse(redirect.url)    
