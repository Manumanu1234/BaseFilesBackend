from sqlalchemy.orm import Session
from db import User, Base,get_db
from fastapi import Depends

class UserService:
    def __init__(self, db: Session=Depends(get_db)):
        self.db = db
        
    def check_user_google(self, google_auth_details: dict):
        return self.db.query(User).filter(User.google_id == google_auth_details["google_id"]).first()

    def check_user_google_by_id(self, google_auth_id: str):
        return self.db.query(User).filter(User.google_id == google_auth_id).first()

    def insert_new_google_user(self, google_auth_details: dict) -> bool:
        new_user = User(**google_auth_details)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return True

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user_normal_auth(self, user_details: dict) -> bool:
        new_user = User(**user_details)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return True
