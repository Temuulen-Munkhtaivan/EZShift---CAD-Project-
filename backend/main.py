from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException

app = FastAPI(title="EZShift API")

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
def get_employees():
    return employees

@app.post("/employees", status_code=201)
def add_employee(employee: EmployeeCreate):
    if not employee.name.strip() or not employee.role.strip():
        raise HTTPException(
            status_code=400,
            detail="Name and role are required"
        )

    new_employee = {
        "id": max(e["id"] for e in employees) + 1,
        "name": employee.name.strip(),
        "role": employee.role.strip()
    }

    employees.append(new_employee)
    return new_employee

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
