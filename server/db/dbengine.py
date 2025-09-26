from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
IS_DOCKER = os.environ.get("IS_DOCKER", "0") == "1"
DB_URL = os.getenv("DBURLDOCKER") if IS_DOCKER else os.getenv("DBURL")
engine = create_engine(DB_URL)
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()