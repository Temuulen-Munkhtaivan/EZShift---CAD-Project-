
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Connect to the SQLite database
engine = create_engine("sqlite:///ezshift.db")


# Base class for our database tables
class Base(DeclarativeBase):
    pass


# Employees table
class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))

# Shifts table
class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id")
    )

    date: Mapped[str] = mapped_column(String(10))
    start_time: Mapped[str] = mapped_column(String(5))
    end_time: Mapped[str] = mapped_column(String(5))


# Create the database tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("EZShift database is ready!")

