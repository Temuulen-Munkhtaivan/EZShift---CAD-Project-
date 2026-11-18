
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database import Base, Employee


def test_employee_database(tmp_path):

    # Create a temporary database for testing
    db_file = tmp_path / "test.db"
    test_engine = create_engine(f"sqlite:///{db_file}")

    Base.metadata.create_all(test_engine)

    # Add an employee
    with Session(test_engine) as session:
        employee = Employee(name="Jamie", role="Chef")

        session.add(employee)
        session.commit()

    # Check that the employee was saved
    with Session(test_engine) as session:
        saved_employee = session.scalar(
            select(Employee).where(Employee.name == "Jamie")
        )

        assert saved_employee is not None
        assert saved_employee.role == "Chef"

    test_engine.dispose()
