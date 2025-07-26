# schemas/transaction.py
from pydantic import BaseModel, Field, ConfigDict

class DepositRequest(BaseModel):
    aadhar_card_number: str
    password: str
    amount: float = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)

class TransferRequest(BaseModel):
    sender_aadhar_card_number:   str
    password:                    str
    receiver_aadhar_card_number: str
    receiver_account_number:     str
    amount:                      float = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)

class AccountRead(BaseModel):
    id:             int
    account_number: str
    full_name:      str
    balance:        float

    model_config = ConfigDict(from_attributes=True)

class DepositResponse(BaseModel):
    account: AccountRead
    model_config = ConfigDict(from_attributes=True)

class TransferResponse(BaseModel):
    sender:   AccountRead
    receiver: AccountRead
    model_config = ConfigDict(from_attributes=True)
