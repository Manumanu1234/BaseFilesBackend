from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import os, jwt
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from db import get_db
from services import check_user_google, insert_new_google_user, check_user_google_by_id
from .normal_auth import create_access_token
load_dotenv()
router = APIRouter(prefix="/auth", tags=["authentication"])

SECRET_KEY = "fsdfsdfj234324f2ifjoijfidjfi2fewifof" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        google_id = payload.get("google_id")

        if not google_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = check_user_google_by_id(db, google_auth_id=google_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    print(user)
    return user


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request, response: Response, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    google_auth_details = {
        "google_id": user_info.get("sub"),
        "email": user_info.get("email"),
        "email_verified": user_info.get("email_verified"),
        "name": user_info.get("name"),
        "profile_picture": user_info.get("picture"),
        "password":"google_auth"
    }


    db_user = check_user_google(db, google_auth_details)
    if not db_user:
        added = insert_new_google_user(db, google_auth_details)
        if not added:
            raise HTTPException(status_code=500, detail="Failed to insert user")


    access_token = create_access_token(
        data={
            "sub": google_auth_details["email"],
            "google_id": google_auth_details["google_id"],
            "name": google_auth_details["name"],
            "profile_picture": google_auth_details["profile_picture"],
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )



    response = RedirectResponse(url="http://localhost:3000/home")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


    return response


@router.get("/logout-google")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}


@router.get("/profile")
def profile(user: dict = Depends(get_current_user)):
    return {"profile": "success", "user": user}
