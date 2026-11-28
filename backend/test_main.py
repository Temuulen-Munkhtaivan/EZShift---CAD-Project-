from fastapi.testclient import TestClient
from main import app

import main

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import Base, Employee, Shift

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
        
def test_update_employee(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'update_test.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Add an employee to the database
    with Session(test_engine) as session:
        employee = Employee(name="Jamie", role="Chef")
        session.add(employee)
        session.commit()
        session.refresh(employee)

        employee_id = employee.id

    # Use our test database
    monkeypatch.setattr(main, "engine", test_engine)

    # Update the employee through FastAPI
    response = client.put(
        f"/employees/{employee_id}",
        json={"name": "Jamie", "role": "Manager"}
    )

    assert response.status_code == 200
    assert response.json()["role"] == "Manager"

    # Check that SQLite saved the changes
    with Session(test_engine) as session:
        updated_employee = session.get(Employee, employee_id)

        assert updated_employee is not None
        assert updated_employee.name == "Jamie"
        assert updated_employee.role == "Manager"

    test_engine.dispose()

def test_delete_employee(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'delete_test.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Add an employee to the database
    with Session(test_engine) as session:
        employee = Employee(name="Chris", role="Waiter")

        session.add(employee)
        session.commit()
        session.refresh(employee)

        employee_id = employee.id

    # Use the temporary database
    monkeypatch.setattr(main, "engine", test_engine)

    # Delete the employee using the API
    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully"

    # Check the employee was removed from SQLite
    with Session(test_engine) as session:
        deleted_employee = session.get(Employee, employee_id)

        assert deleted_employee is None

    test_engine.dispose()
    
def test_delete_nonexistent_employee(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'missing_employee_test.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Use the temporary database
    monkeypatch.setattr(main, "engine", test_engine)

    # Try deleting an employee that doesn't exist
    response = client.delete("/employees/999999")

    assert response.status_code == 404

    test_engine.dispose()

def test_get_shifts(tmp_path, monkeypatch):

    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'get_shifts_test.db'}",
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(test_engine)

    # Create an employee and a shift
    with Session(test_engine) as session:
        employee = Employee(name="Morgan", role="Chef")
        session.add(employee)
        session.flush()

        employee_id = employee.id

        shift = Shift(
            employee_id=employee_id,
            date="2026-11-28",
            start_time="09:00",
            end_time="17:00"
        )

        session.add(shift)
        session.commit()

        shift_id = shift.id

    # Use our temporary database
    monkeypatch.setattr(main, "engine", test_engine)

    # Retrieve shifts using the API
    response = client.get("/shifts")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": shift_id,
            "employeeId": employee_id,
            "date": "2026-11-28",
            "startTime": "09:00",
            "endTime": "17:00"
        }
    ]

    test_engine.dispose()