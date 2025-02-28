from fastapi import APIRouter
from fastapi import FastAPI, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # Import OAuth2 password form for authentication
from sqlalchemy.orm import Session  # Import Session for database interaction
from .database import engine, sessionLocal, get_db
from . import models, schema, utils
from fastapi.params import Depends
from .schema import LoginSchema
from sqlalchemy.orm import session
from typing import List
from .oauth2 import create_access_token 
from . import oauth2





# Define an API router with a prefix and tags for organization

router = APIRouter(
    prefix="/login",
    tags=["Authenticating"]  
)  

@router.post("/", response_model=schema.TokenResponseSchema )  # Define login route that returns a token response
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),  # Extract login credentials from request
    db: Session = Depends(get_db)  # Inject database session dependency
):
    # Check if user exists in the database using the provided email (username field in OAuth2)
    user = db.query(models.User).filter(models.User.USER_NAME == user_credentials.username).first()
    
    # If user is not found, raise an HTTP 403 Forbidden error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    # Verify the provided password against the stored hashed password
    if not utils.verify(user_credentials.password, user.PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # Generate an access token for the authenticated user
    access_token = oauth2.create_access_token(data={"user_id": user.ID})

    # Return the generated token in response
    return {"access_token": access_token, "token_type": "bearer"}
