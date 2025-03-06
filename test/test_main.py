from article_api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_home():
    response = client.get("/")
    print(response.json)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Article API!"}