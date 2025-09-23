from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from models import LoginDetails,RegisterDetails
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from services import create_user_normal_auth,get_user_by_id
from db import get_db
router2=APIRouter(
    prefix="/normal-auth",
    tags=['authentication-normal']
)

SECRET_KEY = "fsdfsdfj234324f2ifjoijfidjfi2fewifof"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="normal-login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str
    
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(email:str,password:str,db:Session):
    user=get_user_by_id(db=db,email=email)
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user



@router2.post("/register-user-normal")
def create_user(details:RegisterDetails,db:Session=Depends(get_db)):
    user=get_user_by_id(db=db,email=details.email)
    if not user:
        return {"result":"user email alredy exist"}
    
    user_details={
        "username":details.username,
        "email":details.email,
        "password":hash_password(details.password)
    }
    create_user_normal_auth(db=db,user_details=user_details)
    return {"status":"user created sucessfully"}
    


@router2.post("/token")
def login_for_access_token(form_data:LoginDetails,db:Session=Depends(get_db)):
    user=authenticate_user(form_data.email,form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token_expire=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(
        data={"sub":user.email},expires_delta=access_token_expire
    )
    return {"access_token":access_token,"token_type":"bearer"}



@router2.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authorized!"}