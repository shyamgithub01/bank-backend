from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class EmployeeRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str