from db import Base,User
from fastapi import Depends
from sqlalchemy.orm import Session

def check_user_google(db: Session, google_auth_details: dict):
    db_user = db.query(User).filter(User.google_id == google_auth_details["google_id"]).first()
    return db_user
def check_user_google_by_id(db: Session, google_auth_id: str):
    db_user = db.query(User).filter(User.google_id == google_auth_id).first()
    return db_user
def insert_new_google_user(db: Session, google_auth_details: dict):
    new_user = User(**google_auth_details)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True



#Normal authentication
def get_user_by_id(db:Session,email:str):
    db_user=db.query(User).filter(User.email==email).first()
    return db_user
def get_user_by_google_id(db:Session,email:str):
    db_user=db.query(User).filter(User.email==email).first()
    return db_user
def create_user_normal_auth(db:Session,user_details:dict):
    new_user=User(**user_details)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True