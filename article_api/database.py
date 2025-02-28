from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker  

# from typing import Annotated  
# from fastapi import Depends, FastAPI, HTTPException, Query  
# from sqlmodel import Field, Session, SQLModel, create_engine, select  

#SQLALCHEMY_DATABASE_URL = "mysql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql://root:DAVID150@localhost/Article_API"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Dependency function to create and close a database session
def get_db():
    db = sessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session for use in request handlers
    finally:
        db.close()  # Ensure the session is closed after the request is handled


