from typing import Optional
from pydantic import BaseModel,EmailStr

class User(BaseModel):
    id : str
    email : EmailStr
    password : str
