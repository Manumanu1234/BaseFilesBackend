from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import urllib.parse
from db import get_db
from services import check_user_google,insert_new_google_user
load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=['authentication']
)


oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user


@router.get("/login")
async def loginrouter(request: Request):
    redirect_uri = request.url_for("auth_via_google")  
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_via_google(request: Request,db:Session=Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    print(user_info)
    frontend_url = "http://localhost:3000/home"
    google_auth_details = {
        "google_id": user_info.get("sub"),
        "email": user_info.get("email"),
        "email_verified": user_info.get("email_verified"),
        "name": user_info.get("name"),
        "profile_picture": user_info.get("picture"),
    }
    db_user=check_user_google(db,google_auth_details)
    if not db_user:
        added=insert_new_google_user(db,google_auth_details)
        if added:
            print("New User added")
            request.session["user"] = google_auth_details
        else:
            raise Exception("Failed to insert user")
    else:
        request.session["user"] = {
            "google_id": db_user.google_id,
            "email": db_user.email,
            "email_verified": db_user.email_verified,
            "name": db_user.name,
            "profile_picture": db_user.profile_picture,
        }
    return RedirectResponse(url=f"{frontend_url}")

@router.get("/logout-google")
async def google_logout(request:Request,user:dict=Depends(get_current_user)):
    request.session.pop("user")
    return {"status":"sucess"}
    

@router.get("/profile")
def profile(user: dict = Depends(get_current_user)):
    return {"profile": "sucess", "user": user}
