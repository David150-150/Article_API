import pytest
from article_api.schema import Users_Schema
from article_api.utils import verify
from jose import jwt
from article_api.config import settings




#Creating a new succesful user
def test_create_user(client):
    user_data = {"USER_NAME": "testuser", "PASSWORD": "testpassword"}
    res = client.post("/users/", json = user_data)
    print(res.json())
    assert res.status_code in [201, 409]
    if res.status_code == 201:
    #This is to check that the user password is not return back
        created_user = res.json()
        assert created_user ["USER_NAME"] == "testuser"
        assert "PASSWORD" not in created_user
    else:
        print("Erroe", res.json())


#Testing for one field not provided by user
def test_create_user_missing_field(client):
    user_data = {"USER_NAME": "testuser"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 422

#Testing for user Duplicate
def test_create_user_duplicate(client):
    user_data = {"USER_NAME": "testuser", "PASSWORD": "testpassword"}
    res_1 = client.post("/users/", json = user_data)
    print(res_1.json())
    assert res_1.status_code in [201,409]
    #Testing for second user
    res_2 = client.post("/users/", json = user_data)
    print(res_2.json())
    assert res_2.status_code == 409
    
#Testing to retreive all created users
def test_get_all_users(client):
    res = client.get("/users/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


#Testing to get an existing user
def test_get_one_user(client):
    res = client.get("/users/1")
    print(res.json())
    assert res.status_code == 200
    assert res.json()["ID"] == 1
    #Testing for non existing user
    ID = 20
    res = client.get(f"/users/{ID}")
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"The user ID:{ID} does not exist!"}
