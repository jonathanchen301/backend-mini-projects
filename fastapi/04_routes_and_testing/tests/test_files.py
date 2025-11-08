from fastapi.testclient import TestClient
from main import app
import pytest

@pytest.fixture(autouse=True)
def client():
    with TestClient(app) as client:
        yield client

def test_file_upload(client):
    response = client.post(
        "/files/upload",
        files={"file": ("test.txt", b"Hello World!", "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"