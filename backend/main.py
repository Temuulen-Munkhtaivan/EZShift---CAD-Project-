from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Employee, engine

app = FastAPI(title="EZShift API")

def get_db():
    with Session(engine) as session:
        yield session
class EmployeeCreate(BaseModel):
    name: str
    role: str


employees = [
    {"id": 1, "name": "Alex", "role": "Barista"},
    {"id": 2, "name": "Sam", "role": "Waiter"}
]


@app.get("/health")
def check_health():
    return {
        "status": "ok",
        "application": "EZShift"
    }

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    employees_db = db.scalars(
        select(Employee).order_by(Employee.id)
    ).all()

    return [
        {
            "id": employee.id,
            "name": employee.name,
            "role": employee.role
        }
        for employee in employees_db
    ]

@app.post("/employees", status_code=201)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

    if not employee.name.strip() or not employee.role.strip():
        raise HTTPException(
            status_code=400,
            detail="Name and role are required"
        )

    new_employee = Employee(
        name=employee.name.strip(),
        role=employee.role.strip()
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "id": new_employee.id,
        "name": new_employee.name,
        "role": new_employee.role
    }
    
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee: EmployeeCreate):

    for employee in employees:
        if employee["id"] == employee_id:

            if not updated_employee.name.strip() or not updated_employee.role.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Name and role are required"
                )

            employee["name"] = updated_employee.name.strip()
            employee["role"] = updated_employee.role.strip()

            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    for employee in employees:
        if employee["id"] == employee_id:
            employees.remove(employee)

            return {
                "message": "Employee deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
