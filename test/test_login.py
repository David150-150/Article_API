# Test for successful login
def test_successful_login(client):
    response = client.post(
        "/login/",  # Updated path
        data={
            "username": "kusi",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Test for invalid password
def test_invalid_password(client):
    response = client.post(
        "/login/",  # Updated path
        data={
            "username": "kusi",
            "password": "password3000"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid credentials"}

# Test for non-existent user
def test_non_existent_user(client):
    response = client.post(
        "/login/",  # Updated path
        data={
            "username": "yaw",
            "password": "love21"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid credentials"}
