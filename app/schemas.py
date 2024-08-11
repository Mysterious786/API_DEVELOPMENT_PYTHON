from typing import Optional
from pydantic import BaseModel, EmailStr, Field, conint
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    #created_At: datetime
    
    class Config:
        from_orm = True


class Post(PostBase):
    id: int
    created_At: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_orm = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    #created_At: datetime
    
    class Config:
        from_orm = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)