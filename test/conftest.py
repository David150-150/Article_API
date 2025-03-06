import pytest
from fastapi.testclient import TestClient
from article_api.main import app  # Import the FastAPI app instance
from article_api.database import get_db, Base  # Import database functions and models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from article_api import models, utils  # Import models and utils for hashing
import pymysql  # Ensure this is installed: pip install pymysql

# Define a test database URL for MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:DAVID150@localhost/test_db"

# Create a new engine and session for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the test database exists
import MySQLdb

try:
    conn = MySQLdb.connect(user='root', passwd='DAVID150', host='localhost')
    conn.cursor().execute("CREATE DATABASE IF NOT EXISTS test_db")
    conn.close()
except MySQLdb.Error as e:
    print(f"Error creating database: {e}")

# Create all tables for the test database
Base.metadata.create_all(bind=engine)

# Fixture to provide a database session for tests
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clear tables after each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)  # Recreate tables for the next test

# Override get_db dependency to use the test database session
@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # Create a test user in the test database
    hashed_password = utils.hash("password123")
    test_user = models.User(USER_NAME="kusi", PASSWORD=hashed_password)
    db.add(test_user)
    db.commit()

    with TestClient(app) as client:
        yield client
