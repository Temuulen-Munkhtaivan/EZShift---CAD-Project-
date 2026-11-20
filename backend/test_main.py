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


def test_add_employee(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'post_test.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Use the test database
    monkeypatch.setattr(main, "engine", test_engine)

    # Create an employee using the API
    response = client.post(
        "/employees",
        json={"name": "Jamie", "role": "Chef"}
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Jamie"

    # Check the employee was saved in SQLite
    with Session(test_engine) as session:
        saved_employee = session.get(
            Employee,
            response.json()["id"]
        )

        assert saved_employee is not None
        assert saved_employee.name == "Jamie"
        assert saved_employee.role == "Chef"

    test_engine.dispose()

def test_get_employees(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'get_test.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Add an employee to SQLite
    with Session(test_engine) as session:
        session.add(Employee(name="Taylor", role="Chef"))
        session.commit()

    # Use our temporary database
    monkeypatch.setattr(main, "engine", test_engine)

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Taylor", "role": "Chef"}
    ]

    test_engine.dispose()
        
def test_update_employee(monkeypatch):

    # Set up an employee in the old Python list
    monkeypatch.setattr(main, "employees", [
        {"id": 15, "name": "Jamie", "role": "Chef"}
    ])

    response = client.put(
        "/employees/15",
        json={"name": "Jamie", "role": "Manager"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Jamie"
    assert response.json()["role"] == "Manager"

def test_delete_employee(monkeypatch):

    # Set up an employee in the old Python list
    monkeypatch.setattr(main, "employees", [
        {"id": 15, "name": "Chris", "role": "Waiter"}
    ])

    response = client.delete("/employees/15")

    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully"

    # Check the employee is gone
    response = client.delete("/employees/15")

    assert response.status_code == 404
    
def test_delete_nonexistent_employee():
    response = client.delete("/employees/999999")

    assert response.status_code == 404
