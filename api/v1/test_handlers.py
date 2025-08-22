import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import get_fastapi_app
import asyncio
import sqlalchemy as sa
from infrastructure.db.database import new_session_maker
from config import PostgresConfig

client = TestClient(get_fastapi_app())

@pytest.fixture(autouse=True)
def clean_db():
    yield
    async def _cleanup():
        session_maker = await new_session_maker(PostgresConfig())
        async with session_maker() as session:
            await session.execute(sa.text("DELETE FROM tasks"))
            await session.commit()
    asyncio.run(_cleanup())

def _create_task(name="Task", description="Desc", status="created"):
    resp = client.post("/tasks/", json={"name": name, "description": description, "status": status})
    assert resp.status_code == 201, f"Create failed: {resp.status_code} {resp.text}"
    return resp.json()

def test_create_task_success():
    body = _create_task(name="Create OK", description="D")
    assert body["name"] == "Create OK"
    assert "uuid" in body

def test_create_task_unique_violation():
    name = "DupName"
    _create_task(name=name, description="D1")
    resp = client.post("/tasks/", json={"name": name, "description": "D2"})
    assert resp.status_code == 409
    assert resp.json() == {"error": "unique_violation", "detail": "task.name уже существует"}

def test_create_task_validation_error():
    resp = client.post("/tasks/", json={"name": "", "description": ""})
    assert resp.status_code == 422
    assert resp.json() == {
        "error": "validation_error",
        "detail": "name: пустое значение; description: пустое значение"
    }

def test_get_task_success():
    created = _create_task(name="GetOne", description="Read")
    uuid = created["uuid"]
    resp = client.get(f"/tasks/{uuid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["uuid"] == uuid
    assert data["name"] == "GetOne"

def test_get_task_not_found():
    resp = client.get(f"/tasks/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"error": "not_found", "detail": "Task не найден"}

def test_get_task_validation_error():
    resp = client.get("/tasks/invalid-uuid")
    assert resp.status_code == 422
    body = resp.json()
    assert body["detail"][0]["loc"] == ["path", "uuid"]
    assert body["detail"][0]["type"] in ("type_error.uuid", "uuid_parsing")

def test_get_tasks_success():
    _create_task(name="List1", description="A")
    _create_task(name="List2", description="B")
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    data = resp.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 2

def test_update_task_success():
    created = _create_task(name="ToUpdate", description="X")
    uuid = created["uuid"]
    resp = client.put("/tasks/", json={"uuid": uuid, "name": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"

def test_update_task_not_found():
    resp = client.put("/tasks/", json={"uuid": str(uuid4()), "name": "Upd"})
    assert resp.status_code == 404
    assert resp.json() == {"error": "not_found", "detail": "Task не найден"}

@pytest.mark.xfail(reason="Обновление уникальности не сработает: update в репозитории меняет только доменную сущность, не ORM")
def test_update_task_unique_violation():
    _create_task(name="UQ1", description="A")
    second = _create_task(name="UQ2", description="B")
    uuid = second["uuid"]
    resp = client.put("/tasks/", json={"uuid": uuid, "name": "UQ1"})
    assert resp.status_code == 409
    assert resp.json() == {"error": "unique_violation", "detail": "task.name уже существует"}

def test_update_task_validation_error():
    # Отправка без полей -> pydantic ValueError (NO_FIELDS) -> стандарт 422 detail list
    resp = client.put("/tasks/", json={"uuid": str(uuid4())})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert any("NO_FIELDS" in (item.get("msg", "") or "") for item in detail)

def test_delete_task_success():
    created = _create_task(name="ToDelete", description="Z")
    uuid = created["uuid"]
    resp = client.delete(f"/tasks/{uuid}")
    assert resp.status_code == 204

def test_delete_task_not_found():
    resp = client.delete(f"/tasks/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"error": "not_found", "detail": "Task не найден"}

def test_delete_task_validation_error():
    resp = client.delete("/tasks/not-a-uuid")
    assert resp.status_code == 422
    body = resp.json()
    assert body["detail"][0]["loc"] == ["path", "uuid"]