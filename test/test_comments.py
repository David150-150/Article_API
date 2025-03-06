#Testing on user comment
def test_create_comment(client):
    comment_data = {"TITLE": "Good news", "COMMENT_TXT": "It has been very inspiring", "USER_ID": 1, "ARTICLE_ID": 2}
    res = client.post("/comment/", json = comment_data)
    #article_id = article_res.json()["ID"]
    print(res.json())
    assert res.status_code == 201
    assert res.json()["TITLE"] == "Good news"
    assert res.json()["COMMENT_TXT"] == "It has been very inspiring"
    assert res.json()["USER_ID"] == 1
    assert res.json()["ARTICLE_ID"] == 2

#Testing for comment on non existing article
def test_not_article(client):
    ID = 40
    comment_data = {"TITLE": "Good news", "COMMENT_TXT": "It has been very inspiring", "USER_ID": 1, "ARTICLE_ID": ID}
    res = client.post("/comment/", json=comment_data)
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"Article ID {ID} not found"}

#Testing for comment on non existing user
def test_not_use(client):
    ID = 2
    user_id = 500
    comment_data = {"TITLE": "Good news", "COMMENT_TXT": "It has been very inspiring", "USER_ID": user_id, "ARTICLE_ID": ID}
    res = client.post("/comment/", json=comment_data)
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"User ID {user_id} not found"}


#Testing for not existing title
def test_not_comment_title(client):
    ID = 40
    comment_data = {"COMMENT_TXT": "It has been very inspiring", "USER_ID": 1, "ARTICLE_ID": ID}
    res = client.post("/comment/", json=comment_data)
    print(res.json())
    assert res.status_code == 422
    
    #assert res.json() == {"detail": "Title is required"}
    assert res.json() == {
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "TITLE"],
            "msg": "Field required",
            "input": {
                "COMMENT_TXT": "It has been very inspiring",
                "USER_ID": 1,
                "ARTICLE_ID": 40
            }
        }
    ]
}
