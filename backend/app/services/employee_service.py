from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.utils.exceptions import raise_400, raise_404


def create_employee(db: Session, email: str, password: str):
    if db.query(Employee).filter_by(email=email).first():
        raise_400("Employee email already exists")
    emp = Employee(email=email, password=password)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def delete_employee(db: Session, employee_id: int):
    emp = db.query(Employee).filter_by(id=employee_id).first()
    if not emp:
        raise_404("Employee not found")
    db.delete(emp)
    db.commit()


def authenticate_employee(db: Session, email: str, password: str):
    emp = db.query(Employee).filter_by(email=email, password=password).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid employee credentials")
    return emp