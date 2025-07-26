# routes/transactions.py
from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.account import Account


from app.services.transaction import deposit, transfer
from app.schemas.transaction  import (
    DepositRequest, DepositResponse,
    TransferRequest, TransferResponse
)

MAX_BALANCE = 250_000
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/transactions", tags=["transactions"])
@router.post("/deposit", response_model=DepositResponse)
def deposit_money(
    req: DepositRequest,
    db: Session = Depends(get_db)
):
    
    acct = db.query(Account).filter_by(aadhar_card_number=req.aadhar_card_number).first()
    if not acct:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    
    if acct.balance + req.amount > MAX_BALANCE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deposit would exceed max balance of ₹{MAX_BALANCE:,}"
        )

    
    updated_acct = deposit(
        db,
        req.aadhar_card_number,
        req.password,
        req.amount
    )

    return {"account": updated_acct}


@router.post("/transfer", response_model=TransferResponse)
def transfer_money(
    req: TransferRequest,
    db: Session = Depends(get_db)
):
    result = transfer(
        db,
        req.sender_aadhar_card_number,
        req.password,
        req.receiver_aadhar_card_number,
        req.receiver_account_number,
        req.amount
    )
    return result
