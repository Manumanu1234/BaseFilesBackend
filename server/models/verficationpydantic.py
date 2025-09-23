from pydantic import BaseModel,EmailStr

class LoginDetails(BaseModel):
    email: EmailStr 
    password: str  

class RegisterDetails(BaseModel):
    email:EmailStr
    password:str
    username:str