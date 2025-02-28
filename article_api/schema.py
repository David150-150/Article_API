from pydantic import BaseModel
from typing import Optional


class Post_Article_Schema(BaseModel):
    #ID: int
    TITLE: str
    DESCRIPTION: str



class Get_All_Article_Schema(Post_Article_Schema):
    ID: int
    
    class Config:
        from_attributes=True


class User_Schema_In(BaseModel):
    USER_NAME: str
    PASSWORD: str

class Users_Schema(BaseModel):
    ID: int
    USER_NAME: str


class LoginSchema(BaseModel):
    USER_NAME: str
    PASSWORD: str


class TokenData(BaseModel):
    id: int 

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str


class Comment_On_Schema(BaseModel):
    ARTICLE_ID: int
    COMMENT_TXT: str
    USER_ID: int
    TITLE: str

class Comment_Schema(Comment_On_Schema):
    ID: int

   

    class Config:
        from_attributes=True


class Vote_On_Schema(BaseModel):
   ARTICLE_ID: int
   USER_ID: int
   VOTE_TYPE: int

class Vote_Schema(Vote_On_Schema): 
    ID: int

    class Config:
        from_attributes=True

