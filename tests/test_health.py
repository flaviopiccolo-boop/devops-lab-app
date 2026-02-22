
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from fastapi.testclient import TestClient
import src.main as main


client = TestClient(main.app)


def setup_function() -> None:
    main._reset_items_for_tests()


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Items CRUD" in response.text


def test_create_item() -> None:
    response = client.post(
        "/items",
        data={"title": "Item 1", "description": "Description 1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Item 1" in response.text
    assert "Description 1" in response.text


def test_update_item() -> None:
    client.post("/items", data={"title": "Old", "description": "Before"})

    response = client.post(
        "/items/1/edit",
        data={"title": "New", "description": "After"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "New" in response.text
    assert "After" in response.text


def test_delete_item() -> None:
    client.post("/items", data={"title": "Delete me", "description": "tmp"})

    response = client.post("/items/1/delete", follow_redirects=True)

    assert response.status_code == 200
    assert "Delete me" not in response.text
