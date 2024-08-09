from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int
    #created_at: datetime

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

