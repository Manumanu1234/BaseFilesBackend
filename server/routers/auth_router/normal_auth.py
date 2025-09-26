from datetime import datetime, timedelta
from fastapi import APIRouter,Response
from models import LoginDetails,RegisterDetails
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from services import UserService
from db import get_db
from .auth_services import AuthService
from datetime import timedelta, datetime, timezone
import uuid
router2=APIRouter(
    prefix="/normal-auth",
    tags=['authentication-normal']
)


ACCESS_TOKEN_EXPIRE_MINUTES=30

@router2.post("/register-user-normal")
def create_user(details:RegisterDetails,auth_class:AuthService=Depends(AuthService),db_class:UserService=Depends(UserService)):
    user=db_class.get_user_by_email(email=details.email)
    print("*"*100)
    print(details.password)
    print("*"*100)
    if user:
        return {"result":"user email alredy exist"}
    user_details={
        "google_id":uuid.uuid4(),
        "email":details.email,
        "email_verified":True,
        "google_login":False,
        "name":details.username,
        "profile_picture":"data:image/png;base64,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",
        "password":auth_class.hash_password(details.password)
    }
    db_class.create_user_normal_auth(user_details=user_details)
    return {"result":"user created sucessfully"}
    
@router2.post("/token")
def login_for_access_token(
    form_data: LoginDetails,
    response:Response, 
    db_class:UserService=Depends(UserService),
    auth_class:AuthService=Depends(AuthService)
):
    user=auth_class.authenticate_user(form_data.email,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token_expire=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user=db_class.get_user_by_email(email=user.email)
    expire_time = datetime.now(timezone.utc) + access_token_expire
    access_token = auth_class.create_access_token(
        data={
            "sub": user.email,
            "google_id": user.google_id,
            "name":user.name,
        },expires_delta=access_token_expire
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,            
        secure=False,             
        samesite="lax",          
        path="/",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=expire_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    )
    user_data={
        "email":user.email,
        "email_verified":user.email_verified,
        "google_id":user.google_id,
        "google_login":user.google_login,
        "id":user.id,
        "name":user.name,
        "password":user.password,
        "profile_picture":user.profile_picture
    }
    return {"message": "Login successful","user":user_data}
