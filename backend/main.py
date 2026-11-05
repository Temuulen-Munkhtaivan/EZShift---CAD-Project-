
from fastapi import FastAPI

app = FastAPI(title="EZShift API")


@app.get("/health")
def check_health():
    return {
        "status": "ok",
        "application": "EZShift"
    }


@app.get("/employees")
def get_employees():
    return [
        {"id": 1, "name": "Alex", "role": "Barista"},
        {"id": 2, "name": "Sam", "role": "Waiter"}
    ]
