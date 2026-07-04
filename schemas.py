from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

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
    id:Optional[str]=None

class Token(BaseModel):
    access_token:str
    token_type:str

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass
class PostOut(PostBase):
    created_at:datetime
    owner_id:int
    owner:UserOut

class Vote(BaseModel):
    post_id: int
    dir:Annotated[int, Field(ge=0,le=1)]