

# Testing for posting an article
def test_post_article(client):
    post_data = {"TITLE": "Good news", "DESCRIPTION": "Knowing about the good things in life"}
    res = client.post("/articles/", json=post_data)
    print(res.json())
    assert res.status_code == 201
    assert res.json()["TITLE"] == "Good news"
    assert res.json()["DESCRIPTION"] == "Knowing about the good things in life"

# Testing on getting all articles
def test_get_all(client):
    res = client.get("/articles/")
    print(res.json())
    assert res.status_code == 200
    assert isinstance(res.json(), list)

# Testing on getting one article
def test_get_one(client):
    # Create an article first
    post_data = {"TITLE": "Good news", "DESCRIPTION": "Knowing about the good things in life"}
    res_post = client.post("/articles/", json=post_data)
    created_article = res_post.json()
    ID = created_article["ID"]
    
    # Get the created article
    res = client.get(f"/articles/{ID}")
    print(res.json())
    assert res.status_code == 200
    assert res.json()["ID"] == ID

    # Check for non-existing ID
    non_existing_id = 999
    res = client.get(f"/articles/{non_existing_id}")
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"The article ID:{non_existing_id} does not exist"}

# Testing on updating article
def test_update_article(client):
    # Create an article first
    post_data = {"TITLE": "Initial", "DESCRIPTION": "Initial description"}
    res_post = client.post("/articles/", json=post_data)
    created_article = res_post.json()
    ID = created_article["ID"]
    
    # Update the article
    update_article_data = update_article_data = {'ID': ID, 'TITLE': 'WOW', 'DESCRIPTION': 'LOVE'}

    res = client.put(f"/articles/{ID}", json=update_article_data)
    print(res.json())
    assert res.status_code == 202
    assert res.json()['TITLE'] == 'WOW'
    assert res.json()['DESCRIPTION'] == 'LOVE'
    assert res.json()['ID'] == ID

    # Check for non-existing ID
    non_existing_id = 333
    res = client.put(f"/articles/{non_existing_id}", json=update_article_data)
    print(res.json())
    assert res.status_code == 404
    assert res.json() == {"detail": f"The article ID:{non_existing_id} does not exist"}

# Testing on deleting article
def test_delete_article(client):
    # Create an article first
    post_data = {'TITLE': 'To Delete', 'DESCRIPTION': 'This will be deleted'}
    res_post = client.post("/articles/", json=post_data)
    created_article = res_post.json()
    ID = created_article["ID"]
    
    # Delete the article
    res = client.delete(f"/articles/{ID}")
    print(res.json())
    assert res.status_code == 200
    assert res.json() == {"Message": "Data successfully deleted!"}

    # Verify the article is deleted by trying to GET it
    res = client.get(f"/articles/{ID}")
    assert res.status_code == 404
    assert res.json() == {"detail": f"The article ID:{ID} does not exist"}
