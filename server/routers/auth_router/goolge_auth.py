from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import os
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from db import get_db
from services import UserService
from .auth_services import AuthService
load_dotenv()

router = APIRouter(prefix="/auth", tags=["authentication"])
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request, response: Response,db_class:UserService=Depends(UserService),auth_class:AuthService=Depends(AuthService)):
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
    db_user = db_class.check_user_google(google_auth_details)
    if not db_user:
        added = db_class.insert_new_google_user(google_auth_details)
        if not added:
            raise HTTPException(status_code=500, detail="Failed to insert user")
    access_token = auth_class.create_access_token(
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
def profile(request:Request,auth_class: AuthService = Depends(AuthService)):
    user=auth_class.get_current_user(request)
    return {"profile": "success", "user": user}
