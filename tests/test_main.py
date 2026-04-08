from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

def test_create_todo():
    response = client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Testing the API", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert "id" in data

def test_list_todos():
    client.post("/todos", json={"title": "Todo 1"})
    client.post("/todos", json={"title": "Todo 2"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_get_specific_todo():
    create_res = client.post("/todos", json={"title": "Find Me"})
    todo_id = create_res.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"

def test_delete_todo():
    create_res = client.post("/todos", json={"title": "Kill Me"})
    todo_id = create_res.json()["id"]
    del_res = client.delete(f"/todos/{todo_id}")
    assert del_res.status_code == 204
    get_res = client.get(f"/todos/{todo_id}")
    assert get_res.status_code == 404
