import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_create_story(client):
    response = client.post("/stories", 
    json={"title": "The Lottery",
     "author": "Shirley Jackson", 
     "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.", "genre": "Short Story"})
    story_id = response.json()["story_id"]
    assert response.status_code == 201
    assert response.json() == {
        "story_id": story_id,
        "has_cover": False,
        "title": "The Lottery",
        "author": "Shirley Jackson",
        "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.",
        "genre": "Short Story"
    }

def test_create_story_invalid_payload(client):
    response = client.post("/stories",
    json={
        "author":"Shirley Jackson",
        "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.",
        "genre": "Short Story"  
    })
    assert response.status_code == 422

def test_get_story(client):
    response = client.post("/stories", 
    json={"title": "The Lottery",
     "author": "Shirley Jackson", 
     "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.", "genre": "Short Story"})
    story_id = response.json()["story_id"]
    response = client.get(f"/stories/{story_id}")
    assert response.status_code == 200
    assert response.json() == {
        "story_id": story_id,
        "has_cover": False,
        "title": "The Lottery",
        "author": "Shirley Jackson",
        "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.",
        "genre": "Short Story"
    }

def test_upload_invalid_file(client):
    response = client.post("/stories",
    json={"title": "The Lottery",
     "author": "Shirley Jackson", 
     "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.", "genre": "Short Story"})
    story_id = response.json()["story_id"]
    assert not response.json()["has_cover"]
    
    response=client.post(f"/stories/{story_id}/cover", files={"file": ("test.pdf", b"...", "application/pdf")})
    assert response.status_code == 400

def test_view_story_page(client):
    response = client.post("/stories",
    json={"title": "The Lottery",
     "author": "Shirley Jackson", 
     "content": "In a small town, a lottery is held every year to determine the fate of one of the town's residents.", "genre": "Short Story"})
    story_id = response.json()["story_id"]
    response = client.get(f"/stories/{story_id}/view")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "The Lottery" in response.text
