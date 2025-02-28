from fastapi import APIRouter
from fastapi import FastAPI, status, HTTPException
from .database import engine, sessionLocal, get_db
from . import models
from fastapi.params import Depends
from .schema import Post_Article_Schema, Get_All_Article_Schema
from sqlalchemy.orm import session
from typing import List
from . oauth2 import get_current_user


router = APIRouter(
    prefix="/articles",
    tags=["Articles"]  
) 





@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_article(article:Post_Article_Schema, db:session = Depends(get_db)):
    new_article = models.Article(TITLE = article.TITLE, DESCRIPTION = article.DESCRIPTION)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get("/", response_model=List[Get_All_Article_Schema], status_code=status.HTTP_200_OK)
async def get_all_article(db:session = Depends(get_db), current_user:  models.User = Depends(get_current_user)):
    my_all_article = db.query(models.Article).all()
    return my_all_article


@router.get("/{ID}", status_code=status.HTTP_200_OK, response_model=Get_All_Article_Schema)
async def get_one_article(ID: int, db:session = Depends(get_db)):
    #my_article = db.query(models.Article).filter(models.Article.ID == ID).first()
    my_article = db.query(models.Article).get(ID)
    if my_article:
        return my_article
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The article ID:{ID} does not exist")


@router.put("/{ID}", status_code=status.HTTP_202_ACCEPTED)
async def update_my_article(ID: int, article:Get_All_Article_Schema, db:session = Depends(get_db)):
    my_update = db.query(models.Article).filter(models.Article.ID == ID).update({"TITLE": article.TITLE, "DESCRIPTION": article.DESCRIPTION})
   
    if not my_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The article ID:{ID} does not exist")
        
        my_update.update(
        {"TITLE": article.TITLE, "DESCRIPTION": article.DESCRIPTION}, 
        synchronize_session=False
    )
    
    db.commit()
    updated_article = db.query(models.Article).filter(models.Article.ID == ID).first()  # Fetch updated article
    return updated_article  # Return the updated article
    #return {"Message": "Data successfully updated!"}
    

    
    

@router.delete("/{ID}", status_code=status.HTTP_200_OK)
async def delete_article(ID: int, db:session = Depends(get_db)):
    my_delete = db.query(models.Article).filter(models.Article.ID == ID).delete(synchronize_session=False) #Remember to read on synchronize_session=False
    if not  my_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The article ID:{ID} does not exist")
    db.commit()
    
    return {"Message": "Data successfully deleted!"}
    

    