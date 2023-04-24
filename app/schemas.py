from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=False

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

#for import in posts as upperside we take UserOut upper
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class Posts(PostBase):
    id : int
    created_at : datetime
    owner_id:int
    owner:UserOut
    
    class Config:
        orm_mode = True
    
class PostOut(BaseModel):
    Post: Posts
    votes:int
    class Config:
        orm_mode = True


class User(BaseModel):
    email:EmailStr
    password:str

class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id: int
    dir:conint(le=1)