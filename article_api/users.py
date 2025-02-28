from fastapi import APIRouter
from fastapi import FastAPI, status, HTTPException
from .database import engine, sessionLocal, get_db
from . import models, utils
from fastapi.params import Depends
from .schema import User_Schema_In, Users_Schema
from sqlalchemy.orm import session
from typing import List


 



router = APIRouter(
   # prefix="/users/articles/{ID}",
    tags=["Users"])


@router.post("/users/", status_code = status.HTTP_201_CREATED, response_model = Users_Schema)
async def article_user(user: User_Schema_In, db:session = Depends(get_db)):

    hashed_password = utils.hash(user.PASSWORD)
    user.PASSWORD = hashed_password
    user_in = models.User(**user.dict())
    #user_in = models.User( USER_NAME = user.USER_NAME, PASSWORD = user.PASSWORD)

    db.add(user_in)
    db.commit()
    db.refresh(user_in)
    return user_in



@router.get("/users/", response_model=List[ Users_Schema], status_code=status.HTTP_200_OK)
async def get_all_article(db:session = Depends(get_db)):
    get_all_user_article = db.query(models.User).all()
    return get_all_user_article


@router.get("/users/{ID}", status_code=status.HTTP_200_OK, response_model= Users_Schema)
async def get_one_article(ID: int, db:session = Depends(get_db)):
    #my_article = db.query(models.Article).filter(models.Article.ID == ID).first()
    get_user_article = db.query(models.User).get(ID)
    if  get_user_article:
        return  get_user_article
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The article ID:{ID} does not exist")
