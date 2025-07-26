from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.employee_service import authenticate_employee

security = HTTPBasic()

def get_admin(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Manager/admin check—replace with real auth logic.
    """
    ADMIN_USER = "admin"
    ADMIN_PASS = "supersecret"

    if not (credentials.username == ADMIN_USER and credentials.password == ADMIN_PASS):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: admin credentials required",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_employee(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Employee-auth dependency.
    """
    return authenticate_employee(db, credentials.username, credentials.password)