from sqlalchemy.orm import Session
import models
import schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def increment_redirect_count(db: Session, redirect: models.Redirect):
    redirect.redirect_count = models.Redirect.redirect_count + 1
    db.commit()

def get_redirects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Redirect).offset(skip).limit(limit).all()

def get_redirect_by_short_str(db: Session, short_str: str):
    return db.query(models.Redirect).filter(models.Redirect.short_str == short_str).first()

def create_user_redirect(db: Session, redirect: schemas.RedirectCreate, user_id: int):
    db_redirect = models.Redirect(**redirect.model_dump(), owner_id=user_id)
    db.add(db_redirect)
    db.commit()
    db.refresh(db_redirect)
    return db_redirect
