from fastapi import FastAPI, status, HTTPException
from fastapi import APIRouter
from fastapi.params import Depends
from .schema import Comment_On_Schema, Comment_Schema
from sqlalchemy.orm import session
from . import models
from .database import get_db


router = APIRouter(
    prefix="/comment",
    tags=["Comment"]  
) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment_Schema)
async def create_comment(comment: Comment_On_Schema, db: session = Depends(get_db)):
    # This ensure ARTICLE_ID and USER_ID exist
    article = db.query(models.Article).filter(models.Article.ID == comment.ARTICLE_ID).first()
    if not article:
        raise HTTPException(status_code=404, detail=f"Article ID {comment.ARTICLE_ID} not found")

    user = db.query(models.User).filter(models.User.ID == comment.USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User ID {comment.USER_ID} not found")

    # This ensure TITLE is not empty
    if not comment.TITLE:
        raise HTTPException(status_code=400, detail="Title is required")

    # This create new comment
    new_comment = models.Comment(
        COMMENT_TXT=comment.COMMENT_TXT,
        TITLE=comment.TITLE,
        ARTICLE_ID=comment.ARTICLE_ID,
        USER_ID=comment.USER_ID
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment
