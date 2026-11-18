
from sqlalchemy import create_engine, String
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


# Create the database tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("EZShift database is ready!")
