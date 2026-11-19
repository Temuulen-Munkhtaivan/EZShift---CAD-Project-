from fastapi.testclient import TestClient
from main import app

import main

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import Base, Employee

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "application": "EZShift"
    }


def test_get_employees(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'employees.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Add a test employee
    with Session(test_engine) as session:
        session.add(Employee(name="Taylor", role="Chef"))
        session.commit()

    # Temporarily use our test database
    monkeypatch.setattr(main, "engine", test_engine)

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Taylor", "role": "Chef"}
    ]

    test_engine.dispose()

def test_add_employee():
    response = client.post(
        "/employees",
        json={"name": "Jamie", "role": "Chef"}
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Jamie"
    

def test_update_employee():
    # Create an employee first
    response = client.post(
        "/employees",
        json={"name": "Jamie", "role": "Chef"}
    )

    employee_id = response.json()["id"]

    # Update the employee
    response = client.put(
        f"/employees/{employee_id}",
        json={"name": "Jamie", "role": "Manager"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Jamie"
    assert response.json()["role"] == "Manager"

def test_delete_employee():
    # Create an employee
    response = client.post(
        "/employees",
        json={"name": "Chris", "role": "Waiter"}
    )

    employee_id = response.json()["id"]

    # Delete the employee
    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully"

    # Try deleting the same employee again
    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 404
    


def test_delete_nonexistent_employee():
    response = client.delete("/employees/999999")

    assert response.status_code == 404
