
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database import Base, Employee, Shift


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

def test_shift_database(tmp_path):
    # Create a temporary database
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'shift_test.db'}"
    )

    Base.metadata.create_all(test_engine)

    # Create an employee and assign a shift
    with Session(test_engine) as session:
        employee = Employee(name="Morgan", role="Chef")

        session.add(employee)
        session.flush()

        employee_id = employee.id

        shift = Shift(
            employee_id=employee_id,
            date="2026-11-27",
            start_time="09:00",
            end_time="17:00"
        )

        session.add(shift)
        session.commit()

        shift_id = shift.id

    # Check that the shift was saved
    with Session(test_engine) as session:
        saved_shift = session.get(Shift, shift_id)

        assert saved_shift is not None
        assert saved_shift.employee_id == employee_id
        assert saved_shift.date == "2026-11-27"
        assert saved_shift.start_time == "09:00"
        assert saved_shift.end_time == "17:00"

    test_engine.dispose()