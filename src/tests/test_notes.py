"""This module holds the tests for the notes endpoints"""
import json

import pytest

from app.api import crud


def test_read_note(test_app, monkeypatch):
    # Create some test data
    test_data = {"id": 1, "title": "something", "description": "something else"}

    # Mock the crud.get function
    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    # Execute the request
    response = test_app.get("/notes/1")

    # Check the results
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    # Mock the crud.get function
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    # Execute the request
    response = test_app.get("/notes/999")

    # Check the results
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    # Execute other request
    response = test_app.get("/notes/0")

    # Check the results
    assert response.status_code == 422


def test_read_all_notes(test_app, monkeypatch):
    # Create some test data
    test_data = [
        {"title": "something", "description": "something else", "id": 1},
        {"title": "someone", "description": "someone else", "id": 2},
    ]

    # Mock the crud.get_all function
    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    # Execute the request
    response = test_app.get("/notes/")

    # Check the results
    assert response.status_code == 200
    assert response.json() == test_data


def test_create_note(test_app, monkeypatch):
    # Create the request and response payloads
    test_request_payload = {"title": "something", "description": "something else"}
    test_response_payload = {"id": 1, "title": "something", "description": "something else"}

    # Mock the crud.post function
    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    # Execute the request
    response = test_app.post("/notes/", data=json.dumps(test_request_payload),)

    # Check the results
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    # Execute the request
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))

    # Check the results
    assert response.status_code == 422

    # Execute other request
    response = test_app.post("/notes/", data=json.dumps({"title": "1", "description": "2"}))

    # Check the results
    assert response.status_code == 422


def test_update_note(test_app, monkeypatch):
    # Create some test data
    test_update_data = {"title": "someone", "description": "someone else", "id": 1}

    # Mock the crud.get and crud.put functions
    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    # Execute the request
    response = test_app.put("/notes/1/", data=json.dumps(test_update_data))

    # Check the results
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    # Mock the crud.get function
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    # Execute the request
    response = test_app.put(f"/notes/{id}/", data=json.dumps(payload),)

    # Check the results
    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch):
    # Create some test data
    test_data = {"title": "something", "description": "something else", "id": 1}

    # Mock the crud.get and crud.delete functions
    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    # Execute the request
    response = test_app.delete("/notes/1/")

    # Check the results
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    # Mock the crud.get function
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    # Execute the request
    response = test_app.delete("/notes/999/")

    # Check the results
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    # Execute other request
    response = test_app.delete("/notes/0/")

    # Check the results
    assert response.status_code == 422
