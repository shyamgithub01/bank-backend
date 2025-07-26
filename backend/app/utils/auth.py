from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.account import Account

def authenticate_account(db: Session, aadhar: str, password: str) -> Account:
    acct = db.query(Account).filter_by(aadhar_card_number=aadhar).first()
    if not acct or acct.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Aadhar number or password"
        )
    return acct
