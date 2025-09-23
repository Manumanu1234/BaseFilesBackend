from db import Base
from sqlalchemy import Column,Integer,String,Boolean
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True, nullable=False)  
    email = Column(String, unique=True, index=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    google_login=Column(Boolean,default=True)
    name = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)

class NormalUser(Base):
    __tablename__ = "normalusers"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,index=True,nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password=Column(String,index=True,nullable=False)
