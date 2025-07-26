from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_admin, get_db, get_current_employee
from app.schemas.account import AccountCreate, AccountRead, UserLogin, PasswordChange
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeLogin

from app.services.account_service import (
    create_account,
    change_password,
    delete_account,
    authenticate_user,
)
from app.services.employee_service import (
    create_employee,
    delete_employee,
    authenticate_employee,
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/login/user", summary="User login")
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, credentials.email, credentials.password)
    return {"message": "Login successful", "account_number": user.account_number}

@router.post("/login/employee", summary="Employee login")
def login_employee(
    credentials: EmployeeLogin,
    db: Session = Depends(get_db)
):
    emp = authenticate_employee(db, credentials.email, credentials.password)
    return {"message": "Employee login successful", "employee_id": emp.id}

@router.post(
    "/employees",
    dependencies=[Depends(get_admin)],
    response_model=EmployeeRead,
    summary="Manager: add new employee"
)
def add_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return create_employee(db, data.email, data.password)

@router.delete(
    "/employees/{employee_id}",
    dependencies=[Depends(get_admin)],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Manager: delete employee"
)
def remove_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    delete_employee(db, employee_id)

@router.post(
    "/",
    response_model=AccountRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new bank account"
)
def register_account(
    data: AccountCreate,
    db: Session = Depends(get_db)
):
    return create_account(db, data)

@router.put(
    "/password",
    dependencies=[Depends(get_current_employee)],
    response_model=AccountRead,
    summary="Employee: change account password by Aadhar"
)
def employee_change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db)
):
    return change_password(db, payload.aadhar_card_number, payload.new_password)

@router.delete(
    "/{aadhar}",
    dependencies=[Depends(get_current_employee)],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Employee: delete account by Aadhar"
)
def employee_delete_account(
    aadhar: str,
    db: Session = Depends(get_db)
):
    delete_account(db, aadhar)

@router.get(
    "/balance",
    summary="Account holder: check your balance"
)
def get_balance(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    acct = authenticate_user(db, email, password)
    return {
        "account_number": acct.account_number,
        "balance": float(acct.balance)
    }
