from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import Employee, Shift ,engine

app = FastAPI(title="EZShift API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

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
    
@app.get("/shifts")
def get_shifts(db: Session = Depends(get_db)):

    shifts_db = db.scalars(
        select(Shift).order_by(Shift.id)
    ).all()

    return [
        {
            "id": shift.id,
            "employeeId": shift.employee_id,
            "date": shift.date,
            "startTime": shift.start_time,
            "endTime": shift.end_time
        }
        for shift in shifts_db
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
def update_employee(
    employee_id: int,
    updated_employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    # Validate the information
    if not updated_employee.name.strip() or not updated_employee.role.strip():
        raise HTTPException(
            status_code=400,
            detail="Name and role are required"
        )

    # Find the employee in SQLite
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Update employee details
    employee.name = updated_employee.name.strip()
    employee.role = updated_employee.role.strip()

    # Save changes
    db.commit()
    db.refresh(employee)

    return {
        "id": employee.id,
        "name": employee.name,
        "role": employee.role
    }

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }