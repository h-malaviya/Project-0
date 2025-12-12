from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserUpdate(BaseModel):
    id : str
    password:str

class UserDelete(BaseModel):
    id:str

class UserOut(BaseModel):
    id : str
    email : EmailStr

