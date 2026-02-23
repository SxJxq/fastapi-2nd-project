from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateUser(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    email:str
    id:int
    created_at:datetime

    class Config:
        from_attributes=True

class TokenData(BaseModel):
    id:[Optional:str]:None