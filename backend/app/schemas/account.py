from pydantic import BaseModel, EmailStr, Field


class AccountCreate(BaseModel):
    full_name: str = Field(..., example="Amit Sharma")
    email: EmailStr
    age: int = Field(..., ge=18)
    aadhar_card_number: str = Field(..., min_length=12, max_length=12)
    mobile_number: str = Field(..., min_length=10, max_length=10)
    password: str = Field(..., min_length=8)
    account_type: str = Field("savings", example="savings")


class AccountRead(BaseModel):
    id: int  # database field name is likely 'id'
    full_name: str
    email: EmailStr
    age: int
    aadhar_card_number: str
    mobile_number: str
    account_number: str
    account_type: str
    balance: float
    is_frozen: bool

    class Config:
        from_attributes = True
        orm_mode = True
        allow_population_by_field_name = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    aadhar_card_number: str = Field(..., min_length=12, max_length=12)
    new_password: str = Field(..., min_length=8)
