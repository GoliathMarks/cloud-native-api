from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "price" in data


def test_get_item_not_found():
    response = client.get("/items/99999")
    assert response.status_code == 404


def test_create_item():
    payload = {"name": "Test Item", "description": "Created in test", "price": 4.99}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 4.99
    assert "id" in data


def test_delete_item():
    # Create one to delete
    payload = {"name": "Doomed Item", "price": 1.00}
    create_resp = client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404
