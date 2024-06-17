from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def create_redirect_for_user(user_id: int, redirect: schemas.RedirectCreate, db: Session = Depends(get_db)):
    return crud.create_user_redirect(db=db, redirect=redirect, user_id=user_id)

@app.get("/{short_str}")
def read_item(short_str: str, db: Session = Depends(get_db)):
    redirect = crud.get_redirect_by_short_str(db=db, short_str=short_str)
    if not redirect:
        raise HTTPException(status_code=404, detail="Redirect not found")
    else:
        # TODO: increase redirect_count
        return RedirectResponse("https://google.com/")    
