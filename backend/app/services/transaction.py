# services/transaction.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.account import Account
from app.services.auth import authenticate_account

MAX_TXN = 200_000

def deposit(db: Session, aadhar: str, password: str, amount: float) -> Account:
    if amount <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    if amount > MAX_TXN:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Deposit cannot exceed ₹{MAX_TXN}"
        )

    acct = authenticate_account(db, aadhar, password)
    acct.balance += amount
    db.commit()
    db.refresh(acct)
    return acct

def transfer(
    db: Session,
    sender_aadhar: str,
    password: str,
    receiver_aadhar: str,
    receiver_account_number: str,
    amount: float
) -> dict:
    if amount <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    if amount > MAX_TXN:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Transfer cannot exceed ₹{MAX_TXN}"
        )

    sender = authenticate_account(db, sender_aadhar, password)
    if sender.balance < amount:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    receiver = (
        db.query(Account)
          .filter_by(
            aadhar_card_number=receiver_aadhar,
            account_number=receiver_account_number
          )
          .first()
    )
    if not receiver:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    # perform the transfer
    sender.balance   -= amount
    receiver.balance += amount

    db.commit()
    db.refresh(sender)
    db.refresh(receiver)

    return {"sender": sender, "receiver": receiver}
