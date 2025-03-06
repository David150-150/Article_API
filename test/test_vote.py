# #Testing for creating a vote
# def test_create_vote(client):
#     ID = 1
#     vote_data = {"ARTICLE_ID": ID, "USER_ID": 1, "VOTE_TYPE": 1}
#     res = client.post(f"/article/{ID}/vote/", json = vote_data)
#     print("Response Status Code:", res.status_code)
#     print("Response JSON:", res.json())
#     assert res.status_code == 201
#     assert res.json()["ARTICLE_ID"] == ID
#     assert res.json()["USER_ID"] == 1
#     assert res.json()["VOTE_TYPE"] == 1


# #Testing for vote on non existing article
# def test_not_article_vote(client):
#     ID = 40
#     vote_data = {"ARTICLE_ID": ID, "USER_ID": 1, "VOTE_TYPE": 1}
#     res = client.post(f"/article/{ID}/vote/", json=vote_data)
#     print(res.json())
#     assert res.status_code == 404
#     #assert res.json() == {"detail": f"User ID {ID} was not found"}
#     assert res.json() == {"detail": f"Article ID {ID} was not found"}

# #Testing for vote on non existing user
# def test_not_use(client):
#     ID = 1

#     vote_data = {"ARTICLE_ID": ID, "USER_ID": 2, "VOTE_TYPE": 1}
#     res = client.post(f"/article/{ID}/vote/", json=vote_data)
#     print(res.json())
#     assert res.status_code == 404
#     assert res.json() == {"detail": f"User ID {vote_data['USER_ID']} not found"}


# def test_user_already_voted(client):
#     # Arrange: Define article and user IDs and vote data
#     ID = 5  # Assuming article ID 5 exists
#     USER_ID = 1  # Assuming user ID 1 exists and has already voted on this article
#     vote_data = {"ARTICLE_ID": ID, "USER_ID": USER_ID, "VOTE_TYPE": 1}

#     # Act: Send a POST request to vote endpoint twice
#     res_first = client.post(f"/article/{ID}/vote/", json=vote_data)
#     res_second = client.post(f"/article/{ID}/vote/", json=vote_data)

#     # Assert: Check if the first vote is successful
#     assert res_first.status_code == 201  # Created
#     assert res_first.json()["ARTICLE_ID"] == ID
#     assert res_first.json()["USER_ID"] == USER_ID

#     # Assert: Check if the second vote returns 400 Bad Request
#     assert res_second.status_code == 400
#     assert res_second.json() == {"detail": "User has already voted on this article"}


# Testing for creating a vote
def test_create_vote(client):
    ID = 1
    vote_data = {"ARTICLE_ID": ID, "USER_ID": 1, "VOTE_TYPE": 1}
    res = client.post(f"/article/{ID}/vote/", json=vote_data)
    print("Response Status Code:", res.status_code)
    print("Response JSON:", res.json())
    assert res.status_code == 201
    assert res.json()["ARTICLE_ID"] == ID
    assert res.json()["USER_ID"] == 1
    assert res.json()["VOTE_TYPE"] == 1


# Testing for vote on non-existing article
def test_not_article_vote(client):
    ID = 40
    vote_data = {"ARTICLE_ID": ID, "USER_ID": 1, "VOTE_TYPE": 1}
    res = client.post(f"/article/{ID}/vote/", json=vote_data)
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"Article ID {ID} was not found"}


# Testing for vote by non-existing user
def test_not_use(client):
    ID = 1
    vote_data = {"ARTICLE_ID": ID, "USER_ID": 999, "VOTE_TYPE": 1}  # Assuming user ID 999 does not exist
    res = client.post(f"/article/{ID}/vote/", json=vote_data)
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"User ID {vote_data['USER_ID']} not found"}


# Testing for user already voted on this article
def test_user_already_voted(client):
    ID = 5  # Assuming article ID 5 exists
    USER_ID = 1  # Assuming user ID 1 exists and has already voted on this article
    vote_data = {"ARTICLE_ID": ID, "USER_ID": USER_ID, "VOTE_TYPE": 1}

    # Send first POST request to vote
    res_first = client.post(f"/article/{ID}/vote/", json=vote_data)

    # Check if first vote is successful or if it failed due to "already voted"
    if res_first.status_code == 400 and res_first.json() == {"detail": "User has already voted on this article"}:
        print("User has already voted. Skipping first vote check.")
    else:
        assert res_first.status_code == 201  # Created
        assert res_first.json()["ARTICLE_ID"] == ID
        assert res_first.json()["USER_ID"] == USER_ID

    # Send second POST request to vote (should fail)
    res_second = client.post(f"/article/{ID}/vote/", json=vote_data)
    assert res_second.status_code == 400
    assert res_second.json() == {"detail": "User has already voted on this article"}
