from fastapi import FastAPI, status, HTTPException
from fastapi import APIRouter
from fastapi.params import Depends
from .schema import Vote_On_Schema, Vote_Schema
from sqlalchemy.orm import session
from . import models
from .database import get_db


router = APIRouter(
    prefix="/article/{ID}/vote",
    tags=["Voting"]  
) 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Vote_Schema)
async def vote_article(vote: Vote_On_Schema, db: session = Depends(get_db)):
    # Check if the article exists
    article = db.query(models.Article).filter(models.Article.ID == vote.ARTICLE_ID).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article ID {vote.ARTICLE_ID} was not found")

    # Check if the user exists
    user = db.query(models.User).filter(models.User.ID == vote.USER_ID).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User ID {vote.USER_ID} was not found")

    # Check if the user has already voted on this article
    existing_vote = db.query(models.Vote).filter(
        models.Vote.ARTICLE_ID == vote.ARTICLE_ID,
        models.Vote.USER_ID == vote.USER_ID
    ).first()

    if existing_vote:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already voted on this article")

    # Insert the new vote
    new_vote = models.Vote(ARTICLE_ID=vote.ARTICLE_ID, USER_ID=vote.USER_ID, VOTE_TYPE=vote.VOTE_TYPE)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return new_vote
