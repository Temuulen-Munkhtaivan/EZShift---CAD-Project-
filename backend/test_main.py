from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "application": "EZShift"
    }


def test_get_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alex", "role": "Barista"},
        {"id": 2, "name": "Sam", "role": "Waiter"}
    ]
