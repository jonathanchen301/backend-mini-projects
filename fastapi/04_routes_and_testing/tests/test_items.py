from fastapi.testclient import TestClient
from main import app
import pytest
from routers.items import memory

@pytest.fixture(autouse=True)
def client():
    with TestClient(app) as client:
        yield client

def test_items_api(client):
    # Test 1: Create an item an verify response.
    response = client.post("/items", json={"name": "Pencil", "price": 10.0, "tags": ["Utencil"]})
    item_id = response.json()["item_id"]
    assert response.status_code == 200
    assert memory[item_id].model_dump() == response.json()

    # Test 2: Get an item by id and verify response.
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert memory[item_id].model_dump() == response.json()

    # Test 3: Update an item and verify response.
    old_length = len(memory)
    response = client.put(f"/items/{item_id}", json={"name": "Strawberry", "price": 5.0, "tags": ["Fruit"]})
    new_length = len(memory)
    assert old_length == new_length
    assert response.status_code == 200
    assert memory[item_id].model_dump() == response.json()

    # Test 4: Delete an item and verify response.
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    assert item_id not in memory
    assert len(memory) == old_length - 1

def test_bad_payload(client):
    # Test 1: Create an item with a bad payload and verify response.
    response = client.post("/items", json={"name": "Pencil", "blah": "blah"})
    assert response.status_code == 422