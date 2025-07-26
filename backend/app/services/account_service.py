import secrets
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.account import Account
from app.utils.exceptions import raise_400, raise_404
from app.schemas.account import AccountCreate

def generate_account_number(db: Session) -> str:
    while True:
        num = "".join(secrets.choice("0123456789") for _ in range(12))
        if not db.query(Account).filter_by(account_number=num).first():
            return num

def create_account(db: Session, data: AccountCreate):
    if db.query(Account).filter_by(email=data.email).first():
        raise_400(f"Email {data.email} already in use")
    if db.query(Account).filter_by(aadhar_card_number=data.aadhar_card_number).first():
        raise_400("Aadhar already registered")
    if db.query(Account).filter_by(mobile_number=data.mobile_number).first():
        raise_400("Mobile number already registered")

    acct = Account(
        full_name            = data.full_name,
        email                = data.email,
        age                  = data.age,
        aadhar_card_number   = data.aadhar_card_number,
        mobile_number        = data.mobile_number,
        password             = data.password,         # plaintext
        account_type         = data.account_type,
        account_number       = generate_account_number(db),
    )
    db.add(acct)
    db.commit()
    db.refresh(acct)
    return acct

def change_password(db: Session, aadhar: str, new_password: str):
    acct = db.query(Account).filter_by(aadhar_card_number=aadhar).first()
    if not acct:
        raise_404("Account not found")
    acct.password = new_password
    db.commit()
    db.refresh(acct)
    return acct

def delete_account(db: Session, aadhar: str):
    acct = db.query(Account).filter_by(aadhar_card_number=aadhar).first()
    if not acct:
        raise_404("Account not found")
    db.delete(acct)
    db.commit()

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Account).filter_by(email=email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user
