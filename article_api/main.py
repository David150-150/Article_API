from fastapi import FastAPI, status, HTTPException

#from pydantic import BaseModel
from .database import engine, sessionLocal
from . import models

from typing import List
from . import articles, users, auth, comment, vote

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)




#This is an object
app = FastAPI()

# # Dependency function to create and close a database session
# def get_db():
#     db = sessionLocal()  # Create a new database session
#     try:
#         yield db  # Yield the session for use in request handlers
#     finally:
#         db.close()  # Ensure the session is closed after the request is handled

# Define the allowed origins (currently allowing all domains)
origins = ["*"]


# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from any origin (* means all)
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)



app.include_router(articles.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(comment.router)
app.include_router(vote.router)



